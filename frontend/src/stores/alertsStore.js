import { defineStore } from 'pinia'

export const useAlertsStore = defineStore('alerts', {
    state: () => ({
        notification: {
            message: '',
            status: '',
            isVisible: false,
        },
        hideTimeout: null,
    }),
    
    actions: {
        showNotification(payload) {
            if (this.hideTimeout) {
                clearTimeout(this.hideTimeout)
                this.hideTimeout = null
            }

            this.notification.isVisible = false

            setTimeout(() => {
                this.notification = {
                    message: payload.message,
                    status: payload.status,
                    isVisible: true
                }

                this.hideTimeout = setTimeout(() => {
                    this.hideNotification()
                }, 5000)
            }, 100)
        },
        
        hideNotification() {
            if (this.hideTimeout) {
                clearTimeout(this.hideTimeout)
                this.hideTimeout = null
            }
            this.notification.isVisible = false
        },
      
        forceHide() {
            this.hideNotification()
        }
    }
})