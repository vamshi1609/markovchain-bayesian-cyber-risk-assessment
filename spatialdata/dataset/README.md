# Proactive and Time-Sensitive Cyber Risk Assessment Model
## Integrating Markov Chains and Bayesian Networks

This directory contains datasets for a comprehensive cyber risk assessment framework for critical infrastructure protection.

---

## Dataset Overview

### 1. **vuln_assets.csv**
Maps critical infrastructure assets to known vulnerabilities with EPSS exploit probabilities.

| Column | Type | Example | Purpose |
|--------|------|---------|---------|
| `asset` | string | Financial_Transaction_Server | System/component name |
| `cve` | string | CVE-2021-44228 | Known CVE identifier |
| `epss_score` | float | 0.92 | Exploit probability (0–1) for **Module 1: EPSS Likelihood** |
| `criticality` | float | 9.8 | Asset importance (1–10) for **Module 5: Impact Assessment** |
| `location` | string | New York | Deployment region |
| `network_criticality` | string | Critical | Network tier (Low/Medium/High/Critical) |
| `business_impact` | string | Severe - Financial transactions halted | Business consequence if compromised |

---

### 2. **asset_dependencies.csv**
Defines interdependencies between systems for Bayesian network topology and attack path modeling.

| Column | Type | Example | Purpose |
|--------|------|---------|---------|
| `source` | string | Database_Cluster | Upstream asset |
| `target` | string | Financial_Transaction_Server | Downstream asset |
| `weight` | float | 0.98 | Dependency strength (0–1) for **Module 2: Bayesian Networks** |
| `attack_difficulty` | string | Very Hard | Relative attack complexity for **Module 3: DFS Attack Paths** |
| `attack_path_risk` | string | Critical | Risk level of this dependency chain |

---

### 3. **vulnerability_timeline.csv**
Tracks vulnerability lifecycle from discovery to patch availability (enables time-sensitive assessment).

**Supports:** Module 1 (EPSS + time urgency), Module 6 (Time-to-Compromise)

| Column | Purpose |
|--------|---------|
| `vulnerability_id` | Unique identifier |
| `cve` | CVE identifier |
| `asset` | Affected asset name |
| `epss_score` | Current EPSS probability (0–1) |
| `discovery_date` | When vulnerability was found |
| `public_disclosure_date` | When vendors disclosed it |
| `exploit_available_date` | When public exploit appeared |
| `patch_available_date` | When fix became available |
| `days_to_exploit` | **Urgency metric** – gap between disclosure and exploit |
| `exploitability_trend` | Rising/Stable/Falling – future attack intensity forecast |

---

### 4. **asset_health_metrics.csv**
Real-time health snapshots of each critical asset (system uptime, patch status, risk scoring).

**Supports:** Module 5 (Impact) via business impact, Module 4 (Risk distribution)

| Column | Purpose |
|--------|---------|
| `asset_id` | Unique asset identifier |
| `asset_name` | System name |
| `assessment_date` | When assessment was performed |
| `uptime_percent` | System availability (0–100%) |
| `patch_level` | Percentage of patches applied (0–100%) |
| `vulnerabilities_unpatched` | Count of open security issues |
| `response_time_sec` | System response latency (seconds) |
| `network_criticality` | Tier: Low/Medium/High/Critical |
| `data_sensitivity` | Data classification: Low/Medium/High/Critical |
| `business_impact` | Consequence of system failure |
| `current_risk_score` | Aggregated risk (1–10) |
| `trend` | Increasing/Stable/Decreasing |

---

### 5. **threat_intelligence.csv**
Real-world threat actor profiles and active campaigns (feeds attack path sources & probability).

**Supports:** Module 3 (Attack path entry points), Module 4 (Markov attack probability)

