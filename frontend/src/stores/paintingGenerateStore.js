import { defineStore } from 'pinia'
import { useRequestsStore } from './requestsStore'

export const useGeneratorStore = defineStore('generator', {
    state: () => ({
        painting_id: null,
    }),
    actions: {
        async _makeRequest(config, successMessage = null) {
            const requestsStore = useRequestsStore()
            return requestsStore._makeRequest(config, successMessage, false)
        },
        async generatePainting(payload) {
            const response = await this._makeRequest({
                url: '/paintings/',
                method: 'POST',
                data: payload
            })
            this.paintingsList = response.data.results
        },
    },
})