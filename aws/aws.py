import os
import boto3
import logging

import pandas as pd
from dotenv import load_dotenv
import re
# import pandas as pd

load_dotenv()  # to load environments from .env file

# aws_s3_client = boto3.client('s3', region_name='us-east-1', aws_access_key_id=os.environ.get(
#     'AWS_ACCESS_KEY'), aws_secret_access_key=os.environ.get('AWS_SECRET_KEY'))

# files_from_bucket = []

# def get_files_from_noaa_bucket(dir):
#     # s3 = boto3.client("s3",
#     #                   aws_access_key_id= None,
#     #                   aws_secret_access_key=None)
#     """
#     This function will list down all files in a folder from S3 bucket
#     :return: None
#     """
#
#     print(dir,"ddddddddddddddddddddd")
#     s3_client = boto3.client("s3",
#                       aws_access_key_id=os.environ.get('AWS_ACCESS_KEY'),
#                       aws_secret_access_key=os.environ.get('AWS_SECRET_KEY'))
#     bucket_name = "noaa-goes18"
#     response = s3_client.list_objects_v2(Bucket=bucket_name, Prefix=dir)
#     files = response.get("Contents")
#     print("---------------------------------------------------------------------")
#     print(type(files))
#     files_from_bucket =[]
#     for file in files:
#         files_from_bucket.append(file['Key'])
#         # f = open("output.txt", "a")
#         # print(file['Key'])
#         print(f"file_name: {file['Key']}, size: {file['Size']}")
#         # f.close()
#     return files_from_bucket

"""
Arguments : Directory of the bucket
returns : list of all files from the dir
"""


def get_files_from_noaa_bucket(dir):
    files_from_bucket = []
    s3_client = boto3.client("s3", region_name='us-east-1', 
                             aws_access_key_id=os.environ.get(
                                 'AWS_ACCESS_KEY'),
                             aws_secret_access_key=os.environ.get('AWS_SECRET_KEY'))
    paginator = s3_client.get_paginator('list_objects_v2')
    # ,PaginationConfig  = {"PageSize":2}
    noaa_bucket = paginator.paginate(Bucket="noaa-goes18", Prefix=dir)
    for count, page in enumerate(noaa_bucket):
        files = page.get("Contents")
        for file in files:
            files_from_bucket.append(file['Key'])
            # print(file['Key'])
            f = open("output.txt", "a")
            print(f"{file['Key']}", file=f)
    # print(files_from_bucket)
    return files_from_bucket


def get_meta_data_for_db_population():
    meta_data_for_db = []
    files = get_files_from_noaa_bucket("ABI-L1b-RadC")
    for file in files:
        ydh = []
        match = re.findall(r"(\d{4})(\d{3})(\d{2})", file)
        # match = pattern.search(file)
        if match:
            year = match[0][0]
            month = match[0][1]
            day = match[0][2]
            ydh.extend([year, month, day])
            if ydh not in meta_data_for_db:
                meta_data_for_db.append(ydh)
    # print(meta_data_for_db,"-------------------------")
    # df = pd.DataFrame(meta_data_for_db, columns=['year', 'day', 'hour'])
    # df.to_csv('sample.csv')
    return meta_data_for_db


# def main():
#     # ydh = []
#     # dir = "ABI-L1b-RadC/2022"
#     # files = get_files_from_noaa_bucket()
#     # pattern = re.findall(r'(\d{4})|(\d{3})|(\d{2})')
#     # for file in files:
#     #     match = re.findall(r"(\d{4})(\d{3})(\d{2})",file)
#     #     # match = pattern.search(file)
#     #     if match:
#     #         year = match[0][0]
#     #         month = match[0][1]
#     #         day = match[0][2]
#     #         ydh.append([])
#     #         # station = match.group(4)
#     #         # print(match[:3])
#     #         f = open("output.txt", "a")
#     #         print(f"{year},{month},{day}",file = f)
#     #         # print(f"{match[:3]}",file = f)
#     #         f.close()
if __name__ == "__main__":
    # main()

    # get_files_from_noaa_bucket("ABI-L1b-RadC/2022")
    meta_data = get_meta_data_for_db_population()
    print(meta_data)
    # piyush_func()
