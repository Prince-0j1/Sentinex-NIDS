from flask import Flask, render_template, request, redirect, url_for, flash, send_file
from pathlib import Path
from datetime import datetime, timezone
import json, os, csv, io, subprocess, shutil, hashlib
app=Flask(__name__); app.secret_key=os.environ.get('FLASK_SECRET','local-nids-change-me')
ROOT=Path(__file__).resolve().parent; CONFIG=ROOT/'config.json'; SAMPLE=ROOT/'data'/'sample_eve.jsonl'; RESPONSES=ROOT/'data'/'responses.json'
ALLOWED_RESPONSE_STATUS={'New','Acknowledged','Investigating','Contained','False positive'}
def load_responses():
    try: return json.loads(RESPONSES.read_text(encoding='utf-8'))
    except (OSError, json.JSONDecodeError): return {}
def event_key(row):
    raw='|'.join(str(row.get(k,'')) for k in ('timestamp','src','dst','signature','flow_id'))
    return hashlib.sha256(raw.encode('utf-8')).hexdigest()
def config():
    try: return json.loads(CONFIG.read_text(encoding='utf-8'))
    except Exception: return {'eve_path':str(SAMPLE),'suricata_path':'suricata','rule_path':str(ROOT/'rules'/'local.rules')}
def parse_events(path):
    p=Path(path); rows=[]; error=''
    if not p.exists(): return [], f'Log file not found: {p}. Configure the eve.json path in config.json.'
    try:
        with p.open('r',encoding='utf-8',errors='replace') as f:
            for line in f:
                if not line.strip(): continue
                try: e=json.loads(line)
                except json.JSONDecodeError: continue
                if e.get('event_type')!='alert' and not e.get('alert'): continue
                a=e.get('alert') or {}; sev=int(a.get('severity',3) or 3)
                level='high' if sev==1 else ('medium' if sev==2 else 'low')
                rows.append({'timestamp':e.get('timestamp','unknown'),'src':e.get('src_ip','—'),'dst':e.get('dest_ip','—'),'sport':e.get('src_port','—'),'dport':e.get('dest_port','—'),'proto':e.get('proto','—'),'signature':a.get('signature','Unlabelled alert'),'category':a.get('category','uncategorized'),'severity':sev,'level':level,'action':a.get('action','alert'),'flow_id':e.get('flow_id','—')})
    except OSError as ex: error=str(ex)
    rows.sort(key=lambda x:x['timestamp'],reverse=True)
    return rows,error
def write_sample():
    SAMPLE.parent.mkdir(parents=True,exist_ok=True)
    now=datetime.now(timezone.utc).isoformat(timespec='milliseconds').replace('+00:00','Z')
    demo=[{'event_type':'alert','timestamp':now,'src_ip':'192.168.56.20','dest_ip':'192.168.56.10','src_port':52144,'dest_port':22,'proto':'TCP','flow_id':10001,'alert':{'signature':'LAB DEMO: repeated SSH connection attempts','category':'Attempted Information Leak','severity':2,'action':'allowed'}},{'event_type':'alert','timestamp':now,'src_ip':'192.168.56.30','dest_ip':'192.168.56.10','src_port':54321,'dest_port':80,'proto':'TCP','flow_id':10002,'alert':{'signature':'LAB DEMO: suspicious HTTP test pattern','category':'Web Application Attack','severity':1,'action':'allowed'}},{'event_type':'alert','timestamp':now,'src_ip':'192.168.56.40','dest_ip':'192.168.56.10','src_port':5353,'dest_port':53,'proto':'UDP','flow_id':10003,'alert':{'signature':'LAB DEMO: unusual DNS request','category':'Potentially Bad Traffic','severity':3,'action':'allowed'}}]
    SAMPLE.write_text(''.join(json.dumps(x)+'\n' for x in demo),encoding='utf-8')
@app.route('/')
def index():
    cfg=config(); path=request.args.get('path') or cfg.get('eve_path',str(SAMPLE)); rows,error=parse_events(path)
    responses=load_responses()
    for row in rows:
        row['event_key']=event_key(row); row['response']=responses.get(row['event_key'],'New')
    severity=request.args.get('severity','all'); search=request.args.get('q','').strip().lower()
    shown=[x for x in rows if (severity=='all' or x['level']==severity) and (not search or search in json.dumps(x).lower())]
    return render_template('index.html',title='SentinelGrid NIDS',subtitle='Suricata alert intelligence • defensive monitoring • local lab',logo='⌬',rows=shown,total=len(rows),high=sum(x['level']=='high' for x in rows),medium=sum(x['level']=='medium' for x in rows),low=sum(x['level']=='low' for x in rows),error=error,path=path,filter=severity,q=request.args.get('q',''),cfg=cfg,sample=str(SAMPLE),suricata=shutil.which(cfg.get('suricata_path','suricata')))
@app.post('/demo')
def demo():
    write_sample(); flash('Demo alert data written. These are clearly labelled simulated lab events, not real detections.'); return redirect(url_for('index',path=str(SAMPLE)))
@app.post('/respond')
def respond():
    key=request.form.get('event_key',''); status=request.form.get('status','')
    if len(key)!=64 or status not in ALLOWED_RESPONSE_STATUS:
        flash('Invalid incident response update.','error'); return redirect(url_for('index'))
    responses=load_responses(); responses[key]={'status':status,'updated_at':datetime.now(timezone.utc).isoformat(timespec='seconds')}
    RESPONSES.parent.mkdir(parents=True,exist_ok=True); RESPONSES.write_text(json.dumps(responses,indent=2),encoding='utf-8')
    flash('Incident response status updated to: '+status); return redirect(url_for('index'))
@app.post('/configure')
def configure():
    cfg=config(); cfg['eve_path']=request.form.get('eve_path','').strip() or str(SAMPLE); CONFIG.write_text(json.dumps(cfg,indent=2),encoding='utf-8'); flash('EVE JSON log path saved.'); return redirect(url_for('index'))
@app.get('/export.csv')
def export():
    cfg=config(); rows,_=parse_events(request.args.get('path') or cfg.get('eve_path',str(SAMPLE))); out=io.StringIO(); fields=['timestamp','src','dst','sport','dport','proto','signature','category','severity','level','action','flow_id']; w=csv.DictWriter(out,fieldnames=fields); w.writeheader(); w.writerows(rows)
    from flask import Response
    return Response(out.getvalue(),mimetype='text/csv',headers={'Content-Disposition':'attachment; filename=sentinelgrid_alerts.csv'})
@app.get('/health')
def health(): return {'ok':True,'suricata_found':bool(shutil.which(config().get('suricata_path','suricata'))),'eve_path':config().get('eve_path')}
if __name__=='__main__': app.run(host='127.0.0.1',port=5002,debug=False,threaded=True)
