import requests
import json

try:
    response = requests.get('http://127.0.0.1:8000/api/simulation')
    if response.status_code == 200:
        data = response.json()
        print(f"Simulation SUCCESS: {data.get('alerts', [])}")
        with open('simulation_results.json', 'w') as f:
            json.dump(data, f, indent=2)
    else:
        print(f"Simulation FAILED: {response.status_code}")
except Exception as e:
    print(f"Error: {e}")
