import { startChatByChatId, processSendingMessage } from './chat_exec.js';

let chatSocket = null;

export const getChatSocket = () => chatSocket;
export const setChatSocket = newChatSocket => { chatSocket = newChatSocket };

export const currentUsername = document.getElementById('chat-container').dataset.username;

document.querySelectorAll('.chat-item').forEach(item => {
    item.addEventListener('click', function() {
        const chatId = this.dataset.chatId;

        startChatByChatId(chatId);
    })
})

document.querySelector('#chat-message-input').onkeyup = function(e) {
    if (e.key === 'Enter') {
        processSendingMessage(chatSocket);
    }
};

document.querySelector('#chat-message-btn').onclick = function(e) {
    processSendingMessage(chatSocket);
};
