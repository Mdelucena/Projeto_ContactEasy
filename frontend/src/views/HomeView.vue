<template>
  <div class="home-view">
    <div class="container">
      <header class="header">
        <div class="logo">
          <img src="@/assets/logo.png" alt="ContatoFácil" class="logo-image">
          <h1>{{ $t('app.title') }}</h1>
        </div>
        <div class="header-actions">
          <button @click="toggleLanguage" class="btn-icon">
            <span class="material-icons">language</span>
            {{ currentLocale.toUpperCase() }}
          </button>
          <router-link v-if="isAuthenticated" to="/contacts" class="btn btn-primary">
            <span class="material-icons">list</span>
            {{ $t('nav.contacts') }}
          </router-link>
          <router-link v-else to="/login" class="btn btn-primary">
            <span class="material-icons">login</span>
            {{ $t('nav.login') }}
          </router-link>
        </div>
      </header>

      <main class="hero">
        <div class="hero-content">
          <h2 class="hero-title">{{ $t('home.welcome') }}</h2>
          <p class="hero-description">{{ $t('home.description') }}</p>
          
          <div class="features">
            <h3>{{ $t('home.features.title') }}</h3>
            <div class="features-grid">
              <div class="feature-card card">
                <span class="material-icons">verified_user</span>
                <p>{{ $t('home.features.auth') }}</p>
              </div>
              <div class="feature-card card">
                <span class="material-icons">folder</span>
                <p>{{ $t('home.features.organize') }}</p>
              </div>
              <div class="feature-card card">
                <span class="material-icons">search</span>
                <p>{{ $t('home.features.search') }}</p>
              </div>
              <div class="feature-card card">
                <span class="material-icons">translate</span>
                <p>{{ $t('home.features.multilang') }}</p>
              </div>
            </div>
          </div>

          <router-link v-if="!isAuthenticated" to="/login" class="btn-get-started">
            {{ $t('home.getStarted') }}
          </router-link>
        </div>
      </main>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useI18n } from 'vue-i18n'
import { useAuthStore } from '@/stores/auth'

const { locale } = useI18n()
const authStore = useAuthStore()

const currentLocale = computed(() => locale.value)
const isAuthenticated = computed(() => authStore.isAuthenticated)

const toggleLanguage = () => {
  locale.value = locale.value === 'pt' ? 'en' : 'pt'
  localStorage.setItem('language', locale.value)
}
</script>

<style scoped>
.home-view {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 20px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 0;
  margin-bottom: 60px;
}

.logo {
  display: flex;
  align-items: center;
  gap: 12px;
}

.logo-image {
  width: 48px;
  height: 48px;
  object-fit: contain;
}

.logo h1 {
  font-size: 24px;
  font-weight: 500;
}

.header-actions {
  display: flex;
  gap: 12px;
  align-items: center;
}

.btn-icon {
  background: rgba(255, 255, 255, 0.2);
  border: none;
  padding: 10px 18px;
  border-radius: 25px;
  color: white;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 6px;
  font-weight: 600;
  letter-spacing: 0.5px;
  transition: all 0.4s ease;
  backdrop-filter: blur(10px);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
}

.btn-icon:hover {
  background: rgba(255, 255, 255, 0.35);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

.hero {
  text-align: center;
  padding: 40px 0;
}

.hero-content {
  max-width: 1000px;
  margin: 0 auto;
}

.hero-title {
  font-size: 48px;
  font-weight: 700;
  margin-bottom: 20px;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

.hero-description {
  font-size: 20px;
  margin-bottom: 60px;
  opacity: 0.95;
}

.features {
  margin: 60px 0;
}

.features h3 {
  font-size: 28px;
  margin-bottom: 30px;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
  margin-bottom: 40px;
}

.feature-card {
  padding: 30px 20px;
  text-align: center;
  background: white;
  color: #333;
  transition: transform 0.3s ease;
}

.feature-card:hover {
  transform: translateY(-5px);
}

.feature-card .material-icons {
  font-size: 48px;
  color: #667eea;
  margin-bottom: 12px;
}

.feature-card p {
  font-size: 14px;
  line-height: 1.6;
}

.btn-large {
  font-size: 16px;
  padding: 16px 32px;
}

.btn-get-started {
  display: inline-block;
  padding: 18px 48px;
  font-size: 18px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 1px;
  color: white;
  background: linear-gradient(45deg, #667eea, #764ba2);
  border: none;
  border-radius: 50px;
  cursor: pointer;
  text-decoration: none;
  box-shadow: 0 8px 24px rgba(102, 126, 234, 0.4);
  transition: all 0.4s ease;
  position: relative;
  overflow: hidden;
}

.btn-get-started::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
  transition: left 0.5s ease;
}

.btn-get-started:hover {
  transform: translateY(-3px);
  box-shadow: 0 12px 32px rgba(102, 126, 234, 0.6);
}

.btn-get-started:hover::before {
  left: 100%;
}

.btn-get-started:active {
  transform: translateY(-1px);
}

@media (max-width: 768px) {
  .hero-title {
    font-size: 32px;
  }

  .hero-description {
    font-size: 16px;
  }

  .features-grid {
    grid-template-columns: 1fr;
  }

  .header {
    flex-direction: column;
    gap: 20px;
  }
}
</style>

