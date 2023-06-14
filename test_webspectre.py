import unittest
from scrapy.http import HtmlResponse
from webspectre import WebSpectreSpider

class TestWebspectre(unittest.TestCase):
    def setUp(self) -> None:
        self.spider = WebSpectreSpider()
    
    def test_parse(self):
        # create a mock response object
        response = HtmlResponse(url="https://www.example.com", body=open("testfiles/test.html", "rb").read())

        # call the parse method
        result = self.spider.parse(response)
        # check that the result is html response 200
        self.assertEqual(result.status, 200)