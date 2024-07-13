<script setup>
import ModuleMenuItems from './ModuleMenuItems.vue';
import { AccordionContent, AccordionHeader, AccordionItem, AccordionRoot, AccordionTrigger } from 'radix-vue'
import { defineProps, defineEmits } from 'vue';

const props = defineProps(["modules", "concepts", "selectedConcepts"])
const emit = defineEmits(["updateSelectedModule", "updateSelectedNodes", "saveDomain"])

const accordionItems = [
{
    module_id: 1,
    title: 'CSS - JavaScript - HTML',
    content_summary: 'Yes. It adheres to the WAI-ARIA design pattern.',
},
{
    module_id: 2,
    title: 'Best Practices + DOM Manipulation',
    content_summary: 'Yes. It\'s unstyled by default, giving you freedom over the look and feel.',
},
{
    module_id: 3,
    title: 'Styling',
    content_summary: 'Yes! You can use the transition prop to configure the animation.'
},
]

function moduleSelected(moduleId) {
    emit("updateSelectedModule", moduleId)
}

</script>

<template>
    <AccordionRoot
    class="module-accordion-container"
    type="single"
    :collapsible="true"
    @update:model-value="moduleSelected"
    >
    <h3 class="roboto-bold">Modules</h3>
        <template
        v-for="item in accordionItems"
        :key="item.module_id"
        >
            <AccordionItem
                class="module-accordion-item roboto-regular"
                :value="item.module_id"
            >
                <AccordionHeader class="module-accordion-header">
                    <AccordionTrigger class="module-accordion-trigger roboto-bold">
                        <span>{{ item.title }}</span>
                        <img 
                            src="/static/assets/icon-chevron.png"
                            class="dropdown-btn-icon"
                        />
                    </AccordionTrigger>
                </AccordionHeader>
                    <AccordionContent class="module-accordion-content">
                        <ModuleMenuItems 
                            :module-summary="item.content_summary"
                            :concepts="Object.values(props.concepts).filter(concept => concept.module.includes(item.module_id))"
                            :selected-concepts="props.selectedConcepts"
                            @update-selected-nodes="value => emit('updateSelectedNodes', 'update', value)"
                        />
                    </AccordionContent>
            </AccordionItem>
        </template>
    </AccordionRoot>
    <div class="save-tools">
        <img @click="emit('saveDomain')" class="domain-save-btn" src="/static/assets/icon-save.png"/>
    </div>
</template>

<style scoped>
h3 {
    margin-top: 8px;
    margin-bottom: 0;
    height: 2rem;
    color: var(--core-primary);
}
.module-accordion-container {
    width: 100%;
    height: 80%;
    overflow: hidden;
}
.module-accordion-item{
    background-color: var(--bg-color);
}
.module-accordion-item[data-state="open"]{
    max-height: calc(100% - 4rem);
    /* height: fit-content; */
    display: flex;
    flex-direction: column;
}

.module-accordion-header {
    margin: 0;
    width:100%;
}
.module-accordion-trigger {
    /* border-radius: 10px; */
    border: none;
    box-shadow: .5px .5px 4px 0px white;
    text-align: center;
    display: flex;
    align-items: center;
    justify-content: space-between;
    height: 2rem;
    width:100%;
    background-color: var(--core-primary);
    color: var(--accent-primary);
    font-weight: bold;
}
.module-accordion-trigger[data-state="open"] > .dropdown-btn-icon {
    transform: rotate(180deg);
    transition: 300ms linear;
}
.module-accordion-trigger[data-state="closed"] > .dropdown-btn-icon {
    transform: rotate(0deg);
    transition: 300ms linear;
}
.module-accordion-content {
    scrollbar-color: var(--accent-primary) var(--bg-color);
    scrollbar-width: thin;
    overflow-y: scroll;
    overflow-x: hidden;
}

.module-accordion-content[data-state="open"] {
    margin-top: 0.5rem;
    margin-bottom: 0.5rem;
    padding-left: 0.5rem;
    padding-right: 0.5rem;
    animation: slideDown 500ms ease-out;
}
.module-accordion-content[data-state="closed"] {
    animation: slideUp 500ms ease-out;
}

@keyframes slideDown {
from {
    height: 0;
    margin-top: 0rem;
    margin-bottom: 0rem;
    padding-left: 0rem;
    padding-right: 0rem;
}
to {
    height: var(--radix-accordion-content-height);
    margin-top: 0.5rem;
    margin-bottom: 0.5rem;
    padding-left: 0.5rem;
    padding-right: 0.5rem;
}
}

@keyframes slideUp {
from {
    height: var(--radix-accordion-content-height);
    margin-top: 0.5rem;
    margin-bottom: 0.5rem;
    padding-left: 0.5rem;
    padding-right: 0.5rem;
}
to {
    height: 0;
    margin-top: 0rem;
    margin-bottom: 0rem;
    padding-left: 0rem;
    padding-right: 0rem;
}
}
.dropdown-btn-icon {
    width: 10%;
    aspect-ratio: 1/1;
    text-align: center;
    padding: 0;

    display: fixed;
    align-items: center;
    justify-content: center;
    margin: 1px;
    position: relative; 
}

.save-tools {
    height: 20%;
}
.domain-save-btn {
    border-radius: 1rem;
}
.domain-save-btn:hover {
    box-shadow: 0px 0px 2px 0px var(--accent-primary) inset;
}
.domain-save-btn:active {
    background-color: #c691145c;
}

</style>