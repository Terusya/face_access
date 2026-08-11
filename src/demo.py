import requests
import uuid

happy_event = {
    "event_id": f"happy-{uuid.uuid4()}",
    "gate_id": "gate-1",
    "camera_id": "cam-1a",
    "captured_at": "2026-07-31T08:52:14Z",
    "frame_uri": "file://demo/frames/happy.jpg",
    "metadata": {"direction": "in", "edge_node": "edge-1", "network": "online"}
}

risky_event = {
    "event_id": f"risky-{uuid.uuid4()}",
    "gate_id": "gate-1",
    "camera_id": "cam-1a",
    "captured_at": "2026-07-31T08:57:41Z",
    "frame_uri": "file://demo/frames/risky.jpg",
    "metadata": {"direction": "in", "edge_node": "edge-1", "network": "online"}
}

url = "http://localhost:8000/verify"

print("Happy path:")
resp = requests.post(url, json=happy_event)
print(resp.json())

print("\nRisky path:")
resp = requests.post(url, json=risky_event)
print(resp.json())