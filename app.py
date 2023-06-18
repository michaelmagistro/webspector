from datetime import date
from flask import Flask , render_template, jsonify, request, redirect, url_for
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from webspectre import WebSpectreSpider
import webspectre as ws
import crochet
crochet.setup()
from scrapy import signals
from scrapy.signalmanager import dispatcher
import time

app = Flask(__name__)
output_data = []
crawl_runner = CrawlerRunner()
baseURL = ""

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/run-scraper', methods=['POST'])
def run_scraper():
    configure_logging({"LOG_FORMAT": "%(levelname)s: %(message)s"})
    s = request.form['url']
    global baseURL
    baseURL = s

    print("URL:", baseURL)

    scrape_with_crochet(baseURL=baseURL)
    time.sleep(3)
    print("Type (app.py) :::: ", ws.html_selector)
    unique_tags = ws.get_unique_tags_count(ws.html_selector)
    return render_template('run-scraper.html', url=baseURL, unique_tags=unique_tags)

@crochet.run_in_reactor
def scrape_with_crochet(baseURL):
    dispatcher.connect(_crawler_result, signal=signals.item_scraped)
    eventual = crawl_runner.crawl(WebSpectreSpider, baseURL=baseURL)
    return eventual

def _crawler_result(item, response, spider):
    output_data.append(dict(item))

if __name__ == '__main__':
    app.run()