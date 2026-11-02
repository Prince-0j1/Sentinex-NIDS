<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&height=190&color=0:080d1c,50:20205c,100:00b8a9&text=SENTINEX&fontColor=ffffff&fontSize=56&fontAlignY=38&desc=Network%20Intrusion%20Detection%20%26%20Alert%20Triage&descAlignY=60&descSize=14" width="100%" alt="Sentinex banner" />






Detect. Analyze. Defend.
A local dashboard for reviewing Suricata alerts and organizing defensive triage.

Features · Architecture · Setup · Real IDS test · Limitations

</div>

◈ What is Sentinex?

Sentinex reads Suricata EVE JSON alert events and presents them in a local dashboard. It helps a learner inspect alert details, filter events, track analyst workflow status, and export alert records.

Project context: Developed for Task 4 — Network Intrusion Detection System, as part of the CodeAlpha Cyber Security Internship.

Important distinction: Suricata is the detection engine. Sentinex is the alert-review dashboard and log parser; it does not independently inspect live network traffic or block attackers.

✦ Features

Capability

What it does

EVE JSON parsing

Reads line-delimited Suricata events and selects alert events.

Alert triage

Shows signature, category, timestamp, IPs, ports, protocol, and severity.

Severity filters

Filters events into high, medium, and low groups based on Suricata severity values.

Search

Searches the displayed alert data.

Analyst status

Stores a response status for an alert (workflow tracking only).

CSV export

Exports alert records to sentinelgrid_alerts.csv.

Demo data

Generates clearly labelled simulated lab events for UI testing.

Health endpoint

/health reports whether the configured Suricata executable is discoverable and shows the configured EVE path.

🧬 How it works

flowchart TD
    A[Authorized network traffic] --> B[Suricata engine]
    B --> C[Detection rules]
    C --> D[EVE JSON log]
    D --> E[Sentinex parser]
    E --> F[Severity mapping and search]
    F --> G[Local alert dashboard]
    F --> H[CSV export]
    G --> I[Analyst triage status]

Suricata monitors an authorized interface and evaluates traffic against enabled rules.

When a rule matches, Suricata can write an alert event to its EVE JSON log.

Sentinex reads the configured log file and extracts alert fields.

The dashboard maps severity 1 to high, 2 to medium, and other values to low, then provides filtering and export.

🖥️ Getting started

Requirements

Python 3.10 or newer recommended.

Flask (installed from requirements.txt).

For actual detection: Suricata installed and configured separately, an authorized interface, enabled EVE JSON alert output, and an applicable rule set.

Run the dashboard (Windows)

git clone https://github.com/<your-username>/Sentinex-NIDS.git
cd Sentinex-NIDS
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
python app.py

Or run run_windows.bat.

Open http://127.0.0.1:5002.

Linux / macOS

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py

🧪 Test the dashboard with demo events

Open the dashboard at http://127.0.0.1:5002.

Select Generate lab demo data.

Confirm that the simulated events appear and that their lab/demo nature is clearly understood.

Try severity filtering and search.

Change an alert's analyst response status and confirm it is retained.

Export the alert list to CSV and inspect the file.

Demo events validate the dashboard workflow only. They are not real detections and must not be presented as live attacks.

🛰️ Connect real Suricata alerts

Install and configure Suricata by following the official documentation.

Configure Suricata to monitor an interface you are authorized to inspect and enable EVE JSON alert output.

Review rules/local.rules and load the included local ICMP echo-request rule in your lab configuration.

Start Suricata and generate permitted test traffic in your isolated/authorized lab (for example, an ICMP ping if the network allows it).

Confirm that the actual eve.json contains a matching event with event_type: "alert".

Update the eve_path value in config.json to the full path of that log file, or use the dashboard's log-path configuration control.

Refresh Sentinex and confirm the real event appears.

The included rule is a simple lab demonstration rule, not a comprehensive attack-detection policy. Suricata's interface names, configuration paths, and service commands vary by operating system and installation method.

🔌 Useful endpoints

Endpoint

Purpose

/

Alert dashboard

/health

Basic application/configuration health response

/export.csv

Download parsed alert records

📁 Project structure

Sentinex-NIDS/
├── app.py                 # EVE JSON parsing and Flask routes
├── config.json            # EVE log path and Suricata/rule configuration
├── requirements.txt       # Flask dependency
├── rules/
│   └── local.rules        # Example local lab rule
├── data/
│   └── sample_eve.jsonl   # Demo alert data
├── templates/
│   ├── base.html
│   └── index.html
├── run_windows.bat
└── run_linux_mac.sh

⚠️ Scope & limitations

Sentinex does not itself capture or inspect packets; Suricata performs detection.

Demo events are simulated. Only events present in the configured real EVE log are evidence of Suricata output.

A rule match is an alert, not proof that an intrusion succeeded. Alerts can be false positives or false negatives.

The response-status feature records analyst workflow state. It does not block an IP, terminate a connection, or change firewall rules.

The severity grouping is a simplified display mapping of Suricata's numeric severity field.

Use only on networks and systems you own or have explicit permission to monitor.

🧑‍💻 Built for learning

Topics explored: network IDS concepts, Suricata rules, EVE JSON, alert triage, severity classification, log parsing, and defensive monitoring workflows.

<div align="center">

SENTINEX · Visibility is the first step in defense.

<sub>CodeAlpha Cyber Security Internship · Network Intrusion Detection System</sub>

</div>
