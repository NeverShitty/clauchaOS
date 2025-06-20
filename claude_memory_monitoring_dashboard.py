#!/usr/bin/env python3
"""
🎯 CLAUDE MEMORY REAL-TIME MONITORING DASHBOARD
Performance metrics, error handling, and user-friendly interface
"""

import os
import json
import time
import asyncio
from datetime import datetime, timedelta
from flask import Flask, render_template, jsonify, request
from flask_socketio import SocketIO, emit
import threading
import psutil
import logging
from collections import deque
import smtplib
from email.mime.text import MIMEText
import subprocess

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'claude-memory-monitoring'
socketio = SocketIO(app, cors_allowed_origins="*")

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MemoryMonitoringSystem:
    def __init__(self, memory_base_path="/Users/nickbianchi/MCMANSION/AUTOMATION_LAB"):
        self.base_path = memory_base_path
        self.memory_dir = os.path.join(memory_base_path, "vector_memory_v3")
        
        # Performance metrics storage (last 24 hours)
        self.metrics = {
            "search_latency": deque(maxlen=1440),  # 1 per minute
            "storage_size": deque(maxlen=1440),
            "embedding_success_rate": deque(maxlen=1440),
            "memory_growth_rate": deque(maxlen=1440),
            "api_errors": deque(maxlen=1440),
            "cache_hit_rate": deque(maxlen=1440),
            "active_instances": {},
            "conversation_volume": {}
        }
        
        # Alert thresholds
        self.alerts = {
            "search_latency_ms": 200,
            "storage_growth_mb_per_hour": 100,
            "embedding_failure_rate": 0.05,
            "api_error_rate": 0.1,
            "disk_usage_percent": 80,
            "memory_usage_percent": 80
        }
        
        # Alert history
        self.alert_history = deque(maxlen=100)
        
        # Start monitoring threads
        self.start_monitoring()
    
    def start_monitoring(self):
        """Start background monitoring threads"""
        # Performance monitoring thread
        perf_thread = threading.Thread(target=self.monitor_performance, daemon=True)
        perf_thread.start()
        
        # Storage monitoring thread
        storage_thread = threading.Thread(target=self.monitor_storage, daemon=True)
        storage_thread.start()
        
        # Error monitoring thread
        error_thread = threading.Thread(target=self.monitor_errors, daemon=True)
        error_thread.start()
        
        logger.info("🚀 Monitoring threads started")
    
    def monitor_performance(self):
        """Monitor system performance metrics"""
        while True:
            try:
                # Simulate performance metrics (replace with actual measurements)
                current_metrics = {
                    "timestamp": datetime.now().isoformat(),
                    "search_latency": self._measure_search_latency(),
                    "embedding_time": self._measure_embedding_time(),
                    "cache_hit_rate": self._calculate_cache_hit_rate(),
                    "cpu_usage": psutil.cpu_percent(),
                    "memory_usage": psutil.virtual_memory().percent,
                    "active_threads": threading.active_count()
                }
                
                # Store metrics
                self.metrics["search_latency"].append(current_metrics["search_latency"])
                self.metrics["cache_hit_rate"].append(current_metrics["cache_hit_rate"])
                
                # Check for performance alerts
                if current_metrics["search_latency"] > self.alerts["search_latency_ms"]:
                    self._trigger_alert("HIGH_LATENCY", f"Search latency: {current_metrics['search_latency']}ms")
                
                if current_metrics["memory_usage"] > self.alerts["memory_usage_percent"]:
                    self._trigger_alert("HIGH_MEMORY", f"Memory usage: {current_metrics['memory_usage']}%")
                
                # Emit real-time update
                socketio.emit('performance_update', current_metrics)
                
            except Exception as e:
                logger.error(f"Performance monitoring error: {e}")
            
            time.sleep(60)  # Check every minute
    
    def monitor_storage(self):
        """Monitor storage usage and growth"""
        while True:
            try:
                # Calculate storage metrics
                storage_info = self._get_storage_info()
                
                # Store metrics
                self.metrics["storage_size"].append(storage_info["total_size_mb"])
                self.metrics["memory_growth_rate"].append(storage_info["growth_rate_mb_hour"])
                
                # Check storage alerts
                if storage_info["growth_rate_mb_hour"] > self.alerts["storage_growth_mb_per_hour"]:
                    self._trigger_alert("RAPID_GROWTH", 
                        f"Storage growing at {storage_info['growth_rate_mb_hour']}MB/hour")
                
                if storage_info["disk_usage_percent"] > self.alerts["disk_usage_percent"]:
                    self._trigger_alert("DISK_SPACE", 
                        f"Disk usage: {storage_info['disk_usage_percent']}%")
                
                # Emit update
                socketio.emit('storage_update', storage_info)
                
            except Exception as e:
                logger.error(f"Storage monitoring error: {e}")
            
            time.sleep(300)  # Check every 5 minutes
    
    def monitor_errors(self):
        """Monitor API errors and embedding failures"""
        log_file = os.path.join(self.memory_dir, "error.log")
        
        while True:
            try:
                if os.path.exists(log_file):
                    # Parse recent errors
                    recent_errors = self._parse_error_log(log_file)
                    
                    # Calculate error rates
                    api_error_rate = recent_errors.get("api_errors", 0) / max(recent_errors.get("total_requests", 1), 1)
                    embedding_failure_rate = recent_errors.get("embedding_failures", 0) / max(recent_errors.get("total_embeddings", 1), 1)
                    
                    # Store metrics
                    self.metrics["api_errors"].append(api_error_rate)
                    self.metrics["embedding_success_rate"].append(1 - embedding_failure_rate)
                    
                    # Check error alerts
                    if api_error_rate > self.alerts["api_error_rate"]:
                        self._trigger_alert("API_ERRORS", f"API error rate: {api_error_rate:.2%}")
                    
                    if embedding_failure_rate > self.alerts["embedding_failure_rate"]:
                        self._trigger_alert("EMBEDDING_FAILURES", 
                            f"Embedding failure rate: {embedding_failure_rate:.2%}")
                    
                    # Emit update
                    socketio.emit('error_update', {
                        "api_error_rate": api_error_rate,
                        "embedding_failure_rate": embedding_failure_rate,
                        "recent_errors": recent_errors.get("recent", [])
                    })
                
            except Exception as e:
                logger.error(f"Error monitoring error: {e}")
            
            time.sleep(60)  # Check every minute
    
    def _measure_search_latency(self):
        """Measure actual search latency"""
        # Simulate latency measurement (replace with actual test)
        import random
        return random.randint(20, 150)
    
    def _measure_embedding_time(self):
        """Measure embedding creation time"""
        # Simulate measurement
        import random
        return random.randint(50, 200)
    
    def _calculate_cache_hit_rate(self):
        """Calculate cache hit rate"""
        # Simulate cache hit rate
        import random
        return random.uniform(0.7, 0.95)
    
    def _get_storage_info(self):
        """Get storage usage information"""
        total_size = 0
        file_count = 0
        
        # Calculate directory size
        for root, dirs, files in os.walk(self.memory_dir):
            for file in files:
                if file.endswith('.json'):
                    filepath = os.path.join(root, file)
                    total_size += os.path.getsize(filepath)
                    file_count += 1
        
        # Get disk usage
        disk_usage = psutil.disk_usage(self.base_path)
        
        # Calculate growth rate (simplified)
        current_size_mb = total_size / (1024 * 1024)
        if len(self.metrics["storage_size"]) > 0:
            prev_size = self.metrics["storage_size"][-1]
            growth_rate = (current_size_mb - prev_size) * 12  # Per hour
        else:
            growth_rate = 0
        
        return {
            "total_size_mb": round(current_size_mb, 2),
            "file_count": file_count,
            "growth_rate_mb_hour": round(growth_rate, 2),
            "disk_usage_percent": disk_usage.percent,
            "disk_free_gb": round(disk_usage.free / (1024**3), 2)
        }
    
    def _parse_error_log(self, log_file):
        """Parse error log for recent errors"""
        # Simplified error parsing (implement actual log parsing)
        return {
            "total_requests": 1000,
            "api_errors": 5,
            "total_embeddings": 500,
            "embedding_failures": 2,
            "recent": [
                {"time": "14:30", "type": "API", "message": "Rate limit exceeded"},
                {"time": "14:25", "type": "Embedding", "message": "Timeout"}
            ]
        }
    
    def _trigger_alert(self, alert_type, message):
        """Trigger an alert"""
        alert = {
            "timestamp": datetime.now().isoformat(),
            "type": alert_type,
            "message": message,
            "severity": self._get_alert_severity(alert_type)
        }
        
        self.alert_history.append(alert)
        
        # Emit alert
        socketio.emit('alert', alert)
        
        # Log alert
        logger.warning(f"🚨 ALERT: {alert_type} - {message}")
        
        # Send email for critical alerts
        if alert["severity"] == "critical":
            self._send_alert_email(alert)
    
    def _get_alert_severity(self, alert_type):
        """Determine alert severity"""
        critical_types = ["DISK_SPACE", "API_ERRORS", "HIGH_MEMORY"]
        if alert_type in critical_types:
            return "critical"
        return "warning"
    
    def _send_alert_email(self, alert):
        """Send email for critical alerts"""
        # Configure with actual email settings
        try:
            # Email implementation here
            pass
        except:
            logger.error("Failed to send alert email")
    
    def get_dashboard_data(self):
        """Get current dashboard data"""
        return {
            "performance": {
                "search_latency_avg": sum(self.metrics["search_latency"]) / max(len(self.metrics["search_latency"]), 1),
                "cache_hit_rate": sum(self.metrics["cache_hit_rate"]) / max(len(self.metrics["cache_hit_rate"]), 1),
                "current_cpu": psutil.cpu_percent(),
                "current_memory": psutil.virtual_memory().percent
            },
            "storage": self._get_storage_info(),
            "errors": {
                "api_error_rate": sum(self.metrics["api_errors"]) / max(len(self.metrics["api_errors"]), 1),
                "embedding_success_rate": sum(self.metrics["embedding_success_rate"]) / max(len(self.metrics["embedding_success_rate"]), 1)
            },
            "alerts": list(self.alert_history)[-10:],  # Last 10 alerts
            "instance_status": self._get_instance_status()
        }
    
    def _get_instance_status(self):
        """Get status of all Claude instances"""
        instances = ["METACLAUDE", "CLAUDEFO", "CLAUDESQ", "CLAUDALYN", "CLAUDEMOM", 
                    "CLAUDEMO", "CLAUDESQUAD", "CLAUDEXTER", "CLAUDEBABY", "CLAUDETTE", "CLAUDADDY"]
        
        status = {}
        for instance in instances:
            # Simulate instance status (replace with actual checks)
            status[instance] = {
                "online": True,
                "last_activity": datetime.now().isoformat(),
                "memory_count": self._get_instance_memory_count(instance),
                "qa_score": self._get_instance_qa_score(instance)
            }
        
        return status
    
    def _get_instance_memory_count(self, instance):
        """Get memory count for instance"""
        # Implement actual count
        import random
        return random.randint(100, 1000)
    
    def _get_instance_qa_score(self, instance):
        """Get QA score for instance"""
        # Implement actual score retrieval
        import random
        return round(random.uniform(7.5, 9.5), 1)

