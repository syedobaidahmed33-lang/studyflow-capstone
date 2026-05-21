// Read a cookie value by name so fetch() can send Django's CSRF token safely.
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i += 1) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === `${name}=`) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Update the visible dashboard progress numbers after the API returns new values.
function updateProgress(data) {
    const completedCount = document.querySelector('#completed-count');
    const totalCount = document.querySelector('#total-count');
    const progressPercent = document.querySelector('#progress-percent');
    const progressFill = document.querySelector('#progress-fill');

    if (completedCount) completedCount.textContent = data.completed_count;
    if (totalCount) totalCount.textContent = data.total_count;
    if (progressPercent) progressPercent.textContent = `${data.progress_percent}%`;
    if (progressFill) progressFill.style.width = `${data.progress_percent}%`;
}

// Toggle a task's status without reloading the page when a user clicks its button.
function handleToggleClick(event) {
    const button = event.currentTarget;
    const url = button.dataset.url;
    const taskId = button.dataset.taskId;
    const taskCard = document.querySelector(`#task-${taskId}`);

    fetch(url, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
        .then(response => response.json())
        .then(data => {
            const statusText = taskCard.querySelector('.status-text');
            statusText.textContent = data.status;
            taskCard.classList.toggle('completed', data.status === 'Completed');
            button.textContent = data.status === 'Completed' ? 'Reopen' : 'Mark Complete';
            updateProgress(data);
        })
        .catch(error => console.log('Error toggling task:', error));
}

// Attach click listeners to every task toggle button after the DOM has loaded.
document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.toggle-task').forEach(button => {
        button.addEventListener('click', handleToggleClick);
    });
});
