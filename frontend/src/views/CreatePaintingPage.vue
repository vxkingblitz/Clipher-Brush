<template>
    <div id="pageView" class="createWrapper">
        <h1 style="margin-bottom: 40px;" v-if="step == 1">Добро пожаловать в <br> создание волшебства!</h1>
        <h1 style="margin-bottom: 40px;" v-if="step == 2">Еще чуть-чуть :)</h1>
        <h1 style="margin-bottom: 40px;" v-if="step == 3">Создание шедевра!</h1>
        <h1 style="margin-bottom: 40px;" v-if="step == 4">Все готово!</h1>

        <div id="pageView" class="createContent" v-if="step == 1" @click="openFileInput()">
            <input 
                ref="fileInput" 
                type="file" 
                accept="image/jpeg,image/png,image/jpg" 
                style="display: none;" 
                @change="handleFileSelect"
            />
            <div class="addPhoto" v-if="!formData.photo">
                <img src="../assets/img/brush.png" alt="brush">
                <h2>Создай свой рисунок</h2>
                <p>Добавь свое изоюражение сюда и начнется магия</p>
                <span>jpg, png</span>
            </div>
            <div v-else style="display: flex; flex-direction: column; gap: 30px; align-items: center; justify-content: center;">
                <img :src="photoPreview" alt="photo_for_drawing" class="imagePreview">
                <div class="actions">
                    <ButtonComponent :variant="1" :label="'Далее'" @click.stop="handleHapticFeedback(); step = 2" :isLoading="false"/>
                    <ButtonComponent :variant="3" :label="'Изменить изображение'" @click.stop="handleHapticFeedback(); openFileInput()" :isLoading="false"/>
                </div>
            </div>
        </div>


        <div id="pageView" class="createContent" v-if="step == 2">
            <img class="imagePreview" :src="photoPreview" alt="photo_for_drawing">
            <div class="actions">
                <InputField
                    :required="true"
                    :type="'tel'"
                    :placeholder="'Введите количество цветов'"
                    v-model="formData.colors_amount"
                />
                <SelectList
                    :options="markersSetsOptions"
                    :searchable="false"
                    :placeholderdata="'Выберите набор маркеров'"
                    v-model="formData.markers_set"
                    :disabled="markersSetsLoading"
                />
                <ButtonComponent :variant="1" :label="'Создать раскраску'" @click="handleHapticFeedback(); step = 3; generatePainting()" :isLoading="false" :disabled="!formData.colors_amount || !formData.markers_set"/>
            </div>
        </div>

        <div id="pageView" class="createContent" v-if="step == 3">
            <img class="imagePreview" :src="photoPreview" alt="photo_for_drawing">
            <h4>Генерация изображения</h4>
            <div class="loadingStatusWrapper">
                <div class="loadingStatusActive" :class="{ 'error': hasError }" :style="{ width: loadingProgress + '%' }"></div>
            </div>
            <span>{{ loadingText }}</span>
        </div>

        <div id="pageView" class="createContent" v-if="step == 4">
            <img class="imagePreview resultImage" :src="resultImage" alt="result">
            <h4>Раскраска готова!</h4>
            <div class="actions">
                <div class="checkbox-wrapper">
                    <input 
                        type="checkbox" 
                        id="publishCheckbox" 
                        v-model="shouldPublish"
                        @change="handleHapticFeedback()"
                    />
                    <label for="publishCheckbox">Опубликовать?</label>
                </div>
                
                <div v-if="shouldPublish" class="publish-section">
                    <SelectList
                        :options="categoriesOptions"
                        :searchable="false"
                        :placeholderdata="'Выберите категорию'"
                        v-model="selectedCategory"
                    />
                    <ButtonComponent 
                        :variant="1" 
                        :label="'Опубликовать'" 
                        @click="handlePublish()" 
                        :isLoading="isPublishing"
                        :disabled="!selectedCategory"
                    />
                </div>
                
                <ButtonComponent :variant="1" :label="'В ленту'" @click="goToFeed()" :isLoading="false"/>
                <ButtonComponent :variant="3" :label="'Создать ещё'" @click="resetForm()" :isLoading="false"/>
            </div>
        </div>
    </div>
</template>

<script>
import { useGeneratorStore } from '../stores/paintingGenerateStore'
import { useFeedStore } from '../stores/feedStore'
import { mapStores } from 'pinia'

