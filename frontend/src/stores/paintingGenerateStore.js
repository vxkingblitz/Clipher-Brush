import { defineStore } from 'pinia'
import { useRequestsStore } from './requestsStore'

export const useGeneratorStore = defineStore('generator', {
    state: () => ({
        painting_id: null,
        markersSets: [],
        markersSetsLoading: false,
    }),
    actions: {
        async _makeRequest(config, successMessage = null) {
            const requestsStore = useRequestsStore()
            return requestsStore._makeRequest(config, successMessage, false)
        },
        async getMarkersSets() {
            if (this.markersSets.length > 0) {
                // Если уже загружены, возвращаем из кеша
                return this.markersSets
            }
            
            this.markersSetsLoading = true
            try {
                const response = await this._makeRequest({
                    url: '/catalog/markers-sets/',
                    method: 'GET'
                })
                // Добавляем опцию "Без набора" в начало списка
                this.markersSets = [
                    { markers_set_id: null, brand_name: 'Без набора', colors_amount: 0 },
                    ...response
                ]
                return this.markersSets
            } catch (error) {
                console.error('Ошибка загрузки наборов маркеров:', error)
                // В случае ошибки возвращаем хотя бы опцию "Без набора"
                this.markersSets = [{ markers_set_id: null, brand_name: 'Без набора', colors_amount: 0 }]
                return this.markersSets
            } finally {
                this.markersSetsLoading = false
            }
        },
        async generatePainting(payload) {
            // Формируем FormData для отправки файла
            const formData = new FormData();
            formData.append('photo', payload.photo);
            formData.append('category_id', payload.category_id);
            formData.append('markers_set_id', payload.markers_set_id);
            formData.append('colors_amount', payload.colors_amount);
            
            // НЕ устанавливаем Content-Type вручную - браузер сам установит с правильным boundary
            const response = await this._makeRequest({
                url: '/paintings/',
                method: 'POST',
                data: formData
                // Не передаем headers - axios сам установит правильный Content-Type для FormData
            })
            this.painting_id = response.painting_id
            return response
        },
        async publishPainting(paintingId, categoryId = null) {
            const payload = {}
            if (categoryId) {
                payload.category_id = categoryId
            }
            const response = await this._makeRequest({
                url: `/paintings/${paintingId}/publish/`,
                method: 'POST',
                data: payload
            })
            return response
        },
    },
})