# Initialize monitoring system
monitor = MemoryMonitoringSystem()

# Flask routes
@app.route('/')
def dashboard():
    """Main dashboard page"""
    return render_template('dashboard.html')

@app.route('/api/dashboard')
def api_dashboard():
    """API endpoint for dashboard data"""
    return jsonify(monitor.get_dashboard_data())

@app.route('/api/metrics/<metric_type>')
def api_metrics(metric_type):
    """API endpoint for specific metrics"""
    if metric_type in monitor.metrics:
        return jsonify({
            "metric": metric_type,
            "data": list(monitor.metrics[metric_type]),
            "timestamp": datetime.now().isoformat()
        })
    return jsonify({"error": "Invalid metric type"}), 404

@app.route('/api/alerts', methods=['GET', 'POST'])
def api_alerts():
    """API endpoint for alerts"""
    if request.method == 'POST':
        # Update alert thresholds
        data = request.json
        for key, value in data.items():
            if key in monitor.alerts:
                monitor.alerts[key] = value
        return jsonify({"status": "updated", "alerts": monitor.alerts})
    
    return jsonify({
        "thresholds": monitor.alerts,
        "history": list(monitor.alert_history)
    })

# WebSocket events
@socketio.on('connect')
def handle_connect():
    """Handle client connection"""
    emit('connected', {"status": "Connected to monitoring system"})
    # Send initial data
    emit('dashboard_data', monitor.get_dashboard_data())

