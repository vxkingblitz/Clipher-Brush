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

    <div v-if="currentTabId == 'favourites'">
        <section class="feed-content" v-if="loadingFavourites">
            <SkeletonLoader v-for="n in 6" :key="n" style="width: 100%; height: 294px;" />
        </section>

        <div class="messageBox" v-if="favouritePaintingsList.length == 0 && !loadingFavourites">
            <img src="../assets/img/book.png" alt="empty-feed">
            <span>Пока ничего нет :(</span>
        </div>

        <section class="feed-content" v-if="favouritePaintingsList.length > 0 && !loadingFavourites">
            <PaintingCard v-for="painting in favouritePaintingsList" :key="painting.painting_id" :painting="painting"/>
        </section>
    </div>

    <div v-if="currentTabId == 'my_works'">
        <section class="feed-content" v-if="loadingMy">
            <SkeletonLoader v-for="n in 6" :key="n" style="width: 100%; height: 294px;" />
        </section>

        <div class="messageBox" v-if="paintingsListMy.length == 0 && !loadingMy">
            <img src="../assets/img/book.png" alt="empty-feed">
            <span>Пока ничего нет :(</span>
        </div>

        <section class="feed-content" v-if="paintingsListMy.length > 0 && !loadingMy">
            <PaintingCard v-for="painting in paintingsListMy" :key="painting.painting_id" :painting="painting"/>
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
            menuTab: { id: 'favourites', label: 'Избранное' },
            loadingFavourites: false,
            loadingMy: false,
        }
    },
    async mounted() {
        this.loadingFavourites = true;
        this.loadingMy = true;
        try {
            await this.profileStore.getFavouritePaintingsList();
            await this.profileStore.getMyPaintingsList();
        } catch (error) {
            console.error('Ошибка загрузки данных:', error);
        } finally {
            this.loadingFavourites = false;
            this.loadingMy = false;
        }
    },
    methods:{
        async setTab(tab) {
            // tab может быть объектом { id: 'favourites', label: 'Избранное' } или строкой
            const tabId = typeof tab === 'object' && tab !== null ? tab.id : tab;
            
            if (tabId === 'favourites') {
                this.loadingFavourites = true;
                try {
                    await this.profileStore.getFavouritePaintingsList();
                } catch (error) {
                    console.error('Ошибка загрузки избранного:', error);
                } finally {
                    this.loadingFavourites = false;
                }
            } else if (tabId === 'my_works') {
                this.loadingMy = true;
                try {
                    await this.profileStore.getMyPaintingsList();
                } catch (error) {
                    console.error('Ошибка загрузки моих работ:', error);
                } finally {
                    this.loadingMy = false;
                }
            }
            
            this.$router.push({ name: 'Profile', params: { tab } })
        },
    },
    computed: {
        ...mapStores(useProfileStore),
        favouritePaintingsList(){
            return this.profileStore.favouritePaintingsList;
        },
        paintingsListMy(){
            return this.profileStore.myPaintingsList;
        },
        currentTabId() {
            // Извлекаем id из menuTab (может быть объектом или строкой)
            if (typeof this.menuTab === 'object' && this.menuTab !== null) {
                return this.menuTab.id;
            }
            return this.menuTab;
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
