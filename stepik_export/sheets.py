import pygsheets
import pandas as pd
import args_parser


INT_MASS = [{
    "one": 1,
    "two": 2,
    "what?": 3
}]


def write_data_to_table(csv_path, google_token, table_id, sheet_id):
    if google_token and sheet_id and table_id:
        gc = pygsheets.authorize(service_file=google_token)
        sh = gc.open_by_key(table_id)

    try:
        sh.worksheets('title', sheet_id)
    except:
        sh.add_worksheet(sheet_id)

    wk_content = sh.worksheet_by_title(sheet_id)

    if csv_path:
        df = pd.read_csv(csv_path)
        content = pd.DataFrame(df.to_dict('records'))
    else:
        content = pd.DataFrame(INT_MASS)
    wk_content.set_dataframe(content, 'A1', copy_head=True)


def main():
    args = args_parser.arg_parser()
    write_data_to_table(args.csv_path, args.google_token, args.table_id, args.sheet_id)


if __name__ == "__main__":
    main()