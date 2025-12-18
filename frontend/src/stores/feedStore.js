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
            // Для GET запросов используем params (query параметры), а не data
            const config = {
                url: '/paintings/feed/',
                method: 'GET',
            }
            
            if (category_id) {
                config.params = { category_id: category_id }
            }
            
            const response = await this._makeRequest(config)
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
            // DRF RetrieveAPIView возвращает данные напрямую или в data
            return response.data || response
        }
    },
})