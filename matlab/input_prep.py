import subprocess

from utils.com_utils import download_input_files, upload_file_to_bucket, KEY_FILE

MATLAB_DIR = r"E:\MIKE\ProductionRun\hourly_run\Matlab"
MATLAB_INPUT_PROCESSOR = r"E:\MIKE\ProductionRun\hourly_run\MikeAutomation\windows_scripts\matlab_input_process.bat"


def prepare_inputs(bucket_time, config):
    print('prepare_inputs|started')
    download_rain_input_files(bucket_time, config)
    download_tide_input_files(bucket_time, config)
    download_discharge_input_files(bucket_time, config)
    run_matlab_input_preparation()
    upload_matlab_rain_file(bucket_time, config, 'inputs')
    upload_matlab_tide_file(bucket_time, config, 'inputs')
    upload_matlab_dis_file(bucket_time, config, 'inputs')
    print('prepare_inputs|completed')


def download_rain_input_files(bucket_time, config):
    try:
        download_input_files(bucket_time, KEY_FILE, MATLAB_DIR, config['bucket_name'],
                             config['input_rain_file'], config['input_rain_file'], 'inputs')
    except Exception as e:
        print('download_rain_input_files|Exception : ', str(e))
        return False


def download_tide_input_files(bucket_time, config):
    try:
        download_input_files(bucket_time, KEY_FILE, MATLAB_DIR, config['bucket_name'],
                             config['input_tide_file'], config['input_tide_file'], 'inputs')
    except Exception as e:
        print('download_tide_input_files|Exception : ', str(e))
        return False


def download_discharge_input_files(bucket_time, config):
    try:
        download_input_files(bucket_time, KEY_FILE, MATLAB_DIR, config['bucket_name'],
                             config['input_discharge_file'], config['input_discharge_file'], 'inputs')
    except Exception as e:
        print('download_discharge_input_files|Exception : ', str(e))
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
                             config['matlab_rain_file'], config['matlab_rain_file'], 'inputs')
    except Exception as e:
        print('download_discharge_input_files|Exception : ', str(e))
        return False


def upload_matlab_tide_file(bucket_time, config):
    try:
        upload_file_to_bucket(bucket_time, KEY_FILE, MATLAB_DIR, config['bucket_name'],
                              config['matlab_tide_file'], config['matlab_tide_file'], 'inputs')
    except Exception as e:
        print('download_discharge_input_files|Exception : ', str(e))
        return False


def upload_matlab_dis_file(bucket_time, config):
    try:
        upload_file_to_bucket(bucket_time, KEY_FILE, MATLAB_DIR, config['bucket_name'],
                              config['matlab_discharge_file'], config['matlab_discharge_file'], 'inputs')
    except Exception as e:
        print('download_discharge_input_files|Exception : ', str(e))
        return False
