<script setup>
import NavBar from "./components/NavBar.vue";
import { getCurrentInstance, inject, ref } from "vue";

const currentTab = inject("currentTab");
const tabWidth = ref(90);
const tabs = getCurrentInstance().appContext.components;

const isDarkMode = ref(false);

const toggleDarkMode = () => {
  isDarkMode.value = !isDarkMode.value;
  if (isDarkMode.value) {
    document.documentElement.classList.add('dark-mode');
  } else {
    document.documentElement.classList.remove('dark-mode');
  }
};


</script>

<template>
  <div id="app-main" :class="['main-container', { 'dark-mode': isDarkMode }]">
    <div class="banner roboto-bold">
      <img 
        :src="isDarkMode ? '/static/assets/aspire-dark-logo.png' : '/static/assets/aspire_logo.png'" 
        :class="[isDarkMode ? 'aspire-logo-dark' : 'aspire-logo']" 
      />
      <img 
        :src="isDarkMode ? '/static/assets/ucsd-dark-logo.png' : '/static/assets/ucsd_logo.png'" 
        :class="['logo', isDarkMode ? 'ucsd-logo-dark' : 'ucsd-logo']" 
      />
    </div>
    <hr class="gold-line"/>
    <div class="dashboard">
      <NavBar :style="{ width: `${100 - tabWidth}%` }" />
      <div class="tab" :style="{ width: `${tabWidth}%` }">
        <!-- Container with the desired styling -->
        <div class="main-content">
          <component :is="tabs[currentTab]"/>
        </div>
      </div>
    </div>
    <button class="dark-mode-toggle" @click="toggleDarkMode">
      <img v-if="isDarkMode" src="/static/assets/Light_Mode.png" alt="Light Mode" title="Light Mode" />
      <img v-else src="/static/assets/Dark_Mode.png" alt="Dark Mode" title="Dark Mode"/>
    </button>
  </div>
</template>

<style scoped>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

html, body {
  width: 100%;
  height: 100%;
  overflow: hidden;
}

.main-container {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.dark-mode {
  --bg-color: #202123;
  --text-color: #ffffff;
  --banner-bg-color: #121212;
  --banner-text-color: #ffffff;
  --gold-line-color: #ffcc00;
  --box-shadow-light: rgba(255, 255, 255, 0.2);
  --box-shadow-dark: rgba(255, 255, 255, 0.6);
  --box-shadow-hover-light: rgba(255, 255, 255, 0.4);
  --box-shadow-hover-dark: rgba(255, 255, 255, 0.8);
}

.main-container {
  width: 100vw;
  height: 100vh;
  background-color: var(--bg-color);
  color: var(--text-color);
  overflow: hidden;
}

.dashboard {
  display: flex;
  width: 100%;
  height: calc(90% - calc(3px + 1rem));
  justify-content: space-between;
}

.tab {
  padding-left: 1rem;
  padding-right: 1rem;
  padding-bottom: 1rem;
  display: flex;
  align-items: center;
  justify-content: center;
  height: calc(100% - 1rem);
  max-height: calc(100% - 1rem);
  
}

.banner {
  background-color: var(--banner-bg-color);
  width: 100vw;
  height: 10%;
  box-shadow: 0px 1px 4px 0px var(--banner-bg-color);
  display: flex;
  align-items: center;
  justify-content: space-between;
  color: var(--banner-text-color);
}

.ucsd-logo {
  padding-right: 1rem !important;
  height: 80% !important;
  width: 17% !important;
}

.aspire-logo {
  height: 75% !important;
  padding-left: 1rem !important;
  width: 9% !important;
}

.aspire-logo-dark {
  height: 40% !important;
  padding-left: 1.3rem !important;
  width: 9% !important;
}

.ucsd-logo-dark {
  padding-right: 1.5rem !important;
  height: 70% !important;
  width: 17% !important;
}

.gold-line {
  width: 97%;
  height: 3px;
  background-color: var(--gold-line-color);
  margin: 0.5rem;
  padding: 0;
  border: none;
}

.dark-mode-toggle {
  position: absolute;
  top: 0.rem;
  right: 22rem;
  background-color: var(--banner-bg-color);
  color: var(--banner-text-color);
  border: none;
  padding: 0.5rem;
  cursor: pointer;
}

.dark-mode-toggle img {
  width: 36px; /* Adjust the width as needed */
  height: 36px; /* Adjust the height as needed */
}

.dark-mode-toggle:hover {
    box-shadow: 1px 1px 2px 2px #C69214;
}

.welcome-header {
  font-size: 3rem;
  margin-bottom: 20px;
}

.main-content {
  padding: 5px;
  margin: 5px;
  /* position: fixed; */
  width: 100%;
  height: 100%;
  flex-direction: column !important;
  border: 1px solid #ccc !important;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1) !important; /* Add a box shadow */
  border-radius: 8px !important; /* Add rounded corners */
  background-color: var(--bg-accent);
  min-width: 88.8% !important;
  min-height: 87% !important;
  font: 300 1.5rem 'Arial', sans-serif !important; /* UCSD Font Family */
}
</style>

