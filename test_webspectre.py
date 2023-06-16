from scrapy.http import HtmlResponse
from webspectre import WebSpectreSpider
import xpath_utils as xpu
import general_utils as gu
import os

def create_mock_response():
    # create a mock response object
    return HtmlResponse(url="https://www.example.com", body=open("testfiles/test.html", "rb").read())

class TestWebspectre:
    def setup_method(self):
        self.spider = WebSpectreSpider()
        self.response = create_mock_response()
        self.result = self.spider.parse(self.response)
        # get raw html from self.result
        self.raw_html = self.result.body.decode("utf-8")
        with open("outputs/report.html", "r") as f:
            self.report_content = f.read()

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
        assert len(self.result.css("*")) == 89

    # def test_get_full_xpath_list(self):
        # check that the length of the full xpath list is 93
        # assert len(xpu.get_full_xpath_list(self.result)) == 93

    def test_xpath_of_imfeelinglucky_button(self):
        assert self.response.xpath("//input[@id='tsuid_1']/@value").extract()[0] == "I'm Feeling Lucky"

    def test_get_max_depth(self):
        # check that the max depth of the tree is 5
        assert xpu.get_max_depth(self.result)[0] == 10
    
    def test_get_unique_tags_count(self):
        # check that the number of unique tags is 15
        print(xpu.get_unique_tags_count(self.result))
        assert len(xpu.get_unique_tags_count(self.result)) == 22

    def test_get_sum(self):
        # check that the sum of the values in the unique tags dictionary is 89
        assert gu.get_sum(xpu.get_unique_tags_count(self.result).values()) == 89

    # test for the existence of the generated html report file called "report.html"
    def test_report_file_exists(self):
        assert os.path.isfile("outputs/report.html") == True

    # test for the existence of a title in the report.html file
    def test_report_title_exists(self):
        assert "<title>WebSpectre Report</title>" in self.report_content

    