export default {
    data(){
        return{
            photoPreview: null,
            step: 1,
            loadingProgress: 0,
            loadingText: 'Подбираем цвета...',
            resultImage: null,
            createdPainting: null,
            shouldPublish: false,
            selectedCategory: null,
            isPublishing: false,
            hasError: false,
            loadingInterval: null,

            formData:{
                photo: null,
                colors_amount: '',
                markers_set: null,
            },
        }
    },
    methods: {
        handleHapticFeedback() {
            if (window.Telegram?.WebApp?.HapticFeedback) {
                window.Telegram.WebApp.HapticFeedback.impactOccurred('light')
            }
        },
        openFileInput() {
            this.$refs.fileInput?.click();
        },
        handleFileSelect(event) {
            const file = event.target.files[0];
            if (file) {
                if (file.type === 'image/jpeg' || file.type === 'image/png' || file.type === 'image/jpg') {
                    this.formData.photo = file;
                    this.photo = true;
                    this.photoPreview = URL.createObjectURL(file);
                } else {
                    alert('Пожалуйста, выберите файл в формате JPG или PNG');
                }
            }
        },
        async generatePainting(){
            // Сбрасываем состояние ошибки
            this.hasError = false;
            
            // Формируем payload только с валидными значениями
            let payload = {
                photo: this.formData.photo,
                colors_amount: parseInt(this.formData.colors_amount) || 0,
            }
            
            // Добавляем category_id только если он есть и больше 0
            if (this.formData.category_id && parseInt(this.formData.category_id) > 0) {
                payload.category_id = parseInt(this.formData.category_id);
            }
            
            // Добавляем markers_set_id только если он есть и валидный
            // formData.markers_set - это объект из markersSetsOptions (с полями id, name, value)
            let markersSetId = null;
            if (this.formData.markers_set) {
                // Если это объект с полем value (наш формат)
                if (this.formData.markers_set.value && this.formData.markers_set.value.markers_set_id) {
                    markersSetId = this.formData.markers_set.value.markers_set_id;
                } 
                // Если это прямой объект набора маркеров
                else if (this.formData.markers_set.markers_set_id !== undefined) {
                    markersSetId = this.formData.markers_set.markers_set_id;
                }
                // Если markers_set_id равен null, это означает "Без набора"
                else if (this.formData.markers_set.markers_set_id === null) {
                    markersSetId = null; // Явно не передаем markers_set_id
                }
            }
            // Передаем markers_set_id только если он не null
            if (markersSetId !== null && markersSetId !== undefined) {
                payload.markers_set_id = markersSetId;
            }
            
            console.log('Sending payload:', payload);
            
            // Запускаем анимацию загрузки
            this.startLoadingAnimation();
            
            try {
                const result = await this.generatorStore.generatePainting(payload);
                console.log('Generation result:', result);
                
                // Останавливаем анимацию загрузки
                if (this.loadingInterval) {
                    clearInterval(this.loadingInterval);
                    this.loadingInterval = null;
                }
                
                this.createdPainting = result;
                // Используем colored или numbered изображение для показа результата
                this.resultImage = result.painting_colored || result.painting_numbered || this.photoPreview;
                
                this.loadingProgress = 100;
                this.loadingText = 'Готово!';
                
                setTimeout(async () => {
                    this.step = 4; // Переход на шаг "Все готово"
                    // Загружаем категории при переходе на шаг 4
                    await this.loadCategories();
                }, 500);
            } catch (error) {
                console.error('Ошибка генерации:', error);
                
                // Останавливаем анимацию загрузки
                if (this.loadingInterval) {
                    clearInterval(this.loadingInterval);
                    this.loadingInterval = null;
                }
                
                // Устанавливаем состояние ошибки
                this.hasError = true;
                this.loadingProgress = 100;
                this.loadingText = 'Произошла ошибка';
                
                // Через 3 секунды возвращаем на шаг выбора параметров
                setTimeout(() => {
                    this.step = 2;
                    this.hasError = false;
                    this.loadingProgress = 0;
                }, 3000);
            }
        },
        startLoadingAnimation() {
            this.loadingProgress = 0;
            this.loadingText = 'Загружаем изображение...';
            this.hasError = false;
            
            // Очищаем предыдущий интервал, если он есть
            if (this.loadingInterval) {
                clearInterval(this.loadingInterval);
            }
            
            const stages = [
                { progress: 20, text: 'Анализируем цвета...' },
                { progress: 40, text: 'Подбираем палитру...' },
                { progress: 60, text: 'Создаём контуры...' },
                { progress: 80, text: 'Нумеруем области...' },
                { progress: 95, text: 'Финальная обработка...' },
            ];
            
            let stageIndex = 0;
            this.loadingInterval = setInterval(() => {
                if (stageIndex < stages.length && this.step === 3 && !this.hasError) {
                    this.loadingProgress = stages[stageIndex].progress;
                    this.loadingText = stages[stageIndex].text;
                    stageIndex++;
                } else {
                    clearInterval(this.loadingInterval);
                    this.loadingInterval = null;
                }
            }, 2000);
        },
        goToFeed() {
            this.$router.push({ name: 'Feed', params: { tab: 'all' } });
        },
        resetForm() {
            // Останавливаем анимацию загрузки, если она активна
            if (this.loadingInterval) {
                clearInterval(this.loadingInterval);
                this.loadingInterval = null;
            }
            
            this.step = 1;
            this.photoPreview = null;
            this.resultImage = null;
            this.createdPainting = null;
            this.loadingProgress = 0;
            this.hasError = false;
            this.shouldPublish = false;
            this.selectedCategory = null;
            this.isPublishing = false;
            this.formData = {
                photo: null,
                colors_amount: '',
                markers_set: null,
            };
        },
        async loadCategories() {
            try {
                await this.feedStore.getCategoriesList();
            } catch (error) {
                console.error('Ошибка загрузки категорий:', error);
            }
        },
        async handlePublish() {
            if (!this.selectedCategory || !this.createdPainting) {
                return;
            }
            
            this.isPublishing = true;
            this.handleHapticFeedback();
            
            try {
                // Получаем category_id из выбранной категории
                // selectedCategory может быть объектом {category_id, name} или просто category_id
                let categoryId = null;
                if (typeof this.selectedCategory === 'object' && this.selectedCategory !== null) {
                    categoryId = this.selectedCategory.category_id;
                } else {
                    categoryId = this.selectedCategory;
                }
                
                if (!categoryId) {
                    alert('Пожалуйста, выберите категорию');
                    this.isPublishing = false;
                    return;
                }
                
                await this.generatorStore.publishPainting(
                    this.createdPainting.painting_id,
                    categoryId
                );
                
                alert('Раскраска успешно опубликована!');
                this.shouldPublish = false;
                this.selectedCategory = null;
            } catch (error) {
                console.error('Ошибка публикации:', error);
                alert('Произошла ошибка при публикации раскраски');
            } finally {
                this.isPublishing = false;
            }
        },
    },
    beforeUnmount() {
        // Останавливаем анимацию загрузки при размонтировании
        if (this.loadingInterval) {
            clearInterval(this.loadingInterval);
            this.loadingInterval = null;
        }
        
        if (this.photoPreview) {
            URL.revokeObjectURL(this.photoPreview);
        }
    },
    computed: {
        ...mapStores(useGeneratorStore),
        ...mapStores(useFeedStore),
        categoriesOptions() {
            return this.feedStore.categoriesList
        },
        markersSetsOptions() {
            return this.generatorStore.markersSets.map(set => ({
                id: set.markers_set_id || 'none',
                name: set.markers_set_id 
                    ? `${set.brand_name}, ${set.colors_amount}шт`
                    : set.brand_name,
                value: set  // Сохраняем весь объект для использования
            }))
        },
        markersSetsLoading() {
            return this.generatorStore.markersSetsLoading
        },
    },
    async mounted() {
        // Загружаем наборы маркеров при монтировании компонента
        await this.generatorStore.getMarkersSets()
    },
}
</script>

