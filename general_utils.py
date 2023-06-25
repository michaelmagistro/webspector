# get_sum() function
def get_sum(iterable):
    total = 0
    for i in iterable:
        total += i
    return total

# convert the html response to plain text
def html_to_text(html):
    html = html.body.decode("utf-8")
    return html