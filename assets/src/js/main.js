function closeNotification(id) {
    document.getElementById(id).remove();
}

function refreshNotificationButtons() {
    const messages = Array.prototype.slice.call(document.getElementsByClassName('delete'));
    messages.forEach(m => m.addEventListener('click', function () {
        closeNotification(m.dataset.for);
    }));
}

document.addEventListener('DOMContentLoaded', function () {
    refreshNotificationButtons();
});