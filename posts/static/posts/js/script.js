// Auto-dismiss Bootstrap alert messages after 4 seconds
document.addEventListener('DOMContentLoaded', function () {
    var alerts = document.querySelectorAll('.alert');
    alerts.forEach(function (alert) {
        setTimeout(function () {
            var bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
            bsAlert.close();
        }, 4000);
    });

    // Simple client-side check: block empty title submissions before hitting the server
    var postForm = document.querySelector('form[enctype="multipart/form-data"]');
    if (postForm) {
        postForm.addEventListener('submit', function (e) {
            var titleField = postForm.querySelector('#id_title');
            if (titleField && titleField.value.trim() === '') {
                e.preventDefault();
                alert('Please enter a title before submitting.');
                titleField.focus();
            }
        });
    }
});
