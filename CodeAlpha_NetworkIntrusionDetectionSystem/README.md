# CodeAlpha — Network Intrusion Detection System (SentinelGrid)

A defensive alert dashboard for Suricata EVE JSON. It parses alert events, maps severity, filters by severity/text, auto-refreshes the dashboard, tracks incident response status (acknowledged/investigating/contained/false positive), and exports CSV. Suricata is the detection engine; this Flask app visualizes its alerts.

## Run dashboard
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```
Open `http://127.0.0.1:5002` and click **Generate lab demo data** to see sample records. The demo records are simulated and clearly marked; they are not real attacks/detections.

## Connect real Suricata events
1. Install Suricata from the official Suricata documentation for your OS.
2. Configure `eve-log` in `suricata.yaml` to output JSON and enable alert events.
3. Add the included rule from `rules/local.rules` to the configured rules list. Check for duplicate SIDs.
4. Validate config/rules using Suricata's test/config command for your installation, then run Suricata on an authorized lab interface.
5. In the dashboard, enter the absolute path to `eve.json` and save.

Example local rule:
```
alert icmp any any -> any any (msg:"LOCAL LAB ICMP echo request"; itype:8; sid:1000001; rev:1;)
```
Rule syntax and service commands can vary by Suricata version and OS; use the official docs for exact deployment options. The dashboard does not configure firewall rules or automatically block traffic. Its response workflow records an analyst decision; it is not an automated containment engine.

## Safety and limits
- Use only on systems/networks you own or are authorized to monitor.
- Alerts are signals for triage, not proof that an event is malicious.
- The included demo data is synthetic.
- Response/blocking is deliberately not automated: false positives can disrupt legitimate traffic.
