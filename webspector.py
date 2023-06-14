import scrapy

class MySpider(scrapy.Spider):
    name = "webspector"

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

        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # create a Selector object from the response body
        html_selector = scrapy.Selector(response=response, type="html")

        # call the get_unique_tags function and pass the html_selector object
        unique_tags = get_unique_tags(html_selector)
        print(unique_tags)
        # print the sum of the values in the unique_tags dictionary
        print("Total number of tags:", get_iterable_sum(unique_tags.values()))

def get_unique_tags(html):
    tags = []
    # loop through all html tags and print only the tag name
    for tag in html.xpath('//*'):
        tags.append(tag.root.tag)

    # remove duplicates from the array
    unique_tags = dict.fromkeys(tags)

    # set unique_tags dictionary values to tags.count(tag) to get the number of times the tag appears
    for tag in unique_tags:
        unique_tags[tag] = tags.count(tag)

    return unique_tags

def get_iterable_sum(iterable):
    total = 0
    for i in iterable:
        total += i
    return total