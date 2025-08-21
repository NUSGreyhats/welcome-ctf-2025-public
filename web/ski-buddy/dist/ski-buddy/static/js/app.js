class SkiBuddy {
    constructor() {
        this.socket = null;
        this.alerts = [];
        this.events = [];
        this.init();
    }

    init() {
        this.initWebSocket();
        this.initSnowAnimation();
    }

    initWebSocket() {
        const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
        const wsUrl = `${protocol}//${window.location.host}/ws`;
        
        this.socket = new WebSocket(wsUrl);
        
        this.socket.onopen = () => {
            console.log('Connected to Ski Buddy server');
            this.updateConnectionStatus(true);
        };

        this.socket.onclose = () => {
            console.log('Disconnected from Ski Buddy server');
            this.updateConnectionStatus(false);
            setTimeout(() => this.initWebSocket(), 3000);
        };

        this.socket.onerror = (error) => {
            console.error('WebSocket error:', error);
            this.updateConnectionStatus(false);
        };

        this.socket.onmessage = (event) => {
            const message = JSON.parse(event.data);
            
            switch(message.type) {
                case 'initial_alerts':
                    this.alerts = message.data;
                    this.renderAlerts();
                    break;
                case 'new_alert':
                    console.log('New alert received:', message.data);
                    this.alerts.unshift(message.data);
                    this.renderAlerts();
                    this.showNotification(message.data);
                    break;
            }
        };
    }

    sendMessage(message) {
        if (this.socket && this.socket.readyState === WebSocket.OPEN) {
            this.socket.send(JSON.stringify(message));
        }
    }

    updateConnectionStatus(connected) {
        const statusElement = document.getElementById('connection-status');
        if (connected) {
            statusElement.innerHTML = '<i class="fas fa-circle text-success me-1"></i>Connected';
        } else {
            statusElement.innerHTML = '<i class="fas fa-circle text-danger me-1"></i>Disconnected';
        }
    }

    initSnowAnimation() {
        this.createSnowflakes();
        setInterval(() => {
            this.createSnowflakes(10);
        }, 1000);
    }

    createSnowflakes(count = 50) {
        const snowContainer = document.getElementById('snow-container');
        const snowflakeChars = ['❄', '❅', '❆', '✻', '✼', '❇', '✳'];
        
        for (let i = 0; i < count; i++) {
            const snowflake = document.createElement('div');
            snowflake.className = 'snowflake';
            snowflake.innerHTML = snowflakeChars[Math.floor(Math.random() * snowflakeChars.length)];
            
            // Random positioning and animation
            snowflake.style.left = Math.random() * 100 + '%';
            snowflake.style.animationDuration = (Math.random() * 3 + 2) + 's';
            snowflake.style.opacity = Math.random() * 0.8 + 0.2;
            snowflake.style.fontSize = (Math.random() * 0.8 + 0.8) + 'em';
            
            snowContainer.appendChild(snowflake);
            
            // Remove snowflake after animation
            setTimeout(() => {
                if (snowflake.parentNode) {
                    snowflake.parentNode.removeChild(snowflake);
                }
            }, 5000);
        }
    }

    renderAlerts() {
        const container = document.getElementById('alerts-container');
        
        if (this.alerts.length === 0) {
            container.innerHTML = `
                <div class="col-12 text-center">
                    <p class="text-muted">No active alerts at this time.</p>
                </div>
            `;
            return;
        }

        container.innerHTML = this.alerts.map(alert => this.createAlertCard(alert)).join('');
    }

    createAlertCard(alert) {
        const severityIcons = {
            'info': 'fas fa-info-circle',
            'warning': 'fas fa-exclamation-triangle',
            'danger': 'fas fa-exclamation-circle'
        };

        const typeIcons = {
            'live_skiing': 'fas fa-skiing'
        };

        const timeAgo = this.getTimeAgo(new Date(alert.timestamp));

        return `
            <div class="col-lg-6 col-xl-4 mb-4">
                <div class="card alert-card severity-${alert.severity} h-100">
                    <div class="card-body">
                        <div class="d-flex align-items-start">
                            <div class="alert-icon severity-${alert.severity} flex-shrink-0">
                                <i class="${typeIcons[alert.type] || severityIcons[alert.severity]}"></i>
                            </div>
                            <div class="flex-grow-1">
                                <h5 class="card-title mb-2">${alert.title}</h5>
                                <p class="card-text text-muted mb-2">${alert.description}</p>
                                <div class="d-flex justify-content-between align-items-center">
                                    <small class="text-muted">
                                        <i class="fas fa-map-marker-alt me-1"></i>
                                        ${alert.location}
                                    </small>
                                    <small class="text-muted">${timeAgo}</small>
                                </div>
                                <span class="badge bg-${this.getSeverityColor(alert.severity)} mt-2">
                                    ${alert.type.replace("_", " ").toUpperCase()}
                                </span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `;
    }

    getTimeAgo(date) {
        const now = new Date();
        const diffInMs = now - date;
        const diffInMinutes = Math.floor(diffInMs / (1000 * 60));
        
        if (diffInMinutes < 1) return 'Just now';
        if (diffInMinutes < 60) return `${diffInMinutes}m ago`;
        
        const diffInHours = Math.floor(diffInMinutes / 60);
        if (diffInHours < 24) return `${diffInHours}h ago`;
        
        const diffInDays = Math.floor(diffInHours / 24);
        return `${diffInDays}d ago`;
    }

    getSeverityColor(severity) {
        const colors = {
            'info': 'info',
            'warning': 'warning',
            'danger': 'danger'
        };
        return colors[severity] || 'secondary';
    }

    showNotification(alert) {
        if ('Notification' in window && Notification.permission === 'granted') {
            new Notification(`Ski Buddy: ${alert.title}`, {
                body: alert.description,
                icon: '/static/favicon.ico'
            });
        }
    }

    requestNotificationPermission() {
        if ('Notification' in window && Notification.permission === 'default') {
            Notification.requestPermission();
        }
    }
}

function scrollToSection(sectionId) {
    const element = document.getElementById(sectionId);
    if (element) {
        element.scrollIntoView({ 
            behavior: 'smooth',
            block: 'start'
        });
    }
}

document.addEventListener('DOMContentLoaded', () => {
    const app = new SkiBuddy();
    window.skiBuddy = app;
});
