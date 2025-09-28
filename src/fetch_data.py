import requests, time, os, logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s: %(message)s",
    handlers=[logging.FileHandler("logs/fetch_data.log"), logging.StreamHandler()]
)

class Scraper:
    def __init__(self, genres, raw_dir="data/raw"):
        self.genres = genres
        self.raw_dir = raw_dir
        os.makedirs(self.raw_dir, exist_ok=True)

    def fetch_all(self):
        for label, url in self.genres.items():
            timestamp = time.strftime('%Y%m%d-%H%M%S')
            filename = f"{self.raw_dir}/{label}-{timestamp}.html"
            
            try:
                resp = requests.get(url)
                resp.raise_for_status()  
                
                with open(filename, "wb") as f:
                    f.write(resp.content)
                
                logging.info(f"Saved {label} HTML to {filename}")
            
            except requests.RequestException as e:
                logging.error(f"Failed to fetch {label} from {url}: {e}")

# --- 실행 ---
if __name__ == "__main__":
    genres = {
        "mystery": "http://books.toscrape.com/catalogue/category/books/mystery_3/index.html",
        "poetry": "http://books.toscrape.com/catalogue/category/books/poetry_23/index.html",
        "science": "http://books.toscrape.com/catalogue/category/books/science_22/index.html"
    }

    scraper = Scraper(genres)
    scraper.fetch_all()