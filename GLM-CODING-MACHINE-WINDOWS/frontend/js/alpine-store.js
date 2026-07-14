document.addEventListener('alpine:init', () => {
    Alpine.store('app', {
        // State
        isConnected: false,
        isThinking: false,
        inputMessage: '',
        messages: [],
        
        // Actions
        addMessage(role, content) {
            this.messages.push({
                id: Date.now(),
                role: role,
                content: content
            });
            // Auto-scroll chat to bottom
            const chatBox = document.getElementById('chat-messages');
            if(chatBox) {
                setTimeout(() => chatBox.scrollTop = chatBox.scrollHeight, 50);
            }
        },
        
        sendMessage() {
            if (!this.inputMessage.trim()) return;
            
            const text = this.inputMessage;
            this.addMessage('user', text);
            this.inputMessage = '';
            this.isThinking = true;
            
            // Emit via Socket.IO (initialized in main.js)
            if (window.socket) {
                window.socket.emit('agent_message', { message: text });
            }
        }
    });
});