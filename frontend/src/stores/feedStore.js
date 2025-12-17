import { defineStore } from 'pinia'
import { useRequestsStore } from './requestsStore'

export const useFeedStore = defineStore('feed', {
    state: () => ({
        paintingsList: [],
        categoriesList: [],
    }),
    actions: {
        async _makeRequest(config, successMessage = null) {
            const requestsStore = useRequestsStore()
            return requestsStore._makeRequest(config, successMessage, false)
        },
        async getPaintingsList() {
            const response = await this._makeRequest({
                url: '/paintings/feed/',
                method: 'GET',
            })
            this.paintingsList = response.data.results
        },
        async getCategoriesList() {
            const response = await this._makeRequest({
                url: '/catalog/categories/',
                method: 'GET',
            })
            this.categoriesList = response.data.results
        },
        async getPainting(id) {
            const response = await this._makeRequest({
                url: `/paintings/${id}/`,
                method: 'GET',
            })
            return response.data
        }
    },
})