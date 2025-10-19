<template>
  <div class="login-view">
    <div class="login-container">
      <div class="login-card card elevation-4">
        <div class="login-header">
          <img src="@/assets/logo.png" alt="ContatoFácil" class="logo-icon">
          <h2>{{ $t('login.title') }}</h2>
          <p>{{ $t('login.description') }}</p>
        </div>

        <div class="login-body">
          <button 
            @click="handleLogin" 
            class="btn-microsoft"
            :disabled="loading"
          >
            <svg width="21" height="21" viewBox="0 0 21 21">
              <rect x="1" y="1" width="9" height="9" fill="#f25022"/>
              <rect x="1" y="11" width="9" height="9" fill="#00a4ef"/>
              <rect x="11" y="1" width="9" height="9" fill="#7fba00"/>
              <rect x="11" y="11" width="9" height="9" fill="#ffb900"/>
            </svg>
            <span v-if="!loading">{{ $t('login.button') }}</span>
            <span v-else>{{ $t('login.loading') }}</span>
          </button>

          <div class="login-footer">
            <button @click="goHome" class="btn-link">
              <span class="material-icons">arrow_back</span>
              {{ $t('nav.home') }}
            </button>
            <button @click="toggleLanguage" class="btn-link">
              <span class="material-icons">language</span>
              {{ currentLocale.toUpperCase() }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const { locale } = useI18n()
const authStore = useAuthStore()

const loading = ref(false)
const currentLocale = computed(() => locale.value)

const handleLogin = async () => {
  loading.value = true
  try {
    await authStore.login()
  } catch (error) {
    console.error('Login error:', error)
    loading.value = false
  }
}

const goHome = () => {
  router.push('/')
}

const toggleLanguage = () => {
  locale.value = locale.value === 'pt' ? 'en' : 'pt'
  localStorage.setItem('language', locale.value)
}
</script>

<style scoped>
.login-view {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 20px;
}

.login-container {
  width: 100%;
  max-width: 450px;
}

.login-card {
  background: white;
  padding: 40px;
  border-radius: 12px;
}

.login-header {
  text-align: center;
  margin-bottom: 40px;
}

.logo-icon {
  width: 72px;
  height: 72px;
  object-fit: contain;
  margin-bottom: 16px;
}

.login-header h2 {
  font-size: 28px;
  color: #333;
  margin-bottom: 12px;
}

.login-header p {
  color: #666;
  font-size: 14px;
  line-height: 1.6;
}

.login-body {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.btn-microsoft {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  padding: 16px 24px;
  background: linear-gradient(45deg, #2f2f2f, #1a1a1a);
  color: white;
  border: none;
  border-radius: 50px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.4s ease;
  width: 100%;
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.3);
  position: relative;
  overflow: hidden;
  letter-spacing: 0.5px;
}

.btn-microsoft::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
  transition: left 0.5s ease;
}

.btn-microsoft:hover:not(:disabled) {
  transform: translateY(-3px);
  box-shadow: 0 10px 28px rgba(0, 0, 0, 0.4);
}

.btn-microsoft:hover:not(:disabled)::before {
  left: 100%;
}

.btn-microsoft:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

.login-footer {
  display: flex;
  justify-content: space-between;
  padding-top: 20px;
  border-top: 1px solid #eee;
}

.btn-link {
  background: none;
  border: none;
  color: #667eea;
  font-size: 14px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 4px;
  font-weight: 500;
  transition: all 0.3s ease;
}

.btn-link:hover {
  color: #5568d3;
  text-decoration: underline;
}

.btn-link .material-icons {
  font-size: 18px;
}

@media (max-width: 768px) {
  .login-card {
    padding: 30px 20px;
  }

  .login-header h2 {
    font-size: 24px;
  }
}
</style>

