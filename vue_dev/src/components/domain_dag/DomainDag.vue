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
// import VNetworkGraph from "v-network-graph"
import dagre from "dagre/dist/dagre.min.js"
import DomainMenu from "./DomainMenu.vue"


const props = defineProps([
    "nodes",
    "edges",
    "selectedNodes",
    "focusNode",
    "defaultSettings",
    "selectedModule",
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
    "moduleConceptDelete"
])

const hovered = ref(null)

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
    else if (node.module === props.selectedModule) {
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

// let x = 0
// function getColor(node, mode="node") {
//     x++
//     console.log(`Count: ${x} - Node: ${node.id}`)
//     return props.defaultSettings.nodeColor
// }

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
    console.log(node)
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
            onBeforeInitialDisplay: () => layout("BT"),
            layoutHandler: new minLayout()
        },
        node: {
            selectable: props.defaultSettings.selectable,
            normal: {
                type: "circle",
                radius: props.defaultSettings.nodeSize / 2,
                strokeWidth: 0,
                strokeColor: "#000000",
                strokeDasharray: "0",
                color: node => getColor(node)
            },
            label: {
                direction: "north",
                color: props.defaultSettings.textColor,
                fontSize: 12,
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
                color: "#aaa",
                width: 3,
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
            radius: props.defaultSettings.nodeSize / 2,
            strokeWidth: 0,
            strokeColor: "#000000",
            strokeDasharray: "0",
            color: node => getColor(node)
        }
        config.node.hover = {
            type: "circle",
            radius: (props.defaultSettings.nodeSize / 2) + 8,
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
    console.log('config complete')
    return config
}

const configs = reactive(vNG.defineConfigs(compileConfig()))

const graph = ref(vNG.VNetworkGraphInstance)

function layout(direction) {
    console.log("layout fired")
    if (Object.keys(props.nodes).length <= 1 || Object.keys(props.edges).length == 0) {
        return
    }
    // convert graph
    // ref: https://github.com/dagrejs/dagre/wiki
    const g = new dagre.graphlib.Graph()
    // Set an object for the graph label
    g.setGraph({
        rankdir: direction,
        nodesep: props.defaultSettings.nodeSize * 2,
        edgesep: props.defaultSettings.nodeSize,
        ranksep: props.defaultSettings.nodeSize * 2,
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

    g.nodes().forEach((nodeId) => {
        if (g.node(nodeId)) {
            const x = g.node(nodeId).x
            const y = g.node(nodeId).y
            layouts.nodes[nodeId] = { x, y }
        }
    })
    console.log("layout complete")
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

const eventHandlers = {
    "node:pointerover": (node) => {
        hovered.value = node.node
    },
    "node:pointerout": (_) => {
        hovered.value = null
    },
    "node:select": (node) => {
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
        <v-network-graph ref="graph" :nodes="props.nodes" :edges="props.edges" :layouts="layouts" :configs="configs"
            :event-handlers="eventHandlers" />
        <div class="options-menu">
            <img title="Refresh Layout" aria-label="Refresh Layout" class="refresh-btn-icon"
                src="/static/assets/loading-icon.png" @click="updateLayout('BT')" />
            <img title="Undo" aria-label="Undo" class="refresh-btn-icon" src="/static/assets/icon-undo.png"
                @click="emit('undo')" />
            <img title="Redo" aria-label="Redo" class="refresh-btn-icon" src="/static/assets/icon-redo.png"
                @click="emit('redo')" />
        </div>
        <div class="menu-wheel">
            <DomainMenu :emit="emit" />
        </div>
    </div>
</template>

<style scoped>
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
    position: absolute;
    display: flex;
    flex-direction: column;
    width: 4%;
    top: 6px;
    right: 6px;
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
    width: 75%;
    aspect-ratio: 1/1;
    text-align: center;
    padding: 0;
    color: #C69214;
    display: fixed;
    align-items: center;
    justify-content: center;
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
