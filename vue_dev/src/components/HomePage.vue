<template>
  <div class="home-page-wrapper">
    <div class="container">
      <div v-if="loadingCompleted" class="home-page">
        <p>Welcome to the Home Page!
          <br>
          If you are seeing this message, it means the endpoint has spit out some data.
        </p>
      </div>
      <div :class="{'home-page': true, 'blurred': isLoading}">
        <div v-if="showInitialScreen" class="initial-screen">
          <div class="option create-course" @click="selectOption('create')">
            <p>Create New Course</p>
          </div>
          <div class="option existing-course" @click="selectOption('existing')">
            <p>Use Existing Course</p>
          </div>
        </div>
        <div v-else class="form-container">
          <div class="left-half">
            <div v-if="isNewCourse">
              <h2>Create New Course</h2>
              <div class="course-details">
                <div class="input-box">
                  <label>Course Name:</label>
                  <input type="text" v-model="courseName">
                </div>
                <div class="input-box">
                  <label>Instructor: <img src="/static/assets/search-bar.png" class="search-bar-inst"></label>
                  <input type="text" v-model="instructor" @input="fetchInstructors" @focus="showAllInstructors" @blur="hideInstructorSuggestions">
                  <ul v-if="showInstructorSuggestions" class="suggestions-list" @mousedown.prevent>
                    <li v-for="(suggestion, index) in filteredInstructors" :key="index" @mousedown="selectInstructor(suggestion)">
                      {{ suggestion }}
                    </li>
                  </ul>
                </div>
                <div class="input-box">
                  <label>Quarter:</label>
                  <div class="quarter-inputs">
                    <select v-model="quarter">
                      <option>Fall</option>
                      <option>Winter</option>
                      <option>Spring</option>
                      <option>Summer Session I</option>
                      <option>Summer Session II</option>
                    </select>
                    <input type="number" v-model="year" min="2000" max="3000" class="quarter-inp">
                  </div>
                </div>
                <div class="input-box">
                  <label>Subject: <img src="/static/assets/search-bar.png" class="search-bar-subj"></label>
                  <input type="text" v-model="subject" @input="fetchSubjects" @focus="showAllSubjects" @blur="hideSubjectSuggestions">
                  <ul v-if="showSubjectSuggestions" class="suggestions-list" @mousedown.prevent>
                    <li v-for="(suggestion, index) in filteredSubjects" :key="index" @mousedown="selectSubject(suggestion)">
                      {{ suggestion }}
                    </li>
                  </ul>
                </div>
                <div class="input-box file-upload">
                  <label for="file-upload" class="file-upload-label">
                    Click to Upload files <img src="/static/assets/upload-file.png" class="upload-file-icon">
                  </label>
                  <input type="file" id="file-upload" multiple @change="handleFilesUpload">
                  <ul>
                    <li v-for="(file, index) in files" :key="file.name">
                      {{ file.name }}
                      <button @click="removeFile(index)">
                        <img src="/static/assets/delete.png" class="delete-icon">
                      </button>
                    </li>
                  </ul>
                </div>
                <div class="input-box fixed-input">
                  <label>Difficulty:</label>
                  <input type="number" v-model="difficulty" min="1" max="5">
                </div>
              </div>
            </div>
            <div v-else>
              <h2>Use Existing Course</h2>
              <p>Please enter at least one of the following to search for an existing course</p>
              <div class="existing-course-details">
                <div class="input-box">
                  <label>Instructor: <img src="/static/assets/search-bar.png" class="search-bar-inst"></label>
                  <input type="text" v-model="instructor" @input="fetchInstructors" @focus="showAllInstructors" @blur="hideInstructorSuggestions">
                  <ul v-if="showInstructorSuggestions" class="suggestions-list" @mousedown.prevent>
                    <li v-for="(suggestion, index) in filteredInstructors" :key="index" @mousedown="selectInstructor(suggestion)">
                      {{ suggestion }}
                    </li>
                  </ul>
                </div>
                <div class="input-box">
                  <label>Quarter:</label>
                  <div class="quarter-inputs">
                    <select v-model="quarter">
                      <option>Fall</option>
                      <option>Winter</option>
                      <option>Spring</option>
                      <option>Summer Session I</option>
                      <option>Summer Session II</option>
                    </select>
                    <input type="number" v-model="year" min="2000" max="3000" class="quarter-inp">
                  </div>
                </div>
                <div class="input-box">
                  <label>Quarter Filter:</label>
                  <select v-model="quarterFilter">
                    <option value="">--</option>
                    <option value="equal">Equal</option>
                    <option value="newer">Newer</option>
                    <option value="older">Older</option>
                    <option value="newer_inclusive">Newer Inclusive</option>
                    <option value="older_inclusive">Older Inclusive</option>
                  </select>
                </div>
                <div class="input-box">
                  <label>Subject: <img src="/static/assets/search-bar.png" class="search-bar-subj"></label>
                  <input type="text" v-model="subject" @input="fetchSubjects" @focus="showAllSubjects" @blur="hideSubjectSuggestions">
                  <ul v-if="showSubjectSuggestions" class="suggestions-list" @mousedown.prevent>
                    <li v-for="(suggestion, index) in filteredSubjects" :key="index" @mousedown="selectSubject(suggestion)">
                      {{ suggestion }}
                    </li>
                  </ul>
                </div>
                <div class="input-box fixed-input">
                  <label>Difficulty:</label>
                  <input type="number" v-model="difficulty" min="1" max="5">
                </div>
              </div>
              <div class="search-container">
                <button class="button" @click="searchCourses">Search</button>
              </div>
              <p>Please select a course to view the course summary</p>
              <div class="input-box">
                <label>Course:</label>
                <select v-model="selectedCourse">
                  <option v-for="course in courses" :key="course.course_id" :value="course">{{ course.name }}</option>
                </select>
              </div>
            </div>
          </div>
          <div class="right-half">
            <div v-if="!isNewCourse && selectedCourse">
              <div class="summary-box">
                <label>Course Summary:</label>
                <div class="course-summary-box">
                  <p>{{ selectedCourse?.course_summary }}</p>
                </div>
              </div>
              <AccordionRoot
                class="module-accordion-container"
                type="single"
                :collapsible="true"
                @update:model-value="moduleSelected"
              >
                <h3 class="roboto-bold">Modules</h3>
                <template v-for="module in modules" :key="module.module_id">
                  <AccordionItem class="module-accordion-item roboto-regular" :value="module.module_id">
                    <AccordionHeader class="module-accordion-header">
                      <AccordionTrigger class="module-accordion-trigger roboto-bold">
                        <span>{{ module.title }}</span>
                        <img src="/static/assets/icon-chevron.png" class="dropdown-btn-icon" />
                      </AccordionTrigger>
                    </AccordionHeader>
                    <AccordionContent class="module-accordion-content">
                      <ModuleMenuItems :module-summary="module.content_summary" />
                      <!-- <p>{{ module.content_summary }}</p> -->
                      <ol>
                        <li v-for="concept in concepts[module.module_id]" :key="concept.name">{{ concept.name }}</li>
                      </ol>
                    </AccordionContent>
                  </AccordionItem>
                </template>
              </AccordionRoot>
              <div class="submit-container">
                <button class="button" @click="submitExistingCourseForm">Submit</button>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div v-if="isLoading" class="loading-overlay">
        <img src="/static/assets/loading-icon.png" class="loading-icon">
        <p>Loading...</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import ModuleMenuItems from './module_menu/ModuleMenuItems.vue';
