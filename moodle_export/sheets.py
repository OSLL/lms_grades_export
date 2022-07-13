#!/usr/bin/python3
import pygsheets
import pandas as pd
import args_parser


INT_MASS = [{
    "one": 1,
    "two": 2,
    "what?": 3
}]


def write_data_to_table(args):
    if args.google_token and args.sheet_id and args.table_id:
        gc = pygsheets.authorize(service_file=args.google_token)
        sh = gc.open_by_key(args.table_id)

    try:
        sh.worksheets('title', args.sheet_id)
    except:
        sh.add_worksheet(args.sheet_id)

    wk_content = sh.worksheet_by_title(args.sheet_id)

    if args.csv_path:
        df = pd.read_csv(args.csv_path)
        content = pd.DataFrame(df.to_dict('records'))
    else:
        content = pd.DataFrame(INT_MASS)
    wk_content.set_dataframe(content, 'A1', copy_head=True)


def main():
    args = args_parser.arg_parser()
    write_data_to_table(args)


if __name__ == "__main__":
    main()
