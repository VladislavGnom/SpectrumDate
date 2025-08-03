import { getChatSocket, setChatSocket, getCurrentUsername } from './chat_start.js';

export function startChatByChatId(chatId) {
    prepareChatEnvironment(chatId);
    connectToChatByChatId(chatId);
}

function prepareChatEnvironment(chatId) {
    showChatWindow();
    showChatHeader(chatId);
}

function showChatWindow() {
    const mainChatWindow = document.getElementById('main-chat-window');

    mainChatWindow.style.display = 'block';
}

function showChatHeader(chatId) {
    alert(`${chatId}_id`)
    console.log(document.getElementById(`${chatId}_id`));
    const participantName = document.getElementById(`${chatId}_id`).dataset.participantName;
    const chatTitleElem = document.getElementById('chat-title')
    chatTitleElem.textContent = participantName;
}

function connectToChatByChatId(chatId) {
    let chatSocket = getChatSocket();
    closeChatSocketIfItOpened(chatSocket);

    let newChatSocket = createAndReturnWebSocketConnection(chatId);
    setChatSocket(newChatSocket);
    chatSocket = getChatSocket();
    
    processChatSocketActions(chatSocket);
}


function closeChatSocketIfItOpened(chatSocket) {
    if (chatSocket) {
        chatSocket.close();
    }
}

function createAndReturnWebSocketConnection(chatId) {
    return new WebSocket(
        `ws://${window.location.host}/ws/chat/${chatId}/`
    );
}

function processChatSocketActions(chatSocket) {
    chatSocket.onmessage = function(event) {
        runWebSocketOnMessageBehaviour(event);
    }
    
    chatSocket.onclose = function(event) {
        runWebSocketOnCloseBehaviour();
    }
}

function runWebSocketOnCloseBehaviour() {
    console.error('Chat socket close unexpectedly');
}

function runWebSocketOnMessageBehaviour(event) {
    const data = getParsedDataFromEvent(event);
    // const message = getCreatedMessage(data);
    
    addMessageToChat(data);
    showDebugInformation(data);
}

function getParsedDataFromEvent(event) {
    return JSON.parse(event.data);
}

function getCreatedMessage(metaData) {
    return `${metaData.sender}: ${metaData.message}`;
}

function addMessageToChat(metaData) {
    const isCurrentUser = checkIsCurrentUser(metaData);

    if (isMessageHistory(metaData)) {
        addMessageToHistory(metaData, isCurrentUser);
    } else {
        addNewMessage(metaData, isCurrentUser);
    }
}

function checkIsCurrentUser(metaData) {
    const currentUsername = getCurrentUsername();

    return metaData.sender === currentUsername;
}

function isMessageHistory(data) {
    return data.is_history;
}

function addMessageToHistory(data, isCurrentUser) {
    const messagesContainer = document.getElementById('chat-log');
    const messageClass = isCurrentUser ? 'message history outgoing' : 'message history incoming';

    messagesContainer.insertAdjacentHTML('afterbegin',
        `<div class="${messageClass}">
            ${!isCurrentUser ? `<img src="${data.avatar_url}" class="user-avatar"></img>` : ''}
            <div class="message-content">
                ${!isCurrentUser ? `<strong>${data.sender}</strong><br>` : ''}
                ${data.message}
                <span class="timestamp">${new Date(data.timestamp).toLocaleString()}</span>
            </div>
        </div>`
    )
}

function addNewMessage(data, isCurrentUser) {
    const messagesContainer = document.getElementById('chat-log');
    const messageClass = isCurrentUser ? 'message new outgoing' : 'message new incoming';

    messagesContainer.insertAdjacentHTML('beforeend',
        `<div class="${messageClass}">
            ${!isCurrentUser ? `<img src="${data.avatar_url}" class="user-avatar"></img>` : ''}
            <div class="message-content">
                ${!isCurrentUser ? `<strong>${data.sender}</strong><br>` : ''}
                ${data.message}
                <span class="timestamp">${new Date(data.timestamp).toLocaleString()}</span>
            </div>
        </div>`
    )

    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

function showDebugInformation(metaData) {
    console.log('Message received: ', metaData.message)
}

export function processSendingMessage(chatSocket) {
    const messageInput = document.querySelector('#chat-message-input');
    const message = messageInput.value;
    chatSocket.send(JSON.stringify({
        'message': message
    }));
    messageInput.value = '';
}
