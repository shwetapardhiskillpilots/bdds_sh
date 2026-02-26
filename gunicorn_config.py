import multiprocessing

# Gunicorn configuration file for BDDS Production

# IP and Port to bind
bind = "0.0.0.0:8000"

# Process Name
proc_name = "bdds_incident_system"

# Worker type - Use Uvicorn's ASGI worker for async performance
worker_class = "uvicorn.workers.UvicornWorker"

# Worker count - Recommendation: (2 x cores) + 1
# Based on your 8-core system, we use 17 workers
workers = (multiprocessing.cpu_count() * 2) + 1

# Maximum number of simultaneous clients
# Each worker can handle many concurrent connections, but we can tune this
worker_connections = 1000

# Timeout for workers
timeout = 300

# Keepalive for connections
keepalive = 5

# Logging
accesslog = "-"  # Log to stdout
errorlog = "-"   # Log to stderr
loglevel = "info"

# Security: Don't run as root in production!
# user = "bdds_user"
# group = "bdds_group"
