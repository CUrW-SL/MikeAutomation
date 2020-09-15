from google.cloud import storage


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


