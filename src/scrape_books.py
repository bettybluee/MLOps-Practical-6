from bs4 import BeautifulSoup
import pandas as pd, os, glob

class ScraperParser:
    def __init__(self, raw_dir="data/raw", processed_file="data/processed/books.csv"):
        self.raw_dir = raw_dir
        self.processed_file = processed_file
        os.makedirs(os.path.dirname(processed_file), exist_ok=True)

    def parse_html(self):
        all_books = []

        for filepath in glob.glob(f"{self.raw_dir}/*.html"):
            label = os.path.basename(filepath).split("-")[0]  
            
            with open(filepath, "r", encoding="utf-8") as f:
                html = f.read()
            
            soup = BeautifulSoup(html, "html.parser")
            
            titles = [a["title"] for a in soup.find_all("a") if a.get("title")]
            
            prices = [p.text.strip() for p in soup.find_all("p", class_="price_color")]
            
            for t, p in zip(titles, prices):
                price_value = float(p.replace("£",""))
                all_books.append({
                    "title": t,
                    "label": label,
                    "price": price_value
                })
        
        return all_books

    def save_csv(self, all_books):
        df = pd.DataFrame(all_books)
        df.to_csv(self.processed_file, index=False)
        print(f"Saved {len(df)} books into {self.processed_file}")

if __name__ == "__main__":
    parser = ScraperParser()
    books = parser.parse_html()
    parser.save_csv(books)