import argparse
from scraper.scraping import run_scraper

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Scraper Automático de Panamericana')
    parser.add_argument('--search', type=str, default='libros', help='Término de búsqueda')
    args = parser.parse_args()
    
    run_scraper(args.search)