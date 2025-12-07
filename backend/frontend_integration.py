"""
Frontend Integration Module - API Client for JavaScript
This file provides examples and utilities for calling the Flask backend from frontend.
"""

# JavaScript code to include in your frontend files:
FRONTEND_API_CLIENT = """
// API Client for AppointmentPro Backend
const API_BASE_URL = 'http://localhost:5000/api';

class AppointmentProAPI {
    constructor() {
        this.token = localStorage.getItem('access_token') || null;
    }

    // ============ APPOINTMENT ENDPOINTS ============

    async createAppointment(appointmentData) {
        try {
            const response = await fetch(`${API_BASE_URL}/appointments`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${this.token}`
                },
                body: JSON.stringify(appointmentData)
            });
            const data = await response.json();
            return data;
        } catch (error) {
            console.error('Create appointment error:', error);
            return { success: false, error: error.message };
        }
    }

    async getAppointments(filters = {}) {
        try {
            const params = new URLSearchParams(filters).toString();
            const response = await fetch(`${API_BASE_URL}/appointments?${params}`, {
                method: 'GET',
                headers: {
                    'Authorization': `Bearer ${this.token}`
                }
            });
            const data = await response.json();
            return data;
        } catch (error) {
            console.error('Get appointments error:', error);
            return { success: false, error: error.message };
        }
    }

    async getAppointment(appointmentId) {
        try {
            const response = await fetch(`${API_BASE_URL}/appointments/${appointmentId}`, {
                method: 'GET',
                headers: {
                    'Authorization': `Bearer ${this.token}`
                }
            });
            const data = await response.json();
            return data;
        } catch (error) {
            console.error('Get appointment error:', error);
            return { success: false, error: error.message };
        }
    }

    async updateAppointmentStatus(appointmentId, status) {
        try {
            const response = await fetch(`${API_BASE_URL}/appointments/${appointmentId}/status`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${this.token}`
                },
                body: JSON.stringify({ status })
            });
            const data = await response.json();
            return data;
        } catch (error) {
            console.error('Update appointment status error:', error);
            return { success: false, error: error.message };
        }
    }

    async deleteAppointment(appointmentId) {
        try {
            const response = await fetch(`${API_BASE_URL}/appointments/${appointmentId}`, {
                method: 'DELETE',
                headers: {
                    'Authorization': `Bearer ${this.token}`
                }
            });
            const data = await response.json();
            return data;
        } catch (error) {
            console.error('Delete appointment error:', error);
            return { success: false, error: error.message };
        }
    }

    async checkAvailability(serviceType, date) {
        try {
            const response = await fetch(`${API_BASE_URL}/availability?service_type=${serviceType}&date=${date}`, {
                method: 'GET'
            });
            const data = await response.json();
            return data;
        } catch (error) {
            console.error('Check availability error:', error);
            return { success: false, error: error.message };
        }
    }

    // ============ AUTHENTICATION ENDPOINTS ============

    async clientSignup(email, password, name, phone) {
        try {
            const response = await fetch(`${API_BASE_URL}/auth/client-signup`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email, password, name, phone })
            });
            const data = await response.json();
            if (data.success) {
                this.token = data.access_token;
                localStorage.setItem('access_token', data.access_token);
            }
            return data;
        } catch (error) {
            console.error('Client signup error:', error);
            return { success: false, error: error.message };
        }
    }

    async clientLogin(email, password) {
        try {
            const response = await fetch(`${API_BASE_URL}/auth/client-login`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email, password })
            });
            const data = await response.json();
            if (data.success) {
                this.token = data.access_token;
                localStorage.setItem('access_token', data.access_token);
                localStorage.setItem('currentUser', JSON.stringify(data.user));
            }
            return data;
        } catch (error) {
            console.error('Client login error:', error);
            return { success: false, error: error.message };
        }
    }

    async staffSignup(email, password, name, phone, role) {
        try {
            const response = await fetch(`${API_BASE_URL}/auth/staff-signup`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email, password, name, phone, role })
            });
            const data = await response.json();
            if (data.success) {
                this.token = data.access_token;
                localStorage.setItem('access_token', data.access_token);
                localStorage.setItem('staffUser', JSON.stringify(data.user));
            }
            return data;
        } catch (error) {
            console.error('Staff signup error:', error);
            return { success: false, error: error.message };
        }
    }

    async staffLogin(email, password) {
        try {
            const response = await fetch(`${API_BASE_URL}/auth/staff-login`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email, password })
            });
            const data = await response.json();
            if (data.success) {
                this.token = data.access_token;
                localStorage.setItem('access_token', data.access_token);
                localStorage.setItem('staffUser', JSON.stringify(data.user));
            }
            return data;
        } catch (error) {
            console.error('Staff login error:', error);
            return { success: false, error: error.message };
        }
    }

    logout() {
        this.token = null;
        localStorage.removeItem('access_token');
        localStorage.removeItem('currentUser');
        localStorage.removeItem('staffUser');
    }

    // ============ STATISTICS ENDPOINTS ============

    async getStatistics() {
        try {
            const response = await fetch(`${API_BASE_URL}/statistics`, {
                method: 'GET',
                headers: {
                    'Authorization': `Bearer ${this.token}`
                }
            });
            const data = await response.json();
            return data;
        } catch (error) {
            console.error('Get statistics error:', error);
            return { success: false, error: error.message };
        }
    }

    async healthCheck() {
        try {
            const response = await fetch(`${API_BASE_URL}/health`, {
                method: 'GET'
            });
            const data = await response.json();
            return data;
        } catch (error) {
            console.error('Health check error:', error);
            return { success: false, error: error.message };
        }
    }
}

// Initialize API client
const api = new AppointmentProAPI();

// Usage examples:
/*
// Create appointment
const result = await api.createAppointment({
    service_type: 'School/College',
    client_name: 'John Doe',
    client_email: 'john@example.com',
    client_phone: '123-456-7890',
    appointment_date: '2025-12-20',
    appointment_time: '14:00',
    purpose: 'Enrollment'
});

// Check availability
const availability = await api.checkAvailability('School/College', '2025-12-20');

// Update appointment
const update = await api.updateAppointmentStatus(appointmentId, 'Confirmed');

// Client login
const login = await api.clientLogin('user@example.com', 'password123');
*/
"""

if __name__ == '__main__':
    print(FRONTEND_API_CLIENT)
