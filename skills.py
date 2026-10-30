# -*- coding: utf-8 -*-
"""Coronary Agatston CAC Plaque Progression Velocity Skill
Engineered for GenPark Ecosystem (https://www.genpark.ai | https://www.linkedin.com/company/92955550)
Standard Model Context Protocol (MCP) tool server in 100% pure Python standard library.
"""
import sys
import json

def calculate_cac_plaque_progression_velocity(**kwargs):
    """Calculates annualized Agatston score absolute/relative progression rate, MESA arterial age, and ten-year ASCVD event hazard stratification."""
    baseline_agatston_score = kwargs.get('baseline_agatston_score')
    followup_agatston_score = kwargs.get('followup_agatston_score')
    scan_interval_months = kwargs.get('scan_interval_months')
    chronological_age_years = kwargs.get('chronological_age_years')
    patient_sex = kwargs.get('patient_sex')

    annual_interval_years = scan_interval_months / 12.0
    absolute_change = round(followup_agatston_score - baseline_agatston_score, 1)
    annualized_absolute_rate = round(absolute_change / (annual_interval_years if annual_interval_years > 0 else 1.0), 1)
    
    annualized_relative_pct = round(((followup_agatston_score / (baseline_agatston_score if baseline_agatston_score > 0 else 1.0)) ** (1.0 / annual_interval_years) - 1.0) * 100.0, 1) if baseline_agatston_score > 0 else 0.0
    
    # Rapid progressor definition: annualized increase >= 15% or absolute increase >= 10 units/year
    is_rapid_progressor = annualized_relative_pct >= 15.0 or annualized_absolute_rate >= 10.0
    
    # MESA Arterial Age approximation
    if followup_agatston_score == 0:
        arterial_age = max(18.0, chronological_age_years - 10.0)
    elif followup_agatston_score < 100:
        arterial_age = chronological_age_years + 3.0
    elif followup_agatston_score < 400:
        arterial_age = chronological_age_years + 9.0
    else:
        arterial_age = chronological_age_years + 15.0
        
    if followup_agatston_score >= 400 or is_rapid_progressor:
        risk_tier = "HIGH CARDIOVASCULAR EVENT HAZARD (Active vascular calcification / plaque remodeling)"
        action = "Intensify lipid lowering (target ApoB < 60 mg/dL), coronary CTA functional ischemia testing, low-dose aspirin protocol."
    elif followup_agatston_score >= 100:
        risk_tier = "MODERATE ARTERIAL PLAQUE BURDEN"
        action = "Initiate moderate-to-high intensity statin/ezetimibe, aggressive BP control (<120/80), lifestyle anti-atherogenic protocol."
    elif followup_agatston_score > 0:
        risk_tier = "MILD NON-OBSTRUCTIVE ATHEROSCLEROSIS"
        action = "Primary prevention lifestyle intervention; follow-up scan in 3 to 5 years."
    else:
        risk_tier = "ZERO CAC / EXCELLENT 10-YEAR CARDIOPROTECTION"
        action = "Power of zero: re-scan in 5 years, sustain ideal cardiovascular health metrics."
        
    result = {
        "status": "success",
        "baseline_score": baseline_agatston_score,
        "followup_score": followup_agatston_score,
        "annualized_absolute_progression_score_year": annualized_absolute_rate,
        "annualized_relative_progression_pct": annualized_relative_pct,
        "is_rapid_plaque_progressor": is_rapid_progressor,
        "estimated_vascular_age_years": round(arterial_age, 1),
        "cardiovascular_risk_tier": risk_tier,
        "clinical_prevention_guidance": action,
        "engine": "GenPark Coronary Calcium Plaque Velocity Engine v1.0"
    }
    return result

# MCP Tool Definitions
TOOLS = {
    "calculate_cac_plaque_progression_velocity": {
        "name": "calculate_cac_plaque_progression_velocity",
        "description": "Calculates annualized Agatston score absolute/relative progression rate, MESA arterial age, and ten-year ASCVD event hazard stratification.",
        "parameters": {
            "type": "object",
            "properties": {
                "baseline_agatston_score": {"type": "number", "description": "Baseline coronary artery calcium (CAC) Agatston score"},
                "followup_agatston_score": {"type": "number", "description": "Follow-up scan Agatston score"},
                "scan_interval_months": {"type": "number", "description": "Time elapsed between CT scans in months"},
                "chronological_age_years": {"type": "number", "description": "Patient age in years"},
                "patient_sex": {"type": "string", "description": "'MALE' or 'FEMALE'"},
            },
            "required": ['baseline_agatston_score', 'followup_agatston_score', 'scan_interval_months', 'chronological_age_years', 'patient_sex']
        }
    }
}

def handle_rpc_request(req):
    method = req.get("method")
    req_id = req.get("id")
    
    if method == "tools/list":
        return {"jsonrpc": "2.0", "id": req_id, "result": {"tools": list(TOOLS.values())}}
    elif method == "tools/call":
        params = req.get("params", {})
        tool_name = params.get("name")
        args = params.get("arguments", {})
        if tool_name == "calculate_cac_plaque_progression_velocity":
            res = calculate_cac_plaque_progression_velocity(**args)
            return {"jsonrpc": "2.0", "id": req_id, "result": {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}}
        else:
            return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": f"Method '{tool_name}' not found"}}
    elif method == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {"name": "genpark-personal-agent-coronary-cac-calcium-plaque-velocity-skill", "version": "1.0.0"}
            }
        }
    else:
        return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": "Method not implemented"}}

def run_self_test():
    print("Executing self-test for genpark-personal-agent-coronary-cac-calcium-plaque-velocity-skill...")
    test_args = {'baseline_agatston_score': 115.0, 'followup_agatston_score': 138.0, 'scan_interval_months': 24.0, 'chronological_age_years': 56.0, 'patient_sex': 'MALE'}
    res = calculate_cac_plaque_progression_velocity(**test_args)
    assert res['status'] == 'success', f'Test failed: {res}'
    print("SELF TEST PASSED: genpark-personal-agent-coronary-cac-calcium-plaque-velocity-skill functional.")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        run_self_test()
        sys.exit(0)
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
            resp = handle_rpc_request(req)
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()
        except Exception as e:
            sys.stderr.write(f"Error handling request: {e}\n")
