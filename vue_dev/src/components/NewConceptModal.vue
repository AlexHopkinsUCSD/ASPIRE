<script setup>
import { ref, defineEmits, defineProps } from 'vue'

const props = defineProps(["modalOpen"])
const emit = defineEmits(["addNode", "updateOpen"])

const conceptForm = ref({})

function cancel() {
    emit("updateOpen", false)
    conceptForm.value = {}
}

function submit() {
    emit("addNode", conceptForm.value)
    emit("updateOpen", false)
    conceptForm.value = {}
}

</script>

<template>
    <div v-if="props.modalOpen" class="concept-modal">
        <div class="concept-form">
            <p>Add a New Concept</p>
            <form>
                <label for="concept-name">Concept Name</label>
                <input id="concept-name" :value="conceptForm.concept_name" @input="event => conceptForm.concept_name = event.target.value"/>
            </form>
            <button @click="cancel">Cancel</button>
            <button @click="submit">Submit</button>
        </div>
    </div>
</template>

<style scoped>
.concept-modal {
    position: fixed;
    display: flex;
    align-items: center;
    justify-content: center;
    background-color: rgba(211, 211, 211, 0.565);
    z-index: 999;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
}
.concept-form {
    display: flex;
    flex-direction: column;
    padding: 1rem;
    border-radius: 5px;
    border: 1px solid black;
    background-color: white;
}
</style>