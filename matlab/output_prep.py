import subprocess

from utils.com_utils import download_input_files, upload_file_to_bucket, KEY_FILE

MATLAB_DIR = r"E:\MIKE\ProductionRun\hourly_run\Matlab"
MATLAB_INPUT_PROCESSOR = r"E:\MIKE\ProductionRun\hourly_run\MikeAutomation\windows_scripts\matlab_input_process.bat"


def prepare_outputs(bucket_time, config):
    print('prepare_outputs|started')
    download_mike_rain_output_files(bucket_time, config)
    print('prepare_outputs|completed')


def download_mike_rain_output_files(bucket_time, config):
    try:
        download_input_files(bucket_time, KEY_FILE, MATLAB_DIR, config['bucket_name'],
                             config['mike_result_file'], config['mike_result_file'])
    except Exception as e:
        print('download_mike_rain_output_files|Exception : ', str(e))
        return False


def run_matlab_output_preparation(bucket_time, config):
    try:
        command = '.\windows_scripts\matlab_output_process.bat'
        print('run_matlab_input_preparation|command: ', command)
        subprocess.call(command, shell=True)
        upload_file_to_bucket(bucket_time, KEY_FILE, MATLAB_DIR, config['bucket_name'],
                              config['output_wl_file'], config['output_wl_file'], 'output')
    except Exception as ex:
        print('run_matlab_output_preparation|Exception: ', str(ex))

