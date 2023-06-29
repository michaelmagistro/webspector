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
    node_id = 0

    def traverse_tree(node, parent_label, parent_id):
        nonlocal node_id

        # label = node.xpath('string(.)').strip()
        # get the html tag name
        label = node.tag
        children = node.xpath('./*')

        node_id += 1
        current_id = node_id

        tree_data.append({'node_id': current_id, 'parent_id': parent_id, 'label': label, 'parent_label': parent_label, 'value': 1})

        for child in children:
            traverse_tree(child, label, current_id)

    # Assign a unique parent ID for the top-level node
    top_level_id = 'root'

    traverse_tree(html_selector.root, '', top_level_id)

    return tree_data