<style scoped>
h4{
    margin: 26px 0;
    font-size: 20px;
    font-weight: 500;
    color: var(--color-black);
}
span{
    font-size: 15px;
    font-weight: 500;
    color: var(--color-dark-gray);
}
.loadingStatusWrapper{
    position: relative;
    height: 20px;
    background-color: var(--color-light-gray);
    border-radius: 10px;
    overflow: hidden;
    width: 80vw;
}
.loadingStatusActive{
    position: absolute;
    height: 20px;
    background-color: var(--color-main);
    transition: width 0.5s ease-out;
}
.loadingStatusActive.error{
    background-color: #ff4444;
}
.imagePreview{
    object-fit: cover;
    width: 50vw;
    height: 40vh;
    border-radius: 32px;
}
.resultImage{
    width: 80vw;
    height: auto;
    max-height: 60vh;
    object-fit: contain;
}
.actions{
    width: 314px;
    display: flex;
    flex-direction: column;
    gap: 10px;
    justify-content: center;
}
.createWrapper{
    height: 100svh;
}
.createContent{
    display: flex;
    flex-direction: column;
    gap: 10px;
    align-items: center;
    justify-content: center;
}
.addPhoto{
    display: flex;
    flex-direction: column;
    gap: 8px;
    align-items: center;
    justify-content: center;
    border: 1px dashed var(--color-black);
    border-radius: 32px;
    width: 280px;
    aspect-ratio: 1;
}
.addPhoto h2{
    text-align: center;
    color: var(--color-black);
    margin: 0;
    font-weight: 500;
    font-size: 20px;
}
.addPhoto p{
    text-align: center;
    color: var(--color-dark-gray);
    margin: 0;
    font-weight: 400;
    font-size: 15px;
}
.addPhoto span{
    text-align: center;
    color: var(--color-blue);
    margin: 0;
    font-weight: 400;
    font-size: 12px;
    margin: 24px 0 10px 0
}
.checkbox-wrapper {
    display: flex;
    align-items: center;
    gap: 10px;
    width: 100%;
    padding: 10px 0;
}
.checkbox-wrapper input[type="checkbox"] {
    width: 20px;
    height: 20px;
    cursor: pointer;
    accent-color: var(--color-main);
}
.checkbox-wrapper label {
    font-family: 'Jost';
    font-size: 16px;
    color: var(--color-black);
    cursor: pointer;
    user-select: none;
}
.publish-section {
    width: 100%;
    display: flex;
    flex-direction: column;
    gap: 10px;
    animation: slideDown 0.3s ease-out;
}
@keyframes slideDown {
    from {
        opacity: 0;
        transform: translateY(-10px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}
</style>