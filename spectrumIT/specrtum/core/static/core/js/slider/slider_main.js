let currentPage = 1;
const dataContainer = document.getElementById('data-container');
const actionBlock = document.getElementById('action-buttons');
const likeButton = document.getElementById('like-btn');                    
const dislikeButton = document.getElementById('dislike-btn');   
const targetUserIdElement = document.getElementById('targetUserId');
const nextPageElement = document.getElementById('nextPage');


function loadUserCardByPageNumber(pageNumber) {
    fetch(`load-another-user?page=${pageNumber}`)
    .then(response => {
        if (!response.ok) throw new Error('404 Not Found');

        return response.json()
    })
    .then(userResponse => {
        loadMetaHelpDataUsingUserResponse(userResponse);

        appendUserCardOnPageUsingUserResponse(userResponse); 

    })
    .catch(error => {
        loadFinishSwipeScreen();
    })
}

function sendNotification(targetUserId) {
    const curUserId = "{{ user.pk }}";
    const formLink = `${location.origin}/slider/${curUserId}`;
    const message =`Вы понравились одному из пользоватлей нашего веб-приложения SpectrumDate. <a href="${formLink}">Анкета</a>`;
    fetch(`send-message/${targetUserId}?message=${message}`)
    .then(response => response.json())
    .then(data => {
        if (data.status == 200) {
                // some code
            }
        })
    }

function loadFinishSwipeScreen() {
    const userElement = document.createElement('div');
    userElement.innerHTML = `Анкеты закончились`;
    dataContainer.insertBefore(userElement, actionBlock);
    
    try {
        const prevUser = userElement.previousElementSibling;
        prevUser.remove(); 
    } catch (TypeError) {
        
    }

    actionBlock.style.display = 'none';
}

function loadMetaHelpDataUsingUserResponse(userResponse) {
    const targetUserId = userResponse.user.id;
    const nextPage = userResponse.next_page; 

    targetUserIdElement.textContent = targetUserId;
    nextPageElement.textContent = nextPage;
}

function printBeautifulGender(rawGender) {
    let beautifulGender;

    switch (rawGender) {
        case 'male':
            beautifulGender = 'Мужчина';
            break;
        case 'female':
            beautifulGender = 'Женщина';
            break;
        default:
            beautifulGender = 'Не определён';
    }

    return beautifulGender;
}

function getUserOnlineStatus(userResponse) {
    if (userResponse.user.status.is_online) {
        return "Online";
    } else {
        return `Last seen: ${ userResponse.user.status.last_seen }`;
    }
}

function insertUserCardBeforeActionBlockAndReturnIt(userResponse) {
    const userCardElement = document.createElement('div');

    userCardElement.innerHTML = `
        <div class="user-card">
            <div class="card-header">
                <img src="${window.location.origin}/media/${userResponse.user.avatar}" alt="Фото профиля" class="card-avatar">
                <div class="card-verified">✓</div>
            </div>
            
            <div class="card-body">
                <h1 class="user-name">${userResponse.user.first_name}<br><span class="user-age">${userResponse.user.age} лет</span></h1>
                <p class="user-status">${ getUserOnlineStatus(userResponse) }</p>
                
                <div class="user-info">
                    <div class="info-item">
                        <div class="info-icon">📍</div>
                        <div class="info-text">${userResponse.user.location}</div>
                    </div>
                    <div class="info-item">
                        <div class="info-icon">💼</div>
                        <div class="info-text">${printBeautifulGender(userResponse.user.gender)}</div>
                    </div>
                    <div class="info-item">
                        <div class="info-icon">🎓</div>
                        <div class="info-text">${userResponse.user.birthdate}</div>
                    </div>
                </div>
                
                <div class="user-bio">
                    ${ userResponse.user.bio ? userResponse.user.bio : 'Описание не задано' }
                </div>
            </div>
        </div>
    `
    dataContainer.insertBefore(userCardElement, actionBlock);

    return userCardElement
}

function appendUserCardOnPageUsingUserResponse(userResponse) {
    const userCardElement = insertUserCardBeforeActionBlockAndReturnIt(userResponse);
    
    deleteUserCardAboveNewOneIfExist(userCardElement);

    showActionBlock();          
}

function deleteUserCardAboveNewOneIfExist(newUserCardElement) {
    try {
        const prevUser = newUserCardElement.previousElementSibling;
        prevUser.remove(); 
    } catch (TypeError) {
        
    }
}

function showActionBlock() {
    actionBlock.style.display = 'block';
}

function updatePageNumberCounterBasedOnUserResponse(userResponse) {
    if (userResponse.has_next) {
        currentPage = nextPage;
        dataContainer.style.display = 'block';
    }
}

function recordSwap(swipedOnUserId, liked=true) {
    fetch(`record-swipe?swiped_on=${swipedOnUserId}&liked=${liked}`)
        .then(response => response.json())
        .then(data => {
            if (data.status == 200) {
                // some code
            }
        })
    }

function getTargetUserId() {
    return targetUserIdElement.textContent;
}

function updateCurrentPageNumberToNextOne() {
    const nextPage = getNextPage();

    updateCurrentPageNumber(nextPage);
}

function getNextPage() {
    return nextPageElement.textContent;
}

function updateCurrentPageNumber(newPageNumber) {
    currentPage = newPageNumber;
}

likeButton.addEventListener('click', event => {
    const targetUserId = getTargetUserId();
    
    sendNotification(targetUserId);

    recordSwap(targetUserId, 'True')
    setTimeout(                     // delay for server API processing
        loadUserCardByPageNumber,
        100,
        currentPage
    );
});
dislikeButton.addEventListener('click', event => {
    const targetUserId = getTargetUserId();
    sendNotification(targetUserId);

    recordSwap(targetUserId, 'False')
    setTimeout(
        loadUserCardByPageNumber,
        100,
        currentPage
    );
});

document.addEventListener('DOMContentLoaded', event => {
    loadUserCardByPageNumber(currentPage);
});
