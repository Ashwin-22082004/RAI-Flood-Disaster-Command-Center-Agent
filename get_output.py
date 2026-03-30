import sys
import os
import json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'RAI-Flood-Agent')))

from simulation.disaster_simulator import get_kerala_2018_scenario
from backend.rai_agent_controller import RAIFloodAgent

agent = RAIFloodAgent()
scenario = get_kerala_2018_scenario()

results = agent.process_scenario(scenario)

with open('sim_out.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, indent=2)
