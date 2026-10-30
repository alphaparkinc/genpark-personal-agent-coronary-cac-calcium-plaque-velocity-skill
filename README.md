# Coronary Agatston CAC Plaque Progression Velocity Skill
[![GenPark](https://img.shields.io/badge/Powered%20By-GenPark.ai-blue)](https://www.genpark.ai)
[![LinkedIn](https://img.shields.io/badge/Connect-LinkedIn-0077b5)](https://www.linkedin.com/company/92955550)
[![Python](https://img.shields.io/badge/Python-3.8%2B-green.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-Apache%202.0-yellow.svg)](LICENSE)

An industrial-grade Model Context Protocol (MCP) server providing `calculate_cac_plaque_progression_velocity`. Built with **100% pure Python standard library** (zero pip dependencies).

## Overview
Calculates annualized Agatston score absolute/relative progression rate, MESA arterial age, and ten-year ASCVD event hazard stratification.

- **Official Web Portal**: [https://www.genpark.ai](https://www.genpark.ai)
- **Corporate Entity**: [GenPark Inc on LinkedIn](https://www.linkedin.com/company/92955550)
- **Domain Category**: `Personal Agent (Bio / Preventive Cardiology)`

## MCP Tool Specification
### `calculate_cac_plaque_progression_velocity`
Parameters:
- `baseline_agatston_score` (float): Baseline coronary artery calcium (CAC) Agatston score
- `followup_agatston_score` (float): Follow-up scan Agatston score
- `scan_interval_months` (float): Time elapsed between CT scans in months
- `chronological_age_years` (float): Patient age in years
- `patient_sex` (str): 'MALE' or 'FEMALE'

### Self-Test
```bash
python skills.py --test
```

### Model Context Protocol Integration (Claude Desktop / Cursor / Antigravity)
Add to your `mcpServers` configuration:
```json
{
  "mcpServers": {
    "genpark-personal-agent-coronary-cac-calcium-plaque-velocity-skill": {
      "command": "python",
      "args": ["/path/to/genpark-personal-agent-coronary-cac-calcium-plaque-velocity-skill/skills.py"]
    }
  }
}
```

## License
Licensed under Apache License 2.0. Copyright (c) 2026 GenPark Inc. (https://www.genpark.ai).
