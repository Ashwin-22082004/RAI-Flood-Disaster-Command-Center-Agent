from backend.flood_detection import generate_flood_map
from backend.dam_management import calculate_safe_release
from backend.vulnerability_model import map_vulnerabilities
from backend.resource_allocator import allocate_resources
from backend.logistics_optimizer import optimize_routes
import random

class Agent:
    def __init__(self, name):
        self.name = name

    def log(self, message):
        return {"message": f"[{self.name}] {message}", "type": "decision"}

class FloodMonitoringAgent(Agent):
    def __init__(self):
        super().__init__("Flood Agent")

    def execute(self, scenario_data):
        flood_map = generate_flood_map(scenario_data['regions'])
        alerts = []
        for region_info in flood_map.values():
            alerts.extend(region_info.get('alerts', []))
            
        logs = [self.log("Environmental data quantified. District-level severity assigned.")]
        return flood_map, alerts, logs

class VulnerabilityAgent(Agent):
    def __init__(self):
        super().__init__("Vulnerability Agent")

    def execute(self, scenario_data, flood_map):
        regions_status = []
        for region in scenario_data['regions']:
            status = dict(region)
            status['flood_severity'] = flood_map[region['name']]['severity_index']
            regions_status.append(status)
            
        vulnerability_map = map_vulnerabilities(regions_status)
        logs = [self.log("Computed holistic district vulnerability utilizing demographic matrices.")]
        
        downstream_critical = any(v > 0.8 for v in vulnerability_map.values())
        return vulnerability_map, regions_status, downstream_critical, logs

class DamManagementAgent(Agent):
    def __init__(self):
        super().__init__("Dam Agent")
        
    def execute(self, dam_data, downstream_critical):
        dam_decision = calculate_safe_release(
            dam_data['current_level'],
            dam_data['forecast_rainfall'],
            dam_data['safe_capacity'],
            dam_data['season'],
            downstream_critical
        )
        alerts = []
        if dam_decision.get('alert'):
            alerts.append(dam_decision['alert'])
            
        logs = [self.log(dam_decision['reasoning'])]
        return dam_decision, alerts, logs

class DroneDeploymentAgent(Agent):
    def __init__(self):
        super().__init__("Drone Agent")

    def execute(self, flood_map, dam_decision):
        drone_logs = []
        deployed_units = []
        
        for district, info in flood_map.items():
            severity = info.get('severity_index', 0)
            dam_risk = dam_decision.get('decision') == "Emergency Spillway Release"
            
            if severity > 0.8 or dam_risk:
                unit_id = f"D-{random.randint(10, 99)}"
                mission = "Aerial flood mapping, Victim detection, Thermal scanning"
                log_str = (
                    f"Drone Unit {unit_id} deployed to {district} district.\n\n"
                    f"Mission:\n{mission}\n\n"
                    f"Coverage Radius: 15 km"
                )
                drone_logs.append(self.log(log_str))
                deployed_units.append({
                    "unit_id": unit_id,
                    "district": district,
                    "mission": mission,
                    "status": "Deployed",
                    "path": [
                        {"x": 15, "y": 15},
                        {"x": info['x'], "y": info['y']}
                    ]
                })
        
        if not deployed_units:
            drone_logs.append(self.log("Environmental conditions stable. Drones on standby."))
            
        return deployed_units, drone_logs

class EvacuationCoordinationAgent(Agent):
    def __init__(self):
        super().__init__("Evacuation Agent")

    def execute(self, scenario_data, flood_map, vulnerability_map):
        evacuation_data = []
        logs = []
        
        shelters = [r for r in scenario_data['regions'] if r.get('has_shelter')]
        
        for district, info in flood_map.items():
            if info.get('severity_index', 0) > 0.6: 
                vuln = vulnerability_map.get(district, 0)
                dist_x, dist_y = info['x'], info['y']
                nearest_shelter = min(shelters, key=lambda s: ((s['x']-dist_x)**2 + (s['y']-dist_y)**2)**0.5)
                
                total_pop = 20000 # Mock pop base
                at_risk = int(total_pop * vuln)
                evacuated = int(at_risk * 0.7)
                
                evac_unit = {
                    "district": district,
                    "target_shelter": nearest_shelter['name'],
                    "at_risk": at_risk,
                    "evacuated": evacuated,
                    "remaining": at_risk - evacuated,
                    "source": {"x": dist_x, "y": dist_y},
                    "destination": {"x": nearest_shelter['x'], "y": nearest_shelter['y']}
                }
                evacuation_data.append(evac_unit)
                
                msg = (
                    f"EVACUATION IN PROGRESS\n"
                    f"District: {district} -> Shelter: {nearest_shelter['name']}\n"
                    f"Evacuated: {evacuated:,} | Remaining: {at_risk - evacuated:,}"
                )
                logs.append(self.log(msg))
                
        return evacuation_data, logs

