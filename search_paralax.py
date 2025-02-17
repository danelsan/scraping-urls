import os
import concurrent.futures
import requests
import time
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from bs4 import XMLParsedAsHTMLWarning
import warnings
from config import conf

warnings.filterwarnings("ignore", category=XMLParsedAsHTMLWarning)

class LinkExtractor:
    def __init__(self):
        self.links = set()  # Usare un set per evitare duplicati
        self.num_processors = os.cpu_count()  # Determina il numero di processori disponibili
        self.total_time = 0
        self.request_count = 0
        self.error_requests = 0
        print(f"Numero di processori disponibili: {self.num_processors}")

    def fetch_links(self, url):
        start_time = time.time()
        try:
            response = requests.get(url, timeout=4)
            response.raise_for_status()  # Verifica se la richiesta ha avuto successo
            soup = BeautifulSoup(response.text, 'html.parser')
            for link in soup.find_all('a', href=True):
                href = link['href']
                if self.is_valid_url(href):
                    self.links.add(href)  # Aggiungi al set
        except requests.exceptions.RequestException:
            self.error_requests += 1
            pass  # Ignora l'errore
        finally:
            elapsed_time = time.time() - start_time
            self.total_time += elapsed_time
            self.request_count += 1

    def is_valid_url(self, url):
        parsed = urlparse(url)
        return bool(parsed.scheme) and bool(parsed.netloc)

    def get_links(self):
        return list(self.links)  # Converti il set in una lista

    def fetch_links_concurrently(self, urls):
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.num_processors/2) as executor:
            executor.map(self.fetch_links, urls)

    def get_average_time_per_request(self):
        if self.request_count > 0:
            return self.total_time / self.request_count
        return 0

# Esempio di utilizzo
if __name__ == '__main__':
    max_links = conf['max_links']
    start_time = time.time()  # Tempo di inizio

    extractor = LinkExtractor()
    seed_links = [
        'https://en.wikipedia.org/wiki/Multiprocessing'
    ]

    # Aggiungi i link seed al set iniziale
    extractor.fetch_links_concurrently(seed_links)

    all_links = set(seed_links)

    while len(all_links) < max_links:
        current_links = list(all_links)
        extractor.fetch_links_concurrently(current_links)
        new_links = set(extractor.get_links())
        all_links.update(new_links)
        print(f"Numero di link trovati: {len(all_links)}")
        print(f"Tempo medio per richiesta: {extractor.get_average_time_per_request()} secondi")

    end_time = time.time()  # Tempo di fine
    total_execution_time = end_time - start_time
    print(f"Tempo totale di esecuzione: {total_execution_time} secondi")

    print(f"Errori nelle richieste con timeout=4 : {extractor.error_requests }")
