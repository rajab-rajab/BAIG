// Initialize Socket.IO Client
document.addEventListener('DOMContentLoaded', () => {
    const socket = io('http://127.0.0.1:5000');
    window.socket = socket; // Expose globally for Alpine store

    socket.on('connect', () => {
        console.log('✅ WebSocket Connected to Backend');
        Alpine.store('app').isConnected = true;
    });

    socket.on('disconnect', () => {
        console.log('❌ WebSocket Disconnected');
        Alpine.store('app').isConnected = false;
    });

    // Agent Activity (Thinking, Routing, etc.)
    socket.on('agent_activity', (data) => {
        if (data.type === 'thinking') {
            Alpine.store('app').isThinking = true;
        }
    });

    // Real-time Streaming Chunks
    socket.on('agent_message_chunk', (data) => {
        Alpine.store('app').isThinking = false;
        
        // Find or create the current assistant message
        let currentMsg = Alpine.store('app').messages.find(m => m.id === 'streaming');
        if (!currentMsg) {
            Alpine.store('app').messages.push({ id: 'streaming', role: 'assistant', content: '' });
        }
        
        // Append content
        currentMsg = Alpine.store('app').messages.find(m => m.id === 'streaming');
        currentMsg.content += data.content;
    });

    // Message Complete
    socket.on('agent_message_complete', (data) => {
        let currentMsg = Alpine.store('app').messages.find(m => m.id === 'streaming');
        if (currentMsg) {
            currentMsg.id = Date.now(); // Finalize ID
        }
        Alpine.store('app').isThinking = false;
    });
});