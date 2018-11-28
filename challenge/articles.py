def search_by_keyword(collection, include=None, exclude=None):
    """
    Perform find operation on collection using include and exclude keywords.
    """
    include = include or []
    exclude = exclude or []
    search_string = ' '.join(include + ['-{}'.format(e) for e in exclude])
    return list(collection.find({'$text': {'$search': search_string}}))
