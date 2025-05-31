import asyncio
import asyncpg
import yaml
import logging
import smtplib
import requests
from jinja2 import Template
from datetime import datetime
import os
import backoff

# -------------------------
# Configuration & Settings
# -------------------------
# Load configuration from environment variables (.env) if present
DB_CONFIG = {
    'user': os.getenv('DB_USER', 'finance_user'),
    'password': os.getenv('DB_PASS', 'finance_pass'),
    'database': os.getenv('DB_NAME', 'finance_db'),
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': int(os.getenv('DB_PORT', 5432)),
    'ssl': {'require_ssl': os.getenv('DB_SSL', 'False').lower() in ('true','1')}
}
RULES_FILE = os.getenv('RULES_FILE', 'rules.yaml')
LISTEN_CHANNEL = os.getenv('LISTEN_CHANNEL', 'db_events')

# Setup logging\logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

# -------------------------
# Rule Model & Loader
# -------------------------
class Rule:
    def __init__(self, id, name, condition, action, enabled=True):
        self.id = id
        self.name = name
        self.condition = condition
        self.action = action
        self.enabled = enabled

def load_rules(path):
    if not os.path.exists(path):
        logging.error(f"Rules file not found: {path}")
        return []
    with open(path) as f:
        data = yaml.safe_load(f)
    rules = []
    for entry in data.get('rules', []):
        rules.append(Rule(
            id=entry['id'],
            name=entry['name'],
            condition=entry['condition'],
            action=entry['action'],
            enabled=entry.get('enabled', True)
        ))
    logging.info(f"Loaded {len(rules)} rules from {path}")
    return rules

# -------------------------
# Action Handlers
# -------------------------
def send_email(params, context):
    try:
        smtp = smtplib.SMTP(params['smtp_server'], params.get('port', 25))
        msg = Template(params['message']).render(**context)
        smtp.sendmail(params['from'], params['to'], msg)
        smtp.quit()
        logging.info(f"Email sent to {params['to']}")
    except Exception as e:
        logging.error(f"Failed to send email: {e}")

async def call_api(params, context):
    try:
        url = params['url']
        payload = yaml.safe_load(Template(yaml.safe_dump(params.get('payload', {}))).render(**context))
        resp = requests.post(url, json=payload, timeout=5)
        logging.info(f"API {url} responded {resp.status_code}")
    except Exception as e:
        logging.error(f"API call failed: {e}")

def log_to_table(conn, params, context):
    try:
        cols = ','.join(params['fields'].keys())
        vals = [Template(v).render(**context) for v in params['fields'].values()]
        placeholders = ','.join(f'${i+1}' for i in range(len(vals)))
        sql = f"INSERT INTO {params['table']} ({cols}) VALUES ({placeholders})"
        return conn.execute(sql, *vals)
    except Exception as e:
        logging.error(f"Failed to log to table: {e}")

# -------------------------
# Rule Evaluation
# -------------------------
async def evaluate_rules(conn, rules, event):
    ctx = {**event, 'event_time': datetime.utcnow().isoformat()}
    for rule in rules:
        if not rule.enabled:
            continue
        try:
            if eval(rule.condition, {}, ctx):
                logging.info(f"Trigger: {rule.name}")
                act = rule.action
                if act['type'] == 'email':
                    send_email(act, ctx)
                elif act['type'] == 'api':
                    await call_api(act, ctx)
                elif act['type'] == 'log':
                    await log_to_table(conn, act, ctx)
        except Exception as e:
            logging.error(f"Rule {rule.name} error: {e}")

# -------------------------
# DB Listener with Backoff
# -------------------------
@backoff.on_exception(backoff.expo, Exception, max_time=60)
async def init_conn():
    return await asyncpg.connect(**DB_CONFIG)

async def listen():
    conn = await init_conn()
    await conn.add_listener(LISTEN_CHANNEL, lambda *args: None)
    logging.info(f"Listening on {LISTEN_CHANNEL}")
    rules = load_rules(RULES_FILE)
    while True:
        msg = await conn.connection.notifies.get()
        event = yaml.safe_load(msg.payload)
        await evaluate_rules(conn, rules, event)

# -------------------------
# Main Entrypoint
# -------------------------
async def main():
    try:
        await listen()
    except asyncio.CancelledError:
        logging.info("Shutting down")

if __name__ == '__main__':
    asyncio.run(main())