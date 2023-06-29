from datetime import date
from flask import Flask , render_template, request
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
from plotly.offline import plot
import plotly.express as px
import pandas as pd # needed for plotly
import os
import plotly.graph_objects as go

print("debug test")
print("debug test 2")

app = Flask(__name__)
output_data = []
crawl_runner = CrawlerRunner()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run-scraper', methods=['POST'])
def run_scraper():
    configure_logging({"LOG_FORMAT": "%(levelname)s: %(message)s"})
    # create outputs directory if it doesn't exist relative to the project directory
    project_dir = os.path.dirname(os.path.abspath(__file__))
    outputs_dir = os.path.join(project_dir, 'outputs')
    if not os.path.exists(outputs_dir):
        os.makedirs(outputs_dir)

    # get the url from the form
    s = request.form['url']
    SharedVars.baseURL = s


    print("URL:", SharedVars.baseURL)

    scrape_with_crochet(baseURL=SharedVars.baseURL)
    time.sleep(3)
    
    print("Type (app.py) :::: ", SharedVars.html_selector)

    # get the unique tags and counts
    unique_tags = xpu.get_unique_tags_count(SharedVars.html_selector)

    # get the full xpath list
    xpath_list = xpu.get_full_xpath_list(SharedVars.html_selector)

    # Pie chart of the HTML tags and counts, where the slices will be ordered and plotted counter-clockwise:
    tags_labels = unique_tags.keys()
    tags_sizes = unique_tags.values()
    fig = px.pie(values=tags_sizes, names=tags_labels, title='Unique Tags by Count')
    # Customize label display
    fig.update_traces(
        textinfo='label',  # Hide percentage labels
        textposition='inside',  # Show labels inside the pie slices
        hovertemplate="%{label}: %{value} (%{percent})"
    )
    fig.update_layout(legend_title_text='Tags', title='HTML Tag Breakdown', xaxis_title='Tag', yaxis_title='Size', barmode='group', showlegend=False, title_text='', margin=dict(l=0, r=0, b=0, t=0, pad=1), height=200)
    # hide overflow tooltip on pie chart
    chart = plot(fig, output_type='div', include_plotlyjs=False)
    plotly_pie = chart

    # create a dataframe from the xpath_list
    df = pd.DataFrame(xpath_list[1:], columns=xpath_list[0])

    # create a histogram of the number of tags that occur on each line
    # convert the line number column to int
    df['Line Number'] = df['Line Number'].astype(int)
    # create a histogram
    fig = px.histogram(df, x="Line Number", title='Line Number vs Tag Count')
    fig.update_layout(legend_title_text='Tags', title='Line Number vs Tag Count', xaxis_title='Line Number', yaxis_title='Tag Count', barmode='group', title_text='')
    chart = plot(fig, output_type='div', include_plotlyjs=False)
    plotly_hist_chart1 = chart
    
    # create a scatter plot of the number of occurrences of each tag against the line number
    # convert the line number column to int
    df['Line Number'] = df['Line Number'].astype(int)
    # create a scatter plot
    fig = px.scatter(df, x="Line Number", y="Name", title='Line Number vs Tag Name')
    fig.update_layout(legend_title_text='Tags', title='Line Number vs Tag Name', xaxis_title='Line Number', yaxis_title='Tag Name', barmode='group', title_text='')
    chart = plot(fig, output_type='div', include_plotlyjs=False)
    plotly_scatter = chart
    
    
    # #############################

    # HTML Selector Tree
    # Create a list of dictionaries representing the tree structure
    # Create a tree chart
    tree_data = gu.create_tree_data(SharedVars.html_selector)
    # Create the Plotly Express figure
    fig = px.treemap(
    tree_data,
        names=[str(node['node_id']) for node in tree_data],
        parents=[str(node['parent_id']) for node in tree_data],
        values=[node['value'] for node in tree_data],
        labels=[node['label'] for node in tree_data],
        title='HTML Selector Tree',
    )
    # Update the layout of the figure
    fig.update_layout(
        margin=dict(l=0, r=0, t=50, b=0),
    )
    # Create a chart from the figure
    chart = fig.to_html(full_html=False)
    plotly_tree_chart = chart

    # ################################################# TESTING

    fig = px.treemap(
    names = ["Eve","Cain", "Seth", "Enos", "Noam", "Abel", "Awan", "Enoch", "Azura"],
    parents = ["", "Eve", "Eve", "Seth", "Seth", "Eve", "Eve", "Awan", "Eve"]
    )
    fig.update_traces(root_color="lightgrey")
    fig.update_layout(margin = dict(t=50, l=25, r=25, b=25))
    chart = plot(fig, output_type='div', include_plotlyjs=False)
    plotly_tree_chart_example = chart

    # ################################################# TESTING


    # convert the unique_tags dictionary to an array of arrays and order by count desc
    unique_tags_ordered = [[k,v] for k,v in unique_tags.items()]
    unique_tags_ordered.sort(key=lambda x: x[1], reverse=True)

    # other variables
    current_date = date.today() # get current date
    total_unique_tags = len(unique_tags) # get total count of unique tags

    # print dataframe to csv
    df.to_csv(os.path.join(outputs_dir, 'webspectre_output.csv'), index=False)

    return render_template('run-scraper.html',
        url=SharedVars.baseURL,
        unique_tags=unique_tags,
        plotly_chart=plotly_pie,
        unique_tags_ordered=unique_tags_ordered,
        total_unique_tags=total_unique_tags,
        current_date=current_date,
        plotly_scatter=plotly_scatter,
        plotly_hist_chart1=plotly_hist_chart1,
        plotly_tree_chart=plotly_tree_chart,
        plotly_tree_chart_example=plotly_tree_chart_example
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
