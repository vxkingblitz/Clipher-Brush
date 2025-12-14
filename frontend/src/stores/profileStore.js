import { defineStore } from 'pinia'
import { useRequestsStore } from './requestsStore'

export const useProfileStore = defineStore('profile', {
    state: () => ({
        user: null,
        favouritePaintingsList: [],
        myPaintingsList: [],
    }),
    actions: {
        async _makeRequest(config, successMessage = null) {
            const requestsStore = useRequestsStore()
            return requestsStore._makeRequest(config, successMessage, false)
        },
        async getFavouritePaintingsList() {
            const response = await this._makeRequest({
                url: '/paintings/',
                method: 'GET',
            })
            this.paintingsList = response.data.results
        },
        async getMyPaintingsList() {
            const response = await this._makeRequest({
                url: '/paintings/',
                method: 'GET',
            })
            this.paintingsList = response.data.results
        },
    },
})