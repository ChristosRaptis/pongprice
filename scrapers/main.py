from scraper import Scraper
   
def main():

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
    # scraper_krefel.run_scraper()
    # scraper_mediamarkt.run_scraper()

if __name__ == "__main__" :
    main()

