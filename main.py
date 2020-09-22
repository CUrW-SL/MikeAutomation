import json
import traceback
from datetime import datetime
from matlab.input_prep import prepare_inputs
from model.model_run import mike_run
from matlab.output_prep import prepare_outputs


def _get_config(config_path):
    config = None
    try:
        config = json.loads(open(config_path).read())
    except FileNotFoundError as nofile:
        print('get_config|FileNotFoundError : ', str(nofile))
        traceback.print_exc()
    finally:
        return config


def input_process(config_path, bucket_time):
    print('input_process')
    config = _get_config(config_path)
    try:
        prepare_inputs(bucket_time, config)
    except Exception as ex:
        print('input_process|Exception : ', str(ex))
        traceback.print_exc()


def model_run(config_path, bucket_time):
    print('model_run')
    config = _get_config(config_path)
    try:
        mike_run(bucket_time, config)
    except Exception as ex:
        print('model_run|Exception : ', str(ex))
        traceback.print_exc()


def output_process(config_path, bucket_time):
    print('output_process')
    config = _get_config(config_path)
    try:
        prepare_outputs(bucket_time, config)
    except Exception as ex:
        print('output_process|Exception : ', str(ex))
        traceback.print_exc()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    config_path = r"E:\MIKE\ProductionRun\hourly_run\MikeAutomation\config.json"
    # config_path = "/home/hasitha/PycharmProjects/MikeAutomation/config.json"
    run_date = datetime.now().strftime('%Y-%m-%d %H:00:00')
    #bucket_time = datetime.now().strftime('%Y-%m-%d_%H-00-00')
    # bucket_time = '2020-09-09_10-00-00'
    bucket_time = '2020-09-10_09-00-00'
    print('run_date : ', run_date)
    print('bucket_time : ', bucket_time)
    config = _get_config(config_path)
    print('config : ', config)
    #prepare_inputs(bucket_time, config)
    #update_mike11_sim_file(bucket_time, config)

