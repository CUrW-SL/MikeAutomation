import fnmatch
import sys
import os
from google.cloud import storage


def download_files(run_datetime, config):
    try:
        key_file = config['']
        bucket_name = config['']
        source_blob_name = config['']
        destination_file_name = config['']
        storage_client = storage.Client.from_service_account_json(key_file)
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(source_blob_name)
        blob.download_to_filename(destination_file_name)

        print(
            "Blob {} downloaded to {}.".format(
                source_blob_name, destination_file_name
            )
        )
        return False
    except Exception as e:
        print('download_files|Exception : ', str(e))
        return False