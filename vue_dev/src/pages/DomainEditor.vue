<script>
export default {
    name: 'DomainEditor',
    view: 'SME',
    friendly_name: "Domain Editor",
    icon: "/static/assets/icon-DomainEditor.png",
    props: {
        msg: String
    }
}
</script>

<script setup>
import NewConceptModal from "../components/NewConceptModal.vue";
import DomainDag from "../components/domain_dag/DomainDag.vue"
import DomainDagUtilities from "../utils/DagUtils.js"
import ModuleMenu from "../components/module_menu/ModuleMenu.vue"
import LoadingWheel from "@/components/LoadingWheel.vue";

import DomainMenu from "@/components/domain_dag/DomainMenu.vue";
import ConceptSearch from '@/components/domain_dag/ConceptSearch.vue'

import axios from "axios";
import { ref, onBeforeMount } from "vue"

const tool_domain = window.contextData.tool_domain
let moduleItems = []

let dagUtil = new DomainDagUtilities()

onBeforeMount(async () => {
    axios.get(`${tool_domain}/module/course`).then((response) => {
        moduleItems = Object.values(response.data)

        let moduleIds = moduleItems.map(item => item.module_id)
        console.log(moduleIds)
        if (moduleIds.length > 0){
            const params = new URLSearchParams()
            params.append("list_of_ids", moduleIds.join(","))
    
            axios.get(`${tool_domain}/concept/from_modules`, {params}).then((response) => {
                let nodes = response.data
                const conceptParams = new URLSearchParams()
                conceptParams.append("list_of_names", Object.keys(nodes).join("|"))
    
                axios.get(`${tool_domain}/concept/cc/many`, {"params": conceptParams}).then((response) => {
                    dagUtil.initialize(nodes, response.data)
    
                })
            })
        }
    })
})

const defaultSettings = {
    nodeColor: "#00629B",
    focusColor: "#ffdd00",
    moduleColor: "#FC8900",
    edgeColor: "",
    textColor: "#00000",
    nodeSize: 30,
    selectable: true,
    hoverable: true,
    focusRing: true,
    showModules: true
}

function getColor(node, mode = "node") {
    let color = defaultSettings.nodeColor
    if (node.params.focusColor) {
        color = node.params.focusColor
    }
    else if (dagUtil.selectedNodes.value.includes(node.id)) {
        color = defaultSettings.focusColor
    }
    else if (node.module.includes(dagUtil.selectedModule.value)) {
        color = defaultSettings.moduleColor
    }
    if (mode === "label")
        return {
            visible: true,
            color: color,
            padding: 2,
            borderRadius: 5
        }
    else {
        return color
    }
}

const modalOpen = ref(false)
const isMenuOpen = ref(false)

console.log(dagUtil.is_initialized.value)

function clearParams() {
    dagUtil.updateNodes(dagUtil.focusNode.value, false, "params", {})
    dagUtil.updateFocusNodes("clear")
}

function onNodeSelect(node) {
    if (node.length === 1) {
        clearParams()
        dagUtil.updateNodes(node[0], true, "focusColor", "#f55d42")
        dagUtil.updateFocusNodes("push", node[0])
        }
    if (node.length === 0) {
        clearParams()
    }
    dagUtil.updateSelectedNodes("update", node)
    
}

function onDomainMenuEmit(event) {
    switch (event) {
        case "deleteConcepts":
            dagUtil.deleteSelectedNodes()
            break;
        case "addConcept":
            modalOpen.value = true
            break;
        case "joinConcepts":
            dagUtil.addSelectedEdges()
            break;
        case "moduleConceptAdd":
            dagUtil.addSelectedNodesToModule()
            break;
        case "junctionDelete":
            dagUtil.deleteSelectedEdges()
            break;
        case "moduleConceptDelete":
            dagUtil.RemoveSelectedNodesFromModule()
            break;
        case "transitiveReduction":
            dagUtil.transitiveReduction()
            break;
    }
}

</script>

