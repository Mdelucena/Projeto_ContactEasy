import { defineStore } from 'pinia'
import axios from 'axios'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    isAuthenticated: false,
    user: null,
    checkedAuth: false,
    authToken: localStorage.getItem('auth_token') || null
  }),

  actions: {
    setAuthToken(token) {
      this.authToken = token
      if (token) {
        localStorage.setItem('auth_token', token)
      } else {
        localStorage.removeItem('auth_token')
      }
    },

    getAuthHeaders() {
      if (this.authToken) {
        return {
          'Authorization': `Bearer ${this.authToken}`,
          'Content-Type': 'application/json'
        }
      }
      return {}
    },

    async checkAuthStatus() {
      try {
        const response = await axios.get(`${API_URL}/auth/status`, {
          headers: this.getAuthHeaders(),
          withCredentials: true
        })
        this.isAuthenticated = response.data.authenticated
        this.checkedAuth = true
        
        if (this.isAuthenticated && !this.user) {
          await this.fetchUserProfile()
        }
        
        return this.isAuthenticated
      } catch (error) {
        console.error('Error checking auth status:', error)
        this.isAuthenticated = false
        this.checkedAuth = true
        return false
      }
    },

    async login() {
      // Redireciona diretamente para o backend para iniciar o fluxo OAuth
      window.location.href = `${API_URL}/auth/login`
    },

    async logout() {
      try {
        await axios.get(`${API_URL}/auth/logout`, {
          headers: this.getAuthHeaders(),
          withCredentials: true
        })
        
        this.setAuthToken(null)
        this.isAuthenticated = false
        this.user = null
      } catch (error) {
        console.error('Error during logout:', error)
      }
    },

    async fetchUserProfile() {
      try {
        const response = await axios.get(`${API_URL}/api/user/profile`, {
          headers: this.getAuthHeaders(),
          withCredentials: true
        })
        
        if (response.data.success) {
          this.user = response.data.user
        }
      } catch (error) {
        console.error('Error fetching user profile:', error)
      }
    }
  }
})

