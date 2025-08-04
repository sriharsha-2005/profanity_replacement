import multiprocessing
import os

# Server socket
bind = "0.0.0.0:" + os.environ.get("PORT", "5000")
backlog = 2048

# Worker processes
workers = 1  # Use only 1 worker to avoid memory issues
worker_class = "sync"
worker_connections = 1000
max_requests = 1000
max_requests_jitter = 50
preload_app = True

# Timeout settings
timeout = 600  # 10 minutes timeout for video processing
keepalive = 2
graceful_timeout = 600

# Memory and process settings
max_requests_jitter = 50
worker_tmp_dir = "/dev/shm"  # Use RAM for temporary files
worker_exit_on_app = False

# Logging
accesslog = "-"
errorlog = "-"
loglevel = "info"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s'

# Process naming
proc_name = "profanity_replacement"

# Security
limit_request_line = 4094
limit_request_fields = 100
limit_request_field_size = 8190

# Memory management
worker_rlimit_nofile = 65536 