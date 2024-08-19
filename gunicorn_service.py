import os
import multiprocessing

# Set the Django settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.pro")

# Set the working directory
working_dir = (
    "/opt/usr/devs/jas_test/jasmin-dashboard-master"  # change this to your working dir
)
os.chdir(working_dir)

# Set the Gunicorn command
cmd = "/opt/usr/devs/jas_test/jasmin-dashboard-master/venv/bin/gunicorn"  # change this to your working dir leave the venv/bin/gunicorn
args = [
    "config.wsgi",
    "--bind=127.0.0.1:8090",  # can change
    "--workers=%d"
    % (multiprocessing.cpu_count() * 2 + 1),  # Adjust the number of workers as needed
    "--timeout=120",
    "--log-level=error",
    "--log-file=-",  # Log to stdout/stderr
    "--access-logfile=-",  # Log access to stdout/stderr
    "--capture-output",
    "--enable-stdio-inheritance",
]

# Set environment variables
env = {
    "DJANGO_SETTINGS_MODULE": "config.settings.pro",
    "USER": "zayyadev",  # change this to your computer username
    "GROUP": "zayyadev",  # change this to your computer username
}

# Run Gunicorn
print("Server started on http://127.0.0.1:8090")
os.execvpe(cmd, [cmd] + args, env)
