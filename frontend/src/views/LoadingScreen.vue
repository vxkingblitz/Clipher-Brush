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

</style>