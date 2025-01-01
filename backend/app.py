from flask import Flask, request, jsonify
import subprocess
from typing import Dict, List, Optional
from functools import wraps

app = Flask(__name__)

def handle_errors(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except subprocess.CalledProcessError as e:
            return jsonify({
                "status": "error",
                "message": f"Command failed: {e.stderr.decode('utf-8')}"
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

@app.route('/health', methods=['GET'])
@handle_errors
def health_check():
    """Check if the service has the required permissions."""
    execute_command(["ip", "link", "show"])
    return jsonify({"status": "healthy", "message": "Service has required permissions"})

@app.route('/bridge', methods=['POST'])
@handle_errors
def create_bridge():
    """Create a new network bridge."""
    data = request.get_json()
    
    if 'name' not in data:
        return jsonify({"status": "error", "message": "Bridge name is required"}), 400
    
    name = data['name']
    
    # Create bridge
    execute_command(["ip", "link", "add", name, "type", "bridge"])
    # Set bridge up
    execute_command(["ip", "link", "set", name, "up"])
    
    return jsonify({"status": "success", "message": f"Bridge {name} created successfully"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)