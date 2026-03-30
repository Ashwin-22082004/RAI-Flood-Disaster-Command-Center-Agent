import sys
import os

# Add parent directory to path
sys.path.append(os.getcwd())

try:
    print("Testing imports from backend.agents...")
    from backend.agents import (
        FloodMonitoringAgent, VulnerabilityAgent, DamManagementAgent, 
        RescueCoordinationAgent, SupplyChainAgent, DroneDeploymentAgent, 
        PreFloodWarningAgent, PostDisasterAssessmentAgent, EvacuationCoordinationAgent
    )
    print("Success: All agents imported.")

    print("Testing initialization of RAIFloodAgent...")
    from backend.rai_agent_controller import RAIFloodAgent
    agent = RAIFloodAgent()
    print("Success: RAIFloodAgent initialized.")

    print("Testing simulation data fetch...")
    from simulation.disaster_simulator import get_dynamic_scenario
    scenario = get_dynamic_scenario()
    print("Success: Scenario data generated.")

    print("Running process_scenario...")
    results = agent.process_scenario(scenario)
    print("Success: Simulation run complete.")
    
except Exception as e:
    print(f"FAILED: {e}")
    import traceback
    traceback.print_exc()
