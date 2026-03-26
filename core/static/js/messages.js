/**
 * RVUverse - Messages JavaScript File
 * Handles functionality specific to the messaging feature
 */

document.addEventListener('DOMContentLoaded', function() {
    // Scroll to bottom of messages container
    scrollToBottomOfMessages();
    
    // Submit form when pressing Enter in textarea
    setupMessageTextareaEnterKey();
    
    // Periodically check for new messages
    setupMessageRefresh();
});

/**
 * Scrolls the messages container to the bottom to show most recent messages
 */
function scrollToBottomOfMessages() {
    const messagesContainer = document.getElementById('messagesContainer');
    if (messagesContainer) {
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }
}

/**
 * Sets up the Enter key to submit the message form
 */
function setupMessageTextareaEnterKey() {
    const messageTextarea = document.querySelector('#messageForm textarea');
    if (messageTextarea) {
        messageTextarea.addEventListener('keydown', function(event) {
            if (event.key === 'Enter' && !event.shiftKey) {
                event.preventDefault();
                document.getElementById('messageForm').submit();
            }
        });
    }
}

/**
 * Sets up periodic refresh of messages to check for new ones
 */
function setupMessageRefresh() {
    // Only set up refresh if we're on a conversation page with a selected user
    const selectedUser = new URLSearchParams(window.location.search).get('user');
    if (!selectedUser) return;
    
    // Check for new messages every 15 seconds
    setInterval(function() {
        checkForNewMessages(selectedUser);
    }, 15000);
}

/**
 * Checks for new messages from the server
 * @param {string} userId - The ID of the user we're chatting with
 */
function checkForNewMessages(userId) {
    const messagesContainer = document.getElementById('messagesContainer');
    if (!messagesContainer) return;
    
    // Get the timestamp of the last message to avoid duplicates
    const lastMessageTime = getLastMessageTimestamp();
    
    // Get CSRF token for the request
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    
    // We're not actually implementing the AJAX endpoint, but this is how it would work
    // In a real implementation, the server would return only new messages since lastMessageTime
    /*
    fetch(`/api/messages/check/?user=${userId}&since=${lastMessageTime}`, {
        method: 'GET',
        headers: {
            'X-CSRFToken': csrfToken,
            'Content-Type': 'application/json'
        },
        credentials: 'same-origin'
    })
    .then(response => response.json())
    .then(data => {
        if (data.new_messages && data.new_messages.length > 0) {
            // Append new messages and scroll down
            appendNewMessages(data.new_messages);
            scrollToBottomOfMessages();
            
            // Update unread count in the navbar if needed
            updateUnreadCount(data.unread_count);
        }
    })
    .catch(error => console.error('Error checking for new messages:', error));
    */
    
    // Since we don't have a real-time endpoint, we'll just refresh the page
    // if this was a production app, we'd use WebSockets or polling
}

/**
 * Gets the timestamp of the last message in the container
 * @returns {string} ISO datetime string or empty if no messages
 */
function getLastMessageTimestamp() {
    const messagesContainer = document.getElementById('messagesContainer');
    if (!messagesContainer) return '';
    
    const messages = messagesContainer.querySelectorAll('.message');
    if (messages.length === 0) return '';
    
    const lastMessage = messages[messages.length - 1];
    const timestampElem = lastMessage.querySelector('small');
    
    // This is a simplified version - in a real app we'd store ISO timestamps in data attributes
    return timestampElem ? timestampElem.textContent.trim() : '';
}

/**
 * Appends new messages to the messages container
 * @param {Array} messages - Array of message objects from the API
 */
function appendNewMessages(messages) {
    const messagesContainer = document.getElementById('messagesContainer');
    if (!messagesContainer) return;
    
    messages.forEach(message => {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message mb-3 ${message.is_from_current_user ? 'sent' : 'received'}`;
        
        const contentDiv = document.createElement('div');
        contentDiv.className = `message-content p-3 rounded ${
            message.is_from_current_user ? 'bg-primary text-white ms-auto' : 'bg-light'
        }`;
        contentDiv.style.maxWidth = '80%';
        contentDiv.style.width = 'fit-content';
        
        const textDiv = document.createElement('div');
        textDiv.textContent = message.content;
        
        const timeDiv = document.createElement('div');
        const timeSmall = document.createElement('small');
        timeSmall.className = message.is_from_current_user ? 'text-light' : 'text-muted';
        timeSmall.textContent = new Date(message.created_at).toLocaleString('en-US', {
            month: 'short',
            day: 'numeric',
            hour: 'numeric',
            minute: '2-digit'
        });
        
        if (message.is_from_current_user && message.is_read) {
            const readIcon = document.createElement('i');
            readIcon.className = 'fa-solid fa-check ms-1';
            readIcon.title = 'Read';
            timeSmall.appendChild(readIcon);
        }
        
        timeDiv.appendChild(timeSmall);
        contentDiv.appendChild(textDiv);
        contentDiv.appendChild(timeDiv);
        messageDiv.appendChild(contentDiv);
        
        messagesContainer.appendChild(messageDiv);
    });
}

/**
 * Updates the unread messages count in the navbar
 * @param {number} count - The new unread count
 */
function updateUnreadCount(count) {
    const unreadBadge = document.querySelector('.nav-item .position-relative[href*="/messages/"] .badge');
    if (unreadBadge) {
        unreadBadge.textContent = count;
        unreadBadge.style.display = count > 0 ? 'block' : 'none';
    }
}