import { AccordionRoot, AccordionItem, AccordionHeader, AccordionTrigger, AccordionContent } from 'radix-vue';
import { ref, computed, watch } from 'vue';
import axios from 'axios';

const showInitialScreen = ref(true);
const isNewCourse = ref(false);
const courseName = ref('');
const quarter = ref('Fall');
const year = ref(2024);
const isLoading = ref(false);
const loadingCompleted = ref(false);
const instructor = ref('');
const subject = ref('CSS-1');
const difficulty = ref('');
const files = ref([]);
const instructors = ref(['Umberto Mignozzetti']);
const courses = ref([]); // Property to store courses
const selectedCourse = ref(null); // Property to store selected course
const modules = ref([]); // Property to store modules
const concepts = ref({});

const showInstructorSuggestions = ref(false);
const showSubjectSuggestions = ref(false);
const quarterFilter = ref('equal'); // Set default to "equal"

const filteredInstructors = computed(() => {
  if (instructor.value === '') {
    return instructors.value;
  }
  const searchTerm = instructor.value.toLowerCase();
  return instructors.value.filter(instr => {
    const nameParts = instr.toLowerCase().split(' ');
    return nameParts.some(part => part.startsWith(searchTerm));
  });
});

const fetchInstructors = () => {
  showInstructorSuggestions.value = filteredInstructors.value.length > 0;
};