| Column | Purpose |
|--------|---------|
| `threat_actor_id` | Unique threat actor identifier |
| `threat_actor_name` | Group/campaign name |
| `attack_vector` | Network Intrusion, Phishing, Supply Chain, etc. |
| `target_asset` | Primary target system |
| `attack_frequency_per_week` | **Urgency metric** – how often they attack |
| `success_rate_percent` | Historical probability of compromise (0–100%) |
| `avg_time_to_compromise_hours` | **Module 6 metric** – speed of attack progression |
| `capability_level` | Low/Medium/High/Critical |
| `intent` | Financial Gain, Espionage, Disruption, etc. |
| `last_observed_date` | Most recent activity date |
| `threat_level` | Medium/High/Critical |

---

### 6. **incident_response_log.csv**
Historical incident timelines showing organizational detection & response capability (SLA metrics).

**Supports:** Module 6 (Time-to-Compromise), improving detection/response times

| Column | Purpose |
|--------|---------|
| `incident_id` | Unique incident identifier |
| `incident_date` | When incident occurred |
| `affected_asset` | System compromised |
| `cve_exploited` | CVE used in attack |
| `threat_actor` | Who conducted the attack |
| `detection_time_minutes` | **SLA metric** – how long before we noticed |
| `analysis_time_minutes` | **SLA metric** – how long to understand it |
| `response_time_minutes` | **SLA metric** – how long to start remediation |
| `remediation_time_hours` | **SLA metric** – how long to fix it |
| `severity_level` | Low/Medium/High/Critical |
| `response_effectiveness_percent` | Success rate of response (0–100%) |
| `lessons_learned` | Recommendations for improvement |

---

### 7. **patch_management.csv**
Patch deployment success rates, downtime windows, and risk reduction metrics.

**Supports:** Module 5 (Impact of delays), Module 6 (Timeline forecasting)

| Column | Purpose |
|--------|---------|
| `patch_id` | Unique patch identifier |
| `asset` | System receiving patch |
| `cve` | CVE being patched |
| `version_before` | Pre-patch software version |
| `version_after` | Post-patch software version |
| `patch_release_date` | When vendor released patch |
| `testing_start_date` | Lab testing began |
| `testing_end_date` | Testing completed |
| `deployment_date` | Production deployment date |
| `deployment_success` | Yes/No |
| `deployment_rollback` | Did we have to revert? |
| `downtime_minutes` | Business impact window |
| `risk_reduction_percent` | How much risk removed (0–100%) |

---

### 8. **daily_risk_scores.csv**
Rolling time-series of daily risk assessments per asset (enables predictive alerts & trending).

**Supports:** All modules – real-time/trending risk data, **time-sensitive decision making**

| Column | Purpose |
|--------|---------|
| `assessment_date` | Date of assessment |
| `asset_name` | System being assessed |
| `daily_risk_score` | Aggregated risk on that day (0–10) |
| `exploit_detections` | Count of exploit attempts detected |
| `active_threats` | Number of active threat actors targeting this asset |
| `patches_applied` | Patches deployed today |
| `incidents_this_week` | Count of incidents affecting this asset |
| `weather_related_alerts` | Environmental risk factors |
| `system_health_percent` | Overall system health (0–100%) |
| `predicted_risk_tomorrow` | **Proactive forecast** – next-day risk estimate |
| `recommended_action` | Auto-generated response advisory |

---

## Module Alignment & Workflow

| Module | Input Datasets | Purpose |
|--------|---|---------|
| 1. **EPSS Likelihood** | `vuln_assets.csv`, `vulnerability_timeline.csv` | Calculate 30-day exploit probability |
| 2. **Asset Dependency (Bayesian)** | `asset_dependencies.csv` | Model infrastructure topology & cascading failures |
| 3. **Attack Paths (DFS)** | `asset_dependencies.csv`, `threat_intelligence.csv` | Find all routes from attacker entry to critical assets |
| 4. **Probabilistic Risk (Markov)** | All datasets combined | Calculate absorption probabilities into high-risk states |
| 5. **Impact Assessment** | `asset_health_metrics.csv`, `patch_management.csv`, `vuln_assets.csv` | Combine risk × criticality for business impact |
| 6. **Attack Progression** | `vulnerability_timeline.csv`, `incident_response_log.csv`, `threat_intelligence.csv` | Estimate hours before critical compromise |
| 7. **Decision Support** | `daily_risk_scores.csv` | Real-time dashboards with predictions & recommendations |

