<template>
  <div class="loading-screen">
    
  </div>
</template>

<script>
import { mapState, mapActions } from 'pinia'
import { useAuthStore } from '../stores/authStore'

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
        this.$router.push('/feed')
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
          this.$router.push('/feed')
        }
      }
    }
  },
  async mounted() {
    if (!this.isAuthenticated && window.Telegram?.WebApp?.initDataUnsafe?.user) {
      try {
        await this.login()
        this.$router.push('/feed')
      } catch (error) {
        console.error('Auto-login failed:', error)
      }
    }
  }
}
</script>

<style scoped>

</style>