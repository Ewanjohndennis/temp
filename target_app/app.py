from flask import Flask, abort
from prometheus_flask_exporter import PrometheusMetrics
import time
import math
import threading

app = Flask(__name__)
# This automatically exposes /metrics AND tracks all HTTP traffic/errors!
metrics = PrometheusMetrics(app)

# A global list to hold junk data for our memory leak simulation
memory_leak_storage = []

def background_cpu_spike():
    """Spins hard to max out CPU"""
    end_time = time.time() + 120  # Run for 2 full minutes
    while time.time() < end_time:
        math.factorial(5000)
        time.sleep(0.001)

@app.route('/')
def hello():
    return "Target App is Running!"

# --- CHAOS ENGINEERING ENDPOINTS ---

@app.route('/chaos/cpu')
def chaos_cpu():
    # Spawns 4 threads at once to absolutely hammer the container's CPU
    for _ in range(4):
        threading.Thread(target=background_cpu_spike).start()
    return "Chaos injected: CPU spike started across 4 threads!"

@app.route('/chaos/memory')
def chaos_memory():
    # Appends 50MB of junk string data into RAM every time you hit this URL
    junk_data = "A" * 50_000_000 
    memory_leak_storage.append(junk_data)
    return f"Chaos injected: Leaked 50MB of Memory. Total chunks: {len(memory_leak_storage)}"

@app.route('/chaos/error')
def chaos_error():
    # Intentionally crashes this specific request with an HTTP 500 Internal Server Error
    abort(500, description="Chaos injected: Simulated database connection failure!")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)