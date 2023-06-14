
from argparse import ArgumentParser
import json
import pandas as pd
import requests


PORTAL_URL = 'https://portal.eeszt.gov.hu/torzspublikacio-portlet/rest/torzsvizualizacio/getEntity'
ENTITY_NAME = 'PUBLIKUS_ORVOS.PUBLIKUS_ORVOS.M'
OUT_FILE = 'output.csv'
CSV_SEPARATOR = ';'
TOTAL_DOWNLOADED = 0
TOTAL_IN_PORTAL = 0
PAGE_SIZE = 50

def main():
    global PORTAL_URL
    global ENTITY_NAME
    global OUT_FILE
    global CSV_SEPARATOR
    global PAGE_SIZE

    entityName = ENTITY_NAME

    parser = ArgumentParser()
    parser.add_argument('-torzs', type=str)
    parser.add_argument('-output', type=str)
    parser.add_argument('-url', type=str)
    parser.add_argument('-csv_sep', type=str)
    parser.add_argument('-page_size', type=int)

    args = parser.parse_args()

    if args.torzs:
        entityName = args.torzs

    if args.output:
        OUT_FILE = args.output
    if args.url:
        PORTAL_URL = args.url
    if args.csv_sep:
        if len(args.csv_sep) > 1:
            raise ValueError('csv separator must be maximal 1 character!')
        CSV_SEPARATOR = args.csv_sep

    if args.page_size:
        PAGE_SIZE = args.page_size

    with open(OUT_FILE, 'w') as fp:
        pass
#T_OLDALISAG.T_OLDALISAG.K
    page = 0
    while True:
        last = download_page(entityName, page, PAGE_SIZE)
        if last:
            break
        page = page + 1


# no more rows returns 'True'
def download_page(entity_name, page, size):
    global TOTAL_DOWNLOADED;
    global TOTAL_IN_PORTAL;
    params = {
        'entityId': entity_name,
        'page': page,
        'size': size
    }
    print("downloading page:" , page, "size:", size,  "...")
    resp = requests.get(PORTAL_URL, params=params)
    if resp.status_code != 200:
        raise ValueError(resp.text)


    data = json.loads(resp.text)
    names = [field['fieldName'] for field in data['fieldNames']]
    rows = [r['fields'] for r in data['entityRows']]

    if len(rows) == 0:
        print("Last page found downloading stopped!")
        print("Total Downloaded rows: " + str(TOTAL_DOWNLOADED))
        print("Total rows in portal: " + str(TOTAL_IN_PORTAL))
        return True;

    df = pd.DataFrame(rows)
    TOTAL_DOWNLOADED = TOTAL_DOWNLOADED + len(rows)

    if page == 0:
         TOTAL_IN_PORTAL = data['totalRowCount']
         df.to_csv(OUT_FILE, mode = "a", header=names, sep= CSV_SEPARATOR, index = False)
    else:
        df.to_csv(OUT_FILE, mode = "a", header=False, sep= CSV_SEPARATOR, index = False)

    return False





if __name__ == "__main__":
    main()
