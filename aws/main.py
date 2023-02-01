import os
import boto3
import logging
from dotenv import load_dotenv

load_dotenv() # to loan environments from env file

aws_s3_client = boto3.client('s3',region_name = 'us-east-1',aws_access_key_id = os.environ.get('AWS_ACCESS_KEY'),aws_secret_access_key = os.environ.get('AWS_SECRET_KEY'))



def get_files_from_noaa_bucket(dir):
    s3 = boto3.client("s3",
                      aws_access_key_id= None,
                      aws_secret_access_key=None)
    """
    This function will list down all files in a folder from S3 bucket
    :return: None
    """
    s3_client = boto3.client("s3",
                      aws_access_key_id=os.environ.get('AWS_ACCESS_KEY'),
                      aws_secret_access_key=os.environ.get('AWS_SECRET_KEY'))
    bucket_name = "noaa-goes18"
    response = s3_client.list_objects_v2(Bucket=bucket_name, Prefix=dir)
    files = response.get("Contents")
    for file in files:
        f = open("output.txt", "a")
        print(file['Key'])
        # print(f"file_name: {file['Key']}, size: {file['Size']}",file = f)
        f.close()


# get_all_files_in_s3_bucket(bucket_name)
def main():
    dir = "ABI-L1b-RadC/2022/224/13"
    get_files_from_noaa_bucket(dir)
    # get_all_files_in_s3_bucket(bucket_name,folder_name)

    # get_files_from_noaa_bucket()

if __name__ == "__main__":
    main()