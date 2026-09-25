import pandas as pd
import os
import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

CSV_PATH = r".\data\phones_enriched.csv"
ROOT = r".\data\image-check\batch3"

df = pd.read_csv(CSV_PATH)

missing = df[
    df["canonical_name"].notna()
    & (
        df["official_image_url"].isna()
        | (df["official_image_url"].astype(str).str.strip() == "")
        | (df["official_image_url"].astype(str).str.lower() == "nan")
    )
].copy()

print("Missing-image rows:", len(missing))

groups = (
    missing.groupby("canonical_name", dropna=True)
    .first()
    .reset_index()
)

print("Unique models:", len(groups))
print()

os.makedirs(ROOT, exist_ok=True)

session = requests.Session()
session.headers.update({
    "User-Agent": "Mozilla/5.0"
})

BAD = re.compile(
    r"(logo|icon|favicon|sprite|placeholder|default|wechat|"
    r"miniprogram|qr|qrcode|avatar|appstore|googleplay|"
    r"facebook|instagram|twitter|youtube)",
    re.I
)

for _, row in groups.iterrows():

    name = str(row["canonical_name"]).strip()
    product_url = str(row.get("official_product_url", "")).strip()

    print("=" * 70)
    print(name)

    if not product_url or product_url.lower() == "nan":
        print("NO PRODUCT URL")
        continue

    print(product_url)

    safe_name = re.sub(r"[^A-Za-z0-9]+", "_", name).strip("_")
    folder = os.path.join(ROOT, safe_name)
    os.makedirs(folder, exist_ok=True)

    try:
        response = session.get(product_url, timeout=30)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        candidates = []

        for img in soup.find_all("img"):

            for attr in [
                "src",
                "data-src",
                "data-original",
                "data-lazy-src"
            ]:
                value = img.get(attr)

                if value:
                    candidates.append(value)

            srcset = img.get("srcset")

            if srcset:
                for part in srcset.split(","):
                    candidates.append(part.strip().split(" ")[0])

        for meta in soup.find_all("meta"):

            prop = meta.get("property") or meta.get("name")
            content = meta.get("content")

            if (
                prop
                and content
                and prop.lower() in [
                    "og:image",
                    "twitter:image",
                    "twitter:image:src"
                ]
            ):
                candidates.append(content)

        cleaned = []

        for image_url in candidates:

            image_url = str(image_url).strip()
            image_url = image_url.replace("\\/", "/")

            if image_url.startswith("//"):
                image_url = "https:" + image_url
            else:
                image_url = urljoin(product_url, image_url)

            if not image_url.startswith(("http://", "https://")):
                continue

            if BAD.search(image_url):
                continue

            if not re.search(
                r"\.(png|jpg|jpeg|webp)(\?|$)",
                image_url,
                re.I
            ):
                continue

            if image_url not in cleaned:
                cleaned.append(image_url)

        print("Candidates found:", len(cleaned))

        if not cleaned:
            print("NO USABLE IMAGE CANDIDATES")
            continue

        for number, image_url in enumerate(cleaned[:6], 1):

            path = urlparse(image_url).path.lower()

            if ".png" in path:
                extension = ".png"
            elif ".webp" in path:
                extension = ".webp"
            else:
                extension = ".jpg"

            output = os.path.join(
                folder,
                "candidate_" + str(number) + extension
            )

            try:
                image_response = session.get(
                    image_url,
                    timeout=30
                )

                image_response.raise_for_status()

                content_type = image_response.headers.get(
                    "Content-Type",
                    ""
                ).lower()

                if "image" not in content_type:
                    print("SKIP:", image_url)
                    continue

                with open(output, "wb") as file:
                    file.write(image_response.content)

                print(
                    "[" + str(number) + "] " + image_url
                )

            except Exception as error:
                print(
                    "FAILED [" + str(number) + "]:",
                    error
                )

    except Exception as error:
        print("FAILED PAGE:", error)

print()
print("=" * 70)
print("BATCH 3 COMPLETE")
print("=" * 70)
