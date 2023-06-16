
from argparse import ArgumentParser
import json
import time
import warnings
import pandas as pd
import requests

####
## Run Example:
## python eeszt_portal_downloader.py -torzs T_ORSZAG.T_ORSZAG.K -output new.csv -csv_sep "|" -page_size  20
####

PORTAL_URL = 'https://portal.eeszt.gov.hu/torzspublikacio-portlet/rest/torzsvizualizacio/getEntity'
ENTITY_NAME = 'PUBLIKUS_ORVOS.PUBLIKUS_ORVOS.M'
OUT_FILE = 'output.csv'
CSV_SEPARATOR = ';'
TOTAL_DOWNLOADED = 0
TOTAL_IN_PORTAL = -1
PAGE_SIZE = 50
MAX_PAGE_TRY = 5
WAIT_SECS_BETWEEN_TRYS = 5

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

    page = 0
    while True:
        last = download_page(entityName, page, PAGE_SIZE, 1)
        if last:
            print("Last page found downloading stopped!")
            print("Total Downloaded rows:", str(TOTAL_DOWNLOADED))
            print("Total rows found in portal:", str(TOTAL_IN_PORTAL))
            break
        page = page + 1

    if TOTAL_DOWNLOADED != TOTAL_IN_PORTAL:
        raise ValueError("Download result is incomplete please check the result or retry downloading!")
    else:
        print("Download successfully completed!")


# no more rows returns 'True'
def download_page(entity_name, page, size, tryCounter):
    global TOTAL_DOWNLOADED;
    global TOTAL_IN_PORTAL;
    params = {
        'entityId': entity_name,
        'page': page,
        'size': size
    }

    print("downloading page:" , page, "size:", size, end= " ")

    resp = requests.get(PORTAL_URL, params=params)
    if resp.status_code != 200 and TOTAL_DOWNLOADED == TOTAL_IN_PORTAL:
        print("Last page detected downloading stopped! downloaded rows: ", TOTAL_DOWNLOADED)
        return True

    if resp.status_code != 200 and tryCounter <= MAX_PAGE_TRY:
        warnings.warn("Page download failed retrying... " + str(tryCounter))
        warnings.warn("status code: " + str(resp.status_code) + " response: " + resp.text)

        time.sleep(WAIT_SECS_BETWEEN_TRYS)

        return download_page(entity_name, page, size, tryCounter + 1)
    elif resp.status_code != 200 and tryCounter > MAX_PAGE_TRY:
        print("Maximal retry exceed application stopped!")
        raise ValueError(resp.text)

    data = json.loads(resp.text)

    names = [field['fieldName'] for field in data['fieldNames']]
    rows = [r['fields'] for r in data['entityRows']]

    if len(rows) == 0:
        return True;

    df = pd.DataFrame(rows)
    TOTAL_DOWNLOADED = TOTAL_DOWNLOADED + len(rows)

    if page == 0:
         TOTAL_IN_PORTAL = int(data['totalRowCount'])
         df.to_csv(OUT_FILE, mode = "a", header=names, sep= CSV_SEPARATOR, index = False)
    else:
        df.to_csv(OUT_FILE, mode = "a", header=False, sep= CSV_SEPARATOR, index = False)

    precentage = ( TOTAL_DOWNLOADED/ TOTAL_IN_PORTAL) * 100
    print("Progress: ", TOTAL_DOWNLOADED, "/", TOTAL_IN_PORTAL, "( " + f"{precentage:.2f}" + " % )" )

    if TOTAL_DOWNLOADED == TOTAL_IN_PORTAL:
        return True

    return False

if __name__ == "__main__":
    main()
