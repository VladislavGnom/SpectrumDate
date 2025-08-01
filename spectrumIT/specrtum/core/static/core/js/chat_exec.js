const path = window.location.pathname;
// const roomName = path.split('/')[2];
const roomName = path.split('/')[2];

let chatSocket = null;


// // Подключение к WebSocket
// const chatSocket = new WebSocket(
//     `ws://${window.location.host}/ws/chat/${roomName}/`
// );


function connectToChat(chatId) {
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
        connectToChat(chatId);
    })
})

document.querySelector('#chat-message-btn').onkeyup = function(e) {
    if (e.key === 'Enter') {
        const messageInput = document.querySelector('#chat-message-input');
        const message = messageInput.value;
        chatSocket.send(JSON.stringify({
            'message': message
        }));
        messageInput.value = '';
    }
};



// // Обработка входящих сообщений
// chatSocket.onmessage = function(e) {
    //     const data = JSON.parse(e.data);
    //     const message = `${data.sender}: ${data.message}`;
//     const messageElement = document.createElement('div');
//     messageElement.textContent = message;
//     document.querySelector('#chat-log').appendChild(messageElement);
// };

// // Отправка сообщений
// document.querySelector('#chat-message-btn').onkeyup = function(e) {
//     if (e.key === 'Enter') {
//         const messageInput = document.querySelector('#chat-message-input');
//         const message = messageInput.value;
//         chatSocket.send(JSON.stringify({
//             'message': message
//         }));
//         messageInput.value = '';
//     }
// };

// // Обработка закрытия соединения
// chatSocket.onclose = function(e) {
//     console.error('Chat socket closed unexpectedly');
// };
