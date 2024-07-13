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
        this.settings = reactive({})
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

        this.saving.value = false
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
                        this.addNode(lastAction.value, true)
                    } else {
                        this.deleteNode(lastAction.value.id, true)
                    }
                    break;
                case "nodeToModule":
                    if (lastAction.action === "add") {
                        this.RemoveNodesFromModule(lastAction.value.nodeIds, lastAction.value.module, true)
                    } else (
                        this.addNodesToModule(lastAction.value.nodeIds, lastAction.value.module, true)
                    )
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
                        this.addNode(lastAction.value, true)
                    } else {
                        this.deleteNode(lastAction.value.id, true)
                    }
                    break;
                case "nodeToModule":
                    if (lastAction.action === "add") {
                        this.addNodesToModule(lastAction.value.nodeIds, lastAction.value.module, true)
                    } else (
                        this.RemoveNodesFromModule(lastAction.value.nodeIds, lastAction.value.module, true)
                    )
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
        this.nodes[node.id] = {name: node.name, id: node.id, module: node.module, params: {focusColor:"#4cff30"}}
        this.focusNode.value = node.id
        if (!isFromHistory) {
            this.updateChangeHistory({object: "node", action: "add", value: node})
        }
    }

    deleteNode = (nodeId, isFromHistory=false) => {
        if (!isFromHistory) {
            const node = this.nodes[nodeId]
            this.updateChangeHistory({object: "node", action: "delete", value: node})
        }
        delete this.nodes[nodeId]
    }

    deleteSelectedNodes = () => {
        for (let nodeId of this.selectedNodes.value) {
            // We delete the edges first so the node deletion is at the end of the change history.
            // This ensures if a user decides to undo this action, the node returns first, then each edge after every subsequent undo action.
            this.deleteAllNodeEdges(nodeId)
            const node = this.nodes[nodeId]
            delete this.nodes[nodeId]
            this.updateChangeHistory({object: "node", action: "delete", value: node})
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
        this.selectedEdges.value = []
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

    addNodesToModule = (nodes, module, isFromHistory=false) => {
        for (let node of nodes) {
            this.nodes[node].module.push(module)
        }
        if (!isFromHistory) {
            this.updateChangeHistory({object: "nodeToModule", action: "add", value: {nodeIds: nodes, module: module}})
        }
    }

    addSelectedNodesToModule = () => {
        const newModule = this.selectedModule.value
        for (let node of this.selectedNodes.value) {
            this.nodes[node].module.push(newModule)
        }
        this.updateChangeHistory({object: "nodeToModule", action: "add", value: {nodeIds: this.selectedNodes.value, module: newModule}})
    }

    RemoveNodesFromModule = (nodes, module, isFromHistory=false) => {
        for (let node of nodes) {
            const updatedModules = this.nodes[node].module.filter(oldModule => oldModule !== module)
            this.nodes[node].module = updatedModules
        }
        if (!isFromHistory) {
            this.updateChangeHistory({object: "nodeToModule", action: "delete", value: {nodeIds: nodes, module: module}})
        }
    }

    RemoveSelectedNodesFromModule = () => {
        const newModule = this.selectedModule.value
        for (let node of this.selectedNodes.value) {
            const updatedModules = this.nodes[node].module.filter(oldModule => oldModule !== newModule)
            this.nodes[node].module = updatedModules
        }
        this.updateChangeHistory({object: "nodeToModule", action: "delete", value: {nodeIds: this.selectedNodes.value, module: newModule}})
        
    }

    _buildAdjacencyList = (edges) => {
        const adjacencyList = {};
        for (const key in edges) {
            const { source, target } = edges[key];
            if (!adjacencyList[source]) {
            adjacencyList[source] = [];
            }
            adjacencyList[source].push(target);
        }
        return adjacencyList;
    }
    
    _dfs = (node, adjacencyList, visited) => {
        if (visited.has(node)) {
            return visited.get(node);
        }
    
        const reachable = new Set();
        if (adjacencyList[node]) {
            for (const neighbor of adjacencyList[node]) {
            reachable.add(neighbor);
            const reachableFromNeighbor = this._dfs(neighbor, adjacencyList, visited);
            for (const item of reachableFromNeighbor) {
                reachable.add(item);
            }
            }
        }
    
        visited.set(node, reachable);
        return reachable;
    }
    
    _findAllReachable = (adjacencyList) => {
        const reachableMap = new Map();
        for (const node in adjacencyList) {
            this._dfs(node, adjacencyList, reachableMap);
        }
        return reachableMap;
    }
    
    transitiveReduction = () => {
        const edges = this.edges
        const adjacencyList = this._buildAdjacencyList(edges);
        const reachableMap = this._findAllReachable(adjacencyList);
        // const reducedEdges = {};
        const removedEdges = []
    
        for (const key in edges) {
            const { source, target } = edges[key];
            const reachableFromSource = new Set(reachableMap.get(source));
            reachableFromSource.delete(target); // Remove the direct edge to avoid self-loop check
    
            // Check if the target is reachable from the source through another path
            let isIndirectlyReachable = false;
            for (const intermediate of reachableFromSource) {
            if (reachableMap.get(intermediate) && reachableMap.get(intermediate).has(target)) {
                isIndirectlyReachable = true;
                break;
            }
            }
    
            if (isIndirectlyReachable) {
                removedEdges.push(key)
            }
        }
    
        this.selectedEdges.value = removedEdges
    }
}