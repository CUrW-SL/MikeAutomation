import subprocess

from google.cloud import storage
import os
KEY_FILE = r"E:\MIKE\ProductionRun\hourly_run\uwcc-admin\uwcc-admin.json"


def remove_previous_run_file_in_dir(dir_path, file_name):
    file_path = os.path.join(dir_path, file_name)
    remove_previous_run_file(file_path)


def remove_previous_run_file(file_path):
    try:
        print('remove_previous_run_file|file_path : ', file_path)
        command = 'del {}'.format(file_path)
        print('remove_previous_run_file|command : ', command)
        subprocess.call(command, shell=True)
        print('remove_previous_run_file|success.')
    except Exception as e:
        print('remove_previous_run_file|Exception : ', str(e))

def download_input_files(bucket_time, key_file, output_dir, bucket_name, src_file, dest_file, type):
    try:
        source_blob_name = 'mike/{}/{}/{}'.format(type, bucket_time, src_file)
        print('download_input_files|source_blob_name : ', source_blob_name)
        destination_file_name = '{}\{}'.format(output_dir, dest_file)
        print('download_input_files|destination_file_name : ', destination_file_name)
        storage_client = storage.Client.from_service_account_json(key_file)
        print('download_input_files|storage_client : ', storage_client)
        bucket = storage_client.bucket(bucket_name)
        print('download_input_files|bucket : ', bucket)
        blob = bucket.blob(source_blob_name)
        print('download_input_files|blob : ', blob.name)
        blob.download_to_filename(destination_file_name)
        print('Blob {} downloaded to {}.'.format(source_blob_name, destination_file_name))
        return True
    except Exception as e:
        print('download_files|Exception : ', str(e))
        return False


def upload_file_to_bucket(bucket_time, key_file, output_dir, bucket_name, src_file, dest_file, type):
    try:
        client = storage.Client.from_service_account_json(key_file)
        bucket = client.get_bucket(bucket_name)
        destination_file_name = 'mike/{}/{}/{}'.format(type, bucket_time, src_file)
        source_file_name = '{}\{}'.format(output_dir, dest_file)
        blob = bucket.blob(destination_file_name)
        blob.upload_from_filename(source_file_name)
        print("File {} uploaded to {}.".format(source_file_name, destination_file_name))
        return True
    except Exception as e:
        print('upload_file_to_bucket|Exception : ', str(e))
        return False

