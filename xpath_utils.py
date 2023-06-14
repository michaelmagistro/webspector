def get_full_xpath_list(html):
    xpath_list = []
    i = 0
    for tag in html.xpath('//*'):
        # get the xpath of the tag
        xpath = tag.root.getroottree().getpath(tag.root)
        # get the depth of the tag
        depth = tag.root.getroottree().getpath(tag.root).count("/")
        # append the xpath and depth to the xpath_count list
        xpath_list.append([xpath, depth])
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