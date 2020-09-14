import fnmatch
import sys
import os
from google.cloud import storage


def download_rain_input_files(bucket_time, config):
    try:
        download_input_files(bucket_time, config['gcp_service_key'], config['output_dir'], config['bucket_name'],
                             config['mike_rf_bucket_file'], config['input_rain_file'])
    except Exception as e:
        print('download_files|Exception : ', str(e))
        return False


def download_tide_input_files(bucket_time, config):
    try:
        download_input_files(bucket_time, config['gcp_service_key'], config['output_dir'], config['bucket_name'],
                             config['mike_tide_bucket_file'], config['input_tide_file'])
    except Exception as e:
        print('download_files|Exception : ', str(e))
        return False


def download_input_files(bucket_time, key_file, output_dir, bucket_name, src_file, dest_file):
    try:
        source_blob_name = 'mike/inputs/{}/{}'.format(bucket_time, src_file)
        print('download_rain_input_files|source_blob_name : ', source_blob_name)
        destination_file_name = '{}/{}/{}'.format(output_dir, bucket_time, dest_file)
        print('download_rain_input_files|destination_file_name : ', destination_file_name)
        storage_client = storage.Client.from_service_account_json(key_file)
        print('download_rain_input_files|storage_client : ', storage_client)
        bucket = storage_client.bucket(bucket_name)
        print('download_rain_input_files|bucket : ', bucket)
        blob = bucket.blob(source_blob_name)
        print('download_rain_input_files|blob : ', blob.name)
        blob.download_to_filename(destination_file_name)
        print('Blob {} downloaded to {}.'.format(source_blob_name, destination_file_name))
        return True
    except Exception as e:
        print('download_files|Exception : ', str(e))
        return False