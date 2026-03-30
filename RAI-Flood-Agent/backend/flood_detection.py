"""
Flood Detection Module

Detects flood zones, classifies severity levels, and generates flood risk maps.
"""

import random

def process_region_data(region_data, flood_map):
    """
    Analyzes environmental data: rainfall, discharge, soil saturation, satellite data.
    """
    rainfall_intensity = region_data.get('rainfall', 0.0)
    river_discharge = region_data.get('discharge', 0.0)

    # Enhanced mock logic incorporating new variables
    base_severity = (rainfall_intensity * 0.4) + \
                    (river_discharge * 0.3) + \
                    (region_data.get('soil_saturation', 0.5) * 0.2) + \
                    (region_data.get('satellite_data', 0.5) * 0.1)
    
    severity = min(1.0, max(0.0, base_severity)) # Normalize 0.0 - 1.0
    
    # Categorize severity based on new scale:
    # 0–0.3 → Low
    # 0.3–0.6 → Moderate
    # 0.6–0.8 → High
    # 0.8–1.0 → Critical Risk
    classification = "Low Risk"
    alert = "Green Alert"
    alerts = []
    
    if severity >= 0.8:
        classification = "Critical Risk"
        alert = "Red Alert"
        alerts.append({
            "type": "FLOOD ALERT",
            "district": region_data['name'],
            "severity": classification,
            "risk_level": float(round(severity, 2)),
            "message": "Immediate evacuation recommended."
        })
    elif severity >= 0.6:
        classification = "High Risk"
        alert = "Orange Alert"
        if severity > 0.75: # The specific 0.75 trigger from requirements
            alerts.append({
                "type": "FLOOD ALERT",
                "district": region_data['name'],
                "severity": classification,
                "risk_level": float(round(severity, 2)),
                "message": "Prepare for potential evacuation. Risk exceeding 0.75 threshold."
            })
    elif severity >= 0.3:
        classification = "Moderate Risk"
        alert = "Yellow Alert"
        
    flood_map[region_data['name']] = {
        'x': region_data.get('x', 50),
        'y': region_data.get('y', 50),
        'has_dam': region_data.get('has_dam', False),
        'is_base': region_data.get('is_base', False),
        'has_shelter': region_data.get('has_shelter', False),
        'severity_index': float(round(severity, 3)),
        'classification': classification,
        'flood_alert': alert,
        'flood_possibility_level': f"{int(severity * 100)}%",
        'alerts': alerts
    }
    return flood_map

def generate_flood_map(region_data_list):
    """
    Generates a flood severity map based on region data.
    """
    flood_map = {}
    for region in region_data_list:
        process_region_data(region, flood_map)
        
    return flood_map

