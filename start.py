import subprocess
import time
import sys

api_process = subprocess.Popen(
    [
        sys.executable,
        "-m",
        "uvicorn",
        "api:app",
        "--host",
        "127.0.0.1",
        "--port",
        "8000"
    ]
)

time.sleep(3)

try:
    subprocess.run(
        [
            sys.executable,
            "app.py"
        ],
        check=True
    )

finally:
    api_process.terminate()