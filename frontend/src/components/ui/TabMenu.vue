<template>
    <div class="menu-container">
        <div class="menu">
            <slot name="before-tabs"></slot>
            <button 
                v-for="tab in tabs" 
                :key="tab.id"
                @click="setActiveTab(tab.id)"
                :style="getTabStyle(tab.id)"
                class="tab-button"
            >
                <slot name="tab-content" :tab="tab" :isActive="isTabActive(tab.id)">
                    <span class="tab-label">{{ tab.label }}</span>
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
            validator: (value) => {
                return value.every(tab => tab.id && tab.label)
            }
        },

        modelValue: {
            type: String,
            default: 'tabname'
        },
    },
    
    emits: ['update:modelValue', 'tab-change'],
    
    data() {
        return {
            activeTab: this.modelValue
        }
    },
    
    watch: {
        modelValue(newVal) {
            this.activeTab = newVal
        }
    },
    
    methods: {
        setActiveTab(tabId) {
            this.activeTab = tabId
            this.$emit('update:modelValue', tabId)
            this.$emit('tab-change', tabId)
        },
        
        isTabActive(tabId) {
            return this.activeTab === tabId
        },
        
        getTabStyle(tabId) {
            return {
                color: this.isTabActive(tabId) ? 'var(--color-white)' : 'var(--color-black)',
                backgroundColor: this.isTabActive(tabId) ? 'var(--color-main)' : 'var(--color-white)'
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