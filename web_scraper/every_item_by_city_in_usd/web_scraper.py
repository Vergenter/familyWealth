# source: https://www.thepythoncode.com/article/convert-html-tables-into-csv-files-in-python

import requests
import pandas as pd
from bs4 import BeautifulSoup as bs

USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"
# US english
LANGUAGE = "en-US,en;q=0.5"

def get_soup(url):
    """Constructs and returns a soup using the HTML content of `url` passed"""
    # initialize a session
    session = requests.Session()
    # set the User-Agent as a regular browser
    session.headers['User-Agent'] = USER_AGENT
    # request for english content (optional)
    session.headers['Accept-Language'] = LANGUAGE
    session.headers['Content-Language'] = LANGUAGE
    # make the request
    html = session.get(url)
    # return the soup
    return bs(html.content, "html.parser")

def get_all_tables(soup):
    """Extracts and returns all tables in a soup object"""
    return soup.find_all("table")

def get_table_headers(table):
    """Given a table soup, returns all the headers"""
    headers = []
    for th in table.find("tr").find_all("th"):
        headers.append(th.text.strip())
    return headers

def get_table_rows(table):
    """Given a table, returns all its rows"""
    rows = []
    for tr in table.find_all("tr")[1:]:
        cells = []
        # grab all td tags in this table row
        tds = tr.find_all("td")
        if len(tds) == 0:
            # if no td tags, search for th tags
            # can be found especially in wikipedia tables below the table
            ths = tr.find_all("th")
            for th in ths:
                cells.append(th.text.strip())
        else:
            # use regular td tags
            for td in tds:
                cells.append(td.text.strip())
        rows.append(cells)
    return rows

def save_as_csv(table_name, headers, rows):
    pd.DataFrame(rows, columns=headers).to_csv(f"{table_name}.csv")

def main(url, url_args, item_id):
    # itemId = 24 -> gasonline
    url = url + str(url_args) + "&itemId=" + str(item_id)
    # get the soup
    soup = get_soup(url)
    # extract all the tables from the web page
    tables = get_all_tables(soup)
    print(f"[+] Found a total of {len(tables)} tables.")
    # iterate over all tables
    for i, table in enumerate(tables, start=1):
        # get the table headers
        headers = get_table_headers(table)
        # get all the rows of the table
        rows = get_table_rows(table)
        # save table as csv file
        table_name = f"table-{i}"
        print(f"[+] Saving {table_name}")
        save_as_csv(table_name + '-' + str(url_args) + '-' + str(item_id), headers, rows)

if __name__ == "__main__":
    url = "https://www.numbeo.com/cost-of-living/historical-prices-by-city?displayCurrency=USD&year="
    url_args = range(2010, 2021)
    item_ids = [101, 100, 228, 224, 60, 66, 64, 62, 110, 118, 121, 14, 19, 17, 15, 11, 16, \
        113, 9, 12, 8, 119, 111, 112, 115, 116, 13, 27, 26, 29, 28, 114, \
        6, 4, 5, 3, 2, 1, 7, 105, 106, 44, 40, 42, 24, 20, 18, 109, 108, \
        107, 206, 25, 32, 30, 33]
    for i in url_args:
        for j in item_ids:
            main(url, i, j)