from datetime import datetime,timedelta
from utils.com_utils import download_input_files, upload_file_to_bucket, KEY_FILE, remove_previous_run_file_in_dir, \
    remove_previous_run_file
import subprocess
import time

M11_SIM_FILE = r"E:\MIKE\ProductionRun\hourly_run\MIKE11\Simulations\M11_Forcast.sim11"
# M11_SIM_FILE = "/home/hasitha/PycharmProjects/MikeAutomation/output/M11_Forcast.sim11"
M21_SIM_FILE = r"E:\MIKE\ProductionRun\hourly_run\MIKE21\Simulations\M21_Forcast.m21"

M11_SIM_FILE_TEMPLATE = r"E:\MIKE\ProductionRun\hourly_run\MikeAutomation\model\mike_scripts\M11_Forcast_template.sim11"
# M11_SIM_FILE_TEMPLATE = "/home/hasitha/PycharmProjects/MikeAutomation/model/mike_scripts/M11_Forcast_template.sim11"
M21_SIM_FILE_TEMPLATE = r"E:\MIKE\ProductionRun\hourly_run\MikeAutomation\model\mike_scripts\M21_Forcast_template.m21"

BC_DIR = r"E:\MIKE\ProductionRun\hourly_run\MIKE11\BoundaryConditions"
RAIN_DIR = r"E:\MIKE\ProductionRun\hourly_run\MIKE11\RR"

MATLAB_DIR = r"E:\MIKE\ProductionRun\hourly_run\Matlab"

RESULTS_DIR = r"E:\MIKE\ProductionRun\hourly_run\Results"


def download_rain_matlab_file(bucket_time, config):
    try:
        return download_input_files(bucket_time, KEY_FILE, RAIN_DIR, config['bucket_name'],
                             config['matlab_rain_file'], config['matlab_rain_file'], 'inputs')
    except Exception as e:
        print('download_rain_matlab_file|Exception : ', str(e))
        return False


def download_tide_matlab_file(bucket_time, config):
    try:
        return download_input_files(bucket_time, KEY_FILE, BC_DIR, config['bucket_name'],
                             config['matlab_tide_file'], config['matlab_tide_file'], 'inputs')
    except Exception as e:
        print('download_tide_matlab_file|Exception : ', str(e))
        return False


def download_dis_matlab_file(bucket_time, config):
    try:
        return download_input_files(bucket_time, KEY_FILE, BC_DIR, config['bucket_name'],
                             config['matlab_discharge_file'], config['matlab_discharge_file'], 'inputs')
    except Exception as e:
        print('download_dis_matlab_file|Exception : ', str(e))
        return False


def _write_data_to_file(file_name, file_data):
    file1 = open(file_name, "w")
    file1.write(file_data)
    file1.close()


def update_mike11_sim_file(bucket_time, config):
    # start = 2020, 9, 6, 0, 0, 0
    # end = 2020, 9, 11, 0, 0, 0
    print('update_mike11_sim_file|bucket_time : ', bucket_time)
    bucket_time = datetime.strptime(bucket_time, '%Y-%m-%d_%H-00-00')
    run_time = datetime.strptime(bucket_time.strftime('%Y-%m-%d 00:00:00'), '%Y-%m-%d 00:00:00')
    start_time = (run_time - timedelta(days=config['backward_days'])).strftime('%Y, %m, %d, 0, 0, 0')
    end_time = (run_time + timedelta(days=config['forward_days'])).strftime('%Y, %m, %d, 0, 0, 0')
    print('update_mike11_sim_file|start_time : ', start_time)
    print('update_mike11_sim_file|end_time : ', end_time)
    with open(M11_SIM_FILE_TEMPLATE, 'r') as file:
        file_data = file.read().replace('{START_TIME}', start_time).replace('{END_TIME}', end_time)
        print('update_mike11_sim_file|file_data : ', file_data)
        _write_data_to_file(M11_SIM_FILE, file_data)
        return True


def update_mike21_sim_file(bucket_time, config):
    # Start_Time = {2020, 9, 6, 0, 0, 0}
    print('update_mike21_sim_file|bucket_time : ', bucket_time)
    bucket_time = datetime.strptime(bucket_time, '%Y-%m-%d_%H-00-00')
    run_time = datetime.strptime(bucket_time.strftime('%Y-%m-%d 00:00:00'), '%Y-%m-%d 00:00:00')
    start_time = (run_time - timedelta(days=config['backward_days'])).strftime('%Y, %m, %d, 0, 0, 0')
    print('update_mike21_sim_file|start_time : ', start_time)
    with open(M21_SIM_FILE_TEMPLATE, 'r') as file:
        file_data = file.read().replace('{START_TIME}', start_time)
        _write_data_to_file(M21_SIM_FILE, file_data)
        return True


def remove_prevous_run_files(config):
    remove_previous_run_file(M11_SIM_FILE)
    remove_previous_run_file(M21_SIM_FILE)
    remove_previous_run_file_in_dir(BC_DIR, config['matlab_discharge_file'])
    remove_previous_run_file_in_dir(BC_DIR, config['matlab_tide_file'])
    remove_previous_run_file_in_dir(RAIN_DIR, config['matlab_rain_file'])
    remove_previous_run_file_in_dir(RESULTS_DIR, config['output_wl_file'])


def mike_run(bucket_time, config):
    try:
        if download_rain_matlab_file(bucket_time, config):
            if download_tide_matlab_file(bucket_time, config):
                if download_dis_matlab_file(bucket_time, config):
                    if update_mike11_sim_file(bucket_time, config):
                        if update_mike21_sim_file(bucket_time, config):
                            command = '.\windows_scripts\mike_run.bat'
                            print('mike_run|command: ', command)
                            subprocess.call(command, shell=True)
                            time.sleep(10)
                            upload_file_to_bucket(bucket_time, KEY_FILE, RESULTS_DIR, config['bucket_name'],
                                                  config['mike_result_file'], config['mike_result_file'], 'outputs')
                        else:
                            print('update_mike21_sim_file|failed')
                    else:
                        print('update_mike11_sim_file|failed')
                else:
                    print('download_dis_matlab_file|failed')
            else:
                print('download_tide_matlab_file|failed')
        else:
            print('download_rain_matlab_file|failed')
    except Exception as ex:
        print('mike_run|Exception: ', str(ex))


