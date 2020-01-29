function setEditable(fields) {
    fields.forEach(field => field.removeAttribute('readonly'));
}

function setReadOnly(fields) {
    fields.forEach(field => field.readOnly = true);
}

document.addEventListener('DOMContentLoaded', function () {
    const editButton = document.getElementById('edit_button');
    const cancelButton = document.getElementById('cancel_button');
    const updateButtons = document.getElementById('update_buttons');
    const infoForm = document.getElementById('info_form');
    const formFields = editableFields.map(value => document.getElementById(value));

    editButton.addEventListener('click', function () {
        setEditable(formFields);
        updateButtons.classList.remove('is-hidden');
    });
});