<template>
  <div class="contacts-view">
    <nav class="navbar">
      <div class="navbar-content">
        <div class="navbar-left">
          <img src="@/assets/logo.png" alt="ContatoFácil" class="navbar-logo">
          <h1>{{ $t('app.title') }}</h1>
        </div>
        <div class="navbar-right">
          <div v-if="authStore.user" class="user-info">
            <span class="material-icons">account_circle</span>
            <span>{{ authStore.user.displayName }}</span>
          </div>
          <button @click="toggleLanguage" class="btn-icon">
            <span class="material-icons">language</span>
            {{ currentLocale.toUpperCase() }}
          </button>
          <button @click="handleLogout" class="btn btn-secondary">
            <span class="material-icons">logout</span>
            {{ $t('nav.logout') }}
          </button>
        </div>
      </div>
    </nav>

    <div class="container">
      <div class="contacts-header">
        <h2>{{ $t('contacts.title') }}</h2>
        <button @click="loadContacts" class="btn btn-primary" :disabled="contactsStore.loading">
          <span class="material-icons">refresh</span>
          {{ $t('contacts.refresh') }}
        </button>
      </div>

      <!-- Stats -->
      <div class="stats-grid" v-if="contactsStore.contacts.length > 0">
        <div class="stat-card card">
          <span class="material-icons">domain</span>
          <div>
            <div class="stat-value">{{ contactsStore.totalDomains }}</div>
            <div class="stat-label">{{ $t('contacts.totalDomains') }}</div>
          </div>
        </div>
        <div class="stat-card card">
          <span class="material-icons">people</span>
          <div>
            <div class="stat-value">{{ contactsStore.totalContacts }}</div>
            <div class="stat-label">{{ $t('contacts.totalContacts') }}</div>
          </div>
        </div>
      </div>

      <div class="filters" v-if="contactsStore.contacts.length > 0">
        <div class="search-box">
          <span class="material-icons">search</span>
          <input 
            v-model="searchQuery" 
            type="text" 
            :placeholder="$t('contacts.search')"
          />
        </div>
        <select v-model="selectedDomain" class="domain-filter">
          <option value="">{{ $t('contacts.allDomains') }}</option>
          <option v-for="domain in contactsStore.domains" :key="domain" :value="domain">
            {{ domain }}
          </option>
        </select>
      </div>

      <div v-if="contactsStore.loading" class="loading-container">
        <div class="spinner"></div>
        <p>{{ $t('contacts.loading') }}</p>
      </div>

      <div v-else-if="contactsStore.error" class="error-container">
        <span class="material-icons">error</span>
        <p>{{ contactsStore.error }}</p>
      </div>

      <div v-else-if="contactsStore.contacts.length === 0" class="empty-container">
        <span class="material-icons">inbox</span>
        <p>{{ $t('contacts.empty') }}</p>
      </div>

      <div v-else class="contacts-list">
        <div 
          v-for="domainGroup in filteredContacts" 
          :key="domainGroup.domain"
          class="domain-group"
        >
          <div class="domain-header">
            <div class="domain-info">
              <span class="material-icons">folder</span>
              <h3>{{ domainGroup.domain }}</h3>
              <span class="contact-count">{{ domainGroup.contacts.length }} {{ $t('contacts.contactsInDomain') }}</span>
            </div>
          </div>

          <div class="contacts-table-container card">
            <table class="contacts-table">
              <thead>
                <tr>
                  <th>{{ $t('contacts.name') }}</th>
                  <th>{{ $t('contacts.email') }}</th>
                  <th>{{ $t('contacts.company') }}</th>
                  <th>{{ $t('contacts.jobTitle') }}</th>
                  <th>{{ $t('contacts.phone') }}</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="contact in domainGroup.contacts" :key="contact.id">
                  <td>
                    <div class="contact-name">
                      <span class="material-icons">person</span>
                      {{ contact.displayName }}
                    </div>
                  </td>
                  <td>{{ contact.email }}</td>
                  <td>{{ contact.companyName || '-' }}</td>
                  <td>{{ contact.jobTitle || '-' }}</td>
                  <td>{{ contact.mobilePhone || contact.businessPhones[0] || '-' }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { useAuthStore } from '@/stores/auth'
import { useContactsStore } from '@/stores/contacts'

const router = useRouter()
const { locale } = useI18n()
const authStore = useAuthStore()
const contactsStore = useContactsStore()

const searchQuery = ref('')
const selectedDomain = ref('')
const currentLocale = computed(() => locale.value)

const filteredContacts = computed(() => {
  let contacts = contactsStore.contacts

  if (selectedDomain.value) {
    contacts = contacts.filter(c => c.domain === selectedDomain.value)
  }

  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    contacts = contacts.map(domainGroup => ({
      ...domainGroup,
      contacts: domainGroup.contacts.filter(contact => 
        contact.displayName.toLowerCase().includes(query) ||
        contact.email.toLowerCase().includes(query) ||
        (contact.companyName && contact.companyName.toLowerCase().includes(query)) ||
        (contact.jobTitle && contact.jobTitle.toLowerCase().includes(query))
      )
    })).filter(domainGroup => domainGroup.contacts.length > 0)
  }

  return contacts
})

