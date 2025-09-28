from bs4 import BeautifulSoup
import pandas as pd, os, glob
import argparse

class ScraperParser:
    def __init__(self, raw_dir="data/raw", processed_file="data/processed/books.csv"):
        self.raw_dir = raw_dir
        self.processed_file = processed_file
        os.makedirs(os.path.dirname(processed_file), exist_ok=True)

    def parse_html(self, genre_filter=None, max_pages=None):
        all_books = []

        for filepath in glob.glob(f"{self.raw_dir}/*.html"):
            label = os.path.basename(filepath).split("-")[0] 
            
            if genre_filter and label != genre_filter:
                continue

            if max_pages:
                filepath_idx = glob.glob(f"{self.raw_dir}/*.html").index(filepath)
                if filepath_idx >= max_pages:
                    break
            
            with open(filepath, "r", encoding="utf-8") as f:
                html = f.read()
            
            soup = BeautifulSoup(html, "html.parser")
            titles = [a["title"] for a in soup.find_all("a") if a.get("title")]
            
            for t in titles:
                all_books.append({"title": t, "label": label})
        
        return all_books

    def save_csv(self, all_books):
        df = pd.DataFrame(all_books)
        df.to_csv(self.processed_file, index=False)
        print(f"Saved {len(df)} books into {self.processed_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--genre", type=str, help="Choose genre to scrape")
    parser.add_argument("--pages", type=int, help="Number of HTML files/pages to parse")
    args = parser.parse_args()

    scraper = ScraperParser()
    books = scraper.parse_html(genre_filter=args.genre, max_pages=args.pages)
    scraper.save_csv(books)
