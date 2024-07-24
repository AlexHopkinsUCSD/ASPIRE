<script>
export default {
    name: 'DomainDag',
    friendly_name: "Domain Editor",
    icon: "/static/assets/icon-DomainEditor.png",
}
</script>
<script setup>
import { ref, toRef, reactive, defineProps, defineEmits } from 'vue';
import * as vNG from "v-network-graph"
import dagre from "dagre/dist/dagre.min.js"
import DomainMenu from "./DomainMenu.vue"
import DomainZoomSlider from "./DomainZoomSlider.vue"
import ConceptSearch from './ConceptSearch.vue'


const props = defineProps([
    "nodes",
    "edges",
    "selectedNodes",
    "focusNode",
    "defaultSettings",
    "selectedModule",
    "selectedEdges"
])
const emit = defineEmits([
    "updateNodes",
    "updateSelectedNodes",
    "updateFocusNodes",
    "updateSelectedEdges",
    "undo",
    "redo",
    "deleteConcepts",
    "addConcept",
    "joinConcepts",
    "moduleConceptAdd",
    "junctionDelete",
    "moduleConceptDelete",
    "transitiveReduction"
])

const hovered = ref(null)
const zoomLevel = ref(1)

const layouts = reactive({
    nodes: {},
})


function getColor(node, mode = "node") {
    let color = props.defaultSettings.nodeColor
    if (node.params.focusColor) {
        color = node.params.focusColor
    }
    else if (props.selectedNodes.includes(node.id)) {
        color = props.defaultSettings.focusColor
    }
    else if (node.module.includes(props.selectedModule)) {
        color = props.defaultSettings.moduleColor
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

function tempGetEdgeColor(edge) {
    if (props.selectedEdges.includes(`edge-${edge.source}-${edge.target}`)) {
        return "#dd8800"
    } else {
        return "#aaa"
    }
}

class minLayout {
    onDeactivate = () => null

    activate(parameters) {
        const { nodePositions, nodes, configs, emitter, scale, svgPanZoom } = parameters
        const onDrag = (positions) => {
            for (const [id, pos] of Object.entries(positions)) {
                const layout = this.getOrCreateNodePosition(nodePositions, id)
                this.setNodePosition(layout, pos)
            }
        }

        emitter.on("node:dragstart", onDrag)
        emitter.on("node:pointermove", onDrag)
        emitter.on("node:dragend", onDrag)

        this.onDeactivate = () => {
            emitter.off("node:dragstart", onDrag)
            emitter.off("node:pointermove", onDrag)
            emitter.off("node:dragend", onDrag)
        }
    }

    deactivate() {
        if (this.onDeactivate) {
            this.onDeactivate()
        }
    }

    setNodePosition(nodeLayout, pos) {
        nodeLayout.value.x = Math.round(pos.x, 3)
        nodeLayout.value.y = Math.round(pos.y, 3)
    }

    getOrCreateNodePosition(nodePositions, node) {
        const layout = toRef(nodePositions.value, node)
        if (!layout.value) {
            layout.value = { x: 0, y: 0 }
        }
        return layout
    }
}

function labelOverflow(node) {
    if (hovered.value === node.id || props.selectedNodes.includes(node.id)) {
        return node.name
    }
    else if (node.name.length > 18) {
        return node.name.slice(0, 15) + '...'
    } else {
        return node.name
    }
}

function compileConfig() {
    let config = {
        view: {
            autoPanAndZoomOnLoad: "fit-content",
            minZoomLevel: 0.1,
            maxZoomLevel: 3,
            onBeforeInitialDisplay: () => layout("BT"),
            layoutHandler: new minLayout()
        },
        node: {
            selectable: props.defaultSettings.selectable,
            normal: {
                type: "circle",
                radius: _ => (props.defaultSettings.nodeSize / 2) * zoomLevel.value,
                strokeWidth: 0,
                strokeColor: "#000000",
                strokeDasharray: "0",
                color: node => getColor(node)
            },
            label: {
                direction: "north",
                color: props.defaultSettings.textColor,
                fontSize: _ => 12 * zoomLevel.value,
                fontFamily: "Roboto",
                margin: 4,
                text: node => labelOverflow(node),
                background: {
                    visible: true,
                    color: "#ffffff",
                    padding: 0,
                    borderRadius: 5
                }
            },
            zOrder: {
                enabled: true,
                zIndex: 0,
                bringToFrontOnHover: true,   
                bringToFrontOnSelected: true, 
                }
        },
        edge: {
            selectable: props.defaultSettings.selectable,
            normal: {
                color: edge => tempGetEdgeColor(edge),
                width: _ => 3 * zoomLevel.value,
            },
            selected: {
                width: 3,
                color: "#dd8800",
                dasharray: "0",
                linecap: "round",
            },
            margin: 12,
            marker: {
                target: {
                    type: "arrow",
                    width: 4,
                    height: 4,
                }
            }
        }
    }

    if (props.defaultSettings.selectable) {
        config.node.selected = {
            type: "circle",
            radius: _ => (props.defaultSettings.nodeSize) * zoomLevel.value,
            strokeWidth: 0,
            strokeColor: "#000000",
            strokeDasharray: "0",
            color: node => getColor(node)
        }
        config.node.hover = {
            type: "circle",
            radius: _ => (props.defaultSettings.nodeSize / 2) * zoomLevel.value + 8,
            strokeWidth: 0,
            strokeColor: "#000000",
            strokeDasharray: "0",
            color: node => getColor(node)
        }
        config.node.focusring = {
            width: 4,
            padding: 3,
            dasharray: "0",
            color: "#000000"
        }
        // config.node.label.color = node => (
        //     props.selectedNodes.includes(node.id) && !(props.focusNode === node.id)
        //         ?
        //         "#fffff"
        //         :
        //         props.defaultSettings.textColor
        // )
        // config.node.label.background = node => getColor(node, "label")
    }
    return config
}


function layout(direction) {
    if (Object.keys(props.nodes).length <= 1 || Object.keys(props.edges).length == 0) {
        return
    }
    // convert graph
    // ref: https://github.com/dagrejs/dagre/wiki
    const g = new dagre.graphlib.Graph()
    // Set an object for the graph label
    g.setGraph({
        align: "UR",
        rankdir: direction,
        nodesep: props.defaultSettings.nodeSize * 2,
        edgesep: 0,
        ranksep: props.defaultSettings.nodeSize * 8,
        // ranker: "tight-tree",
        acyclicer: 'greedy'
    })
    // Default to assigning a new object as a label for each new edge.
    g.setDefaultEdgeLabel(() => ({}))

    // Add nodes to the graph. The first argument is the node id. The second is
    // metadata about the node. In this case we're going to add labels to each of
    // our nodes.
    Object.entries(props.nodes).forEach(([nodeId, node]) => {
        g.setNode(nodeId, { label: node.name, width: props.defaultSettings.nodeSize, height: props.defaultSettings.nodeSize })
    })

    // Add edges to the graph.
    Object.values(props.edges).forEach(edge => {
        g.setEdge(edge.source, edge.target)
    })
    dagre.layout(g)
    console.log(g)

    g.nodes().forEach((nodeId) => {
        if (g.node(nodeId)) {
            const x = g.node(nodeId).x
            const y = g.node(nodeId).y
            layouts.nodes[nodeId] = { x, y }
        }
    })
}

function updateLayout(direction) {
    graph.value?.transitionWhile(() => {
        layout(direction)
    })
    graph.value.panToCenter()
}

function clearParams() {
    emit("updateNodes", props.focusNode, false, "params", {})
    emit('updateFocusNodes', "clear")
}


const configs = reactive(vNG.defineConfigs(compileConfig()))

const graph = ref(vNG.VNetworkGraphInstance)

const isBoxSelectionMode = ref(false)

function startBoxSelection() {
    console.log("fired")
    graph.value?.startBoxSelection({
        stop: "click", // Trigger to exit box-selection mode
        type: "append", // Behavior when a node is within a selection rectangle
        withShiftKey: "invert", // `type` value if the shift key is pressed
    })
}

function stopBoxSelection() {
    console.log('fired2')
    graph.value?.stopBoxSelection()
}

const eventHandlers = {
    "view:mode": mode => {
    // Observe mode change events
    isBoxSelectionMode.value = mode === "box-selection"
    },
    "node:pointerover": (node) => {
        hovered.value = node.node
    },
    "node:pointerout": (_) => {
        hovered.value = null
    },
    "node:select": (node) => {
        console.log("selected")
        if (node.length === 1) {
            clearParams()
            emit("updateNodes", node[0], true, "focusColor", "#f55d42")
            emit('updateFocusNodes', "push", node[0])
        }
        if (node.length === 0) {
            clearParams()
        }
        emit("updateSelectedNodes", "update", node)
    },
    "edge:select": (edge) => {
        emit("updateSelectedEdges", edge)
    }
}

</script>

<template>
    <div class="graph-box">
        <v-network-graph 
            ref="graph" 
            :nodes="props.nodes" 
            :edges="props.edges" 
            :layouts="layouts" 
            :configs="configs"
            :event-handlers="eventHandlers" 
            v-model:zoom-level="zoomLevel"

        />
        <div class="menu-wheel">
            <DomainMenu 
                :emit="emit" 
                :selected-concepts="props.selectedNodes"
                :selected-edges="props.selectedEdges"
                :selected-module="props.selectedModule"
                @box-select="isBoxSelectionMode ? stopBoxSelection() : startBoxSelection()"
            />
        </div>
        <div class="display-options">
            <div class="options-menu">
                <img title="Refresh Layout" aria-label="Refresh Layout" class="refresh-btn-icon"
                src="/static/assets/loading-icon.png" @click="updateLayout('BT')" />
                <img title="Undo" aria-label="Undo" class="refresh-btn-icon" src="/static/assets/icon-undo.png"
                @click="emit('undo')" />
                <img title="Redo" aria-label="Redo" class="refresh-btn-icon" src="/static/assets/icon-redo.png"
                @click="emit('redo')" />
            </div>
            <DomainZoomSlider v-model:zoom-level="zoomLevel" />
            <ConceptSearch 
                :concepts="props.nodes" 
                :selected-concepts="props.selectedNodes"
                :emit="emit"
            />
        </div>
    </div>
</template>

<style scoped>
.display-options {
    position: absolute;
    display: flex;
    flex-direction: column;
    top: 6px;
    left: 6px;
    z-index: 999;
    width: 10rem;
    
}
.popover-test {
    display: flex;
    width: fit-content;
    position: relative;
    left: calc(60px + var(width));
    top: 380px;
}

.graph-box {
    position: relative;
    display: flex;
    flex-direction: column;
    width: 100%;
    height: 100%;
    background-color: var(--bg-color);
    box-shadow: 1px 1px 2px 0px rgb(169, 169, 169);
    border-radius: 8px;
    text-transform: capitalize;
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
