import argparse


def arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--moodle_token', type=str, required=True, help='Specify moodle token')
    parser.add_argument('--url', type=str, required=True, help='url of the platform')
    parser.add_argument('--course_id', type=lambda s: [i for i in s.split(',')], required=True, help='Id of a course to parse')
    parser.add_argument('--csv_path', type=str, required=True, help='Specify path to output csv file')
    parser.add_argument('--google_token', type=str, required=False, help='Specify path to google token file')
    parser.add_argument('--table_id', type=lambda s: [i for i in s.split(',')], required=False, help='Specify Google sheet document id (can find in url)')
    parser.add_argument('--sheet_id', type=lambda s: [i for i in s.split(',')], required=False, help='Specify title for a sheet in a document in which data will be printed')
    parser.add_argument('--percentages', required=False, action='store_true', help='If set then grades will be printed as percentages')
    parser.add_argument('--options', type=lambda s: [i for i in s.split(',')], required=False, help='Specify options for column names')
    args = parser.parse_args()
    return args