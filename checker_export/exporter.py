#/bin/python3
import pygsheets
import pandas as pd
import argparse
import requests
from io import StringIO
import urllib.parse
import yadisk

INT_MASS = [{
    "one": 1,
    "two": 2,
    "what?": 3
}]


EXPORT_URL = "https://slides-checker.moevm.info/get_csv/?limit=0&offset=0&sort=&order="


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--google_token', type=str, required=False, default='conf.json', help='Specify path to google token file')
    parser.add_argument('--checker_token', type=str, required=True, help='Specify session cookie for slides-checker')
    parser.add_argument('--checker_filter', type=str, required=False, help='Specify filter for slides-checker')
    parser.add_argument('--table_id', type=str, required=False, help='Specify Google sheet document id (can find in url)')
    parser.add_argument('--sheet_id', type=str, required=False, help='Specify title for a sheet in a document in which data will be printed')
    parser.add_argument('--yandex_token', type=str, required=False, help='Specify Yandex token from https://oauth.yandex.ru/client/new application')
    parser.add_argument('--yandex_path', type=str, required=False, help='Specify output filename on Yandex Disk')
    args = parser.parse_args()
    return args


def load_data_from_dis(checker_filter, checker_token):
    url = f'{EXPORT_URL}&{checker_filter}&access_token={checker_token}'
    csv_data = StringIO(requests.get(url).content.decode('utf-8'))

    if csv_data:
        df = pd.read_csv(csv_data)
        df_data = pd.DataFrame(df.to_dict('records'))
    else:
        df_data = pd.DataFrame(INT_MASS)
    return csv_data, df_data


def write_data_to_table(checker_token, checker_filter, google_token, table_id, sheet_id, yandex_token=None, yandex_path=None):
    csv_data, df_data = load_data_from_dis(checker_filter, checker_token)
    
    if google_token and sheet_id and table_id:
        gc = pygsheets.authorize(service_file=google_token)
        sh = gc.open_by_key(table_id)

        wk_content = sh.worksheet_by_title(sheet_id)

        wk_content.set_dataframe(df_data, 'A1', copy_head=True)
    
    # write data to yandex disk
    if yandex_token and yandex_path:
        # TODO: refactor нadisk
        from utils import write_sheet_to_file
        write_sheet_to_file(yandex_token, yandex_path, csv_data, sheet_name="reports")
        
        print(f'DIS data w/filter: {checker_filter} uploaded to table on Disk! Path to the table is: {yandex_path}')


def main():
    args = parse_args()
    write_data_to_table(args.checker_token, args.checker_filter, args.google_token, args.table_id, args.sheet_id, args.yandex_token, args.yandex_path)


if __name__ == "__main__":
    main()
