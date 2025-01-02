from flask import Flask, request, render_template
import requests

app = Flask(__name__)

def get_ip_data(ip):
    """Fetch geolocation data for the given IP address using the ipinfo.io API."""
    try:
        response = requests.get(f"https://ipinfo.io/{ip}/json")
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        print(f"Error fetching IP data: {e}")
    return {}

@app.route('/')
def index():
    # Get visitor's IP address
    visitor_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    ip_data = get_ip_data(visitor_ip)

    # Device and browser info from User-Agent header
    user_agent = request.headers.get('User-Agent', 'Unknown')

    # Collect data for rendering
    data = {
        "ip": visitor_ip,
        "country": ip_data.get("country", "Unknown"),
        "city": ip_data.get("city", "Unknown"),
        "isp": ip_data.get("org", "Unknown"),
        "user_agent": user_agent
    }

    return render_template('index.html', data=data)

if __name__ == "__main__":
    app.run(debug=True)
