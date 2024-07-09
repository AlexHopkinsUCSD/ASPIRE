<script setup>
import { getCurrentInstance, ref } from 'vue'
import NavBtn from "./NavBtn.vue"

// Get the current instance and components
const tabs = Object.values(getCurrentInstance().appContext.components).filter(comp => comp.name)
// State for controlling the collapsed state of the navbar
const isCollapsed = ref(false)

// Function to toggle the collapsed state
const toggleCollapse = () => {
    isCollapsed.value = !isCollapsed.value
}
</script>

<template>
    <div class="nav-container" :class="{ collapsed: isCollapsed }">
        <button class="toggle-button" @click="toggleCollapse" title="Toggle Sidebar">
            <img src="/static/assets/icon-SideBar.png" alt="Toggle" class="icon" />
        </button>
        <div class="tabs-container" v-if="!isCollapsed">
            <NavBtn v-for="tab in tabs" :tab="tab" :key="tab"/>
        </div>
    </div>
</template>

<style>
.nav-container {
    width: 6% !important;
    height: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
    padding-top: 1rem;
    background-color: #13294B;
    transition: width 0.5s, background-color 0.5s; /* Added transition for smooth collapse */
    position: relative; /* Ensure positioning context for the toggle button */
}

.nav-container.collapsed {
    width: 6% !important; /* Adjust the width as needed for the collapsed state */
    height: 99%;
    justify-content: center; /* Center the toggle button vertically */
    background-color: white;
}

.tabs-container {
    display: flex;
    flex-direction: column;
    width: 100%;
    align-items: center;
    flex-grow: 0.8; /* Ensure it takes the remaining space */
    justify-content: space-between; /* Spread out the icons evenly */
    margin-top: 5rem;
    height: 100;
}

.toggle-button {
    background-color: transparent;
    color: #ffffff;
    border: none;
    padding: 0.5rem 2rem;
    cursor: pointer;
    position: absolute; /* Position the toggle button absolutely */
    top: 1rem;
    left: 50%; /* Center the button horizontally within the nav-container */
    transform: translateX(-50%);
    display: flex; /* Use flex to align the icon */
    justify-content: center; /* Center the icon horizontally */
    align-items: center; /* Center the icon vertically */
}

.toggle-button:hover {
    box-shadow: 1px 1px 2px 2px #C69214 !important;
}

.toggle-button:focus {
    outline: none;
}

.icon {
    width: 48px;  /* Adjust the width as needed */
    height: 48px; /* Adjust the height as needed */
    display: block;
}
</style>
