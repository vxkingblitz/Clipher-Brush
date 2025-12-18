import { defineStore } from 'pinia'
import { useRequestsStore } from './requestsStore'

export const useFeedStore = defineStore('feed', {
    state: () => ({
        paintingsList: [],
        categoriesList: [],
        paintingsListMy: [],
    }),
    actions: {
        async _makeRequest(config, successMessage = null) {
            const requestsStore = useRequestsStore()
            return requestsStore._makeRequest(config, successMessage, false)
        },
        async getPaintingsList(category_id = null) {
            const response = await this._makeRequest({
                url: '/paintings/feed/',
                method: 'GET',
                data: category_id ? {
                    category_id: category_id
                } : null,
            })
            // DRF ListAPIView возвращает результаты напрямую или в results
            this.paintingsList = response.results || response.data?.results || response || []
            console.log('Paintings list loaded:', this.paintingsList)
        },
        async getPaintingsMyList() {
            const response = await this._makeRequest({
                url: '/paintings/my/',
                method: 'GET',
            })
            this.paintingsListMy = response.data.results
        },
        async getCategoriesList() {
            const response = await this._makeRequest({
                url: '/catalog/categories/',
                method: 'GET',
            })
            this.categoriesList = Array.isArray(response) ? response : []
            console.log('Categories list loaded:', this.categoriesList)
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