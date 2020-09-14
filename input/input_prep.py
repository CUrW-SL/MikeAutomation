import fnmatch
import subprocess
import sys
import os
from google.cloud import storage

MATLAB_DIR = r"E:\MIKE\ProductionRun\hourly_run\Matlab"
KEY_FILE = r"E:\MIKE\ProductionRun\hourly_run\uwcc-admin\uwcc-admin.json"
MATLAB_INPUT_PROCESSOR = r"E:\MIKE\ProductionRun\hourly_run\MikeAutomation\windows_scripts\matlab_run.bat"


def download_rain_input_files(bucket_time, config):
    try:
        download_input_files(bucket_time, KEY_FILE, MATLAB_DIR, config['bucket_name'],
                             config['input_rain_file'], config['input_rain_file'])
    except Exception as e:
        print('download_rain_input_files|Exception : ', str(e))
        return False


def download_tide_input_files(bucket_time, config):
    try:
        download_input_files(bucket_time, KEY_FILE, MATLAB_DIR, config['bucket_name'],
                             config['input_tide_file'], config['input_tide_file'])
    except Exception as e:
        print('download_tide_input_files|Exception : ', str(e))
        return False


def download_discharge_input_files(bucket_time, config):
    try:
        download_input_files(bucket_time, KEY_FILE, MATLAB_DIR, config['bucket_name'],
                             config['input_discharge_file'], config['input_discharge_file'])
    except Exception as e:
        print('download_discharge_input_files|Exception : ', str(e))
        return False


def download_input_files(bucket_time, key_file, output_dir, bucket_name, src_file, dest_file):
    try:
        source_blob_name = 'mike/inputs/{}/{}'.format(bucket_time, src_file)
        print('download_rain_input_files|source_blob_name : ', source_blob_name)
        destination_file_name = '{}/{}'.format(output_dir, dest_file)
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


def run_matlab_input_preparation():
    try:
        command = '.\windows_scripts\matlab_run.bat'
        print('run_matlab_input_preparation|command: ', command)
        subprocess.call(command, shell=True)
    except Exception as ex:
        print('run_matlab_input_preparation|Exception: ', str(ex))


def upload_matlab_rain_file(bucket_time, config):
    try:
        upload_file_to_bucket(bucket_time, KEY_FILE, MATLAB_DIR, config['bucket_name'],
                             config['input_discharge_file'], config['input_discharge_file'])
    except Exception as e:
        print('download_discharge_input_files|Exception : ', str(e))
        return False


def upload_file_to_bucket(bucket_time, key_file, output_dir, bucket_name, src_file, dest_file):
    try:
        client = storage.Client.from_service_account_json(key_file)
        bucket = client.get_bucket(bucket_name)
        destination_file_name = 'mike/inputs/{}/{}'.format(bucket_time, src_file)
        source_file_name = '{}/{}'.format(output_dir, dest_file)
        blob = bucket.blob(destination_file_name)
        blob.upload_from_filename(source_file_name)
        print("File {} uploaded to {}.".format(source_file_name, destination_file_name))
        return True
    except Exception as e:
        print('upload_file_to_bucket|Exception : ', str(e))
        return False

