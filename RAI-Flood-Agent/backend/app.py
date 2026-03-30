"""
FastAPI application to serve the RAI Flood Agent data to the frontend.
"""

import sys
import os

# Add root folder to path so backend/ and simulation/ modules are found
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  # type: ignore
from fastapi.staticfiles import StaticFiles
from simulation.disaster_simulator import get_dynamic_scenario
from backend.rai_agent_controller import RAIFloodAgent

app = FastAPI(title="RAI Flood Agent API")

# Mount static files to serve the frontend
app.mount("/frontend", StaticFiles(directory=os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "frontend"))), name="frontend")

# Enable CORS for the frontend to access the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # For local development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

agent = RAIFloodAgent()

@app.get("/api/simulation")
def run_simulation():
    """Runs the mock scenario and returns the agent's decision data."""
    scenario = get_dynamic_scenario()
    results = agent.process_scenario(scenario)
    return results

if __name__ == "__main__":
    import uvicorn
    # Pass the app instance directly to avoid pathing / module import issues
    uvicorn.run(app, host="127.0.0.1", port=8000)
