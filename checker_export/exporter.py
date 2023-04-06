#/bin/python3
import pygsheets
import pandas as pd
import argparse
import requests
from io import StringIO
import urllib.parse


INT_MASS = [{
    "one": 1,
    "two": 2,
    "what?": 3
}]

EXPORT_URL = "https://slides-checker.moevm.info/get_csv?limit=10&&offset=0&sort=&order=&latest=true"

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--google_token', type=str, required=False, default='conf.json', help='Specify path to google token file')
    parser.add_argument('--checker_token', type=str, required=True, help='Specify session cookie for slides-checker')
    parser.add_argument('--checker_filter', type=str, required=False, help='Specify filter for slides-checker')
    parser.add_argument('--table_id', type=str, required=True, help='Specify Google sheet document id (can find in url)')
    parser.add_argument('--sheet_id', type=str, required=True, help='Specify title for a sheet in a document in which data will be printed')
    args = parser.parse_args()
    return args

def write_data_to_table(checker_token, checker_filter, google_token, table_id, sheet_id):
    if google_token and sheet_id and table_id:
        gc = pygsheets.authorize(service_file=google_token)
        sh = gc.open_by_key(table_id)

    wk_content = sh.worksheet_by_title(sheet_id)
    
    url = f'{EXPORT_URL}&{checker_filter}'
    print(url)
    csv_path = StringIO(requests.get(url, cookies={'session':checker_token}).content.decode('utf-8'))

    if csv_path:
        df = pd.read_csv(csv_path)
        content = pd.DataFrame(df.to_dict('records'))
    else:
        content = pd.DataFrame(INT_MASS)
    wk_content.set_dataframe(content, 'A1', copy_head=True)


def main():
    args = parse_args()
    write_data_to_table(args.checker_token, args.checker_filter, args.google_token, args.table_id, args.sheet_id)


if __name__ == "__main__":
    main()
