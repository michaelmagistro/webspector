def get_full_xpath_list(html):
    # get the full xpath of each tag in the html tree
    xpath_list = ['XPATH', 'DEPTH', 'TEXT', 'TAG']
    i = 0
    for tag in html.xpath('//*'):
        # get the tag name
        tag_name = tag.root.tag
        # get the depth of the tag
        depth = tag.root.getroottree().getpath(tag.root).count("/")
        # get the text of the tag
        text = tag.xpath('text()').extract_first()
        # get the xpath of the tag
        xpath = tag.root.getroottree().getpath(tag.root)
        # get the class of the tag if any
        class_name = tag.xpath('@class')
        # get the id of the tag if any
        id_name = tag.xpath('@id')
        # populate the list
        xpath_list.append([tag_name, depth, text, class_name, id_name, xpath])
        i =+ 1
    return xpath_list


def get_max_depth(html):
    # get max depth of the html tree
    max_depth = [0,None]
    for tag in html.xpath('//*'):
        xpath = tag.root.getroottree().getpath(tag.root)
        depth = tag.root.getroottree().getpath(tag.root).count("/")
        if depth > max_depth[0]:
            max_depth[0] = depth
            max_depth[1] = xpath
    return max_depth


def get_unique_tags_count(html):
    tags = []
    # loop through all html tags and append only the tag name to the tags array
    for tag in html.xpath('//*'):
        tags.append(tag.root.tag)

    # remove duplicates from the array
    unique_tags = dict.fromkeys(tags)

    # set unique_tags dictionary values to tags.count(tag) to get the number of times the tag appears
    for tag in unique_tags:
        unique_tags[tag] = tags.count(tag)

    return unique_tags