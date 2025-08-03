import { startChatByChatId, processSendingMessage } from './chat_exec.js';

let chatSocket = null;
const currentUsername = document.getElementById('chat-container').dataset.username;

export const getChatSocket = () => chatSocket;
export const setChatSocket = newChatSocket => { chatSocket = newChatSocket };

export const getCurrentUsername = () => currentUsername;


document.querySelectorAll('.chat-item').forEach(item => {
    item.addEventListener('click', function() {
        const chatId = this.dataset.chatId;
        
        startChatByChatId(chatId);
    })
})

function preSendingValidation() {
    const message = document.querySelector('#chat-message-input');

    if (!message.value) {
        alert('Сообщение не может быть пустым');
        return false;
    }
    return true;
}

document.querySelector('#chat-message-input').onkeyup = function(e) {
    if (e.key === 'Enter') {
        const statusValidation = preSendingValidation();

        if (statusValidation) {
            processSendingMessage(chatSocket);
        }
    }
};

document.querySelector('#chat-message-btn').onclick = function(e) {
    const statusValidation = preSendingValidation();

    if (statusValidation) {
        processSendingMessage(chatSocket);
    }
};
