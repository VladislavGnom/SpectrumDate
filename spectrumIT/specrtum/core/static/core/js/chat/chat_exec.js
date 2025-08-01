import { getChatSocket, setChatSocket } from './chat_start.js';

export function startChatByChatId(chatId) {
    prepareChatEnvironment();
    connectToChatByChatId(chatId);
}

function prepareChatEnvironment() {
    showChatWindow();
}

function showChatWindow() {
    const mainChatWindow = document.getElementById('main-chat-window');

    mainChatWindow.style.display = 'block';
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
    const message = getCreatedMessage(data);
    
    addMessageAsDOMElement(message);
    showDebugInformation(data);
}

function getParsedDataFromEvent(event) {
    return JSON.parse(event.data);
}

function getCreatedMessage(metaData) {
    return `${metaData.sender}: ${metaData.message}`;
}

function addMessageAsDOMElement(message) {
    const messageElement = document.createElement('div');
    messageElement.textContent = message;
    
    document.querySelector('#chat-log').appendChild(messageElement);
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
