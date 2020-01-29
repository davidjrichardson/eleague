function closeMessage(id) {
    document.getElementById(id).remove();
}

document.addEventListener('DOMContentLoaded', function () {
    const messages = Array.prototype.slice.call(document.getElementsByClassName('delete'));
    messages.forEach(m => m.addEventListener('click', function () {
        closeMessage(m.dataset.for);
    }));
});