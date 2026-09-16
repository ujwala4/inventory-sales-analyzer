import subprocess
import time


# Start FastAPI
api_process = subprocess.Popen(
    [
        "uvicorn",
        "api:app",
        "--host",
        "127.0.0.1",
        "--port",
        "8000"
    ]
)


# Give FastAPI a moment to start
time.sleep(3)


# Start Gradio
subprocess.run(
    [
        "python",
        "app.py"
    ]
)