from scraper import Scraper
import time
   
def main():
    start_time = time.perf_counter()   

    url_vandenborre = "https://www.vandenborre.be/web/sitemap.xml"
    url_krefel = "https://media.krefel.be/sys-master/sitemap/index-fr.xml"
    url_mediamarkt = "https://www.mediamarkt.be/sitemaps/fr/sitemap-index.xml"

    sitemap_condition_vandenborre = "productcatalog.xml"
    sitemap_condition_krefel = "product"
    sitemap_condition_mediamarkt = "productdetailspages"

    scraper_vandenborre = Scraper(url_vandenborre, sitemap_condition_vandenborre)
    scraper_krefel = Scraper(url_krefel, sitemap_condition_krefel)
    scraper_mediamarkt = Scraper(url_mediamarkt, sitemap_condition_mediamarkt)

    scraper_vandenborre.run_scraper()
    scraper_krefel.run_scraper()
    scraper_mediamarkt.run_scraper()

    end_time = time.perf_counter()
    print(f"Finished scraping all sites in {round((end_time - start_time)/60, 2)} minutes")
if __name__ == "__main__" :
    main()

