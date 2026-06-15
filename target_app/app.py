# A simple Python web server that exposes /metrics
1.  from flask import Flask
2.  from prometheus_client import make_wsgi_app, Counter, Histogram
3.  from werkzeug.middleware.dispatcher import DispatcherMiddleware
4.  import time
5.  import math
6.  
7.  app = Flask(__name__)
8.  
9.  # Add prometheus wsgi middleware to route /metrics requests
10. app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {
11.     '/metrics': make_wsgi_app()
12. })
13. 
14. @app.route('/')
15. def hello():
16.     return "Target App is Running!"
17. 
18. @app.route('/cpu-spike')
19. def cpu_spike():
20.     # Simulate a CPU-heavy task for testing alerts
21.     end_time = time.time() + 10  # Run for 10 seconds
22.     while time.time() < end_time:
23.         math.factorial(10000) 
24.     return "CPU Spike Triggered!"
25. 
26. if __name__ == '__main__':
27.     app.run(host='0.0.0.0', port=5000)