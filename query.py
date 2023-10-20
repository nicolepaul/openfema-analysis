# Load dependencies
import pandas as pd
import numpy as np
import requests
import json


# Get endpoint
def get_endpoint(name):
    """Retrieve the endpoint for openFEMA dataset queries

    Args:
        name (str): dataset name from openFEMA
    """    
    allowed = ['HousingAssistanceOwners', 'HousingAssistanceRenters', 'IndividualsAndHouseholdsProgramValidRegistrations']
    assert name in allowed, f"Could not find endpoint for {name}; only {allowed} supported"
    if name in ['HousingAssistanceOwners', 'HousingAssistanceRenters']:
        return f"https://www.fema.gov/api/open/v2/{name}"
    elif name == 'IndividualsAndHouseholdsProgramValidRegistrations':
        return f"https://www.fema.gov/api/open/v1/{name}"


# Build filter string
def get_filter_str(filters):
    """Build a string to filter retrieved openFEMA dataset

    Args:
        filters (dict): key (field name) = value
    """
    if filters:
        prefix = '$filter='
        join_str = "%20and%20"
        filters = {k: f'%27{v}%27' if isinstance(v, str) else v for k, v in filters.items()}
        body = join_str.join([f"{k}%20eq%20{v}" for k, v in filters.items()])
        return prefix + body


# Build select string
def get_select_str(selects):
    """Build a string to reduce retrieved dataset to a limited number of fields

    Args:
        selects (list): desired attributes to be retrieved
    """
    if selects:
        prefix = '$select='
        body = ",".join(selects)
        return prefix + body


# Build url
def get_url(name, filters={}, selects=[], filter_str=''):
    """Build url to query openFEMA datasets

    Args:
        name (str): openFEMA dataset name
        filters (dict, optional): Provide dictionary of key, value pairs to filter (by equality, e.g., state=PR)
        filter_str (str, optional): Manually provide your own filter string, if desired. Should begin with "$filter=" 
        selects (list, optional): List of attributes you want to query from the dataset
    """
    endpoint = get_endpoint(name)
    if not filter_str:
        filter_str = get_filter_str(filters)
    select_str = get_select_str(selects)
    suffix = '$inlinecount=allpages'
    body = filter(None, [filter_str, select_str, suffix])
    query = "&".join(body)
    return endpoint + '?' + query


def get_response(url):
    """Retrieve response for desired url; raise error if status not OK

    Args:
        url (str): HTTP request url
    """    
    r = requests.get(url)
    r.raise_for_status()
    r_json = json.loads(r.text)
    return r_json


def convert_json_to_dataframe(r_json, name):
    """_summary_

    Args:
        r_json (dict): Response in json format (document/dict)
        name (str): Name of the openFEMA dataset
    """    
    return pd.json_normalize(r_json, name)


def get_record_count(name, filters={}, filter_str=''):
    """Determine number of records that satisfy query

    Args:
        name (str): Name of the openFEMA dataset
        filters (dict, optional): Provide dictionary of key, value pairs to filter (by equality, e.g., state=PR)
        filter_str (str, optional): Manually provide your own filter string, if desired. Should begin with "$filter=" 
    """    
    base_url = get_url(name, filters=filters, filter_str=filter_str)
    suffix = '&$top=1'
    r = get_response(base_url + suffix)
    metadata = r['metadata']
    return metadata['count']


def paginate_records(url, name, count):
    """openFEMA restricts queries to 10k records, beyond that we need
    to paginate by skipping each 10k

    Args:
        url (str): endpoint to query (with filters, selects, etc)
        name (str): dataset name
        count (int): total number of records expected
    """
    increment = 10000
    pages = list(np.arange(0, count, increment))
    n_pages = len(pages)
    all_data = [pd.DataFrame() for _ in range(n_pages)]
    for i in range(n_pages):
        skip = f"&$skip={pages[i]}"
        suffix = f"&$top={increment}"
        new_url = url + skip + suffix
        r_json = get_response(new_url)
        all_data[i] = convert_json_to_dataframe(r_json, name)
    return pd.concat(all_data, axis=0)



def get_all_records(url, name, count):
    """Retrieve all records

    Args:
        url (str): endpoint to query (with filters, selects, etc)
        name (str): dataset name
        count (int): total number of records expected
    """    
    if count <= 10000:
        suffix = f"&$top={count}"
        r_json = get_response(url + suffix)
        records = convert_json_to_dataframe(r_json, name=name)
    else:
        print(f"Found >10k records; need to paginate. This may take a few minutes...")
        records = paginate_records(url, name, count)
    return records