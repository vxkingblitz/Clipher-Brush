<template>
  <div id="pageView" class="painting-detail-wrapper">
    <div v-if="loading" class="loading-container">
      <SkeletonLoader v-for="n in 3" :key="n" style="width: 100%; height: 400px; margin-bottom: 20px;" />
    </div>

    <div v-else-if="painting" class="painting-detail-content">
      <div class="images-container">
        <div class="image-item" v-if="getImageUrl(painting.photo)">
          <h3>Исходник</h3>
          <img :src="getImageUrl(painting.photo)" alt="Original" @error="handleImageError" />
        </div>
        
        <div class="image-item" v-if="getImageUrl(painting.painting_numbered)">
          <h3>С цифрами</h3>
          <img :src="getImageUrl(painting.painting_numbered)" alt="Numbered" @error="handleImageError" />
        </div>
        
        <div class="image-item" v-if="getImageUrl(painting.painting_colored)">
          <h3>Раскрашенное</h3>
          <img :src="getImageUrl(painting.painting_colored)" alt="Colored" @error="handleImageError" />
        </div>
      </div>

      <div class="download-section">
        <ButtonComponent 
          @click="downloadAll" 
          :disabled="!canDownload"
          :label="'Скачать все 3 изображения'"
          :variant="1"
          class="download-button"
        />
      </div>
    </div>

    <div v-else class="error-container">
      <p>Картина не найдена</p>
    </div>
  </div>
</template>

<script>
import { useFeedStore } from '../stores/feedStore'
import { mapStores } from 'pinia'
import ButtonComponent from '../components/ui/ButtonComponent.vue'
import SkeletonLoader from '../components/ui/SkeletonLoader.vue'

export default {
  components: {
    ButtonComponent,
    SkeletonLoader
  },
  data() {
    return {
      painting: null,
      loading: true,
    }
  },
  computed: {
    ...mapStores(useFeedStore),
    canDownload() {
      return this.painting && (
        this.getImageUrl(this.painting.photo) ||
        this.getImageUrl(this.painting.painting_numbered) ||
        this.getImageUrl(this.painting.painting_colored)
      )
    }
  },
  async mounted() {
    const paintingId = this.$route.params.id
    if (paintingId) {
      await this.loadPainting(paintingId)
    }
  },
  methods: {
    async loadPainting(id) {
      this.loading = true
      try {
        this.painting = await this.feedStore.getPainting(id)
      } catch (error) {
        console.error('Ошибка загрузки картины:', error)
      } finally {
        this.loading = false
      }
    },
    getImageUrl(url) {
      if (!url) return null
      if (typeof url === 'string') {
        if (url.startsWith('http')) {
          return url
        }
        return 'https://cipherbrush.ru' + url
      }
      return null
    },
    handleImageError(e) {
      e.target.src = 'https://via.placeholder.com/300x300?text=Error'
    },
    async downloadAll() {
      if (!this.painting) return

      const images = [
        { url: this.getImageUrl(this.painting.photo), name: 'original.png' },
        { url: this.getImageUrl(this.painting.painting_numbered), name: 'numbered.png' },
        { url: this.getImageUrl(this.painting.painting_colored), name: 'colored.png' }
      ].filter(img => img.url)

      if (images.length === 0) {
        alert('Нет доступных изображений для скачивания')
        return
      }

      // Скачиваем все изображения
      for (const image of images) {
        try {
          const response = await fetch(image.url)
          const blob = await response.blob()
          const url = window.URL.createObjectURL(blob)
          const a = document.createElement('a')
          a.href = url
          a.download = image.name
          document.body.appendChild(a)
          a.click()
          window.URL.revokeObjectURL(url)
          document.body.removeChild(a)
          
          // Небольшая задержка между скачиваниями
          await new Promise(resolve => setTimeout(resolve, 300))
        } catch (error) {
          console.error(`Ошибка скачивания ${image.name}:`, error)
        }
      }
    }
  }
}
</script>

<style scoped>
.painting-detail-wrapper {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.loading-container {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.painting-detail-content {
  display: flex;
  flex-direction: column;
  gap: 30px;
}

.images-container {
  display: flex;
  flex-direction: column;
  gap: 30px;
}

.image-item {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.image-item h3 {
  font-size: 18px;
  font-weight: 600;
  color: var(--color-text, #333);
  margin: 0;
}

.image-item img {
  width: 100%;
  height: auto;
  border-radius: 16px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.download-section {
  display: flex;
  justify-content: center;
  padding: 20px 0;
  position: sticky;
  bottom: 0;
  background-color: var(--color-white, #fff);
  z-index: 10;
}

.download-button {
  margin-bottom: 110px;
  min-width: 250px;
}

.error-container {
  text-align: center;
  padding: 40px;
  color: var(--color-text, #333);
}

@media (max-width: 768px) {
  .painting-detail-wrapper {
    padding: 10px;
  }
  
  .images-container {
    gap: 20px;
  }
  
  .image-item h3 {
    font-size: 16px;
  }
}
</style>