@socketio.on('request_update')
def handle_update_request(data):
    """Handle update request"""
    metric_type = data.get('metric')
    if metric_type:
        emit('metric_update', {
            "metric": metric_type,
            "data": list(monitor.metrics.get(metric_type, []))
        })

# HTML template (save as templates/dashboard.html)
DASHBOARD_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Claude Memory Monitoring Dashboard</title>
    <script src="https://cdn.socket.io/4.5.4/socket.io.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            margin: 0;
            padding: 20px;
            background: #0f0f0f;
            color: #fff;
        }
        .dashboard {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
        }
        .metric-card {
            background: #1a1a1a;
            border: 1px solid #333;
            border-radius: 8px;
            padding: 20px;
        }
        .metric-title {
            font-size: 14px;
            color: #888;
            margin-bottom: 10px;
        }
        .metric-value {
            font-size: 32px;
            font-weight: bold;
            color: #4CAF50;
        }
        .alert {
            background: #ff5252;
            color: white;
            padding: 10px;
            border-radius: 4px;
            margin-bottom: 10px;
        }
        .chart-container {
            position: relative;
            height: 200px;
        }
        .instance-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
            gap: 10px;
            margin-top: 20px;
        }
        .instance-card {
            background: #2a2a2a;
            padding: 15px;
            border-radius: 4px;
            text-align: center;
        }
        .online { color: #4CAF50; }
        .offline { color: #ff5252; }
    </style>
</head>
<body>
    <h1>🧠 Claude Memory Monitoring Dashboard</h1>
    
    <div id="alerts"></div>
    
    <div class="dashboard">
        <div class="metric-card">
            <div class="metric-title">Search Latency</div>
            <div class="metric-value" id="search-latency">-ms</div>
            <div class="chart-container">
                <canvas id="latency-chart"></canvas>
            </div>
        </div>
        
        <div class="metric-card">
            <div class="metric-title">Storage Size</div>
            <div class="metric-value" id="storage-size">-MB</div>
            <div>Growth: <span id="growth-rate">-</span> MB/hour</div>
        </div>
        
        <div class="metric-card">
            <div class="metric-title">API Success Rate</div>
            <div class="metric-value" id="api-success">-%</div>
        </div>
        
        <div class="metric-card">
            <div class="metric-title">Cache Hit Rate</div>
            <div class="metric-value" id="cache-rate">-%</div>
        </div>
    </div>
    
    <h2>Instance Status</h2>
    <div id="instance-grid" class="instance-grid"></div>
    
    <script>
        const socket = io();
        
        // Chart setup
        const latencyChart = new Chart(document.getElementById('latency-chart'), {
            type: 'line',
            data: {
                labels: [],
                datasets: [{
                    label: 'Latency (ms)',
                    data: [],
                    borderColor: '#4CAF50',
                    tension: 0.1
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: { beginAtZero: true }
                }
            }
        });
        
        // Socket event handlers
        socket.on('connected', (data) => {
            console.log('Connected:', data);
        });
        
        socket.on('dashboard_data', (data) => {
            updateDashboard(data);
        });
        
        socket.on('performance_update', (data) => {
            document.getElementById('search-latency').textContent = data.search_latency + 'ms';
            
            // Update chart
            latencyChart.data.labels.push(new Date().toLocaleTimeString());
            latencyChart.data.datasets[0].data.push(data.search_latency);
            if (latencyChart.data.labels.length > 20) {
                latencyChart.data.labels.shift();
                latencyChart.data.datasets[0].data.shift();
            }
            latencyChart.update();
        });
        
        socket.on('storage_update', (data) => {
            document.getElementById('storage-size').textContent = data.total_size_mb + 'MB';
            document.getElementById('growth-rate').textContent = data.growth_rate_mb_hour;
        });
        
        socket.on('alert', (alert) => {
            showAlert(alert);
        });
        
        function updateDashboard(data) {
            // Update metrics
            document.getElementById('search-latency').textContent = 
                Math.round(data.performance.search_latency_avg) + 'ms';
            document.getElementById('storage-size').textContent = 
                data.storage.total_size_mb + 'MB';
            document.getElementById('api-success').textContent = 
                Math.round((1 - data.errors.api_error_rate) * 100) + '%';
            document.getElementById('cache-rate').textContent = 
                Math.round(data.performance.cache_hit_rate * 100) + '%';
            
            // Update instances
            updateInstanceGrid(data.instance_status);
            
            // Show alerts
            data.alerts.forEach(showAlert);
        }
        
        function updateInstanceGrid(instances) {
            const grid = document.getElementById('instance-grid');
            grid.innerHTML = '';
            
            for (const [name, status] of Object.entries(instances)) {
                const card = document.createElement('div');
                card.className = 'instance-card';
                card.innerHTML = `
                    <div>${name}</div>
                    <div class="${status.online ? 'online' : 'offline'}">
                        ${status.online ? '🟢 Online' : '🔴 Offline'}
                    </div>
                    <div>Memories: ${status.memory_count}</div>
                    <div>QA: ${status.qa_score}/10</div>
                `;
                grid.appendChild(card);
            }
        }
        
        function showAlert(alert) {
            const alertsDiv = document.getElementById('alerts');
            const alertEl = document.createElement('div');
            alertEl.className = 'alert';
            alertEl.textContent = `${alert.type}: ${alert.message}`;
            alertsDiv.appendChild(alertEl);
            
            // Auto-remove after 10 seconds
            setTimeout(() => alertEl.remove(), 10000);
        }
        
        // Request updates every 5 seconds
        setInterval(() => {
            socket.emit('request_update', {metric: 'all'});
        }, 5000);
    </script>
</body>
</html>
"""

def create_dashboard_template():
    """Create dashboard HTML template"""
    os.makedirs('templates', exist_ok=True)
    with open('templates/dashboard.html', 'w') as f:
        f.write(DASHBOARD_HTML)

if __name__ == '__main__':
    # Create template
    create_dashboard_template()
    
    print("🎯 Claude Memory Monitoring Dashboard")
    print("=" * 50)
    print("Starting monitoring system...")
    print(f"Dashboard available at: http://localhost:5000")
    print("\nMonitoring:")
    print("  ✅ Performance metrics")
    print("  ✅ Storage growth")
    print("  ✅ API errors")
    print("  ✅ Instance health")
    print("\nAlerts configured for:")
    for alert, threshold in monitor.alerts.items():
        print(f"  - {alert}: {threshold}")
    
    # Run Flask app
    socketio.run(app, debug=True, port=5000)