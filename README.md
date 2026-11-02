<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&amp;height=190&amp;color=0:080d1c,50:20205c,100:00b8a9&amp;text=SENTINEX&amp;fontColor=ffffff&amp;fontSize=56&amp;fontAlignY=38&amp;desc=Network%20Intrusion%20Detection%20%26%20Alert%20Triage&amp;descAlignY=60&amp;descSize=14" width="100%" alt="SENTINEX — Network Intrusion Detection and Alert Triage" />






DETECT · ANALYZE · DEFEND

A local dashboard for reviewing Suricata alerts, exploring network events, and organizing defensive triage.

Overview · Features · Architecture · Installation · Testing · Limitations

</div>

◈ Overview

SENTINEX is a Network Intrusion Detection System (NIDS) support dashboard built with Python and Flask. It reads alert events from Suricata's EVE JSON log and presents useful information in a single interface.

Use it to inspect alert signatures, source and destination addresses, protocols, timestamps, severity, and analyst workflow status. You can also search, filter, and export alert records.

Internship task: CodeAlpha Cyber Security — Task 4: Network Intrusion Detection System.

Architecture note: Suricata is the network detection engine. SENTINEX parses and displays Suricata's alert output. SENTINEX itself does not capture packets, independently detect attacks, or block traffic.

✦ Features

Feature

Description

Suricata EVE JSON

Reads structured Suricata events and extracts alert records.

Alert overview

Displays signature, timestamp, IP addresses, ports, protocol, and severity when available.

Severity filtering

Groups alerts using the severity value supplied by Suricata.

Search

Helps locate alerts in the dashboard.

Analyst workflow

Tracks an alert's review status; this is record-keeping, not automated containment.

CSV export

Exports alert records for further analysis.

Demo data

Provides clearly labelled simulated records to test the dashboard interface.

Health check

Provides a basic application health/configuration endpoint.

🧬 Architecture

flowchart TD
    A[Authorized network traffic] --> B[Suricata detection engine]
    B --> C[Enabled detection rules]
    C --> D[EVE JSON log]
    D --> E[SENTINEX log parser]
    E --> F[Alert fields and severity]
    F --> G[Search and filtering]
    G --> H[Local web dashboard]
    G --> I[CSV export]
    H --> J[Analyst triage status]
    style B fill:#172554,stroke:#38bdf8,color:#fff
    style E fill:#134e4a,stroke:#2dd4bf,color:#fff
    style H fill:#312e81,stroke:#a5b4fc,color:#fff

Event flow

Suricata monitors a network interface that you are authorized to inspect.

Suricata evaluates observed traffic against its enabled rules.

When a rule matches, Suricata can write an alert event to its EVE JSON log.

SENTINEX reads the configured log and extracts available alert fields.

The dashboard presents events for search, filtering, review, and export.

🧰 Technology stack

Technology

Role

Python

Application logic and log parsing

Flask

Local web application and routes

Suricata

Network traffic inspection and rule-based detection

EVE JSON

Structured event/log format

HTML, CSS, JavaScript

Dashboard interface and interactions

CSV

Portable alert export

⚡ Installation

Requirements

Python 3.10 or newer recommended.

The Python packages listed in requirements.txt.

For real IDS alerts: Suricata installed and configured separately.

An interface and network you own or have explicit permission to monitor.

Windows

git clone https://github.com/<your-username>/Sentinex-NIDS.git
cd Sentinex-NIDS
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
python app.py

Alternatively, run the included run_windows.bat.

Open http://127.0.0.1:5002 in your browser.

Linux / macOS

git clone https://github.com/<your-username>/Sentinex-NIDS.git
cd Sentinex-NIDS
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python app.py

Then open http://127.0.0.1:5002.

🧪 Testing

1. Test the dashboard with demo events

Start SENTINEX and open http://127.0.0.1:5002.

Use Generate lab demo data in the dashboard.

Confirm that sample alert rows appear.

Try the severity filters and search.

Change an alert's analyst status, if the control is available.

Export the displayed records to CSV and open the file.

Expected result: The dashboard displays sample records and its filtering/export workflow functions as expected.

Be transparent: Demo events are simulated UI test data. They are not proof that Suricata detected real malicious traffic.

2. Test with real Suricata output

Install Suricata using the official Suricata documentation.

Configure it to monitor an authorized interface.

Enable EVE JSON output and ensure alert events are included.

Review rules/local.rules and load the included local ICMP echo-request rule in your lab configuration.

Start Suricata and generate permitted test traffic in your own lab. For example, use an ICMP ping if your network permits it.

Check the actual eve.json file for an event whose event_type is alert.

Set SENTINEX's EVE log path to that file using the dashboard's log-path setting or the relevant configuration in config.json.

Refresh the dashboard and verify that the real event appears.

The included ICMP rule is a simple lab test rule, not a complete intrusion-detection policy. Suricata configuration paths and service commands vary by operating system and installation.

🔎 Application endpoints

Endpoint

Purpose

/

Main alert dashboard

/health

Basic application/configuration health information

/export.csv

CSV export of parsed alert records

🗂️ Project structure

Sentinex-NIDS/
├── app.py
├── config.json
├── requirements.txt
├── rules/
│   └── local.rules
├── data/
│   └── sample_eve.jsonl
├── templates/
│   ├── base.html
│   └── index.html
├── run_windows.bat
└── run_linux_mac.sh

⚠️ Scope and limitations

Suricata performs the actual network inspection and rule matching; SENTINEX displays the resulting alert records.

A rule match is an alert, not proof that an intrusion succeeded.

Detection depends on configured rules, interface visibility, and Suricata configuration. False positives and false negatives are possible.

Demo records are simulated and must not be described as real attack detections.

Analyst status tracking does not block IP addresses, terminate connections, or modify firewall rules.

Severity labels are a simplified presentation of the severity values in the log.

Do not use the tool to monitor networks or devices without authorization.

📚 Learning outcomes

Working on SENTINEX introduces practical concepts in network intrusion detection, Suricata rules, EVE JSON log analysis, IP/port/protocol context, alert triage, severity review, Python log processing, and Flask dashboards.

<div align="center">

SENTINEX

Visibility is the first step in defense.

<sub>Built as a learning project for the CodeAlpha Cyber Security Internship.</sub>

</div>
