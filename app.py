from flask import Flask
app = Flask(__name__)
import webspectre
app.debug = True # debug mode
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0 # debug mode

from flask import Flask
from scrapy.crawler import CrawlerProcess
from webspectre.spiders import myspider

app = Flask(__name__)
app.debug = True
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

@app.route("/")
def webspectre_route():
    process = CrawlerProcess()
    process.crawl(myspider.MySpider)
    process.start()
    return "Scraping complete!"

if __name__ == "__main__":
    app.run()