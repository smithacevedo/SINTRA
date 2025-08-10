function setupAutoNotifications() {
    if (typeof md !== 'undefined') {
        md.showNotification = function(from, align, message, messageType) {
            if (arguments.length === 2) {
                var type = ['', 'info', 'danger', 'success', 'warning', 'rose', 'primary'];
                var color = Math.floor((Math.random() * 6) + 1);
                $.notify({
                    icon: "add_alert",
                    message: "Welcome to <b>Material Dashboard Pro</b> - a beautiful admin panel for every web developer."
                }, {
                    type: type[color],
                    timer: 3000,
                    placement: { from, align }
                });
            } else {
                var typeMap = {
                    success: 'success',
                    error: 'danger',
                    warning: 'warning',
                    info: 'info',
                    debug: 'info'
                };
                var notifyType = typeMap[messageType] || 'info';
                $.notify({
                    icon: "add_alert",
                    message: message
                }, {
                    type: notifyType,
                    timer: 4000,
                    placement: { from, align }
                });
            }
        };
    }
}

function showDjangoMessagesAsNotifications() {
    $('.alert').each(function() {
        var $alert = $(this);
        var message = $alert.text().trim();
        var alertClasses = $alert.attr('class');
        var messageType = 'info';
        if (alertClasses.includes('alert-success')) {
            messageType = 'success';
        } else if (alertClasses.includes('alert-danger') || alertClasses.includes('alert-error')) {
            messageType = 'error';
        } else if (alertClasses.includes('alert-warning')) {
            messageType = 'warning';
        }
        if (message) {
            md.showNotification('top', 'right', message, messageType);
        }
        $alert.hide();
    });
}

// Inicializar cuando el documento esté listo
$(document).ready(function() {
    setupAutoNotifications();
    
    // Mostrar Django messages como notificaciones automáticamente
    setTimeout(function() {
        showDjangoMessagesAsNotifications();
    }, 500);
});
