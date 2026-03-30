"""
Resource Allocation Engine

Responsible for ethical resource distribution based on calculated vulnerability 
scores and the principles of fairness and bias mitigation.
"""

def allocate_resources(vulnerability_map, total_resources, regions_status=None):
    """
    Distributes resources proportionally based on vulnerability scores,
    but dynamically prioritizes critical baselines for severe situations.
    vulnerability_map: dict of {region_name: vulnerability_score}
    total_resources: dict of {resource_type: total_amount}
    regions_status: list of dicts with raw region metrics
    """
    # Filter out regions with 0 vulnerability to avoid unnecessary allocations
    active_regions = {k: v for k, v in vulnerability_map.items() if v > 0}
    
    if not active_regions:
        return {}, ["No vulnerable regions detected."]

    allocation_plan = {region: {res: 0 for res in total_resources} for region in active_regions}
    explanation_log = []
    remaining_resources: dict[str, int] = {str(k): int(v) for k, v in total_resources.items()}
    
    # 1. Dynamic AI Override: Fulfill Critical Baselines First
    if regions_status:
        for region_data in regions_status:
            region = region_data['name']
            if region in active_regions:
                # Urgent Medical Deficit -> allocate 20% of total medical teams immediately
                if region_data.get('hospital_availability_deficit', 0) > 0.7 and remaining_resources.get('medical_teams', 0) > 0:
                    critical_allocation = int(total_resources['medical_teams'] * 0.2)
                    actual_allocation = min(critical_allocation, remaining_resources['medical_teams'])
                    allocation_plan[region]['medical_teams'] += actual_allocation
                    remaining_resources['medical_teams'] -= actual_allocation
                    explanation_log.append(
                        f"AI Override: Redirected {actual_allocation} medical_teams to {region} immediately due to critical medical access deficit (>0.7), bypassing standard proportional fairness."
                    )
                
                # Urgent Infrastructure Damage -> allocate 30% of rescue boats and evacuation vehicles immediately
                if region_data.get('infra_damage', 0) > 0.8:
                    for urgent_res in ['rescue_boats', 'evacuation_vehicles', 'helicopters']:
                        if remaining_resources.get(urgent_res, 0) > 0:
                            critical_allocation = int(total_resources[urgent_res] * 0.3)
                            actual_allocation = min(critical_allocation, remaining_resources[urgent_res])
                            if actual_allocation > 0:
                                allocation_plan[region][urgent_res] += actual_allocation
                                remaining_resources[urgent_res] -= actual_allocation
                                explanation_log.append(
                                    f"AI Override: Redirected {actual_allocation} {urgent_res} to {region} immediately due to severe infrastructure collapse (>0.8)."
                                )

    # 2. Proportional Allocation logic for remaining resources (Principle 9.1 & 9.4)
    total_vuln_score = sum(active_regions.values())
    
    for region, v_score in active_regions.items():
        if total_vuln_score > 0:
            proportion = v_score / total_vuln_score
            for res_type, amount in remaining_resources.items():
                allocated = int(amount * proportion)
                allocation_plan[region][res_type] += allocated
                
            explanation_log.append(
                f"{region} received standard proportional allocation of remaining resources (vulnerability score {v_score}, {(proportion*100):.1f}% of remainder)."
            )
            
    return allocation_plan, explanation_log

