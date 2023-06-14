import scrapy


class WebspectorSpider(scrapy.Spider):
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
        # Print the URL being visited
        # self.logger.info("Visited URL: %s", response.url)

        # Print the HTML content
        # self.logger.info("HTML Content:\n%s", response.text)

        # Print the title of the page

        # output the response text to a text file
        with open('output.txt', 'w') as f:
            f.write(response.css('title::text').get() + '\n')
            # for p in response.css('p'):
            #     f.write(p.get() + '\n')
            # create an array for all html tags
            tags = []
            # loop through all html tags and print only the tag name
            for tag in response.xpath('//*'):
                tags.append(tag.root.tag)
            # remove duplicates from the array
            unique_tags = list(dict.fromkeys(tags))
            # for each of the unique tags, print the number of times it appears in the html
            for tag in unique_tags:
                f.write(tag + ": " + str(tags.count(tag)) + '\n')
            # print the tags to the console
            print('\n'.join(tags))