/**
 * RVUverse - Notifications JavaScript File
 * Handles functionality specific to the notifications feature
 */

document.addEventListener('DOMContentLoaded', function() {
    // Mark notifications as read when clicked
    setupNotificationReadMarking();
    
    // Set up polling for new notifications
    setupNotificationPolling();
});

/**
 * Sets up click handlers to mark notifications as read
 */
function setupNotificationReadMarking() {
    const notificationItems = document.querySelectorAll('.list-group-item:not(.text-center)');
    
    notificationItems.forEach(item => {
        // If the notification is unread, add a click handler to mark it as read
        if (item.classList.contains('list-group-item-primary')) {
            const markReadBtn = item.querySelector('a[href*="mark_read"]');
            
            if (markReadBtn) {
                markReadBtn.addEventListener('click', function(e) {
                    // Remove the highlight immediately for better UX
                    item.classList.remove('list-group-item-primary');
                });
            }
        }
    });
    
    // Handle the "Mark All Read" button
    const markAllReadBtn = document.querySelector('a[href*="mark_all_read"]');
    if (markAllReadBtn) {
        markAllReadBtn.addEventListener('click', function(e) {
            // Remove all highlights immediately for better UX
            document.querySelectorAll('.list-group-item-primary').forEach(item => {
                item.classList.remove('list-group-item-primary');
            });
        });
    }
}

/**
 * Sets up periodic polling for new notifications
 */
function setupNotificationPolling() {
    // Check for new notifications every 30 seconds
    setInterval(checkForNewNotifications, 30000);
}

/**
 * Checks for new notifications from the server
 */
function checkForNewNotifications() {
    // Get CSRF token for the request
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    
    // We're not actually implementing the AJAX endpoint, but this is how it would work
    // In a real implementation, the server would return only new notifications
    /*
    fetch('/api/notifications/check/', {
        method: 'GET',
        headers: {
            'X-CSRFToken': csrfToken,
            'Content-Type': 'application/json'
        },
        credentials: 'same-origin'
    })
    .then(response => response.json())
    .then(data => {
        if (data.new_notifications) {
            // Update the notification count in the navbar
            updateNotificationCount(data.unread_count);
            
            // If we're on the notifications page, append the new ones
            if (window.location.pathname.includes('/notifications/')) {
                prependNewNotifications(data.new_notifications);
            }
        }
    })
    .catch(error => console.error('Error checking for new notifications:', error));
    */
    
    // Since we don't have a real-time endpoint, we'll just update the count
    // if this was a production app, we'd use WebSockets or polling
    updateNotificationCountFromDOM();
}

/**
 * Updates the notification count in the navbar
 * @param {number} count - The new unread count
 */
function updateNotificationCount(count) {
    const notificationBadge = document.querySelector('.nav-item .position-relative[href*="/notifications/"] .badge');
    if (notificationBadge) {
        notificationBadge.textContent = count;
        notificationBadge.style.display = count > 0 ? 'block' : 'none';
    }
}

/**
 * Updates the notification count based on the current DOM
 * This is a temporary solution until we have a real API
 */
function updateNotificationCountFromDOM() {
    if (window.location.pathname.includes('/notifications/')) {
        const unreadCount = document.querySelectorAll('.list-group-item-primary').length;
        updateNotificationCount(unreadCount);
    }
}

/**
 * Prepends new notifications to the notifications list
 * @param {Array} notifications - Array of notification objects from the API
 */
function prependNewNotifications(notifications) {
    const notificationsList = document.querySelector('.list-group');
    if (!notificationsList) return;
    
    notifications.forEach(notification => {
        // Create notification element
        const notificationItem = document.createElement('div');
        notificationItem.className = 'list-group-item list-group-item-primary fade-in';
        
        // Create notification content - this would be replaced with proper HTML templating
        notificationItem.innerHTML = `
            <div class="d-flex justify-content-between align-items-center">
                <div class="d-flex align-items-center">
                    <div class="avatar-placeholder me-3">
                        ${notification.from_user ? notification.from_user.username[0].toUpperCase() : '<i class="fa-solid fa-bell"></i>'}
                    </div>
                    <div>
                        <div class="notification-text mb-1">
                            ${notification.text}
                        </div>
                        <small class="text-muted">
                            just now
                        </small>
                    </div>
                </div>
                
                <div class="d-flex">
                    <a href="?mark_read=${notification.id}" class="btn btn-sm btn-outline-primary me-2">
                        <i class="fa-solid fa-check"></i>
                    </a>
                    
                    ${getNotificationActionButton(notification)}
                </div>
            </div>
        `;
        
        // Add the notification to the top of the list
        notificationsList.prepend(notificationItem);
    });
}

/**
 * Gets the appropriate action button for a notification type
 * @param {Object} notification - The notification object
 * @returns {string} HTML for the action button
 */
function getNotificationActionButton(notification) {
    switch(notification.notification_type) {
        case 'like':
        case 'comment':
            return `
                <a href="/post/${notification.post.id}/" class="btn btn-sm btn-outline-info">
                    <i class="fa-solid fa-external-link-alt"></i>
                </a>
            `;
        case 'follow':
            return `
                <a href="/profile/${notification.from_user.username}/" class="btn btn-sm btn-outline-info">
                    <i class="fa-solid fa-external-link-alt"></i>
                </a>
            `;
        case 'message':
            return `
                <a href="/messages/?user=${notification.from_user.id}" class="btn btn-sm btn-outline-info">
                    <i class="fa-solid fa-external-link-alt"></i>
                </a>
            `;
        default:
            return '';
    }
}
