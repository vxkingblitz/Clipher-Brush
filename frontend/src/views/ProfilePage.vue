<template>
  <div id="pageView" class="profileWrapper">
    <h1>Добро пожаловать<br>в твои шедевры!</h1>

    <TabMenu
        style="position: sticky; top: 0; z-index: 1; background-color: var(--color-white);"
        v-model="menuTab" 
        :tabs="[
            { id: 'favourites', label: 'Избранное' },
            { id: 'my_works', label: 'Мои работы' },
        ]" 
        @tab-change="val => setTab(val)"
    />

    <div v-if="menuTab == 'favourites'">
        <section class="feed-content" v-if="loadingFavourites">
            <SkeletonLoader style="width: 100%; height: 294px;" v-for="i in 6" />
        </section>

        <div class="messageBox" v-if="favouritePaintingsList.length == 0 && !loadingFavourites">
            <img src="../assets/img/book.png" alt="empty-feed">
            <span>Пока ничего нет :(</span>
        </div>

        <section class="feed-content" v-if="favouritePaintingsList.length > 0 && !loadingFavourites">
            <PaintingCard id="pageView" v-for="i in 10" :key="i.id"/>
        </section>
    </div>

    <div v-if="menuTab == 'my_works'">
        <section class="feed-content" v-if="loadingMy">
            <SkeletonLoader style="width: 100%; height: 294px;" v-for="i in 6" />
        </section>

        <div class="messageBox" v-if="paintingsListMy.length == 0 && !loadingMy">
            <img src="../assets/img/book.png" alt="empty-feed">
            <span>Пока ничего нет :(</span>
        </div>

        <section class="feed-content" v-if="paintingsListMy.length > 0 && !loadingMy">
            <PaintingCard id="pageView" v-for="i in 10" :key="i.id"/>
        </section>
    </div>
    
  </div>
</template>

<script>
import { useProfileStore } from '../stores/profileStore'
import { mapStores } from 'pinia'

export default {
    data(){
        return{
            menuTab: 'favourites',
            loadingFavourites: false,
            loadingMy: false,
        }
    },
    mounted() {
        this.loadingFavourites = true;
        this.loadingMy = true;
        setTimeout(() => {
            this.profileStore.getFavouritePaintingsList()
            this.loadingFavourites = false;
        }, 1000);

        setTimeout(() => {
            this.profileStore.getPaintingsMyList()
            this.loadingMy = false;
        }, 1000);
    },
    methods:{
        setTab(tab) {
            this.$router.push({ name: 'Profile', params: { tab } })
        },
    },
    computed: {
        ...mapStores(useProfileStore),
        favouritePaintingsList(){
            return this.profileStore.favouritePaintingsList;
        },
        paintingsListMy(){
            return this.profileStore.paintingsListMy;
        },
    },
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
