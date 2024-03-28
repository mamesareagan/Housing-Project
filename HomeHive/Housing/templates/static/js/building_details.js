const deleteBuildingButton = document.getElementById('delete-building-button');
const confirmationDialog = document.getElementById('confirmation-dialog');

// Show confirmation dialog when delete building button is clicked
deleteBuildingButton.addEventListener('click', function() {
    confirmationDialog.style.display = 'block';
});

// Get the confirm and cancel buttons from the confirmation dialog
const confirmDeleteButton = document.getElementById('confirm-delete-button');
const cancelDeleteButton = document.getElementById('cancel-delete-button');

// Hide confirmation dialog when cancel button is clicked
cancelDeleteButton.addEventListener('click', function() {
    confirmationDialog.style.display = 'none';
});