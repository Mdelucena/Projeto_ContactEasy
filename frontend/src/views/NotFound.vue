<template>
  <div class="not-found">
    <div class="content">
      <span class="material-icons">error_outline</span>
      <h1>404</h1>
      <h2>{{ $t('notFound.title') }}</h2>
      <p>{{ $t('notFound.description') }}</p>
      <router-link to="/" class="btn btn-primary">
        <span class="material-icons">home</span>
        {{ $t('notFound.backHome') }}
      </router-link>
    </div>
  </div>
</template>

<script setup>
</script>

<style scoped>
.not-found {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  text-align: center;
  padding: 20px;
}

.content {
  max-width: 500px;
}

.content .material-icons {
  font-size: 120px;
  margin-bottom: 20px;
  opacity: 0.9;
}

.content h1 {
  font-size: 80px;
  font-weight: 700;
  margin-bottom: 16px;
}

.content h2 {
  font-size: 32px;
  margin-bottom: 12px;
}

.content p {
  font-size: 18px;
  margin-bottom: 32px;
  opacity: 0.9;
}
</style>

