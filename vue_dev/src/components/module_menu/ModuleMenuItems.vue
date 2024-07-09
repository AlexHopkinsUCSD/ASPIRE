<script setup>
import { defineProps, defineEmits, ref, watch } from 'vue';
import { ListboxContent, ListboxItem, ListboxItemIndicator, ListboxRoot } from 'radix-vue'
const emit = defineEmits(["updateSelectedNodes"])
const props = defineProps(["moduleSummary", "concepts", 'selectedConcepts'])
const selectedConcepts = ref([])

watch(props.selectedConcepts, (newVal) => {
    selectedConcepts.value.value = Object.values(newVal)
})

</script>
<template>
        <p class="module-summary">{{ props.moduleSummary }}</p>
        <hr style="width: 100%; border-color: var(--gold-line-color);"/>
        <div class="module-header">
            <p class="roboto-bold">Module Concepts:</p>
            <div class="icon-box">
                <img class="module-icon" src="/static/assets/icon-add.png"/>
                <img class="module-icon" src="/static/assets/delete.png"/>
            </div>

        </div>
        <ListboxRoot
            class="list-root"
            v-model="selectedConcepts.value"
            @update:model-value="(value) => emit('updateSelectedNodes', Object.values(value))"
            multiple
        >
            <ListboxContent
                class="concept-box"
            >
                <ListboxItem
                    v-for="concept in props.concepts"
                    :key="concept.id"
                    :value="concept.id"
                    class="concept-item"
                >
                    <span>{{concept.name}}</span>
                    <ListboxItemIndicator />
                </ListboxItem>
            </ListboxContent>
        </ListboxRoot>

</template>
<style scoped>

.module-summary{
    /* box-shadow: 1px 1px 5px -2px #ffffff; */
    padding: .5rem;
}

p {
    margin: 0;
    /* background-color: white; */
}
.module-header {
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: space-between;
    height: 2rem;
    padding-bottom: 0.5rem;
}

.icon-box {
    height: 100%;
    display: flex;
    align-items: center;
}

.module-icon {
    height: 100%;
    aspect-ratio: 1/1;
    text-align: center;
    padding: 0;
    border-radius: 50%;
    display: fixed;
    align-items: center;
    justify-content: center;
    margin: 1px;
    position: relative; 
    /* border: 1px solid transparent; */
}

.module-icon:hover {
    /* border: 1px solid var(--gold-line-color); */
    box-shadow: 0px 0px 3px 1px var(--gold-line-color) inset;
}
.list-root {
    box-shadow: 1px 1px 5px -2px #000000;
}
.concept-box {
    display: flex;
    flex-direction: column;
    /* background-color: white; */
}
.concept-item {
    user-select: none;
    border-bottom: 1px solid var(--gold-line-color);
    font-size: 1rem;
    color: var(--text-muted)
}
.concept-item:hover {
    font-weight: bold;
    color: var(--text-color)
}
.concept-item[data-state="checked"] {
    background-color: #7aff9e;
    font-weight: bold;
    color: var(--text-color)

}
</style>