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
        async getPaintingsList() {
            const response = await this._makeRequest({
                url: '/paintings/feed/',
                method: 'GET',
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
            // CategoryListView возвращает массив напрямую через Response(serializer.data)
            // _makeRequest уже возвращает response.data, поэтому response - это массив категорий
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