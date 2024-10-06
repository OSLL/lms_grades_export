"""Script with DiskManager class and functions for moodle backup

"""
from datetime import datetime
from os import environ
from logging import getLogger

import yadisk


logger = getLogger()


class DiskManager():
    """Light YaDisk manager
    """
    def __init__(self):
        self.client = yadisk.Client(token=environ.get('YADISK_TOKEN'))


    def upload(self, local_path: str, disk_path: str, overwrite=True):
        """upload from local_path to disk_path

        Args:
            local_path (str): path to local file 
            disk_path (str): full path to file on yadisk
            overwrite (bool): overwrite file. Defaults to true
        """
        logger.info("Uploading %s to %s", *(local_path, disk_path))
        self.client.upload(local_path, disk_path, overwrite=overwrite)


def upload_file_to_disk(file_path: str, abs_disk_path="/MOEVM/Публичные ведомости МОЭВМ", overwrite=True):
    """hardcoded logic for uploading rating file to yadisk in pdf format
    might be run from bash

    Args:
        file_path (str): path to local file 
        abs_disk_path (str, optional): full path to file on yadisk.
            Defaults to "/MOEVM/Публичные ведомости МОЭВМ".
        overwrite (bool): overwrite file. Defaults to true

    """
    disk_manager = DiskManager()
    disk_manager.upload(file_path, f"{abs_disk_path}/{file_path}", overwrite=overwrite)