const loadContacts = async () => {
  await contactsStore.fetchContacts()
}

const handleLogout = async () => {
  await authStore.logout()
  contactsStore.clearContacts()
  router.push('/')
}

const toggleLanguage = () => {
  locale.value = locale.value === 'pt' ? 'en' : 'pt'
  localStorage.setItem('language', locale.value)
}

onMounted(async () => {
  // Verifica se há um token temporário na URL
  const urlParams = new URLSearchParams(window.location.search)
  const tempToken = urlParams.get('token')
  
  if (tempToken) {
    // Salva o token no localStorage via authStore
    authStore.setAuthToken(tempToken)
    
    // Remove o token da URL
    const url = new URL(window.location)
    url.searchParams.delete('token')
    url.searchParams.delete('auth')
    window.history.replaceState({}, '', url)
  }
  
  loadContacts()
})
</script>

<style scoped>
.contacts-view {
  min-height: 100vh;
  background: #f5f5f5;
}

.navbar {
  background: white;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  position: sticky;
  top: 0;
  z-index: 100;
}

.navbar-content {
  max-width: 1400px;
  margin: 0 auto;
  padding: 16px 24px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.navbar-left {
  display: flex;
  align-items: center;
  gap: 12px;
}

.navbar-logo {
  width: 36px;
  height: 36px;
  object-fit: contain;
}

.navbar-left h1 {
  font-size: 20px;
  color: #333;
}

.navbar-right {
  display: flex;
  align-items: center;
  gap: 16px;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #666;
  font-size: 14px;
}

.container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 32px 24px;
}

.contacts-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 32px;
}

.contacts-header h2 {
  font-size: 32px;
  color: #333;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
  margin-bottom: 32px;
}

.stat-card {
  padding: 24px;
  display: flex;
  align-items: center;
  gap: 16px;
}

.stat-card .material-icons {
  font-size: 48px;
  color: #667eea;
}

.stat-value {
  font-size: 36px;
  font-weight: 700;
  color: #333;
}

.stat-label {
  font-size: 14px;
  color: #666;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.filters {
  display: flex;
  gap: 16px;
  margin-bottom: 32px;
}

.search-box {
  flex: 1;
  display: flex;
  align-items: center;
  gap: 12px;
  background: white;
  padding: 14px 20px;
  border-radius: 25px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.08);
  transition: all 0.3s ease;
}

.search-box:focus-within {
  box-shadow: 0 6px 16px rgba(102, 126, 234, 0.2);
  transform: translateY(-1px);
}

.search-box .material-icons {
  color: #667eea;
}

.search-box input {
  flex: 1;
  border: none;
  outline: none;
  font-size: 15px;
  font-weight: 500;
}

.domain-filter {
  padding: 14px 20px;
  border: 2px solid #e0e0e0;
  border-radius: 25px;
  background: white;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  min-width: 200px;
  transition: all 0.3s ease;
  box-shadow: 0 2px 8px rgba(0,0,0,0.05);
}

.domain-filter:hover {
  border-color: #667eea;
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.15);
}

.domain-filter:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.25);
}

.loading-container,
.error-container,
.empty-container {
  text-align: center;
  padding: 60px 20px;
}

.loading-container p,
.error-container p,
.empty-container p {
  margin-top: 16px;
  color: #666;
  font-size: 16px;
}

.error-container .material-icons,
.empty-container .material-icons {
  font-size: 72px;
  color: #999;
}

.contacts-list {
  display: flex;
  flex-direction: column;
  gap: 32px;
}

.domain-group {
  animation: fadeIn 0.3s ease;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

.domain-header {
  margin-bottom: 16px;
}

.domain-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.domain-info .material-icons {
  font-size: 28px;
  color: #667eea;
}

.domain-info h3 {
  font-size: 22px;
  color: #333;
}

.contact-count {
  font-size: 14px;
  color: #999;
  background: #f0f0f0;
  padding: 4px 12px;
  border-radius: 12px;
}

.contacts-table-container {
  overflow-x: auto;
}

.contacts-table {
  width: 100%;
  border-collapse: collapse;
}

.contacts-table thead {
  background: #f8f9fa;
}

.contacts-table th {
  padding: 16px;
  text-align: left;
  font-weight: 500;
  color: #666;
  font-size: 13px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.contacts-table td {
  padding: 16px;
  border-top: 1px solid #eee;
  color: #333;
  font-size: 14px;
}

.contacts-table tbody tr:hover {
  background: #f8f9fa;
}

.contact-name {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 500;
}

.contact-name .material-icons {
  font-size: 20px;
  color: #999;
}

@media (max-width: 768px) {
  .navbar-content {
    flex-direction: column;
    gap: 16px;
  }

  .navbar-right {
    width: 100%;
    justify-content: space-between;
  }

  .contacts-header {
    flex-direction: column;
    gap: 16px;
    align-items: flex-start;
  }

  .filters {
    flex-direction: column;
  }

  .domain-filter {
    width: 100%;
  }

  .contacts-table {
    font-size: 12px;
  }

  .contacts-table th,
  .contacts-table td {
    padding: 12px 8px;
  }

  .user-info span:last-child {
    display: none;
  }
}
</style>

