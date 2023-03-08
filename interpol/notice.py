import requests
import os
import sys
import config
import json
import producer


def get_data(url):
    """
    Get data from the url and return the data
    """
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print('Error: Could not get data from the url')
        sys.exit(1)


def get_all_notices(url, page=1, all_data=[]):
    """
    Get all notices from the url
    :param page: page number to start from (default is 1)
    :param url: url to get data from
    :param all_data: list of all notices
    :return: list of all notices
    """

    data = get_data(url + '?page=' + str(page) + '&resultPerPage=1000')
    total = data['total']
    query_page = data['query']['page']
    if total == 0:
        return all_data

    if page != query_page:
        return all_data

    all_data.extend(data["_embedded"]["notices"])
    page += 1
    print(f'Page: {page} - Total: {total} - Length: {len(all_data)}')

    return get_all_notices(url, page, all_data)


def send_notice_to_queue(notice):
    """
    Send notice to the queue
    :param notice: notice to send to the queue
    :return: None
    """
    producer.send_notice_to_queue(notice)


def send_notices_to_queue(notices):
    """
    Send notices to the queue
    :param notices: notices to send to the queue
    :return: None
    """
    for notice in notices:
        send_notice_to_queue(notice)
