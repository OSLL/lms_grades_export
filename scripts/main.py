import os

from openpyxl import load_workbook

from yadisk_manager import DiskManager

from utils import add_csv_to_table


def write_sheet_to_file(remote_path, csv_path):
    disk_manager = DiskManager()

    # download file to filesystem
    local_path = disk_manager.download_file_from_disk(remote_path) 

    # create openpyxl.Workbook from existing xlsx file
    wb = load_workbook(filename=local_path)

    # add csv to table as sheet 
    add_csv_to_table(csv_path, wb, sheet_name='export')

    # save openpyxl.Workbook to filesystem with same name
    wb.save(local_path)

    # download file to disk
    disk_manager.upload(local_path, remote_path)

    os.remove(local_path)
