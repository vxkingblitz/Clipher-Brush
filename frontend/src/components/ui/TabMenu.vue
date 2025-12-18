<template>
    <div class="menu-container">
        <div class="menu">
            <slot name="before-tabs"></slot>
            <button 
                v-for="tab in tabs" 
                :key="getTabKey(tab)"
                @click="setActiveTab(tab)"
                :style="getTabStyle(tab)"
                class="tab-button"
            >
                <slot name="tab-content" :tab="tab" :isActive="isTabActive(tab)">
                    <span class="tab-label">{{ getTabLabel(tab) }}</span>
                </slot>
            </button>
            <slot name="after-tabs"></slot>
        </div>
    </div>
</template>

<script>
export default {
    name: 'TabsMenu',
    props: {
        tabs: {
            type: Array,
            required: true,
            default: () => [
                { id: 'tab1', label: 'Вкладка 1' },
                { id: 'tab2', label: 'Вкладка 2' },
                { id: 'tab3', label: 'Вкладка 3' },
            ],
        },
        modelValue: {
            // Можно строкой или числом или объектом (любой тип)
            default: null
        },
        tabKey: {
            // Ключ для идентификации вкладки (например: 'id', 'category_id')
            type: String,
            default: 'id'
        },
        tabLabel: {
            // Ключ для отображения названия вкладки (например: 'label', 'name')
            type: String,
            default: 'label'
        }
    },
    emits: ['update:modelValue', 'tab-change'],
    data() {
        return {
            active: this.modelValue
        }
    },
    watch: {
        modelValue(newVal) {
            this.active = newVal
        }
    },
    methods: {
        getTabKey(tab) {
            // Возвращает значение уникального ключа вкладки
            return tab[this.tabKey] ?? tab.id ?? tab.category_id ?? tab.name ?? JSON.stringify(tab);
        },
        getTabLabel(tab) {
            // Возвращает отображаемый лейбл вкладки
            return tab[this.tabLabel] ?? tab.label ?? tab.name ?? '';
        },
        setActiveTab(tab) {
            window?.Telegram?.WebApp?.HapticFeedback?.impactOccurred?.('light');
            this.active = tab;
            this.$emit('update:modelValue', tab);
            this.$emit('tab-change', tab);
        },
        isTabActive(tab) {
            // Сравнивает текущую активную вкладку
            if (typeof this.active === 'object' && this.active !== null) {
                // Если модель — объект, сравниваем по уникальному ключу
                return this.getTabKey(tab) == this.getTabKey(this.active);
            } else {
                return this.getTabKey(tab) == this.active;
            }
        },
        getTabStyle(tab) {
            return {
                color: this.isTabActive(tab) ? 'var(--color-white)' : 'var(--color-black)',
                backgroundColor: this.isTabActive(tab) ? 'var(--color-main)' : 'var(--color-white)'
            }
        }
    }
}
</script>

<style scoped>

.menu-container {
    position: relative;
    width: 100%;
    padding: 16px 0;
}

.menu {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 0 6px;
    width: 100%;
    position: relative;
    overflow-x: auto;
}


.menu button {
    transition: all .2s ease;
    font-size: 14px;
    font-weight: 400;
    font-family: 'Jost';
    border: 1px solid var(--color-main);
    height: 38px;
    border-radius: 19px;
    padding: 4px 10px;
    min-width: fit-content;
    position: relative;
    z-index: 1;
}
</style>