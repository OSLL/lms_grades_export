"""utils module for yadisk interactions
"""
import csv
import os


CSV_DELIMITER = os.getenv('CSV_DELIMITER', ',')


def add_csv_to_table(csv_filepath, workbook, sheet_name='export', delimiter=CSV_DELIMITER):
    # delete existing sheet to rewrite
    if sheet_name in workbook.sheetnames:
        workbook.remove(workbook[sheet_name])
    ws = workbook.create_sheet(sheet_name)
    
    with open(csv_filepath, encoding="utf-") as f:
        reader = csv.reader(f, delimiter=delimiter)
        for row in reader:
            ws.append(row)
