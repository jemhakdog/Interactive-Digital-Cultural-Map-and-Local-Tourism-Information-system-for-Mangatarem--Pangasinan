document.addEventListener('DOMContentLoaded', () => {
    const roomIdInput = document.getElementById('room_id');
    const currentUserIdInput = document.getElementById('current_user_id');
    const csrfToken = document.getElementById('csrf_token')?.value;
    
    if (!roomIdInput || !currentUserIdInput) return;
    
    const roomId = roomIdInput.value;
    const currentUserId = parseInt(currentUserIdInput.value);
    
    const chatMessages = document.getElementById('chat-messages');
    const chatForm = document.getElementById('chat-form');
    const messageInput = document.getElementById('message-input');
    const connectionStatus = document.getElementById('connection-status');
    const typingIndicator = document.getElementById('typing-indicator');
    
    // Connect to Socket.IO
    // The server is at the same origin
    const socket = io({
        auth: {
            token: csrfToken // Optional: pass CSRF if strict verification is on
        }
    });
    
    let typingTimeout = null;
    let isTyping = false;
    let page = 1;
    let hasNextPage = true;
    let isLoadingHistory = false;
    
    // UI Helpers
    function setConnectionStatus(status, text) {
        if (!connectionStatus) return;
        
        let html = '';
        if (status === 'connected') {
            html = `
                <span class="relative flex h-2 w-2 mr-1.5">
                  <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
                  <span class="relative inline-flex rounded-full h-2 w-2 bg-emerald-500"></span>
                </span>
                Connected
            `;
            connectionStatus.className = "flex items-center text-emerald-600 font-medium";
        } else if (status === 'disconnected') {
            html = `
                <span class="relative flex h-2 w-2 mr-1.5">
                  <span class="relative inline-flex rounded-full h-2 w-2 bg-red-500"></span>
                </span>
                Disconnected
            `;
            connectionStatus.className = "flex items-center text-red-600 font-medium";
        } else {
            html = `
                <i class="fas fa-circle-notch fa-spin text-amber-500 mr-1.5"></i>
                Connecting...
            `;
            connectionStatus.className = "flex items-center text-amber-600 font-medium";
        }
        connectionStatus.innerHTML = html;
    }
    
    function appendMessage(msg, prepend = false) {
        const isMe = msg.sender_id === currentUserId;
        const msgTime = new Date(msg.created_at).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});
        
        const wrapper = document.createElement('div');
        wrapper.className = `flex w-full ${isMe ? 'justify-end' : 'justify-start'}`;
        
        // Premium glassmorphic chat bubble
        const bubbleHTML = `
            <div class="flex flex-col max-w-[75%] sm:max-w-[60%] ${isMe ? 'items-end' : 'items-start'}">
                ${!isMe ? `<span class="text-xs text-gray-500 ml-1 mb-1">${msg.sender_name}</span>` : ''}
                <div class="px-4 py-2.5 rounded-2xl ${
                    isMe 
                    ? 'bg-emerald-600 text-white rounded-br-sm shadow-md' 
                    : 'bg-white text-gray-800 rounded-bl-sm shadow-sm border border-gray-100'
                } break-words whitespace-pre-wrap leading-relaxed">${msg.content}</div>
                <span class="text-[10px] text-gray-400 mt-1 ${isMe ? 'mr-1' : 'ml-1'}">${msgTime}</span>
            </div>
        `;
        
        wrapper.innerHTML = bubbleHTML;
        
        if (prepend) {
            chatMessages.insertBefore(wrapper, chatMessages.firstChild);
        } else {
            chatMessages.appendChild(wrapper);
            scrollToBottom();
        }
    }
    
    function scrollToBottom() {
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
    
    // Fetch History via API
    async function loadHistory() {
        if (!hasNextPage || isLoadingHistory) return;
        
        isLoadingHistory = true;
        document.getElementById('loading-history')?.classList.remove('hidden');
        
        try {
            const res = await fetch(`/chat/${roomId}?page=${page}`, {
                headers: { 'Accept': 'application/json' }
            });
            const data = await res.json();
            
            if (data.status === 'success') {
                // If it's the first page, we append normally
                const oldScrollHeight = chatMessages.scrollHeight;
                
                // Messages come chronologically reversed for the view (oldest first in the array)
                // Wait, if it's page 1, the most recent messages are returned.
                // We actually want to prepend them to the top if we are scrolling up.
                
                if (page === 1) {
                    data.messages.forEach(m => appendMessage(m, false));
                } else {
                    // Prepend to top
                    // Reverse the array so we prepend the oldest first
                    [...data.messages].reverse().forEach(m => appendMessage(m, true));
                    // Maintain scroll position
                    chatMessages.scrollTop = chatMessages.scrollHeight - oldScrollHeight;
                }
                
                hasNextPage = data.has_next;
                page++;
            }
        } catch (e) {
            console.error('Failed to load history', e);
        } finally {
            isLoadingHistory = false;
            document.getElementById('loading-history')?.classList.add('hidden');
        }
    }

    // Auto-expand textarea
    messageInput.addEventListener('input', function() {
        this.style.height = 'auto';
        this.style.height = (this.scrollHeight < 120 ? this.scrollHeight : 120) + 'px';
        
        // Emit typing event
        if (!isTyping) {
            isTyping = true;
            socket.emit('typing', { room_id: roomId, is_typing: true });
        }
        
        clearTimeout(typingTimeout);
        typingTimeout = setTimeout(() => {
            isTyping = false;
            socket.emit('typing', { room_id: roomId, is_typing: false });
        }, 1500);
    });
    
    // Enter to send
    messageInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            chatForm.dispatchEvent(new Event('submit'));
        }
    });

    // Handle Form Submit
    chatForm.addEventListener('submit', (e) => {
        e.preventDefault();
        const content = messageInput.value.trim();
        if (!content) return;
        
        socket.emit('send_message', {
            room_id: roomId,
            content: content
        });
        
        messageInput.value = '';
        messageInput.style.height = 'auto';
        
        // Stop typing immediately
        isTyping = false;
        clearTimeout(typingTimeout);
        socket.emit('typing', { room_id: roomId, is_typing: false });
    });

    // Infinite scroll for history
    chatMessages.addEventListener('scroll', () => {
        if (chatMessages.scrollTop <= 50) {
            loadHistory();
        }
    });

    // Socket Event Listeners
    socket.on('connect', () => {
        setConnectionStatus('connected');
        socket.emit('join', { room_id: roomId });
    });
    
    socket.on('disconnect', () => {
        setConnectionStatus('disconnected');
    });
    
    socket.on('receive_message', (data) => {
        appendMessage(data, false);
    });
    
    let activeTypers = new Set();
    socket.on('typing_status', (data) => {
        if (data.is_typing) {
            activeTypers.add(data.username);
        } else {
            activeTypers.delete(data.username);
        }
        
        if (typingIndicator) {
            if (activeTypers.size > 0) {
                const names = Array.from(activeTypers).join(', ');
                typingIndicator.textContent = `${names} ${activeTypers.size > 1 ? 'are' : 'is'} typing...`;
                typingIndicator.classList.remove('hidden');
            } else {
                typingIndicator.classList.add('hidden');
            }
        }
    });
    
    socket.on('error', (err) => {
        console.error('Socket error:', err);
    });

    // Initial Load
    setConnectionStatus('connecting');
    loadHistory();
});
