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
            // Формируем FormData для отправки файла
            const formData = new FormData();
            formData.append('photo', payload.photo);
            formData.append('category_id', payload.category_id);
            formData.append('markers_set_id', payload.markers_set_id);
            formData.append('colors_amount', payload.colors_amount);
            
            const response = await this._makeRequest({
                url: '/paintings/',
                method: 'POST',
                data: formData,
                headers: {
                    'Content-Type': 'multipart/form-data'
                }
            })
            this.painting_id = response.painting_id
            return response
        },
    },
})