<template>
  <div id="pageView" class="feedWrapper">
    <h1>Добро пожаловать<br>в страну раскрасок!</h1>

    <div style="display: flex; gap: 6px; align-items: center; padding: 16px 6px;" v-if="loadingFeed || categories.length == 0">
        <SkeletonLoader style="width: 150px; height: 38px;" />
        <SkeletonLoader style="width: 80px; height: 38px;" />
        <SkeletonLoader style="width: 200px; height: 38px;" />
        <SkeletonLoader style="width: 140px; height: 38px;" />
    </div>

    <TabMenu
        v-else
        style="position: sticky; top: 0; z-index: 1; background-color: var(--color-white);"
        v-model="menuTab" 
        :tabs="categories" 
        tab-key="category_id"
        tab-label="name"
        @tab-change="val => setTab(val)"
    />


    <section class="feed-content" v-if="loadingFeed">
        <SkeletonLoader v-for="n in 6" :key="n" style="width: 100%; height: 294px;" />
    </section>

    <div class="messageBox" v-if="paintings.length == 0 && !loadingFeed">
        <img src="../assets/img/book.png" alt="empty-feed">
        <span>Пока ничего нет :(</span>
    </div>

    <section class="feed-content" v-if="paintings.length > 0 && !loadingFeed">
        <PaintingCard v-for="painting in paintings" :key="painting.painting_id" :painting="painting"/>
    </section>
  </div>
</template>

<script>
import { useFeedStore } from '../stores/feedStore'
import { mapStores } from 'pinia'

export default {
    data(){
        return{
            menuTab: 'all',
            loadingFeed: false,
        }
    },
    async mounted() {
        this.loadingFeed = true;
        try {
            await this.feedStore.getCategoriesList();
            await this.feedStore.getPaintingsList(); // Без category_id - все картины
        } catch (error) {
            console.error('Ошибка загрузки данных:', error);
        } finally {
            this.loadingFeed = false;
        }
    },
    computed: {
        ...mapStores(useFeedStore),
        paintings(){
            return this.feedStore.paintingsList;
        },
        categories(){
            // Добавляем вкладку "Все" в начало списка
            const allTab = { category_id: null, name: 'Все' };
            return [allTab, ...this.feedStore.categoriesList];
        },
    },
    methods:{
        setTab(tab) {
            this.loadingFeed = true;
            // Если tab - это строка 'all' или объект без category_id, передаем null
            const categoryId = (typeof tab === 'object' && tab !== null && tab.category_id !== undefined) 
                ? tab.category_id 
                : null;
            
            this.feedStore.getPaintingsList(categoryId).then(() => {
                this.loadingFeed = false;
            }).catch(() => {
                this.loadingFeed = false;
            });
            
            this.$router.push({ name: 'Feed', params: { tab } })
        },
    }
}
</script>

<style scoped>
.feed-content {
    margin-bottom: 110px;
    padding: 0 6px;
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
    grid-gap: 6px;
}
@media (max-width: 768px){
    .feed-content{
        padding: 0 6px;
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        grid-template-rows: 1fr;
        grid-column-gap: 6px;
        grid-row-gap: 6px;
        margin-bottom: 110px;
    }
}

</style>