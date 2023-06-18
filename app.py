from datetime import date
from flask import Flask, render_template, request
from globals import webspectre_selector_list
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings
from twisted.internet import reactor
from twisted.internet.task import deferLater
from webspectre import WebSpectreSpider


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run-scraper', methods=['POST'])
def run_scraper():
    runner = CrawlerRunner()
    configure_logging({"LOG_FORMAT": "%(levelname)s: %(message)s"})
    d = runner.crawl(WebSpectreSpider)
    d.addBoth(lambda _: reactor.stop()) # noqa
    reactor.run()  # the script will block here until the crawling is finished # noqa
    
    
    print(type(webspectre_selector_list))
    print(webspectre_selector_list)
    current_date = date.today()
    url = request.form['url']
    # print("Selector List Type: ",type(WebSpectreSpider.selector_list))
    # subprocess.run(['python', 'webspectre.py', url])
    return render_template('run-scraper.html', current_date=current_date, url=url)

if __name__ == '__main__':
    app.run()