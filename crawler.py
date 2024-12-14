import requests
from bs4 import BeautifulSoup

def crawl(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        text = soup.get_text(separator='\n')
        if url.startswith("https://www.forbes.com/"):
            text = text.split("Forbes Digital Assets")[-1].strip()
            text = text.split("Follow me on")[0].strip()
        elif url.startswith("https://finance.yahoo.com"):
            text = text.split("View Comments")[0].strip()
        return text
    else:
        return ""