<template>
    <div class="domain-editor" v-if="dagUtil.is_initialized.value">
        <div class="left-section" :data-state="isMenuOpen ? 'min' : 'max'">
            <div class="menu-collapse" @click="isMenuOpen = !isMenuOpen">
                <img src="/static/assets/icon-chevron.png"/>
            </div>
            <div class="graph roboto-bold">
                <DomainDag 
                    :nodes="dagUtil.nodes.value" 
                    :edges="dagUtil.edges.value" 
                    :focus-node="dagUtil.focusNode.value"
                    :selectedNodes="dagUtil.selectedNodes.value" 
                    :selectedModule="dagUtil.selectedModule.value"
                    :defaultSettings="defaultSettings"
                    :selected-edges="dagUtil.selectedEdges.value"
                    :getColor="getColor"

                    @onNodeSelect="onNodeSelect"
                    @onEdgeSelect="dagUtil.updateSelectedEdges"

                    >
                    <template #default="{boxSelect, updateLayout}">
                        <div class="menu-wheel">
                            <DomainMenu 
                                :selected-concepts="dagUtil.selectedNodes.value"
                                :selected-edges="dagUtil.selectedEdges.value"
                                :selected-module="dagUtil.selectedModule.value"
                                @box-select="boxSelect"
                                @emitHandler="onDomainMenuEmit"
                            />
                        </div>
                            <div class="display-options">
                                <div class="options-menu">
                                    <img title="Refresh Layout" aria-label="Refresh Layout" class="refresh-btn-icon"
                                    src="/static/assets/loading-icon.png" @click="updateLayout('BT')" />
                                    <img title="Undo" aria-label="Undo" class="refresh-btn-icon" src="/static/assets/icon-undo.png"
                                    @click="dagUtil.undoChange" />
                                    <img title="Redo" aria-label="Redo" class="refresh-btn-icon" src="/static/assets/icon-redo.png"
                                    @click="dagUtil.redoChange" />
                                </div>
                                <ConceptSearch 
                                    :concepts="dagUtil.nodes.value" 
                                    :selected-concepts="dagUtil.selectedNodes.value"
                                    @updateSelectedNodes="dagUtil.updateSelectedNodes"
                                />
                        </div>
                    </template>
                </DomainDag>
            </div>
            <NewConceptModal @add-node="dagUtil.addNode" @update-open="val => modalOpen = val" :modal-open="modalOpen" />
        </div>
        <div class="right-section" :data-state="isMenuOpen ? 'max' : 'min'">
            <ModuleMenu 
                :concepts="dagUtil.nodes.value" 
                :selected-concepts="dagUtil.selectedNodes"
                :module-items="moduleItems"
                @update-selected-module="dagUtil.updateSelectedModule" 
                @update-selected-nodes="dagUtil.updateSelectedNodes"
                @save-domain="dagUtil.saveDomain" 
                @add-file="dagUtil.uploadDomain"
                />
        </div>
        <div v-if="dagUtil.saving.value" class="save-overlay">
        </div>
    </div>
    <div class="domain-editor" v-else>
        <LoadingWheel :loading-text="'Loading...'"/>

    </div>
</template>

<style scoped>

.menu-collapse {
    position: absolute;
    top: calc(50% - 2rem);
    right:-1rem;
    width: 2rem;
    height: 4rem;
    z-index: 999;
    background-color: var(--core-primary);
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 8px;
}

.menu-collapse > img {
    height: 100%;
}
.left-section[data-state='max'] > .menu-collapse > img {
    transform: rotate(270deg);
    transition: transform .5s ease-out;
}

.left-section[data-state='min'] > .menu-collapse > img {
    transform: rotate(90deg);
    transition: transform .5s ease-out;
}
.save-overlay {
    position: relative;
    top: 0;
    left: 0;
    background-color: rgba(128, 128, 128, 0.508);
    width: 100vw;
    height: 100vh;
    z-index: 999;
}

.domain-editor {
    display: flex;
    flex-direction: row;
    height: 100% !important;
    width: 100%;
    min-height: 100% !important;
}

.left-section[data-state='max'] {
    animation: slide-out 1s ease-out;
    width: 100%;
}
.left-section[data-state='min'] {
    width: 75%;
    animation: slide-in 1s ease-out;
}
.left-section {
    position: relative;
}
@keyframes slide-out {
    from {
        width: 75%;
    }
    to {
        width: 100%;
    }
}

@keyframes slide-in {
    from {
        width: 100%;
    }
    to {
        width: 75%;
    }
}

@keyframes slide-out-menu {
    from {
        width: 0%;
        visibility: collapse;
    }
    to {
        width: 25%;
        visibility: visible;
    }
}

@keyframes slide-in-menu {
    from {
        width: 25%;
        visibility: visible;
    }
    to {
        width: 0%;
        visibility: collapse;
    }
}
.right-section {
    box-shadow: 1px 1px 2px 0px rgb(169, 169, 169);
    display: flex;
    flex-direction: column;
    align-items: center;
    overflow: hidden;
    background-color: var(--bg-color);
    border-radius: 8px;
}

.right-section[data-state='min'] {
    width: 0%;
    margin-left: 0px;
    padding-top: 0.5rem;
    padding-bottom: 0.5rem;
    visibility: collapse;
    animation: slide-in-menu 1s ease-out;
}

.right-section[data-state='max'] {
    margin-left: 5px;
    padding: .5rem;
    width: 25%;
    animation: slide-out-menu 1s ease-out;
}

.bottom-menu {
    margin: .5rem;
}

.graph {
    height: 100%;
    position: relative;
    top: 0;
    left: 0;

}

.display-options {
    position: absolute;
    display: flex;
    flex-direction: column;
    top: 32px;
    left: 6px;
    z-index: 999;
    width: 10rem;
    
}
.options-menu {
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: center;
}


.menu-wheel {
    position: absolute;
    display: flex;
    flex-direction: column;
    bottom: 6px;
    left: 6px;
    align-items: center;
    justify-content: center;
}

.refresh-btn-icon {
    border-radius: 50%;
    width: 2rem;
    aspect-ratio: 1/1;
    text-align: center;
    padding: 0;
    color: #C69214;
    margin: 1px;
    position: relative;
}

.refresh-btn-icon:hover {
    border: 1px solid #c6911400;
}

.refresh-btn-icon:active {
    border: 2px groove #C69214;
}
</style>
