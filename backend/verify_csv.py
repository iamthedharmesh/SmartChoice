import pandas as pd
import os

csv_path = os.path.join(os.path.dirname(__file__), "artifacts", "processed_movies.csv")
df = pd.read_csv(csv_path)
print("Columns:", list(df.columns))
print("Shape:", df.shape)
print()
langs = sorted([l for l in df["original_language"].dropna().unique().tolist() if l])
print("Languages:", langs[:20])
print("Rating range:", df["vote_average"].min(), "-", df["vote_average"].max())
print("Release dates sample:", df["release_date"].head(5).tolist())
print("Popularity range:", df["popularity"].min(), "-", df["popularity"].max())
print("Runtime range:", df["runtime"].min(), "-", df["runtime"].max())
print()
print(df[["movie_id", "title", "original_language", "vote_average", "release_date", "popularity", "genres"]].head(3).to_string())