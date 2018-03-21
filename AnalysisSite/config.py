# TODO
#   - If you need more modules at one machine, than edit this part
#   - If you want to know total number of gpu, than use GPUtil and GPUtil.getGPUs()


WORKER_MIN_SCALER = 20
WORKER_MAX_SCALER = 50
WORKER_CONCURRENCY = (WORKER_MIN_SCALER + WORKER_MAX_SCALER) // 2