class RescueCoordinationAgent(Agent):
    def __init__(self):
        super().__init__("Rescue Coordination Agent")
        
    def execute(self, vulnerability_map, available_resources, regions_status):
        allocation_plan, _ = allocate_resources(
            vulnerability_map, 
            available_resources,
            regions_status
        )
        
        base_regions = [r for r in regions_status if r.get('is_base')]
        default_base = base_regions[0] if base_regions else {"x": 10, "y": 10, "name": "Unknown Base"}

        moving_units = []
        logs = []
        
        for region_data in regions_status:
            region = region_data['name']
            if region in allocation_plan:
                plan = allocation_plan[region]
                dispatched_any = False
                
                for res_type, count in plan.items():
                    if count > 0:
                        dispatched_any = True
                        unit_type = "Vehicle"
                        if "boat" in res_type: unit_type = "Rescue Boat"
                        elif "helicopter" in res_type: unit_type = "Helicopter"
                        elif "medical" in res_type: unit_type = "Ambulance"
                        elif "vehicle" in res_type: unit_type = "Evacuation Bus"
                        
                        moving_units.append({
                            "type": unit_type,
                            "id": f"{res_type[0].upper()}-{random.randint(10, 99)}",
                            "source": {"x": default_base['x'], "y": default_base['y'], "name": default_base['name']},
                            "destination": {"x": region_data['x'], "y": region_data['y'], "name": region},
                            "status": "In Transit"
                        })

                if dispatched_any:
                    sev_score = region_data.get('flood_severity', 0)
                    log_str = (
                        f"Region: {region}\n"
                        f"Priority: {'CRITICAL' if sev_score > 0.8 else 'HIGH'}\n"
                        f"Action: Dispatched {plan.get('rescue_boats', 0)} boats, {plan.get('helicopters', 0)} helis."
                    )
                    logs.append(self.log(log_str))
                
        return allocation_plan, moving_units, logs

class PreFloodWarningAgent(Agent):
    def __init__(self):
        super().__init__("Warning Agent")

    def execute(self, scenario_data):
        warnings = []
        logs = []
        for region in scenario_data['regions']:
            rainfall_forecast = region.get('rainfall', 0) * 1.5 
            if rainfall_forecast > 0.8:
                prob = int(rainfall_forecast * 100)
                msg = (
                    f"PRE-FLOOD WARNING\n"
                    f"District: {region['name']}\n"
                    f"Forecast Rainfall: Extreme\n"
                    f"Flood Probability: {prob}%\n\n"
                    f"Recommended Actions: Lower dam levels, Activate shelters."
                )
                warnings.append({
                    "type": "PRE-FLOOD WARNING",
                    "district": region['name'],
                    "severity": "Urgent",
                    "message": "Heavy rainfall predicted. Activate preventive protocols."
                })
                logs.append(self.log(msg))
        
        if not warnings:
            logs.append(self.log("No extreme rainfall predicted in near-term forecast."))
        return warnings, logs

class PostDisasterAssessmentAgent(Agent):
    def __init__(self):
        super().__init__("Assessment Agent")

    def execute(self, scenario_data, flood_map):
        reports = []
        logs = []
        for district, info in flood_map.items():
            if info.get('severity_index', 0) > 0.5:
                displaced = random.randint(5000, 30000)
                infra_damage = "Severe" if info.get('severity_index', 0) > 0.8 else "Moderate"
                report = {
                    "district": district,
                    "displaced": f"{displaced:,}",
                    "infra_damage": infra_damage,
                    "medical_demand": "High" if infra_damage == "Severe" else "Medium"
                }
                reports.append(report)
                log_msg = f"POST-DISASTER DAMAGE REPORT\nDistrict: {district}\nDisplaced: {report['displaced']}\nInfra: {infra_damage}"
                logs.append(self.log(log_msg))
        return reports, logs

class SupplyChainAgent(Agent):
    def __init__(self):
        super().__init__("Supply Chain Agent")
        
    def execute(self, scenario_data, vulnerability_map):
        target_regions = [r for r in vulnerability_map.keys() if vulnerability_map[r] > 0]
        logistics_plan = optimize_routes(
            scenario_data['infrastructure_nodes'],
            scenario_data['road_network'],
            scenario_data['warehouse_node'],
            target_regions
        )
        logs = [self.log("Optimized disaster relief delivery pathways generated.")]
        return logistics_plan, logs
