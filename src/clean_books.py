import pandas as pd
import sqlite3, os

class Cleaner:
    def __init__(self, input_file="data/processed/books.csv", 
                 cleaned_file="data/processed/books_clean.csv", 
                 db_file="data/books.db"):
        self.input_file = input_file
        self.cleaned_file = cleaned_file
        self.db_file = db_file
        os.makedirs(os.path.dirname(cleaned_file), exist_ok=True)
        os.makedirs(os.path.dirname(db_file), exist_ok=True)

    def clean_text(self, text_series):
        text_series = text_series.str.lower().str.strip()
        # text_series = text_series.str.replace(r"[^\w\s]", "", regex=True)
        return text_series

    def add_price_label(self, df):
        if "price" in df.columns:
            df["price"] = df["price"].astype(float)
            df["price_label"] = df["price"].apply(lambda x: "cheap" if x <= 10 else "expensive")
        return df

    def run(self):
        # 1. Load CSV
        df = pd.read_csv(self.input_file)
        print(f"Loaded {len(df)} rows from {self.input_file}")

        # 2. Clean text
        df["title"] = self.clean_text(df["title"])

        # 3. Add price label
        df = self.add_price_label(df)

        # 4. Save cleaned CSV
        df.to_csv(self.cleaned_file, index=False)
        print(f"Saved cleaned dataset to {self.cleaned_file}")

        # 5. Store in SQLite
        conn = sqlite3.connect(self.db_file)
        df.to_sql("books", conn, if_exists="replace", index=False)
        conn.close()
        print(f"Stored cleaned dataset in SQLite: {self.db_file}")

        # 6. Verify
        conn = sqlite3.connect(self.db_file)
        check = pd.read_sql("SELECT * FROM books LIMIT 5;", conn)
        conn.close()
        print("🔍 Preview from SQLite:")
        print(check)

if __name__ == "__main__":
    cleaner = Cleaner()
    cleaner.run()