import scrapy
from scrapy.crawler import CrawlerProcess

SPORTS = "volleyball"

# this FollowSpider is created to crawl an inital web page defined in
class FollowSpider(scrapy.Spider):
    """This spider is created to scrape an initial web page defined in start_urls 
        and find an entry that will match the given sports category defined in the 
        global parameter SPORTS. Once the entry was found the spider continues 
        crawling pages to follow until the final page will be reached and the desired 
        information can be extracted.
    
    Arguments:
        scrapy {Spider} -- Spider object that defines the crawling process
    
    Yields:
        result.csv -- Crawled information will be stored as csv file
    """

    # name of the spider - usage: scrapy crawl follow_spider
    name = "follow_spider"

    # define inital scraping url
    start_urls = [
        "https://muenster.hochschulsport-nrw.de/angebote/aktueller_zeitraum/index.html"
    ]

    # parse inital url
    def parse(self, response):
        print("START INITIAL CRAWLING PROCESS.")
        # scraping inital page for links to follow and their assigned text
        text = response.xpath("//dd/a/text()").extract()
        raw_urls = response.xpath("//dd/a/@href").extract()

        # create following urls to scrape
        urls = [
            f"https://muenster.hochschulsport-nrw.de/angebote/aktueller_zeitraum/{url_item.split('.html')[0]}.html"
            for url_item in raw_urls
        ]
        zipped_data = zip(text, urls)

        for text_item, url_item in zipped_data:
            # normalize scraped text to lowercase and go on crawling only the requested sports category
            if SPORTS.lower() in text_item.lower():
                print(f"SELECTED COURSE: {text_item}")
                print("START FOLLOWING CRAWLING PROCESS.")
                # follow next page to scrape information with different parse method
                yield response.follow(url_item, callback=self.parse_table)

    # parsing method for following 3rd page
    def parse_table(self, response):
        print(f"RESPONSE URL: {response.url}")
        # create following urls to scrape
        url_raw = response.xpath(
            "//table//tbody//tr/td[@class='bs_szr']/a/@href"
        ).extract()
        url_list = [
            f"https://muenster.hochschulsport-nrw.de/{url_item}" for url_item in url_raw
        ]
        print(url_list)

        for url_item in url_list:
            print("START FOLLOWING CRAWLING PROCESS.")
            # follow next page to scrape information with different parse method
            yield scrapy.Request(url_item, callback=self.parse_dates)

    def parse_dates(self, response):
        print(f"RESPONSE URL: {response.url}")
        dates = response.xpath("//table//tr/td[2]//text()").extract()
        times = response.xpath("//table//tr/td[3]//text()").extract()
        print(dates)
        print(times)

        zipped_data = zip(dates, times)

        for date_item, time_item in zipped_data:
            yield {"date": date_item, "time": time_item}


mySettings = {"FEED_URI": "results.csv", "FEED_FORMAT": "CSV"}

process = CrawlerProcess(settings=mySettings)
process.crawl(FollowSpider)
process.start()
