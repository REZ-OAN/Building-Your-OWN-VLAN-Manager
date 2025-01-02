# Variables
API_URL = http://localhost:5000/vlan-bridge
JSON_PAYLOAD = '{"name": "br0", "subnet": "192.168.1.1/24"}'

req-install :
	pip3 install -r requirements.txt
start-app :
	python3 app.py

test-vlan-bridge:
	@echo "Testing VLAN Bridge creation... route /vlan-bridge"
	curl -X POST $(API_URL) \
		-H "Content-Type: application/json" \
		-d $(JSON_PAYLOAD)
.PHONY: req-install start-app