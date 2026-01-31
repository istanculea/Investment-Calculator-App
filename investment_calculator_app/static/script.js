// Form Validation and Interactivity
document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('investmentForm');
    
    if (form) {
        // Real-time validation
        const inputs = form.querySelectorAll('input[required]');
        
        inputs.forEach(input => {
            input.addEventListener('blur', function() {
                validateField(this);
            });
            
            input.addEventListener('input', function() {
                // Clear error on input
                const errorElement = document.getElementById(`error-${this.id}`);
                if (errorElement) {
                    errorElement.classList.remove('show');
                }
            });
        });
        
        // Form submission validation
        form.addEventListener('submit', function(e) {
            let isValid = true;
            
            inputs.forEach(input => {
                if (!validateField(input)) {
                    isValid = false;
                }
            });
            
            if (!isValid) {
                e.preventDefault();
                showNotification('Please fix the errors before submitting', 'error');
            }
        });
    }
    
    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
    
    // Print button functionality
    const printButton = document.getElementById('printButton');
    if (printButton) {
        printButton.addEventListener('click', function() {
            window.print();
        });
    }
    
    // Add animation to cards on scroll
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);
    
    // Observe cards and feature cards
    document.querySelectorAll('.card, .feature-card, .result-card').forEach(card => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        card.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
        observer.observe(card);
    });
});

// Field validation function
function validateField(field) {
    const errorElement = document.getElementById(`error-${field.id}`);
    let isValid = true;
    let errorMessage = '';
    
    if (!errorElement) return true;
    
    // Check if field is empty
    if (field.hasAttribute('required') && !field.value.trim()) {
        isValid = false;
        errorMessage = 'This field is required';
    }
    // Validate numeric fields
    else if (field.type === 'number') {
        const value = parseFloat(field.value);
        const minAttr = field.getAttribute('min');
        const maxAttr = field.getAttribute('max');
        const min = minAttr !== null ? parseFloat(minAttr) : null;
        const max = maxAttr !== null ? parseFloat(maxAttr) : null;
        
        if (isNaN(value)) {
            isValid = false;
            errorMessage = 'Please enter a valid number';
        } else if (min !== null && !isNaN(min) && value < min) {
            isValid = false;
            errorMessage = `Value must be at least ${min}`;
        } else if (max !== null && !isNaN(max) && value > max) {
            isValid = false;
            errorMessage = `Value must be at most ${max}`;
        }
    }
    
    // Show or hide error
    if (!isValid) {
        errorElement.textContent = errorMessage;
        errorElement.classList.add('show');
        field.style.borderColor = '#ef4444';
    } else {
        errorElement.classList.remove('show');
        field.style.borderColor = '#10b981';
    }
    
    return isValid;
}

// Show notification (simple toast notification)
function showNotification(message, type = 'info') {
    // Remove existing notifications
    const existing = document.querySelector('.toast-notification');
    if (existing) {
        existing.remove();
    }
    
    const toast = document.createElement('div');
    toast.className = `toast-notification toast-${type}`;
    toast.innerHTML = `
        <i class="fas fa-${type === 'error' ? 'exclamation-circle' : 'info-circle'}"></i>
        <span>${message}</span>
    `;
    
    // Add styles
    toast.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: ${type === 'error' ? '#fee2e2' : '#dbeafe'};
        color: ${type === 'error' ? '#991b1b' : '#1e40af'};
        padding: 1rem 1.5rem;
        border-radius: 10px;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
        display: flex;
        align-items: center;
        gap: 0.75rem;
        z-index: 10000;
        animation: slideInRight 0.3s ease;
    `;
    
    document.body.appendChild(toast);
    
    // Auto remove after 4 seconds
    setTimeout(() => {
        toast.style.animation = 'slideOutRight 0.3s ease';
        setTimeout(() => toast.remove(), 300);
    }, 4000);
}

// Add CSS for toast animations
const style = document.createElement('style');
style.textContent = `
    @keyframes slideInRight {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOutRight {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);
