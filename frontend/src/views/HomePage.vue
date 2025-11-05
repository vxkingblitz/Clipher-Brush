<template>
  <div>
    <div>
        <h2>user.first_name: {{ user.first_name }}!</h2>
        <p>user.id: {{ user.id }}</p>
        <p v-if="user.username">Username: @{{ user.username }}</p>
    </div>
  </div>
</template>

<script>
import { mapState, mapActions } from 'pinia'
import { useAuthStore } from '../stores/auth'

export default {
  name: 'HomePage',
  computed: {
    ...mapState(useAuthStore, ['user'])
  },
  methods: {
    ...mapActions(useAuthStore, ['logout']),
    
    logout() {
      this.logout()
      this.$router.push('/')
    }
  }
}
</script>

<style scoped>
</style>