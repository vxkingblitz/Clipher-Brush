<template>
  <div class="loading-screen">
    <div class="loading-content">
      <div v-if="auth?.isLoading">
        <p>Проверка авторизации...</p>
      </div>
      
      <div v-else-if="!auth?.isAuthenticated">
        <button 
          @click="handleLogin" 
          :disabled="auth?.isLoading"
          class="auth-button"
        >
          {{ auth?.isLoading ? 'Авторизация...' : 'Авторизоваться' }}
        </button>
      </div>

      <div v-else>
        лол
      </div>
    </div>
  </div>
</template>

<script>
import { mapState, mapActions } from 'pinia'
import { useAuthStore } from '../stores/auth'

export default {
  name: 'LoadingScreen',
  computed: {
    ...mapState(useAuthStore, ['isLoading', 'isAuthenticated'])
  },
  methods: {
    ...mapActions(useAuthStore, ['login']),
    
    async handleLogin() {
      try {
        await this.login()
        this.$router.push('/home')
      } catch (error) {
        alert('Ошибка авторизации: ' + error.message)
      }
    }
  },
  watch: {
    isAuthenticated: {
      immediate: true,
      handler(newVal) {
        if (newVal) {
          this.$router.push('/home')
        }
      }
    }
  },
  async mounted() {
    if (!this.isAuthenticated && window.Telegram?.WebApp?.initDataUnsafe?.user) {
      try {
        await this.login()
        this.$router.push('/home')
      } catch (error) {
        console.error('Auto-login failed:', error)
      }
    }
  }
}
</script>

<style scoped>

</style>