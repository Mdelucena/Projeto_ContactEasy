import { defineStore } from 'pinia'
import axios from 'axios'
import { useAuthStore } from './auth'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000'

export const useContactsStore = defineStore('contacts', {
  state: () => ({
    contacts: [],
    loading: false,
    error: null,
    totalDomains: 0,
    totalContacts: 0
  }),

  getters: {
    domains: (state) => {
      return state.contacts.map(c => c.domain)
    },
    
    contactsByDomain: (state) => (domain) => {
      const found = state.contacts.find(c => c.domain === domain)
      return found ? found.contacts : []
    }
  },

  actions: {
    async fetchContacts() {
      this.loading = true
      this.error = null
      
      const authStore = useAuthStore()
      
      try {
        const response = await axios.get(`${API_URL}/api/contacts`, {
          headers: authStore.getAuthHeaders(),
          withCredentials: true
        })
        
        if (response.data.success) {
          this.contacts = response.data.data
          this.totalDomains = response.data.total_domains
          this.totalContacts = response.data.total_contacts
        }
      } catch (error) {
        console.error('Error fetching contacts:', error)
        this.error = error.response?.data?.error || 'Erro ao carregar contatos'
        
        if (error.response?.status === 401) {
          // Token expirad = redireciona para login
          const authStore = useAuthStore()
          authStore.isAuthenticated = false
        }
      } finally {
        this.loading = false
      }
    },

    clearContacts() {
      this.contacts = []
      this.totalDomains = 0
      this.totalContacts = 0
      this.error = null
    }
  }
})

