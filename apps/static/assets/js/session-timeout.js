// Auto logout after 30 minutes of inactivity
(function() {
    let timeout;
    const TIMEOUT_DURATION = 30 * 60 * 1000; // 30 minutes in milliseconds
    
    function resetTimer() {
        clearTimeout(timeout);
        timeout = setTimeout(logout, TIMEOUT_DURATION);
    }
    
    function logout() {
        window.location.href = '/logout/';
    }
    
    // Events that reset the timer
    const events = ['mousedown', 'mousemove', 'keypress', 'scroll', 'touchstart', 'click'];
    
    events.forEach(event => {
        document.addEventListener(event, resetTimer, true);
    });
    
    // Initialize timer
    resetTimer();
})();