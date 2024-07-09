import { reactive, ref } from "vue";

export default class DomainDagUtilities {
    constructor(initialNodes={}, initialEdges={}) {
        this.nodes = reactive(initialNodes)
        this.edges = reactive(initialEdges)
        this.focusNode = ref()
        this.selectedNodes = ref([])
        this.selectedEdges = ref([])
        this.selectedModule = ref()
        this.changeHistory = []
        this.historyIndex = -1
        this.saving = ref(false)
    }
    
    
    test = () => {
        console.log(!(this.focusNode.value === 'strings'))
        console.log(this.selectedNodes.value.includes('strings'))
        console.log(this.selectedNodes.value.includes('strings') && !(this.focusNode.value === 'strings'))
        console.log(this.edges)
        console.log(this.changeHistory, this.historyIndex)
    }

    saveDomain = () => {
        this.saving.value = true
        const date = new Date().toDateString()
        const fileName = `domain_model_${date}.json`
        const currentDomain = {"nodes": this.nodes, "edges": this.edges}
        const blob = new Blob([JSON.stringify(currentDomain)], {type: "text/plain"})
        const downloadURL = window.URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = downloadURL;
        link.target = '_blank';
        link.download = fileName;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        this.saving = false
    }

    undoChange = () => {
        if (this.historyIndex > -1) {
            const lastAction = this.changeHistory[this.historyIndex]

            switch(lastAction.object) {
                case "edge":
                    if (lastAction.action === "delete") {
                        this.addEdge(lastAction.value, true)
                    } else {
                        const edgeId = `edge-${lastAction.value.target}-${lastAction.value.source}` 
                        this.deleteEdge(edgeId, true)
                    }
                    break;
                case "node":
                    if (lastAction.action === "delete") {
                        this.addNode({concept_name: lastAction.value}, true)
                    } else {
                        this.deleteNode(lastAction.value, true)
                    }
            }
            this.historyIndex --
        }
    }

    redoChange = () => {
        if (this.changeHistory.length > this.historyIndex + 1) {
            
            const lastAction = this.changeHistory[this.historyIndex + 1]

            switch(lastAction.object) {
                case "edge":
                    if (lastAction.action === "add") {
                        this.addEdge(lastAction.value, true)
                    } else {
                        const edgeId = `edge-${lastAction.value.target}-${lastAction.value.source}` 
                        this.deleteEdge(edgeId, true)
                    }
                    break;
                case "node":
                    if (lastAction.action === "add") {
                        this.addNode({concept_name: lastAction.value}, true)
                    } else {
                        this.deleteNode(lastAction.value, true)
                    }
            }
            this.historyIndex ++
        }
    }

    resetHistoryTail = () => {
        if (this.historyIndex === -1) {
            this.changeHistory = []
        } else {
            this.changeHistory.splice(this.historyIndex + 1)
        }
        
    }

    updateChangeHistory = (changeObj) => {
        if (this.historyIndex !== (this.changeHistory.length - 1)) {
            this.resetHistoryTail()
        }
        this.changeHistory.push(changeObj)
        this.historyIndex = this.changeHistory.length - 1
    }

    addNode = (node, isFromHistory=false) => {
        this.nodes[node.concept_name] = {name: node.concept_name, id: node.concept_name, module: null, params: {focusColor:"#4cff30"}}
        this.focusNode.value = node.concept_name
        if (!isFromHistory) {
            this.updateChangeHistory({object: "node", action: "add", value: node.concept_name})
        }
    }

    deleteNode = (nodeId, isFromHistory=false) => {
        if (!isFromHistory) {
            this.updateChangeHistory({object: "node", action: "delete", value: nodeId})
        }
        delete this.nodes[nodeId]
    }

    deleteSelectedNodes = () => {
        for (let nodeId of this.selectedNodes.value) {
            // We delete the edges first so the node deletion is at the end of the change history.
            // This ensures if a user decides to undo this action, the node returns first, then each edge after every subsequent undo action.
            this.deleteAllNodeEdges(nodeId)
            delete this.nodes[nodeId]
            this.updateChangeHistory({object: "node", action: "delete", value: nodeId})
        }
    }

    updateNodes = (node, is_param, key, value) => {
        if (!this.nodes[node]) {
        return
        }
        if (is_param) {
        this.nodes[node].params[key] = value
        } else {
        this.nodes[node][key] = value
        }
    }

    addEdge = (edge, isFromHistory=false) => {
        const newEdgeId = `edge-${edge.target}-${edge.source}`
        // const edgeValues = Object.keys(this.edges)
        if (!this.edges[newEdgeId]) {
            this.edges[newEdgeId] = edge
        }
        if (!isFromHistory) {
            this.updateChangeHistory({object: "edge", action: "add", value: edge})
        }
    }

    addSelectedEdges = () => {
        const edgeValues = Object.values(this.edges)
        for (let node in this.selectedNodes.value) {
            const newEdge = {source: this.selectedNodes.value[node], target: this.focusNode.value,}
            // checks if the new edge already exists and that the new edge doesn't contain nodes linked to themselves
            if (!edgeValues.some(node => JSON.stringify(node) === JSON.stringify(newEdge)) && newEdge.source !== newEdge.target) {
                this.edges[`edge-${newEdge.target}-${newEdge.source}`] = newEdge
                this.updateChangeHistory({object: "edge", action: "add", value: newEdge})
            }
        }
    }

    deleteEdge = (edgeId, isFromHistory=false) => {
        if (!isFromHistory) {
            this.updateChangeHistory({object: "edge", action: "delete", value: this.edges[edgeId]})
        }
        delete this.edges[edgeId]
    }

    deleteSelectedEdges = () => {
        for (let edgeId of this.selectedEdges.value) {
            this.updateChangeHistory({object: "edge", action: "delete", value: this.edges[edgeId]})
            delete this.edges[edgeId]
        }
    }

    deleteAllNodeEdges = (nodeId) => {
        // creates a list of edge ids containing the id of the node being deleted
        // edge id must be formatted as 'edge-{source node id}-{target node id}' for the split and filter statement to work properly
        const validEdgeIds = Object.keys(this.edges).filter(key => key.split("-").includes(nodeId))
        for (let edgeId of validEdgeIds) {
            this.updateChangeHistory({object: "edge", action: "delete", value: this.edges[edgeId]})
            delete this.edges[edgeId]
        }
    }

    updateFocusNodes = (mode, value=null) => {
        switch (mode) {
        case "push":
            this.focusNode.value = value
            break;
    
        default:
            this.focusNode.value = null
            break;
        }
    }

    updateSelectedNodes = (mode, value=null) => {
        console.log(value)
        switch (mode) {
        case "push":
            this.selectedNodes.value.push(value)
            break;

        case "update":
            this.selectedNodes.value = value
            break;
        default:
            this.selectedNodes.value = []
            break;
        }
    }

    updateSelectedEdges = (edge) => {
        this.selectedEdges.value = edge
    }

    updateSelectedModule = (moduleId) => {
        this.selectedModule.value = moduleId
    }
}