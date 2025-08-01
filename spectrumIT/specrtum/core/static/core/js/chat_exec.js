const path = window.location.pathname;
const roomName = path.split('/')[2];

let chatSocket = null;

function connectToChatByChatId(chatId) {
    if (chatSocket) {
        chatSocket.close();
    }

    chatSocket = new WebSocket(
        `ws://${window.location.host}/ws/chat/${chatId}/`
    );
    
    chatSocket.onmessage = function(e) {
        const data = JSON.parse(e.data);
        const message = `${data.sender}: ${data.message}`;
        const messageElement = document.createElement('div');
        messageElement.textContent = message;
        document.querySelector('#chat-log').appendChild(messageElement);
        console.log('Message received: ', data.message)
    }
    
    chatSocket.onclose = function(e) {
        console.error('Chat socket close unexpectedly');
    }
}

document.querySelectorAll('.chat-item').forEach(item => {
    item.addEventListener('click', function() {
        const chatId = this.dataset.chatId;
        prepareChatEnvironment();
        connectToChatByChatId(chatId);
    })
})

document.querySelector('#chat-message-input').onkeyup = function(e) {
    if (e.key === 'Enter') {
        processSendingMessage();
    }
};

document.querySelector('#chat-message-btn').onclick = function(e) {
    processSendingMessage();
};

function prepareChatEnvironment() {
    showChatWindow();
}

function showChatWindow() {
    const mainChatWindow = document.getElementById('main-chat-window');

    mainChatWindow.style.display = 'block';
}

function processSendingMessage() {
    const messageInput = document.querySelector('#chat-message-input');
    const message = messageInput.value;
    chatSocket.send(JSON.stringify({
        'message': message
    }));
    messageInput.value = '';
}