const showAllInstructors = () => {
  showInstructorSuggestions.value = instructors.value.length > 0;
};

const fetchConcepts = async (moduleId) => {
  if (!concepts.value[moduleId]) {
    try {
      const response = await axios.get(`http://localhost:8080/concept/cm/${moduleId}`);
      concepts.value[moduleId] = response.data.concepts;
    } catch (error) {
      console.error('Failed to fetch concepts:', error);
    }
  }
};

const hideInstructorSuggestions = () => {
  setTimeout(() => {
    showInstructorSuggestions.value = false;
  }, 200);
};

const selectInstructor = (selectedInstructor) => {
  instructor.value = selectedInstructor;
  showInstructorSuggestions.value = false;
};

const searchCourses = async () => {
  const quarterToMonthMapping = {
    'Fall': '09',
    'Winter': '01',
    'Spring': '04',
    'Summer Session I': '07',
    'Summer Session II': '08',
  };
  const month = quarterToMonthMapping[quarter.value];
  const date = `${year.value}-${month}-01`;

  const filterParams = {
    name: courseName.value,
    instructor: instructor.value,
    quarter: date,
    quarter_filter: quarterFilter.value,
    subject: subject.value,
    difficulty: difficulty.value
  };


  const handleAccordionClick = (moduleId) => {
  fetchConcepts(moduleId);
};

  const filteredParams = {};
  Object.keys(filterParams).forEach(key => {
    if (filterParams[key]) {
      filteredParams[key] = filterParams[key];
    }
  });

  const queryParams = new URLSearchParams(filteredParams).toString();
  const requestUrl = `http://localhost:8080/course/filter/{course_filter}?${queryParams}`;

  try {
    const response = await axios.get(requestUrl);
    console.log("Courses fetched:", response.data);
    courses.value = response.data;
  } catch (error) {
    console.error('Error filtering courses:', error);
  }
};

const handleFilesUpload = (event) => {
  const uploadedFiles = Array.from(event.target.files);
  files.value = [...files.value, ...uploadedFiles];
};

const removeFile = (index) => {
  files.value.splice(index, 1);
};

const fetchModules = async (courseId) => {
  const url = `http://localhost:8080/module/get/${courseId}/course`;
  try {
    const response = await axios.get(url);
    modules.value = response.data;
  } catch (error) {
    console.error('Error fetching modules:', error);
  }
};

// Watch for changes in selectedCourse to fetch modules
watch(selectedCourse, async (newVal) => {
  if (newVal && newVal.course_id) {
    await fetchModules(newVal.course_id);
    // Optionally fetch concepts for the first module immediately
    if (modules.value.length > 0) {
      fetchConcepts(modules.value[0].module_id);
    }
  }
});

function moduleSelected(moduleId) {
  console.log("Module selected:", moduleId);
  // Additional logic for selecting a module can be added here
}

const selectOption = (option) => {
  showInitialScreen.value = false;
  isNewCourse.value = option === 'create';
};
</script>

<script>
export default {
  name: "HomePage",
  friendly_name: "Home Page",
  icon: "/static/assets/icon-HomePage.png"
}
</script>

<style scoped>
.home-page-wrapper {
  position: relative;
  height: 100%;
}

.home-page {
  display: flex;
  flex-direction: row;
  width: 100%;
  height: 100%;
  transition: filter 0.3s ease;
}

.container {
  max-width: 100%;
  width: 100%;
  height: 100%;
  margin: 0 auto;
  height: 100%;
}

@media (max-width: 768px) {
  .container {
    padding: 0 10px;
  }
}

.form-container {
  display: flex;
  width: 100%;
  height: 100%;
}

.left-half {
  flex: 1;
  padding: 10px;
  display: flex;
  flex-direction: column;
  border-right: 2px solid #000000;
  overflow-y: auto;
  height: 95%;
}

.right-half {
  flex: 1;
  padding: 10px;
  padding-bottom: 50px;
  display: flex;
  overflow-y: auto;
  height: 95%;
}

.input-box input[type="text"],
.input-box select,
.input-box button {
  width: 100%;
  padding: 10px;
  margin-bottom: 10px;
  box-sizing: border-box;
  max-width: 400px;
}

