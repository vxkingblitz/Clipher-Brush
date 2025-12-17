<template>
  <div class="paintingCardWrapper">
    {{ painting }}
    <img :src="getImageUrl()" alt="painting" @error="handleImageError">
    <div class="paintingCard-bottom">
        <svg width="20" height="18" viewBox="0 0 20 18" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M1.73389 8.36012L6.86798 15.2602C8.34549 17.246 11.1545 17.246 12.632 15.2602L17.7661 8.36012C19.078 6.597 19.078 4.09172 17.7661 2.3286C15.8457 -0.252356 11.4071 0.514189 9.75 3.2981C8.09289 0.514189 3.65428 -0.252356 1.7339 2.3286C0.422036 4.09172 0.422033 6.597 1.73389 8.36012Z" stroke="#F4F4F4" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
        <p class="nickname">{{ painting.username }}</p>
    </div>
  </div>
</template>

<script>
export default {
    props: {
        painting: {
            type: Object,
            required: true
        }
    },
    computed: {
        getImageUrl() {
            return 'https://cipherbrush.ru' + this.painting.painting_colored;
        },
    },
    methods: {
        handleImageError(e) {
            e.target.src = 'https://via.placeholder.com/300x300?text=Error';
        }
    }
}
</script>

<style scoped>
.paintingCard-bottom{
    height: 64px;
    background: #000000;
    background: linear-gradient(180deg,rgba(55, 55, 55, 0) 0%, rgb(28, 28, 28) 100%);
    position: absolute;
    bottom: 0;
    display: flex;
    align-items: end;
    padding: 16px;
    gap: 10px;
}
.paintingCardWrapper{
    position: relative;
    width: 100%;
    height: 294px;
    border-radius: 32px;
    overflow: hidden;
}
.nickname{
    font-size: 12px;
    font-weight: 500;
    color: var(--color-white);
}
.paintingCardWrapper img{
    width: 100%;
    height: 100%;
    object-fit: cover;
}
</style>