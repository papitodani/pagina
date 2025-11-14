/**
 * Main JavaScript file for Payroll Management System
 */

// Global configuration
const API_BASE_URL = '/api';

// Utility Functions
const Utils = {
    /**
     * Format number as currency
     */
    formatCurrency(amount) {
        return new Intl.NumberFormat('es-MX', {
            style: 'currency',
            currency: 'MXN'
        }).format(amount || 0);
    },

    /**
     * Format date
     */
    formatDate(dateString) {
        const date = new Date(dateString);
        return date.toLocaleDateString('es-MX', {
            year: 'numeric',
            month: 'long',
            day: 'numeric'
        });
    },

    /**
     * Format short date
     */
    formatShortDate(dateString) {
        const date = new Date(dateString);
        return date.toLocaleDateString('es-MX', {
            year: 'numeric',
            month: 'short',
            day: 'numeric'
        });
    },

    /**
     * Show loading state
     */
    showLoading(elementId) {
        const element = document.getElementById(elementId);
        if (element) {
            element.innerHTML = `
                <div class="text-center py-4">
                    <div class="spinner-border text-primary" role="status">
                        <span class="visually-hidden">Cargando...</span>
                    </div>
                </div>
            `;
        }
    },

    /**
     * Show error message
     */
    showError(elementId, message) {
        const element = document.getElementById(elementId);
        if (element) {
            element.innerHTML = `
                <div class="alert alert-danger" role="alert">
                    <i class="bi bi-exclamation-triangle-fill"></i> ${message}
                </div>
            `;
        }
    },

    /**
     * Show success message
     */
    showSuccess(elementId, message) {
        const element = document.getElementById(elementId);
        if (element) {
            element.innerHTML = `
                <div class="alert alert-success" role="alert">
                    <i class="bi bi-check-circle-fill"></i> ${message}
                </div>
            `;
        }
    },

    /**
     * Show empty state
     */
    showEmpty(elementId, message) {
        const element = document.getElementById(elementId);
        if (element) {
            element.innerHTML = `
                <div class="text-center text-muted py-4">
                    <i class="bi bi-inbox fs-1"></i>
                    <p class="mt-3">${message}</p>
                </div>
            `;
        }
    },

    /**
     * Confirm action
     */
    confirm(message) {
        return window.confirm(message);
    },

    /**
     * Alert message
     */
    alert(message) {
        window.alert(message);
    }
};

// API Service
const API = {
    /**
     * Generic GET request
     */
    async get(endpoint) {
        try {
            const response = await fetch(`${API_BASE_URL}${endpoint}`);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return await response.json();
        } catch (error) {
            console.error('API GET Error:', error);
            throw error;
        }
    },

    /**
     * Generic POST request
     */
    async post(endpoint, data) {
        try {
            const response = await fetch(`${API_BASE_URL}${endpoint}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            });
            
            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || `HTTP error! status: ${response.status}`);
            }
            
            return await response.json();
        } catch (error) {
            console.error('API POST Error:', error);
            throw error;
        }
    },

    /**
     * Generic PUT request
     */
    async put(endpoint, data) {
        try {
            const response = await fetch(`${API_BASE_URL}${endpoint}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            });
            
            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || `HTTP error! status: ${response.status}`);
            }
            
            return await response.json();
        } catch (error) {
            console.error('API PUT Error:', error);
            throw error;
        }
    },

    /**
     * Generic DELETE request
     */
    async delete(endpoint) {
        try {
            const response = await fetch(`${API_BASE_URL}${endpoint}`, {
                method: 'DELETE'
            });
            
            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || `HTTP error! status: ${response.status}`);
            }
            
            return await response.json();
        } catch (error) {
            console.error('API DELETE Error:', error);
            throw error;
        }
    }
};

// Form Validation
const FormValidator = {
    /**
     * Validate required fields
     */
    validateRequired(formId, requiredFields) {
        const form = document.getElementById(formId);
        if (!form) return false;

        let isValid = true;
        const errors = [];

        requiredFields.forEach(fieldId => {
            const field = document.getElementById(fieldId);
            if (!field || !field.value.trim()) {
                isValid = false;
                errors.push(`Campo ${fieldId} es requerido`);
                if (field) {
                    field.classList.add('is-invalid');
                }
            } else {
                if (field) {
                    field.classList.remove('is-invalid');
                }
            }
        });

        if (!isValid) {
            console.error('Form validation errors:', errors);
        }

        return isValid;
    },

    /**
     * Validate numeric field
     */
    validateNumeric(fieldId, min = null, max = null) {
        const field = document.getElementById(fieldId);
        if (!field) return false;

        const value = parseFloat(field.value);
        
        if (isNaN(value)) {
            field.classList.add('is-invalid');
            return false;
        }

        if (min !== null && value < min) {
            field.classList.add('is-invalid');
            return false;
        }

        if (max !== null && value > max) {
            field.classList.add('is-invalid');
            return false;
        }

        field.classList.remove('is-invalid');
        return true;
    },

    /**
     * Clear validation errors
     */
    clearErrors(formId) {
        const form = document.getElementById(formId);
        if (!form) return;

        const invalidFields = form.querySelectorAll('.is-invalid');
        invalidFields.forEach(field => {
            field.classList.remove('is-invalid');
        });
    }
};

// Toast Notifications (if needed)
const Toast = {
    show(message, type = 'info') {
        // Simple alert for now, can be enhanced with a toast library
        console.log(`[${type.toUpperCase()}] ${message}`);
        Utils.alert(message);
    },

    success(message) {
        this.show(message, 'success');
    },

    error(message) {
        this.show(message, 'error');
    },

    info(message) {
        this.show(message, 'info');
    },

    warning(message) {
        this.show(message, 'warning');
    }
};

// Export for use in other scripts
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { Utils, API, FormValidator, Toast };
}

// Initialize on DOM ready
document.addEventListener('DOMContentLoaded', function() {
    console.log('Payroll Management System initialized');
    
    // Add fade-in animation to main content
    const mainContent = document.querySelector('main');
    if (mainContent) {
        mainContent.classList.add('fade-in');
    }
});
