from lxml import html

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

def create_tree_data(html_selector):
    tree_data = []

    def traverse_tree(node, parent_label):
        label = node.xpath('string(.)').strip()
        children = node.xpath('./*')

        if parent_label:
            tree_data.append({'label': label, 'parent': parent_label, 'value': 1})
        else:
            tree_data.append({'label': label, 'parent': '', 'value': 1})

        for child in children:
            traverse_tree(child, label)

    traverse_tree(html_selector.root, '')
    return tree_data