---

## Loading the Datasets

### Option 1: Management Command (Recommended)
```bash
python manage.py load_risk
```
Automatically loads `vuln_assets.csv` and `asset_dependencies.csv` into Django models.

### Option 2: Admin Upload Page
Navigate to: **http://127.0.0.1:8000/admin-upload/**
1. Select "Vulnerability Assets" from dropdown
2. Upload `vuln_assets.csv`
3. Repeat for "Asset Dependencies" with `asset_dependencies.csv`

### Option 3: Direct Database Query
```python
from risk.models import Asset, Vulnerability
# Verify data was loaded
print(Asset.objects.count(), Vulnerability.objects.count())
```

---

## Accessing the Risk Dashboard

Once datasets are loaded, visit: **http://127.0.0.1:8000/risk/dashboard/**

The dashboard displays all 7 risk modules:
✅ EPSS Likelihood  
✅ Bayesian Asset Network (topology)  
✅ DFS Attack Paths (entry→target)  
✅ Markov Chain (probabilistic distribution)  
✅ Impact Assessment (business risk)  
✅ Time-to-Compromise (hours to breach)  
✅ Decision Support (alerts & recommendations)  

---

## Customizing for Your Infrastructure

### Replace with Real Data
1. **Export asset inventory** from your CMDB → `vuln_assets.csv`
2. **Document dependencies** (which systems feed which) → `asset_dependencies.csv`
3. **Feed threat intel** (from OSINT, threat feeds) → `threat_intelligence.csv`
4. **Log incidents** (from SIEM/ticketing) → `incident_response_log.csv`
5. **Track patches** (from patch management tool) → `patch_management.csv`
6. **Collect metrics** (from monitoring/health checks) → `asset_health_metrics.csv`

### Fetch Real EPSS Scores
Replace static scores in `vuln_assets.csv` with live data:
- API: `https://api.first.org/data/v1/epss?filter=cve:CVE-XXXX-XXXXX`
- [FIRST EPSS Documentation](https://www.first.org/epss/)

---

## Key Insights: Proactive & Time-Sensitive Assessment

This framework enables:

- **🔮 Proactive** – Predicts tomorrow's attacks via threat trends + EPSS urgency + threat intel
- **⏱️ Time-Sensitive** – Tracks hours-to-compromise, patch windows, incident response SLAs
- **📊 Decision-Ready** – Combines all factors into ranked action items with business impact
- **📈 Data-Driven** – Historical incident data + attack patterns → better forecasts
- **🎯 Bayesian Networks** – Models asset interdependencies to identify critical attack chains
- **🔗 Markov Chains** – Calculates exploitation probability distributions across attack paths

---

## Example Scenario

**Day 1 (Feb 24):**
- Financial_Transaction_Server shows EPSS 0.92 for CVE-2021-44228
- Asset network identifies 5 attack paths from Internet → Financial_Transaction_Server
- Markov chain calculates 15% absorption probability (exploitation likelihood)
- Risk score: 8.7/10; Recommendation: "Increase monitoring - APT activity detected"

**Day 2 (Feb 25):**
- Three exploit attempts detected yesterday
- Threat actors increased attack frequency from 3→4 per week
- Predicted risk tomorrow: 8.9/10
- New recommendation: "Critical - Isolate if possible"

**Action Taken:**
- Admin applies emergency security patch (98% risk reduction)
- Activates incident response procedures
- Daily risk score drops to 6.2/10 by next assessment

---

## Requirements
- Django 4.1+
- pandas, numpy, networkx
- MySQL 8.0 (or PostgreSQL)
- Risk app models (Asset, Vulnerability, AssetDependency)

