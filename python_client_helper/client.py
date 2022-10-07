import requests


def endpoint_request(endpoint):
    get_response = requests.get(endpoint)
    json_data = get_response.json()
    return json_data


def retrieve_data(title=None):
    if title is None:
        title = "some title"

    endpoint = f"https://openlibrary.org/search.json?q={title}"

    get_response = requests.get(endpoint)

    # print(get_response.json())
    json_data = get_response.json()
    docs_data = json_data['docs']
    list_of_pairs = []

    for i in docs_data:
        try:
            pair = (i['publish_date'][0], i['author_name'][0], i['title'])
            list_of_pairs.append(pair)
        except Exception as E:
            # print(str(E))
            pass

    return list_of_pairs
