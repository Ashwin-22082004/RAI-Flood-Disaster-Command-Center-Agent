"""
RAI Agent Controller

The main decision engine orchestrating inputs from flood detection, dam management, 
and vulnerability models to issue resource allocation and logistics commands.
"""

from backend.agents import (
    FloodMonitoringAgent, VulnerabilityAgent, DamManagementAgent, 
    RescueCoordinationAgent, SupplyChainAgent, DroneDeploymentAgent, 
    PreFloodWarningAgent, PostDisasterAssessmentAgent, EvacuationCoordinationAgent
)

class RAIFloodAgent:
    """
    Main controller representing the RAI Flood Disaster Command Center.
    Coordinates the 8 cooperating AI agents with live visualization data.
    """
    
    def __init__(self):
         self.logs = []

    def log_action(self, action_dict):
        # action_dict contains 'message' and 'type' keys
        self.logs.append(action_dict)

    def process_scenario(self, scenario_data):
        """
        Executes the multi-agent disaster response workflow sequentially.
        """
        self.logs = [] # Reset logs per run
        self.log_action({"message": "Initializing RAI Flood Disaster Command Center multi-agent sequence.", "type": "info"})
        
        # 1. Pre-Flood Warning Agent
        warning_agent = PreFloodWarningAgent()
        warnings, warning_logs = warning_agent.execute(scenario_data)
        for log in warning_logs: self.log_action(log)

        # 2. Flood Monitoring Agent
        flood_agent = FloodMonitoringAgent()
        flood_map, alerts, flood_logs = flood_agent.execute(scenario_data)
        for log in flood_logs: self.log_action(log)
        
        # 3. Vulnerability Agent
        vuln_agent = VulnerabilityAgent()
        vulnerability_map, regions_status, downstream_critical, vuln_logs = vuln_agent.execute(scenario_data, flood_map)
        for log in vuln_logs: self.log_action(log)

        # 4. Dam Management Agent
        dam_agent = DamManagementAgent()
        dam_decision, dam_alerts, dam_logs = dam_agent.execute(scenario_data['dam'], downstream_critical)
        alerts.extend(dam_alerts)
        for log in dam_logs: self.log_action(log)

        # 5. Drone Deployment Agent
        drone_agent = DroneDeploymentAgent()
        drone_missions, drone_logs = drone_agent.execute(flood_map, dam_decision)
        for log in drone_logs: self.log_action(log)

        # 6. Rescue Coordination Agent
        rescue_agent = RescueCoordinationAgent()
        allocation_plan, moving_units, rescue_logs = rescue_agent.execute(vulnerability_map, scenario_data['available_resources'], regions_status)
        for log in rescue_logs: self.log_action(log)

        # 7. Evacuation Coordination Agent
        evac_agent = EvacuationCoordinationAgent()
        evacuation_data, evac_logs = evac_agent.execute(scenario_data, flood_map, vulnerability_map)
        for log in evac_logs: self.log_action(log)
            
        # 8. Supply Chain Agent
        supply_agent = SupplyChainAgent()
        logistics_plan, supply_logs = supply_agent.execute(scenario_data, vulnerability_map)
        for log in supply_logs: self.log_action(log)

        # 9. Post-Disaster Assessment Agent
        assessment_agent = PostDisasterAssessmentAgent()
        reports, assessment_logs = assessment_agent.execute(scenario_data, flood_map)
        for log in assessment_logs: self.log_action(log)

        self.log_action({"message": "All cooperating agents have resolved. Output ready for dashboard.", "type": "info"})

        return {
            'alerts': alerts + warnings,
            'flood_map': flood_map,
            'dam_decision': dam_decision,
            'vulnerability_map': vulnerability_map,
            'allocation_plan': allocation_plan,
            'logistics_plan': logistics_plan,
            'drone_missions': drone_missions,
            'damage_reports': reports,
            'moving_units': moving_units,
            'evacuation_data': evacuation_data,
            'agent_logs': self.logs
        }

