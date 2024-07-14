class WebSocketClient {
    constructor(url) {
        this.url = url;
        this.socket = null;
        this.listeners = {};
    }

    connect(authToken) {
        return new Promise((resolve, reject) => {
            this.socket = new WebSocket(this.url);

            this.socket.onopen = () => {
                this.socket.send(authToken);
                resolve();
            };

            this.socket.onerror = (error) => {
                reject(error);
            };

            this.socket.onmessage = (event) => {
                const message = JSON.parse(event.data);
                if (this.listeners[message.type]) {
                    this.listeners[message.type](message.content);
                }
            };

            this.socket.onclose = () => {
                console.log('WebSocket connection closed');
                // Implement reconnection logic here if needed
            };
        });
    }

    send(type, content) {
        if (this.socket && this.socket.readyState === WebSocket.OPEN) {
            const message = JSON.stringify({ type, content });
            this.socket.send(message);
        } else {
            console.error('WebSocket is not connected');
        }
    }

    on(messageType, callback) {
        this.listeners[messageType] = callback;
    }

    close() {
        if (this.socket) {
            this.socket.close();
        }
    }
}

// Usage example:
// const wsClient = new WebSocketClient('wss://your-server-url/ws');
// wsClient.connect(authToken)
//     .then(() => {
//         console.log('Connected to WebSocket');
//         wsClient.on('game_update', handleGameUpdate);
//         wsClient.on('error', handleError);
//     })
//     .catch(error => console.error('WebSocket connection error:', error));
