import json
import traceback
from datetime import datetime,timedelta
from input.input_prep import download_rain_input_files, \
    download_tide_input_files, download_discharge_input_files, \
    run_matlab_input_preparation, upload_matlab_rain_file, \
    upload_matlab_tide_file, upload_matlab_dis_file


def _get_config(config_path):
    config = None
    try:
        config = json.loads(open(config_path).read())
    except FileNotFoundError as nofile:
        print('get_config|FileNotFoundError : ', str(nofile))
        traceback.print_exc()
    finally:
        return config


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    config_path = r"E:\MIKE\ProductionRun\hourly_run\MikeAutomation\config.json"
    run_date = datetime.now().strftime('%Y-%m-%d %H:00:00')
    #bucket_time = datetime.now().strftime('%Y-%m-%d_%H-00-00')
    bucket_time = '2020-09-14_10-00-00'
    print('run_date : ', run_date)
    print('bucket_time : ', bucket_time)
    config = _get_config(config_path)
    print('config : ', config)
    download_rain_input_files(bucket_time, config)
    download_tide_input_files(bucket_time, config)
    download_discharge_input_files(bucket_time, config)
    run_matlab_input_preparation()
    upload_matlab_rain_file(bucket_time, config)
    upload_matlab_tide_file(bucket_time, config)
    upload_matlab_dis_file(bucket_time, config)

