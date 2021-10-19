def get_path_for_filter_pagination(kwargs):
    filter_pagination_path = ''
    for keys in kwargs:
        for arg in kwargs[keys]:
            filter_pagination_path += f'{keys}={arg}&'
    return filter_pagination_path


def get_data_for_filter(kwargs):
    print(kwargs)
    filter_data = []
    for keys in kwargs:
        for arg in kwargs[keys]:
            filter_data.append(f'{keys}_{arg}')
    return filter_data


def get_data_comment(qs):
    res = []
    dictionary = {}
    for comment in qs:
        c = {
            'id': comment.id,
            'text': comment.text,
            'timestamp': comment.timestamp.strftime("%Y-%m-%d %H:%m"),
            'author': comment.user.username,
            'is_child': comment.is_child,
            'parent_id': comment.parent_id,
            'children': [],
        }
        res.append(c)
        dictionary[comment.id] = c
    return {'data_list': res, 'nodes': dictionary}


def create_comment_tree(**kwargs):

    forest = []

    for i in kwargs['data_list']:
        id, parent_id = i['id'], i['parent_id']
        node1 = kwargs['nodes'][id]

        if not i['parent_id']:
            forest.append(i)

        else:
            parent = kwargs['nodes'][parent_id]

            children = parent['children']
            children.append(node1)
    return forest