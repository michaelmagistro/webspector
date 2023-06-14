import scrapy

class MySpider(scrapy.Spider):
    name = "webspector"

    def start_requests(self):
        # Get the URL from the command line
        # If no URL is provided, use Google
        # loop to ask user again until they provide a url which includes the scheme
        while True:
            url = input("Enter a URL: ") or "https://www.msn.com"
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
        with open("output.html", "w") as f:
            f.write(response.body.decode("utf-8"))

        # call the get_unique_tags function and pass the html_selector object
        print("Unique tags by count:\n", get_unique_tags_count(html_selector))
        # print the sum of the values in the unique_tags dictionary
        print("Total number of tags:", get_iterable_sum(get_unique_tags_count(html_selector).values()))
        # print the max depth of the html tree
        print("Max depth of the tree:", get_max_depth(html_selector))

def get_unique_tags_count(html):
    tags = []
    # loop through all html tags and append only the tag name to the tags array
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

# get max depth of the html tree
def get_max_depth(html):
    max_depth = [0,None]
    for tag in html.xpath('//*'):
        xpath = tag.root.getroottree().getpath(tag.root)
        depth = tag.root.getroottree().getpath(tag.root).count("/")
        if depth > max_depth[0]:
            max_depth[0] = depth
            max_depth[1] = xpath
    return max_depth