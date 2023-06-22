from datetime import date
from flask import Flask , render_template, jsonify, request, redirect, url_for
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from webspectre import WebSpectreSpider
import crochet
crochet.setup()
from scrapy import signals
from scrapy.signalmanager import dispatcher
import time
from shared_vars import SharedVars
import xpath_utils as xpu
import general_utils as gu
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.figure_factory as ff
from plotly.offline import plot
import plotly.express as px
import pandas as pd # needed for plotly


app = Flask(__name__)
output_data = []
crawl_runner = CrawlerRunner()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run-scraper', methods=['POST'])
def run_scraper():
    configure_logging({"LOG_FORMAT": "%(levelname)s: %(message)s"})
    s = request.form['url']
    SharedVars.baseURL = s

    print("URL:", SharedVars.baseURL)

    scrape_with_crochet(baseURL=SharedVars.baseURL)
    time.sleep(3)
    
    print("Type (app.py) :::: ", SharedVars.html_selector)

    # get the unique tags and counts
    unique_tags = xpu.get_unique_tags_count(SharedVars.html_selector)

    # Pie chart of the HTML tags and counts, where the slices will be ordered and plotted counter-clockwise:
    tags_labels = unique_tags.keys()
    tags_sizes = unique_tags.values()
    fig = px.pie(values=tags_sizes, names=tags_labels, title='Unique Tags by Count')
    fig.update_traces(textinfo='label')  # Set textinfo to display tag names
    # set tooltip to include percentage
    fig.update_traces(hovertemplate="%{label}: %{value} (%{percent})")
    # modify legend to include counts
    fig.update_layout(legend_title_text='Tags', title='HTML Tag Breakdown', xaxis_title='Tag', yaxis_title='Size', barmode='group')
    plotly_chart = plot(fig, output_type='div', include_plotlyjs=False)

    # convert the unique_tags dictionary to an array of arrays and order by count desc
    unique_tags_ordered = [[k,v] for k,v in unique_tags.items()]
    unique_tags_ordered.sort(key=lambda x: x[1], reverse=True)

    # other variables
    current_date = date.today() # get current date
    total_unique_tags = len(unique_tags) # get total count of unique tags

    return render_template('run-scraper.html',
        url=SharedVars.baseURL,
        unique_tags=unique_tags,
        plotly_chart=plotly_chart,
        unique_tags_ordered=unique_tags_ordered,
        total_unique_tags=total_unique_tags,
        current_date=current_date
    )



@crochet.run_in_reactor
def scrape_with_crochet(baseURL):
    dispatcher.connect(_crawler_result, signal=signals.item_scraped)
    eventual = crawl_runner.crawl(WebSpectreSpider, baseURL=baseURL)
    return eventual

def _crawler_result(item, response, spider):
    output_data.append(dict(item))

if __name__ == '__main__':
    app.run()
