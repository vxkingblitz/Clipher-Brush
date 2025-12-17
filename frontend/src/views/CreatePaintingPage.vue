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
                    :options="markers_list"
                    :searchable="false"
                    :placeholderdata="'Выберите набор маркеров'"
                    v-model="formData.markers_set"
                />
                <ButtonComponent :variant="1" :label="'Создать раскраску'" @click="handleHapticFeedback(); step = 3; generatePainting()" :isLoading="false" :disabled="!formData.colors_amount || !formData.markers_set"/>
            </div>
        </div>

        <div id="pageView" class="createContent" v-if="step == 3">
            <img class="imagePreview" :src="photoPreview" alt="photo_for_drawing">
            <h4>Генерация изображения</h4>
            <div class="loadingStatusWrapper">
                <div class="loadingStatusActive" :style="{ width: loadingProgress + '%' }"></div>
            </div>
            <span>{{ loadingText }}</span>
        </div>

        <div id="pageView" class="createContent" v-if="step == 4">
            <img class="imagePreview resultImage" :src="resultImage" alt="result">
            <h4>Раскраска готова!</h4>
            <div class="actions">
                <ButtonComponent :variant="1" :label="'В ленту'" @click="goToFeed()" :isLoading="false"/>
                <ButtonComponent :variant="3" :label="'Создать ещё'" @click="resetForm()" :isLoading="false"/>
            </div>
        </div>
    </div>
</template>

<script>
import { useGeneratorStore } from '../stores/paintingGenerateStore'
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

            formData:{
                photo: null,
                colors_amount: '',
                markers_set: '',
            },

            markers_list:[
                'Без набора',
                'GuangNa, 240шт',
                'GuangNa, 120шт',
                'GuangNa, 64шт',
                'GuangNa, 32шт',
                'Languo , 240шт',
                'Languo , 120шт',
                'Languo , 64шт',
                'Languo , 32шт',
            ]
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
            // Пока markers_set - это строка из списка, нужно будет загружать реальные ID из API
            // Временно не передаем markers_set_id, будет использоваться дефолтная палитра
            // TODO: загрузить markers-sets из API и использовать реальные ID
            
            console.log('Sending payload:', payload);
            
            // Запускаем анимацию загрузки
            this.startLoadingAnimation();
            
            try {
                const result = await this.generatorStore.generatePainting(payload);
                console.log('Generation result:', result);
                
                this.createdPainting = result;
                // Используем colored или numbered изображение для показа результата
                this.resultImage = result.painting_colored || result.painting_numbered || this.photoPreview;
                
                this.loadingProgress = 100;
                this.loadingText = 'Готово!';
                
                setTimeout(() => {
                    this.step = 4; // Переход на шаг "Все готово"
                }, 500);
            } catch (error) {
                console.error('Ошибка генерации:', error);
                alert('Произошла ошибка при создании раскраски');
                this.step = 2; // Возврат на шаг выбора параметров
            }
        },
        startLoadingAnimation() {
            this.loadingProgress = 0;
            this.loadingText = 'Загружаем изображение...';
            
            const stages = [
                { progress: 20, text: 'Анализируем цвета...' },
                { progress: 40, text: 'Подбираем палитру...' },
                { progress: 60, text: 'Создаём контуры...' },
                { progress: 80, text: 'Нумеруем области...' },
                { progress: 95, text: 'Финальная обработка...' },
            ];
            
            let stageIndex = 0;
            const interval = setInterval(() => {
                if (stageIndex < stages.length && this.step === 3) {
                    this.loadingProgress = stages[stageIndex].progress;
                    this.loadingText = stages[stageIndex].text;
                    stageIndex++;
                } else {
                    clearInterval(interval);
                }
            }, 2000);
        },
        goToFeed() {
            this.$router.push({ name: 'Feed', params: { tab: 'all' } });
        },
        resetForm() {
            this.step = 1;
            this.photoPreview = null;
            this.resultImage = null;
            this.createdPainting = null;
            this.loadingProgress = 0;
            this.formData = {
                photo: null,
                colors_amount: '',
                markers_set: '',
            };
        },
    },
    beforeUnmount() {
        if (this.photoPreview) {
            URL.revokeObjectURL(this.photoPreview);
        }
    },
    computed: {
        ...mapStores(useGeneratorStore),
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
</style>