.suggestion-content {
  width: 100%;
  max-width: 800px;
  margin: 20px auto;
  word-wrap: break-word;
}

.upload-section {
  max-width: 600px;
  margin: 20px auto;
}

@media (max-width: 768px) {
  .upload-section {
    padding: 0 10px;
  }
}

body {
  font-size: 16px;
  line-height: 1.5;
}

h1 {
  font-size: 2rem;
}

h2 {
  font-size: 1.5rem;
}

@media (max-width: 768px) {
  body {
    font-size: 14px;
  }

  h1 {
    font-size: 1.75rem;
  }

  h2 {
    font-size: 1.25rem;
  }
}

.initial-screen {
  display: flex;
  flex: 1;
  justify-content: center;
  align-items: center;
  gap: 20px;
  width: 100%;
  height: 90vh;
}

.option {
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
  cursor: pointer;
  text-align: center;
  border-radius: 8px;
}

.create-course {
  background-color: #00629B; /* Adjust color as needed */
  color: white;
  height: 100%;
  width: 100%;
  margin-bottom: -3pc;
}

.existing-course {
  background-color: #FFCD00; /* Adjust color as needed */
  color: black;
  height: 100%;
  width: 90%;
  margin-right: 3pc;
  margin-bottom: -3pc;
}

.option p {
  font-size: 1.5em;
  color: white; /* Adjust color as needed */
}

.existing-course-details, .course-details {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); /* Auto-fit content based on available space */
  gap: 20px;
}

@media (max-width: 768px) {
  .course-details, .existing-course-details {
    grid-template-columns: 1fr;
  }
}

.blurred {
  filter: blur(5px);
  pointer-events: none;
}

.button {
  padding: 15px 30px;
  margin-bottom: 10px;
  font-size: 1em;
  background-color: #007BFF;
  color: #fff;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.button:hover {
  background-color: #0056b3;
}

.loading-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 150px;
  background: rgba(255, 255, 255, 0.7);
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  align-items: center;
  z-index: 1000;
}

.input-box {
  position: relative;
  display: flex;
  flex-direction: column;
  justify-content: space-between; /* Distribute space evenly */
  padding: 10px;
  border: 2px solid #ccc;
  border-radius: 8px;
  background-color: #fff;
  box-sizing: border-box;
  width: 100%; /* Ensure full width within grid column */
  height: 150px; /* Set a fixed height to make all boxes the same size */
}

.fixed-input {
  min-width: 200px; /* Set a fixed width to maintain consistent size */
  max-height: 99px;
}

.input-box label {
  font-weight: bold;
  margin-bottom: 5px;
  font-size: 0.8em;
}

.quarter-inputs select,
.quarter-inputs input {
  flex: 1;
}

.input-box input, .input-box select, .quarter-inp {
  padding: 10px;
  font-size: 0.6em;
  border: 1px solid #ccc;
  border-radius: 4px;
  box-sizing: border-box;
  width: 100%;
  max-width: 100%;
  margin-bottom: 10px;
}

.quarter-inputs {
  display: flex;
  align-items: center;
  gap: 10px;
  flex: 1;
}

.quarter-inp {
  width: 20%;
}

.file-upload {
  display: flex;
  flex-direction: column;
  align-items: center;
  cursor: pointer;
  text-align: center;
  height: 100%;
  padding: 10px;
  border: 2px solid #ccc;
  border-radius: 8px;
  background-color: #fff;
  box-sizing: border-box;
  width: 100%;
  font-size: 1em;
}

.align-top-left {
  align-self: flex-start;
}

.file-upload input[type="file"] {
  display: none;
}

.file-upload ul {
  list-style: none;
  padding: 0;
  margin-top: 10px;
  width: 100%;
  max-height: 150px;
  overflow-y: auto;
}

.file-upload li {
  background-color: #f0f0f0;
  padding: 10px;
  margin-bottom: 5px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 0.6em;
}

.file-upload li button {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 1em;
  color: red;
}

.tutorial-section {
  display: flex;
  flex-direction: column;
  flex-grow: 1;
  padding: 20px;
  border: 2px solid #ccc;
  border-radius: 8px;
  background-color: #fff;
  max-height: 70vh;
  overflow: hidden;
}

.center-text {
  text-align: center;
}

.tutorial-section p {
  font-size: 1.2em;
  font-weight: bold;
  margin-bottom: 10px;
  margin-right: 20px;
}

