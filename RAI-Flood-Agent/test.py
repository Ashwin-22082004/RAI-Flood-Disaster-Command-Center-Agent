import sys
import os

# Ensure the correct path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from simulation.disaster_simulator import get_dynamic_scenario
from backend.rai_agent_controller import RAIFloodAgent

try:
    print("Running Multi-Agent Scenario...")
    controller = RAIFloodAgent()
    scenario = get_dynamic_scenario()
    results = controller.process_scenario(scenario)
    
    print(f"Success! Generated {len(results.get('flood_map', {}))} regions.")
    for name, info in results.get('flood_map', {}).items():
        print(f" - {name}: x={info.get('x')}, y={info.get('y')}")
    print(f"Total AI reasoning logs: {len(results.get('agent_logs', []))}")
    print(f"Top alert: {results.get('alerts')[0]['message'] if results.get('alerts') else 'No alerts'}")
except Exception as e:
    print(f"Error during simulation: {e}")
    sys.exit(1)
