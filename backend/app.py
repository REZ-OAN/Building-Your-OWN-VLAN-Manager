from flask import Flask, request, jsonify
import subprocess
from typing import Dict, List, Optional
from functools import wraps
from flask_cors import CORS 
app = Flask(__name__)

# Enable CORS for all routes and domains
CORS(app,resources={r"/*": {"origins": "*"}})

def handle_errors(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except subprocess.CalledProcessError as e:
            return jsonify({
                "status": "error",
                "message": f"Command failed: {e.stderr.decode('utf-8') if e.stderr else str(e)}"
            }), 400
        except Exception as e:
            return jsonify({
                "status": "error",
                "message": str(e)
            }), 500
    return wrapper

def execute_command(command: List[str]) -> tuple[str, str]:
    """Execute a network command and return output."""
    result = subprocess.run(
        command,
        check=True,
        capture_output=True,
        text=True
    )
    return result.stdout, result.stderr

@app.route('/vlan-bridge', methods=['POST'])
@handle_errors
def create_vlan_bridge():
    """Create a VLAN-aware bridge."""
    data = request.get_json()
    if 'name' not in data or 'subnet' not in data:
        return jsonify({"status": "error", "message": "Bridge name is required"}), 400
    
    name = data['name']
    subnet = data['subnet']
    # Create bridge
    execute_command(["ip", "link", "add", name, "type", "bridge"])
    # Enable VLAN filtering
    execute_command(["ip", "link", "set", name, "type", "bridge", "vlan_filtering", "1"])
    # Set bridge up
    execute_command(["ip", "link", "set", name, "up"])
    # Add IP address to bridge
    execute_command(["ip", "addr", "add", f"{subnet}", "dev", name])

    return jsonify({
        "status": "success", 
        "message": f"VLAN-aware bridge {name} created successfully"
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)