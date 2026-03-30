"""
Disaster Simulator

Simulates flood events to evaluate the Responsible AI Disaster Management Agent.
"""

import sys
import os
import json

# Ensure backend modules can be imported when running from simulation/
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.rai_agent_controller import RAIFloodAgent  # type: ignore

import random

def get_dynamic_scenario():
    """Generates a dynamic disaster scenario with varied parameters per run."""
    
    # Randomly fluctuate dam levels
    base_dam_level = random.uniform(2390.0, 2404.0)
    forecast_rain = random.uniform(50.0, 300.0)
    
    # Helper to generate region data
    def random_region(name, x, y, has_dam=False, is_base=False, has_shelter=False):
        return {
            "name": name,
            "x": x,
            "y": y,
            "has_dam": has_dam,
            "is_base": is_base,
            "has_shelter": has_shelter,
            "rainfall": random.uniform(0.1, 1.0),
            "discharge": random.uniform(0.2, 1.0),
            "soil_saturation": random.uniform(0.4, 1.0),
            "satellite_data": random.uniform(0.3, 1.0),
            "pop_density": random.uniform(0.3, 1.0),
            "hospital_availability_deficit": random.uniform(0.2, 0.9),
            "elderly_pop": random.uniform(0.2, 0.6),
            "infra_damage": random.uniform(0.1, 0.95),
            "evacuation_access_deficit": random.uniform(0.2, 0.8)
        }
        
    # Explicit regional mapping for stable visualization
    selected_regions = [
        random_region("Kochi Base", 15, 15, is_base=True),
        random_region("Ernakulam", 30, 60, has_shelter=True),
        random_region("Idukki", 60, 40, has_dam=True),
        random_region("Thiruvananthapuram", 45, 85, has_shelter=True),
        random_region("Kottayam", 50, 55, has_shelter=True)
    ]

    return {
        "name": f"Dynamic Simulation Run {random.randint(1000, 9999)}",
        "season": "Monsoon",
        "dam": {
            "name": "Idukki Dam",
            "current_level": round(base_dam_level, 2),
            "forecast_rainfall": round(forecast_rain, 2), 
            "safe_capacity": 2403.0,
            "season": "Monsoon",
            "rainfall_forecast": round(random.uniform(50, 400), 2)
        },
        "regions": selected_regions,
        "available_resources": {
            "rescue_boats": random.randint(30, 100),
            "helicopters": random.randint(5, 15),
            "medical_teams": random.randint(20, 50),
            "food_supplies": random.randint(5000, 20000),
            "evacuation_vehicles": random.randint(50, 200)
        },
        "warehouse_node": "Kochi Base",
        "infrastructure_nodes": [r['name'] for r in selected_regions],
        "road_network": {
            "Kochi Base": {"Ernakulam": 15, "Kottayam": 60},
            "Ernakulam": {"Kochi Base": 15, "Idukki": 110, "Kottayam": 60},
            "Kottayam": {"Kochi Base": 60, "Ernakulam": 60, "Idukki": 90, "Thiruvananthapuram": 150},
            "Idukki": {"Ernakulam": 110, "Kottayam": 90},
            "Thiruvananthapuram": {"Kottayam": 150}
        }
    }

def get_kerala_2018_scenario():
    """Returns a scenario reflective of the 2018 Kerala Flood event."""
    return {
        "name": "Kerala 2018 Historical Flood Simulation",
        "season": "Monsoon",
        "dam": {
            "name": "Idukki Dam",
            "current_level": 2401.5,
            "forecast_rainfall": 450.0,
            "safe_capacity": 2403.0,
            "season": "Monsoon",
            "rainfall_forecast": 500.0
        },
        "regions": [
            {
                "name": "Kochi Base", "x": 15, "y": 15, "is_base": True,
                "rainfall": 0.9, "discharge": 0.8, "soil_saturation": 0.95,
                "pop_density": 0.8, "infra_damage": 0.4, "elderly_pop": 0.3
            },
            {
                "name": "Ernakulam", "x": 30, "y": 60, "has_shelter": True,
                "rainfall": 0.95, "discharge": 0.9, "soil_saturation": 0.98,
                "pop_density": 0.9, "infra_damage": 0.7, "elderly_pop": 0.4
            },
            {
                "name": "Idukki", "x": 60, "y": 40, "has_dam": True,
                "rainfall": 1.0, "discharge": 1.0, "soil_saturation": 1.0,
                "pop_density": 0.4, "infra_damage": 0.8, "elderly_pop": 0.5
            },
            {
                "name": "Thiruvananthapuram", "x": 45, "y": 85, "has_shelter": True,
                "rainfall": 0.7, "discharge": 0.6, "soil_saturation": 0.8,
                "pop_density": 0.7, "infra_damage": 0.3, "elderly_pop": 0.4
            },
            {
                "name": "Kottayam", "x": 50, "y": 55, "has_shelter": True,
                "rainfall": 0.85, "discharge": 0.8, "soil_saturation": 0.9,
                "pop_density": 0.6, "infra_damage": 0.6, "elderly_pop": 0.4
            }
        ],
        "available_resources": {
            "rescue_boats": 50,
            "helicopters": 10,
            "medical_teams": 30,
            "food_supplies": 10000,
            "evacuation_vehicles": 100
        },
        "warehouse_node": "Kochi Base",
        "infrastructure_nodes": ["Kochi Base", "Ernakulam", "Idukki", "Thiruvananthapuram", "Kottayam"],
        "road_network": {
            "Kochi Base": {"Ernakulam": 15, "Kottayam": 60},
            "Ernakulam": {"Kochi Base": 15, "Idukki": 110, "Kottayam": 60},
            "Kottayam": {"Kochi Base": 60, "Ernakulam": 60, "Idukki": 90, "Thiruvananthapuram": 150},
            "Idukki": {"Ernakulam": 110, "Kottayam": 90},
            "Thiruvananthapuram": {"Kottayam": 150}
        }
    }

def run_simulation():
    print("Starting RAI Flood Disaster Simulation...")
    agent = RAIFloodAgent()
    scenario = get_dynamic_scenario()
    
    results = agent.process_scenario(scenario)
    
    print("\n--- Simulation Results ---")
    print(json.dumps(results, indent=2))
    
    return results

if __name__ == "__main__":
    run_simulation()

