import requests
from pathlib import Path

images = {
    "Motorola_Edge_30_5G": {
        "edge30_1.png":
            "https://motorolain.vtexassets.com/arquivos/ids/157225/Motorola-edge-30-pdp-render-Mojito-4-31f5yjhf.png?v=637878943961030000",
        "edge30_2.png":
            "https://motorolain.vtexassets.com/arquivos/ids/157226/Motorola-edge-30-pdp-render-Mojito-2-sl4117up.png?v=637878944079430000",
        "edge30_3.png":
            "https://motorolain.vtexassets.com/arquivos/ids/157227/Motorola-edge-30-pdp-render-Mojito-5-uggdgbjn.png?v=637878944198970000",
    },

    "Motorola_Edge_30_Fusion_5G": {
        "fusion_1.png":
            "https://motorolain.vtexassets.com/arquivos/ids/157906/motorola-edge-30-fusion-pdp-ecom-render-21-barberry-5nfzuirw.png?v=638833323210500000",
        "fusion_2.png":
            "https://motorolain.vtexassets.com/arquivos/ids/157907/motorola-edge-30-fusion-pdp-ecom-render-25-barberry-mzmsdq55.png?v=638833323210800000",
    }
}

root = Path(r".\data\image-check\batch5")

headers = {
    "User-Agent": "Mozilla/5.0"
}

for model, files in images.items():

    folder = root / model
    folder.mkdir(parents=True, exist_ok=True)

    print("=" * 70)
    print(model)

    for filename, url in files.items():

        try:
            r = requests.get(url, headers=headers, timeout=30)
            r.raise_for_status()

            path = folder / filename
            path.write_bytes(r.content)

            print("Downloaded:", path)
            print("Size:", len(r.content), "bytes")

        except Exception as e:
            print("ERROR:", filename, e)

print()
print("MOTOROLA CANDIDATES DOWNLOADED")
