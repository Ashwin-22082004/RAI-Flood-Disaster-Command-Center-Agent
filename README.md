# RAI-Flood-Disaster-Command-Center-Agent

## 🌊 Overview
A **Responsible AI (RAI) Driven Flood Disaster Management Agent** designed to assist authorities by integrating real-time flood monitoring, climate-aware dam management, and ethical resource allocation into a unified decision-support system.

This project implements a multi-agent architecture where specialized agents collaborate to manage flood disasters, from initial detection to humanitarian aid distribution.

## 🚀 Key Features
- **Multi-Agent System**: Coordinating agents for flood monitoring, dam management, resource allocation, and logistics.
- **Climate-Aware Dam Management**: Monitors reservoir levels and predicts safe water release based on seasonal climate conditions.
- **Ethical Resource Allocation**: Uses a vulnerability-based scoring system (Severity, Population Density, Medical Access) to ensure fair aid distribution.
- **Humanitarian Supply Chain Optimization**: Calculates optimal routes and schedules for delivering relief supplies to affected regions.
- **Real-time Command Dashboard**: A professional visualization interface for monitoring disaster severity, dam levels, and rescue progress.

## 🛠️ Technology Stack
- **Backend**: Python 3.x, FastAPI, Uvicorn, Pydantic
- **Frontend**: HTML5, CSS3 (Vanilla), JavaScript (Dynamic Map Visualization)
- **Logic**: Multi-agent orchestration, Optimization algorithms

## 📁 Directory Structure
```text
RAI-Flood-Agent/
├── backend/            # AI decision engines, API services, and controllers
├── frontend/           # Dashboard UI and map visualization components
├── simulation/         # Disaster scenario simulation logic
├── data/               # Population density, climate, and infrastructure data
├── models/             # Trained models for vulnerability and risk assessment
├── docs/               # Detailed documentation and research specifications
└── run_agent.py        # Main system startup script
```

## ⚡ Getting Started

### Prerequisites
- Python 3.10+
- `pip` package manager

### Installation
1. Clone the repository:
   ```bash
   git clone <repository-url>
   ```
2. Install required dependencies:
   ```bash
   pip install fastapi uvicorn pydantic
   ```

### Running the System
The project includes an automated startup script that launches both the backend and frontend servers simultaneously:
```bash
python run_agent.py
```
After running, the system will automatically open the dashboard in your default browser at:
**`http://localhost:3000/index.html`**

## 🛡️ Responsible AI Principles
- **Fairness**: Allocates resources based on vulnerability and severity, not region or socioeconomic status.
- **Transparency**: Every AI decision is accompanied by a reasoning log (e.g., *"Region A prioritized due to high flood severity and limited medical facilities"*).
- **Accountability**: All decisions and simulation outputs are logged for audit and review.
- **Bias Mitigation**: Actively balances resource distribution to prevent systemic neglect of isolated areas.

## 📊 Outputs
- **Flood Risk Heatmaps**: Visualizes affected districts and severity levels.
- **Dam Level Alerts**: Real-time monitoring and automated release recommendations.
- **Rescue Deployment Plans**: Optimal allocation of boats, helicopters, and rescue teams.
- **Logistics Schedules**: Delivery timelines for food, water, and medical supplies.

---
*Empowering disaster management with ethical, data-driven intelligence.*
