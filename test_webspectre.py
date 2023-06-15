from scrapy.http import HtmlResponse
from webspectre import WebSpectreSpider

def create_mock_response():
    # create a mock response object
    return HtmlResponse(url="https://www.example.com", body=open("testfiles/test.html", "rb").read())

class TestWebspectre:
    def setup_method(self):
        self.spider = WebSpectreSpider()
        self.result = self.spider.parse(create_mock_response())

    def test_status(self):
        # check that the result is html response 200
        assert self.result.status == 200

    def test_html_element_count(self):
        # check that the html elements in the selector list is equal to the number of elements in the test html file
        assert len(self.result.css("html")) == 1

    def test_div_element_count(self):
        # check that the div elements in the selector list is equal to the number of elements in the test html file
        assert len(self.result.css("div")) == 13

    def test_total_element_count(self):
        # check that the total elements in the selector list is equal to the number of elements in the test html file
        print(self.result.css("*"))
        assert len(self.result.css("*")) == 89