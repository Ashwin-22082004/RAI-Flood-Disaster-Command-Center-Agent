import sys
import os
import json

# Ensure the correct path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from simulation.disaster_simulator import get_dynamic_scenario
from backend.rai_agent_controller import RAIFloodAgent

try:
    controller = RAIFloodAgent()
    scenario = get_dynamic_scenario()
    results = controller.process_scenario(scenario)
    
    # Extract only the flood_map for Inspection
    flood_map = results.get('flood_map', {})
    print(json.dumps(flood_map, indent=2))
    
except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)
