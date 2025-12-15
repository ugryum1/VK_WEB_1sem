// Функция для получения CSRF токена
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

document.addEventListener('DOMContentLoaded', function() {
    // Обработчик для лайков/дизлайков
    document.querySelectorAll('.vote-up, .vote-down').forEach(button => {
        button.addEventListener('click', function() {
            const voteId = this.getAttribute('data-id');
            const voteType = this.getAttribute('data-type');
            const isUpButton = this.classList.contains('vote-up');
            const isDownButton = this.classList.contains('vote-down');
            const ratingElement = this.parentElement.querySelector('.rating');
            const upButton = this.parentElement.querySelector('.vote-up');
            const downButton = this.parentElement.querySelector('.vote-down');

            // Определяем текущее действие
            let action;
            if (isUpButton) {
                action = upButton.classList.contains('active') ? 'remove' : 'like';
            } else if (isDownButton) {
                action = downButton.classList.contains('active') ? 'remove' : 'dislike';
            }

            // Отправляем AJAX запрос
            const url = voteType === 'question'
            ? `/question/${voteId}/like/`
            : `/answer/${voteId}/like/`;

            fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: `action=${action}`
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Обновляем рейтинг
                    ratingElement.textContent = data.new_rating;

                    // Обновляем состояние кнопок
                    if (data.user_vote === 1) {
                        upButton.classList.add('active');
                        downButton.classList.remove('active');
                    } else if (data.user_vote === -1) {
                        upButton.classList.remove('active');
                        downButton.classList.add('active');
                    } else {
                        upButton.classList.remove('active');
                        downButton.classList.remove('active');
                    }
                } else {
                    if (data.error === 'Authentication required') {
                        // Перенаправляем на страницу логина
                        const nextUrl = encodeURIComponent(window.location.pathname);
                        window.location.href = `/core/login/?next=${nextUrl}`;
                    } else {
                        alert('Ошибка: ' + data.error);
                    }
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Произошла ошибка при голосовании');
            });
        });
    });
});

// Обработчик для кнопки "Ответ подходит"
document.querySelectorAll('.accept-btn').forEach(button => {
    button.addEventListener('click', async function() {
        const answerId = this.getAttribute('data-answer-id');
        const isCurrentlyAccepted = this.getAttribute('data-accepted') === 'true';

        try {
            const response = await fetch(`/answer/${answerId}/accept/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'X-CSRFToken': getCookie('csrftoken')
                }
            });

            const data = await response.json();

            if (data.success) {
                const answerElement = this.closest('.question.answer');

                if (!answerElement) {
                    console.error('Не найден элемент ответа');
                    return;
                }

                const badge = answerElement.querySelector('.accepted-badge');
                const button = answerElement.querySelector('.accept-btn');

                if (data.is_accepted) {
                    answerElement.classList.add('accepted-answer');
                    if (!badge) {
                        const badgeDiv = document.createElement('div');
                        badgeDiv.className = 'accepted-badge';
                        badgeDiv.textContent = '✓ Правильный ответ';
                        answerElement.querySelector('.question-text').appendChild(badgeDiv);
                    }
                    button.textContent = 'Отменить принятие';
                    button.setAttribute('data-accepted', 'true');
                } else {
                    answerElement.classList.remove('accepted-answer');
                    if (badge) badge.remove();
                    button.textContent = 'Ответ подходит';
                    button.removeAttribute('data-accepted');
                }

            } else {
                alert('Ошибка: ' + data.error);
            }

        } catch (error) {
            console.error('Error:', error);
            alert('Произошла ошибка');
        }
    });
});
