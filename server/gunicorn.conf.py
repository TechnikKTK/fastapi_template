import multiprocessing


bind = "127.0.0.1:5555"
workers = 2 * multiprocessing.cpu_count() + 1
user = "ds_owner"
timeout = 120
worker_class = "uvicorn.workers.UvicornWorker"
