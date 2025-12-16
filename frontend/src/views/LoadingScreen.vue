<template>
  <div id="pageView" class="loading-screen">
    <img class="loading-logo" src="../assets/img/logo.png" alt="logo">
    <img class="loading-spinner" src="../assets/img/loader.svg" alt="loader">
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
  watch: {
    isAuthenticated: {
      immediate: true,
      handler(newVal) {
        if (newVal) {
          this.$router.push('/feed/all')
        }
      }
    }
  },
}
</script>

<style scoped>
.loading-screen {
  display: flex;
  flex-direction: column;
  height: 100svh;
  align-items: center;
  justify-content: center;
}
.loading-logo {
  width: 220px;
}
.loading-spinner {
  animation: spin 2s linear infinite;
}
@keyframes spin {
  0% { transform: rotate(0deg);}
  100% { transform: rotate(360deg);}
}
</style>