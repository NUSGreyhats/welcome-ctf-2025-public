import os
import socket
from flask import Flask, render_template, request
import json
import time
import threading
import random
from datetime import datetime, timedelta
from simple_websocket import Server, ConnectionClosed
import jwt

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(32).hex()

connected_clients = set()


SKIING_EVENTS = [
    {
        "id": 1,
        "title": "Powder Day Festival",
        "description": "Celebrate the fresh snowfall with live music and hot cocoa!",
        "date": (datetime.now() + timedelta(days=2)).strftime("%Y-%m-%d"),
        "time": "10:00 AM - 4:00 PM",
        "location": "Base Lodge",
        "type": "festival"
    },
    {
        "id": 2,
        "title": "Night Skiing Session",
        "description": "Experience the slopes under the stars with illuminated trails.",
        "date": (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d"),
        "time": "6:00 PM - 10:00 PM",
        "location": "Main Slope",
        "type": "activity"
    },
    {
        "id": 3,
        "title": "Ski Safety Workshop",
        "description": "Learn essential skiing safety tips from certified instructors.",
        "date": (datetime.now() + timedelta(days=5)).strftime("%Y-%m-%d"),
        "time": "2:00 PM - 4:00 PM",
        "location": "Training Center",
        "type": "workshop"
    }
]

def generate_random_alert():
    alert_types = ["weather", "trail", "safety", "equipment", "avalanche", "live_skiing"]
    severities = ["info", "warning", "danger"]
    locations = ["Alpine Valley", "Summit Ridge", "Pine Trail", "Eagle's Nest", "Powder Bowl"]
    
    titles = {
        "weather": ["Fresh Powder Alert", "Blizzard Warning", "Perfect Skiing Conditions", "Temperature Drop"],
        "trail": ["Trail Closure", "New Trail Opened", "Grooming Complete", "Trail Conditions Update"],
        "safety": ["Safety Reminder", "Visibility Warning", "Equipment Check", "First Aid Alert"],
        "equipment": ["Lift Maintenance", "Equipment Rental Available", "Ski Patrol Update"],
        "avalanche": ["Avalanche Risk High", "Backcountry Warning", "Avalanche Advisory", "Snow Stability Alert"],
        "live_skiing": ["Live Powder Conditions", "Current Slope Status", "Real-time Snow Report", "Live Trail Update", "Skiing Conditions Alert", "Live Weather Update"]
    }
    
    descriptions = {
        "weather": [
            "6-12 inches of fresh powder expected overnight. Perfect skiing conditions!",
            "Heavy snowfall warning in effect. Visibility may be reduced.",
            "Clear skies and perfect temperature for skiing today.",
            "Sudden temperature drop expected. Dress warmly."
        ],
        "trail": [
            "Trail temporarily closed for maintenance and safety.",
            "New expert trail now open after grooming completion.",
            "All main trails have been freshly groomed overnight.",
            "Trail conditions updated - check current status before heading out."
        ],
        "safety": [
            "Remember to wear proper safety equipment at all times.",
            "Low visibility conditions - ski with extra caution.",
            "Equipment safety check recommended before skiing.",
            "First aid station available at base lodge."
        ],
        "equipment": [
            "Lift maintenance scheduled - temporary service interruption.",
            "Ski equipment rental now available at discounted rates.",
            "Ski patrol conducting routine safety inspections."
        ],
        "avalanche": [
            "Backcountry areas have high avalanche risk. Stay on marked trails.",
            "Avalanche warning issued for off-piste areas.",
            "Current snow conditions present avalanche risk.",
            "Snow stability assessment shows elevated danger levels."
        ],
        "live_skiing": [
            "Fresh powder detected on slopes - excellent skiing conditions right now!",
            "Current visibility is excellent with light snowfall continuing.",
            "Live update: All main slopes are in perfect condition for skiing.",
            "Real-time report: Temperature is ideal for powder snow.",
            "Live conditions: Light winds, perfect skiing weather.",
            "Current status: Fresh grooming completed, slopes ready for skiing."
        ]
    }
    
    alert_type = random.choice(alert_types)
    return {
        "id": random.randint(1000, 9999),
        "type": alert_type,
        "severity": random.choice(severities),
        "title": random.choice(titles[alert_type]),
        "description": random.choice(descriptions[alert_type]),
        "location": random.choice(locations),
        "timestamp": datetime.now().isoformat()
    }

def broadcast_to_all(message):
    disconnected = set()
    for client in connected_clients:
        try:
            client.send(json.dumps(message))
        except:
            disconnected.add(client)
    
    for client in disconnected:
        connected_clients.discard(client)

def background_alert_sender():
    while True:
        time.sleep(random.randint(10, 30))
        alert = generate_random_alert()
        broadcast_to_all({"type": "new_alert", "data": alert})

ADMIN_HOST = os.environ.get('ADMIN_HOST', '127.0.0.1')
try:
    ADMIN_HOST = socket.gethostbyname(ADMIN_HOST)
    print(f"Resolved ADMIN_HOST: {ADMIN_HOST}")
except Exception as e:
    print(f"Failed to resolve ADMIN_HOST: {e}")
    ADMIN_HOST = '127.0.0.1'
ADMIN_PORT = int(os.environ.get('ADMIN_PORT', 3001))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit_news', methods=['POST'])
def submit_news():
    try:
        data = request.form
        url = data.get('url', '').strip()
        if not url:
            return "URL is required", 400

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((ADMIN_HOST, ADMIN_PORT))
        s.sendall(url.encode())
        s.close()

        return "News URL submitted for admin review"

    except Exception as e:
        print(e)
        return "Error submitting URL", 500

@app.route('/ws', websocket=True)
def handle_websocket():
    ws = Server.accept(request.environ)
    connected_clients.add(ws)

    secret = os.environ.get('JWT_SECRET', os.urandom(32).hex())
    payload = {
        "username": "guest",
        "iat": int(time.time()),
        "exp": int(time.time()) + 3600  # expires in 1 hour
    }
    token = jwt.encode(payload, secret, algorithm="HS256")
    ws.send(json.dumps({"type": "token", "token": token}))
    
    try:
        ws.send(json.dumps({"type": "initial_alerts", "data": [generate_random_alert() for _ in range(6)]}))
        
        while True:
            try:
                message = ws.receive()
                data = json.loads(message)
                if data.get("type") == "auth":
                    token = data.get("token")
                    try:
                        decoded = jwt.decode(token, secret, algorithms=["HS256"])
                        username = decoded.get("username", "guest")
                        ws.send(json.dumps({"type": "auth_success", "username": username}))
                        if username == "admin":
                            if request.remote_addr == ADMIN_HOST:
                                ws.send(json.dumps({"type": "flag", "message": os.environ.get('FLAG', 'No flag set')}))
                            else:
                                ws.send(json.dumps({"type": "flag", "error": "Unauthorized flag access from IP: " + request.remote_addr}))
                    except jwt.ExpiredSignatureError:
                        ws.send(json.dumps({"type": "auth_error", "error": "Token expired"}))
                    except jwt.InvalidTokenError:
                        ws.send(json.dumps({"type": "auth_error", "error": "Invalid token"}))
            except ConnectionClosed:
                break
            except:
                break
                
    except:
        pass
    finally:
        connected_clients.discard(ws)
    
    return ''

if __name__ == '__main__':
    alert_thread = threading.Thread(target=background_alert_sender, daemon=True)
    alert_thread.start()
    app.run(host='0.0.0.0', port=8000)
