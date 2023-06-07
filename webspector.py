import scrapy


class WebspectorSpider(scrapy.Spider):
    name = "webspector"

    def start_requests(self):
        url = input("Enter a URL: ") or "https://www.google.com"
        print("You entered:", url)

        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # Print the URL being visited
        self.logger.info("Visited URL: %s", response.url)

        # Print the HTML content
        self.logger.info("HTML Content:\n%s", response.text)
        
        # output the response text to a text file
        with open('output.txt', 'w') as f:
            f.write(response.text)
        