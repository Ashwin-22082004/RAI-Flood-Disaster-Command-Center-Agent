"""
Dam Management Module

Monitors dam reservoir levels, determining safe storage and release strategies
based on seasonal and climate constraints.
"""

def calculate_safe_release(current_level, forecast_rainfall, safe_capacity, season, downstream_critical=False):
    """
    Calculates the amount of water to release to maintain safe dam levels.
    Incorporates dynamic AI logic to prevent exacerbating downstream disasters.
    """
    # Base calculation formula from Agent.md
    safe_release = current_level + forecast_rainfall - safe_capacity
    
    # Apply seasonal strategies
    if season == "Monsoon":
        # Goal: prevent reservoir overflow
        # Be more aggressive with release if expecting heavy rain
        safe_release *= 1.2 
    elif season == "Summer":
        # Goal: maintain water reserves for drinking/irrigation
        # Reduce release unless absolutely necessary
        safe_release -= (safe_capacity * 0.1) 
    elif season == "Winter":
         # Goal: balanced reservoir storage
         pass

    explanation = f"Standard {season} protocol followed."

    # Dynamic AI Override: Protect downstream lives
    if downstream_critical and safe_release > 0:
        # Reduce release by 50% to mitigate downstream flooding, absorbing more risk in the dam
        reduced_release = safe_release * 0.5
        # Ensure we don't breach absolute critical failure limits (e.g., 105% of safe capacity)
        if (current_level + forecast_rainfall - reduced_release) < (safe_capacity * 1.05):
            safe_release = reduced_release
            explanation = "AI Override: Reduced dam release to protect critically vulnerable downstream regions, accepting manageable increased structural risk."
        else:
            explanation = "AI Override Voided: Dam structural failure imminent. Emergency release mandatory despite downstream vulnerability."

    # Ensure we don't return negative release
    final_release = max(0.0, safe_release)
    
    decision = "Safe Storage"
    alert = None
    
    if final_release > (safe_capacity * 0.3) or (current_level + forecast_rainfall > safe_capacity * 1.02):
        decision = "Emergency Spillway Release"
        alert = {
            "type": "DAM OVERFLOW WARNING",
            "dam": "Idukki Dam",
            "capacity": f"{min(100, int((current_level / safe_capacity) * 100))}%",
            "forecast": "High" if forecast_rainfall > 100 else "Moderate",
            "message": "Controlled water release required immediately to prevent structural failure."
        }
    elif final_release > 0:
        decision = "Controlled Release"
        
    return {
        'suggested_release_volume': float(f"{final_release:.2f}"),
        'decision': decision,
        'strategy_applied': season,
        'reasoning': explanation,
        'alert': alert
    }