.tutorial-gif {
  height: 400px;
  background-color: #f0f0f0;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 20px;
}

.course-summary-box {
  max-height: 1000px; /* Set the desired fixed height */
  overflow-y: auto; /* Enable vertical scrolling */
  padding: 10px; /* Add some padding for better readability */
  border: 1px solid #ccc; /* Optional: Add a border for better visibility */
  border-radius: 4px; /* Optional: Add border-radius for rounded corners */
  background-color: #f9f9f9; /* Optional: Add background color */
}

.summary-box {
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
  background-color: #f9f9f9;
  margin-bottom: 20px;
}

.search-bar-inst {
  width: 20px;
  height: 20px;
  margin-left: 237px;
}

.submit-container,
.search-container {
  display: flex;
  justify-content: flex-end; /* Align buttons to the right */
  margin-top: 20px;
  margin-bottom: 50px;
  width: 100%;
}

.submit-button {
  display: flex;
  justify-content: flex-end;
}

.search-bar-subj {
  width: 20px;
  height: 20px;
  margin-left: 257px;
}

.search-bar-template {
  width: 20px;
  height: 20px;
  margin-left: 180px;
}

.upload-file-icon {
  width: 40px;
  height: 40px;
  position: relative;
  top: 10px;
}

.upload-container {
  display: flex;
  flex-direction: column;
  align-items: flex-start;  /* Align items to the start of the container */
  overflow: auto;  /* Add scroll if content overflows */
  max-height: 200px;  /* Set a maximum height */
}

.loading-icon {
  width: 50px;
  height: 50px;
  margin-bottom: 10px;
  animation: spin 2s linear infinite;
}

.delete-icon {
  width: 30px;
  height: 30px;
}

textarea {
  margin-top: 10px;
  width: 100%;
  height: 100px;
  padding: 10px;
  font-size: 1em;
  border: 1px solid #ccc;
  border-radius: 4px;
  flex-grow: 1;
}

button {
  padding: 15px 30px;
  font-size: 1em;
  background-color: #007BFF;
  color: #fff;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

button:hover {
  background-color: #0056b3;
}

.suggestions-list {
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  max-height: 150px;
  overflow-y: auto;
  border: 1px solid #ccc;
  border-top: none;
  background-color: #fff;
  z-index: 1000;
  list-style-type: none;
  font-size: 14px;
  padding-left: 0;
}

.suggestions-list li {
  padding: 10px;
  cursor: pointer;
}

.suggestions-list li:hover {
  background-color: #f0f0f0;
}

.search-button {
  padding: 10px 20px; /* Smaller padding for a smaller button */
  font-size: 0.8em; /* Smaller font size */
}

.search-button:hover {
  background-color: #0056b3;
}

.module-accordion-container {
  max-height: 500px;
  padding-bottom: 20px;
  overflow-y: auto;
}
.module-accordion-item {
  background-color: var(--bg-color);
}
.module-accordion-header {
  margin: 0;
  width: 100%;
}
.module-accordion-trigger {
  font-size: 1.2rem; /* Adjust this value as needed */
  text-align: center;
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 2rem; /* Adjust height accordingly if needed */
  width: 100%;
  background-color: var(--core-primary);
  color: var(--accent-primary);
}

.module-accordion-trigger[data-state="open"] > .dropdown-btn-icon {
  transform: rotate(180deg);
  transition: 300ms linear;
}
.module-accordion-trigger[data-state="closed"] > .dropdown-btn-icon {
  transform: rotate(0deg);
  transition: 300ms linear;
}

/* Adjusting the size of the dropdown arrows */
.dropdown-btn-icon {
  width: 30px; /* Smaller width */
  height: 30px; /* Smaller height */
  transition: transform 300ms linear;
}


.module-accordion-content {
  max-height: 300px; /* Adjust this value as necessary for your layout */
  overflow-y: auto; /* Enables vertical scrolling when content is too tall */
  padding: 10px;
  scrollbar-width: thin; /* For browsers that support it */
  scrollbar-color: #888 #e0e0e0; /* For browsers that support it */
}

.module-accordion-content::-webkit-scrollbar {
  width: 8px;
}

.module-accordion-content::-webkit-scrollbar {
  width: 8px;
}

.module-accordion-content::-webkit-scrollbar-thumb {
  background-color: #888;
  border-radius: 10px;
  border: 2px solid #e0e0e0;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}
</style>
