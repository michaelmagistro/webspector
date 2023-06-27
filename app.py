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

    # Create a tree chart
    # create a list of dictionaries representing the HTML tree structure
    # tree_data = [{'label': tag.extract(), 'parent': '', 'value': 1} for tag in SharedVars.html_selector.xpath('//*')]
    # tree_data = gu.create_tree_data(SharedVars.html_selector)
    # for i, node in enumerate(tree_data):
    #     if i == 0:
    #         continue
    #     parent = tree_data[i-1]
    #     if node['label'] in parent['label']:
    #         node['parent'] = parent['label']
    #         parent['value'] += 1
    # # create the Plotly figure
    # fig = go.Figure(go.Treemap(
    #     labels=[node['label'] for node in tree_data],
    #     parents=[node['parent'] for node in tree_data],
    #     values=[node['value'] for node in tree_data],
    #     textinfo='label+value',
    #     hovertemplate='<b>%{label}</b><br>Count: %{value}<br>Parent: %{parent}<extra></extra>',
    # ))
    # # update the layout of the figure
    # fig.update_layout(
    #     title='HTML Selector Tree',
    #     title_x=0.5,
    #     margin=dict(l=0, r=0, t=50, b=0),
    # )
    # # create a chart from the figure
    # chart = plot(fig, output_type='div', include_plotlyjs=False)
    # plotly_tree_chart = chart

    # Create a tree chart

    # #############################



    # ################################################# TESTING
    # test treemap
    # Create a list of dictionaries representing the tree structure
    # tree_data = [{'label': 'Root', 'value': 100}, {'label': 'Node 1', 'value': 50}, {'label': 'Node 2', 'value': 25}, {'label': 'Node 3', 'value': 12.5}, {'label': 'Node 4', 'value': 6.25}]
    # # Create the Plotly figure
    # fig = px.treemap(tree_data, values='value', labels='label')
    # # Update the layout of the figure
    # fig.update_layout(
    #     title='Treemap Example',
    #     title_x=0.5,
    #     margin=dict(l=0, r=0, t=50, b=0),
    # )
    # chart = plot(fig, output_type='div', include_plotlyjs=False)
    # plotly_tree_chart_example = chart

    tree_data = [{'label': 'Root', 'value': 100}, {'label': 'Node 1', 'value': 50}, {'label': 'Node 2', 'value': 25}, {'label': 'Node 3', 'value': 12.5}, {'label': 'Node 4', 'value': 6.25}]

    fig = px.treemap(tree_data, values='value', labels='label')
    fig.update_layout(
        title='Treemap Example',
        title_x=0.5,
        margin=dict(l=0, r=0, t=50, b=0),
    )

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
        # plotly_tree_chart=plotly_tree_chart,
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
