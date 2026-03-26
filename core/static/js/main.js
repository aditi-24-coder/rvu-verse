/**
 * RVUverse - Main JavaScript File
 * Contains common functionality used across the platform
 */

document.addEventListener('DOMContentLoaded', function() {
    // Initialize Bootstrap tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Initialize Bootstrap popovers
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
    
    // Auto-dismiss alerts after 5 seconds
    setTimeout(function() {
        const alerts = document.querySelectorAll('.alert');
        alerts.forEach(function(alert) {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
    }, 5000);
    
    // Handle like/unlike button clicks
    setupLikeButtons();
    
    // Handle textarea auto-resize
    setupTextareaAutoResize();
    
    // Handle hashtag input formatting
    setupHashtagInput();
});

/**
 * Sets up like/unlike functionality for posts
 */
function setupLikeButtons() {
    document.querySelectorAll('.like-btn, .like-btn-active').forEach(button => {
        button.addEventListener('click', function() {
            const postId = this.getAttribute('data-post-id');
            const action = this.getAttribute('data-action');
            const likeCount = this.querySelector('.like-count');
            const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
            
            let url = '';
            if (action === 'like') {
                url = `/post/${postId}/like/`;
            } else {
                url = `/post/${postId}/unlike/`;
            }
            
            fetch(url, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrfToken,
                    'Content-Type': 'application/json'
                },
                credentials: 'same-origin'
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    // Update like count
                    if (likeCount) {
                        likeCount.textContent = data.likes_count;
                    }
                    
                    // Toggle button appearance
                    if (action === 'like') {
                        this.classList.remove('btn-outline-primary', 'like-btn');
                        this.classList.add('btn-primary', 'like-btn-active');
                        this.setAttribute('data-action', 'unlike');
                    } else {
                        this.classList.remove('btn-primary', 'like-btn-active');
                        this.classList.add('btn-outline-primary', 'like-btn');
                        this.setAttribute('data-action', 'like');
                    }
                }
            })
            .catch(error => console.error('Error:', error));
        });
    });
}

/**
 * Sets up auto-resizing for textareas when typing
 */
function setupTextareaAutoResize() {
    const textareas = document.querySelectorAll('textarea');
    textareas.forEach(textarea => {
        textarea.addEventListener('input', function() {
            this.style.height = 'auto';
            this.style.height = (this.scrollHeight) + 'px';
        });
        
        // Initial resize
        textarea.style.height = 'auto';
        textarea.style.height = (textarea.scrollHeight) + 'px';
    });
}

/**
 * Sets up hashtag input field with proper formatting and validation
 */
function setupHashtagInput() {
    const hashtagInputs = document.querySelectorAll('input[name="hashtags"]');
    
    hashtagInputs.forEach(input => {
        input.addEventListener('input', function() {
            // Remove any characters that aren't alphanumeric, comma, or space
            this.value = this.value.replace(/[^a-zA-Z0-9, ]/g, '');
            
            // Format hashtags by splitting, trimming, and rejoining
            const tags = this.value.split(',')
                .map(tag => tag.trim())
                .filter(tag => tag.length > 0)
                .join(', ');
                
            if (tags !== this.value) {
                this.value = tags;
            }
        });
    });
}

/**
 * Confirms an action with a modal dialog
 * @param {string} message - The confirmation message
 * @param {function} callback - The function to call if confirmed
 */
function confirmAction(message, callback) {
    if (confirm(message)) {
        callback();
    }
}

/**
 * Format timestamps to relative time (e.g., "5 minutes ago")
 * @param {string} dateString - ISO date string
 * @returns {string} Relative time string
 */
function timeAgo(dateString) {
    const date = new Date(dateString);
    const now = new Date();
    const seconds = Math.floor((now - date) / 1000);
    
    let interval = Math.floor(seconds / 31536000);
    if (interval >= 1) {
        return interval + " year" + (interval === 1 ? "" : "s") + " ago";
    }
    
    interval = Math.floor(seconds / 2592000);
    if (interval >= 1) {
        return interval + " month" + (interval === 1 ? "" : "s") + " ago";
    }
    
    interval = Math.floor(seconds / 86400);
    if (interval >= 1) {
        return interval + " day" + (interval === 1 ? "" : "s") + " ago";
    }
    
    interval = Math.floor(seconds / 3600);
    if (interval >= 1) {
        return interval + " hour" + (interval === 1 ? "" : "s") + " ago";
    }
    
    interval = Math.floor(seconds / 60);
    if (interval >= 1) {
        return interval + " minute" + (interval === 1 ? "" : "s") + " ago";
    }
    
    return "just now";
}

/**
 * Truncates text to a specified length and adds ellipsis
 * @param {string} text - The text to truncate
 * @param {number} length - Maximum length
 * @returns {string} Truncated text
 */
function truncateText(text, length = 100) {
    if (text.length <= length) return text;
    return text.substring(0, length) + '...';
}
