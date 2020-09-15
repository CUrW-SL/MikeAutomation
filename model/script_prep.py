from google.cloud import storage

from utils.com_utils import download_input_files, upload_file_to_bucket


M11_SIM_FILE = r"E:\MIKE\ProductionRun\hourly_run\Matlab"
M11_SIM_FILE = r"E:\MIKE\ProductionRun\hourly_run\Matlab"


def update_mike11_sim_file(bucket_time, config):
    # start = 2020, 9, 6, 0, 0, 0
    # end = 2020, 9, 11, 0, 0, 0
    print('update_mike11_sim_file|bucket_time : ', bucket_time)


def update_mike21_sim_file(bucket_time, config):
    # Start_Time = {2020, 9, 6, 0, 0, 0}
    print('update_mike21_sim_file|bucket_time : ', bucket_time)


