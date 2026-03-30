import os
import sys
import time
import threading
import subprocess
import webbrowser

def install_requirements():
    print("=== Step 1: Installing/Verifying Dependencies ===")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "fastapi", "uvicorn", "pydantic"], stdout=subprocess.DEVNULL)
    print("Dependencies are fully installed!\n")

def start_backend():
    print("=== Step 2: Starting AI Backend API on Port 8000 ===")
    app_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "RAI-Flood-Agent")
    # Setting PYTHONPATH so the application resolves 'backend.something' cleanly
    env = os.environ.copy()
    env["PYTHONPATH"] = app_dir
    
    uvicorn_cmd = [sys.executable, "-m", "uvicorn", "backend.app:app", "--app-dir", app_dir, "--host", "127.0.0.1", "--port", "8000"]
    subprocess.call(uvicorn_cmd, env=env)

def start_frontend():
    print("=== Step 3: Starting Dashboard Local Server on Port 3000 ===")
    frontend_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "RAI-Flood-Agent", "frontend", "dashboard")
    os.chdir(frontend_dir)
    subprocess.call([sys.executable, "-m", "http.server", "3000"])

if __name__ == "__main__":
    print("\n" + "="*50)
    print("  RAI Flood Agent - Automated System Startup")
    print("="*50)
    print(f"\nUsing Python Environment: {sys.executable}\n")
    
    try:
        install_requirements()
    except Exception as e:
        print(f"Failed to install requirements: {e}")
        sys.exit(1)

    # Start servers
    backend_thread = threading.Thread(target=start_backend, daemon=True)
    backend_thread.start()

    frontend_thread = threading.Thread(target=start_frontend, daemon=True)
    frontend_thread.start()

    # Wait for servers to spin up
    print("Waiting 4 seconds for servers to initialize...\n")
    time.sleep(4)
    
    # Automatically open the browser tab for the user
    dashboard_url = "http://localhost:3000/index.html"
    print(f">>> Successfully deployed! Opening the dashboard at {dashboard_url} ... <<<")
    webbrowser.open(dashboard_url)

    print("\nSystem is Fully Operational! Keep this terminal open.")
    print("Press CTRL+C at any time in this terminal to safely shut down both servers.\n")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nShutting down RAI Flood Agent servers...")
