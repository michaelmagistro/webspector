from general_utils import get_sum
from xpath_utils import get_full_xpath_list, get_max_depth, get_unique_tags_count
import scrapy
from scrapy.http import HtmlResponse

class WebSpectreSpider(scrapy.Spider):
    name = "webspectre"

    def start_requests(self):
        # Get the URL from the command line
        # If no URL is provided, use Google
        # loop to ask user again until they provide a url which includes the scheme
        while True:
            url = input("Enter a URL: ") or "https://www.google.com"
            if url.startswith("http://") or url.startswith("https://"):
                break
            print("Please enter a URL which includes the scheme (http:// or https://)")
        print("You entered:", url)

        # yield scrapy.Request(url=url, callback=self.parse)
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        
        # create a Selector object from the response body
        html_selector = scrapy.Selector(response=response, type="html")
        
        # output raw html to text file
        with open("outputs/raw.html", "w+") as f:
            f.write(response.body.decode("utf-8"))

        # create the report.html file
        with open("outputs/report.html", "w+") as f:
            # write the html header
            f.write("<!DOCTYPE html>\n<html>\n<head>\n<title>WebSpectre Report</title>\n</head>\n<body>\n")
            # write the html title
            f.write("<h1>WebSpectre Report</h1>\n")
            # write the url
            f.write("<h2>URL: " + response.url + "</h2>\n")
            # write the html body
            f.write("<h2>HTML Body:</h2>\n")
            f.write("<pre>" + response.body.decode("utf-8") + "</pre>\n")
            # write the html footer
            f.write("</body>\n</html>")

        # call the get_unique_tags function and pass the html_selector object
        print("Unique tags by count:\n", get_unique_tags_count(html_selector))
        
        # print the sum of the values in the unique_tags dictionary
        print("Total number of tags:", get_sum(get_unique_tags_count(html_selector).values()))
        
        # print the max depth of the html tree
        print("Max depth of the tree:", get_max_depth(html_selector))
        
        # output full xpath list to text file
        with open("outputs/xpath_list.txt", "w") as f:
            f.write(str(get_full_xpath_list(html_selector)))
        # output full xpath list to text file with line endings
        with open("outputs/xpath_list_line_endings.txt", "w") as f:
            for item in get_full_xpath_list(html_selector):
                f.write("%s\n" % item)

        # extract data from the response
        title = response.css("title::text").get()

        # create a new HtmlResponse object with the extracted data
        http_response = HtmlResponse(
            url=response.url,
            status=response.status,
            headers=response.headers,
            body=response.body,
            encoding=response.encoding,
            request=response.request,
            flags=response.flags,
        )

        return http_response
    
    # wait 5 seconds before closing the spider
    custom_settings = {
        "CLOSESPIDER_TIMEOUT": 5
    }
