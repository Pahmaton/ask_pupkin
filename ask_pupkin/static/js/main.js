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
const csrftoken = getCookie('csrftoken');

$('.js-vote').on('click', function(e) {
    e.preventDefault();
    const $btn = $(this);
    const $container = $btn.closest('.vote-box');
    
    $.ajax({
        url: '/vote/',
        method: 'POST',
        headers: {'X-CSRFToken': csrftoken},
        data: {
            'id': $container.data('id'),
            'type': $container.data('type'),
            'action': $btn.data('action')
        },
        success: function(response) {
            $container.find('.vote-count').text(response.new_rating);
        },
        error: function(xhr) {
            if (xhr.status === 403) alert("Нужно авторизоваться!");
            else alert("Ошибка при голосовании");
        }
    });
});

$('.js-correct-answer').on('change', function() {
    const $checkbox = $(this);
    const qId = $checkbox.data('question-id');
    const aId = $checkbox.data('answer-id');

    $.ajax({
        url: '/mark_correct/',
        method: 'POST',
        headers: {'X-CSRFToken': csrftoken},
        data: {
            'question_id': qId,
            'answer_id': aId
        },
        success: function(response) {
            $('.js-correct-answer').not($checkbox).prop('checked', false);
        },
        error: function() {
            $checkbox.prop('checked', !$checkbox.prop('checked'));
            alert("Ошибка доступа");
        }
    });
});

let debounceTimer;
const searchInput = document.querySelector('input[type="search"]');
const resultsContainer = document.createElement('div');
resultsContainer.className = 'list-group position-absolute w-100';
searchInput.parentElement.appendChild(resultsContainer);

searchInput.addEventListener('input', function() {
    clearTimeout(debounceTimer);
    const query = this.value;

    if (query.length < 3) {
        resultsContainer.innerHTML = '';
        return;
    }

    debounceTimer = setTimeout(() => {
        fetch(`/search-suggestions/?q=${query}`)
            .then(response => response.json())
            .then(data => {
                resultsContainer.innerHTML = '';
                data.suggestions.forEach(item => {
                    const link = document.createElement('a');
                    link.href = `/question/${item.id}`;
                    link.className = 'list-group-item list-group-item-action';
                    link.innerText = item.title;
                    resultsContainer.appendChild(link);
                });
            });
    }, 300);
});