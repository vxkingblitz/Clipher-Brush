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
        @tab-change="val => setTab(val)"
    />

    <section class="feed-content" v-if="loadingFeed">
        <SkeletonLoader style="width: 100%; height: 294px;" v-for="i in 6" />
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
    mounted() {
        this.loadingFeed = true;
        setTimeout(() => {
            this.feedStore.getCategoriesList()
            this.feedStore.getPaintingsList()
            this.loadingFeed = false;
        }, 1000);
    },
    computed: {
        ...mapStores(useFeedStore),
        paintings(){
            return this.feedStore.paintingsList;
        },
        categories(){
            return this.feedStore.categoriesList;
        },
    },
    methods:{
        setTab(tab) {
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