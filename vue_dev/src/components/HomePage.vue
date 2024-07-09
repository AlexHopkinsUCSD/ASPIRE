<template>
  <div class="home-page-wrapper">
    <div v-if="loadingCompleted" class="home-page">
      <!-- Empty Home Page Content -->
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
        <div v-if="isNewCourse" class="left-half">
          <div class="course-details">
            <!-- Existing course details code -->
            <div class="input-box">
              <label>Course Name:</label>
              <input type="text" v-model="courseName" @input="fetchCourses" @focus="showAllCourses" @blur="hideCourseSuggestions">
              <ul v-if="showCourseSuggestions" class="suggestions-list" @mousedown.prevent>
                <li v-for="(suggestion, index) in filteredCourses" :key="index" @mousedown="selectCourse(suggestion)">
                  {{ suggestion }}
                </li>
              </ul>
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
          <div class="submit-button">
            <button @click="submitForm">Submit</button>
          </div>
        </div>
        <div v-else class="left-half">
          <div class="existing-course-details">
            <!-- Existing course details code -->
            <div class="input-box">
              <label>Course:</label>
              <input type="text" v-model="existingCourse" @input="fetchExistingCourses" @focus="showAllExistingCourses" @blur="hideExistingCourseSuggestions">
              <ul v-if="showExistingCourseSuggestions" class="suggestions-list" @mousedown.prevent>
                <li v-for="(suggestion, index) in filteredExistingCourses" :key="index" @mousedown="selectExistingCourse(suggestion)">
                  {{ suggestion }}
                </li>
              </ul>
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
            <div class="input-box">
              <label>Course Template: <img src="/static/assets/search-bar.png" class="search-bar-template"></label>
              <input type="text" v-model="template" @input="fetchTemplates" @focus="showAllTemplates" @blur="hideTemplateSuggestions">
              <ul v-if="showTemplateSuggestions" class="suggestions-list" @mousedown.prevent>
                <li v-for="(suggestion, index) in filteredTemplates" :key="index" @mousedown="selectedTemplate(suggestion)">
                  {{ suggestion.name }}
                  <p>{{ suggestion.content }}</p>
                </li>
              </ul>
            </div>
            <div class="input-box fixed-input">
              <label>Difficulty:</label>
              <input type="number" v-model="difficulty" min="1" max="5">
            </div>
          </div>
          <div class="submit-button">
            <button @click="submitExistingCourseForm">Submit</button>
          </div>
        </div>
        <div class="right-half">
          <div class="tutorial-section">
            <div class="center-text">
              <p>How To Upload a File</p>
            </div>
            <div class="tutorial-gif">
              <img :src="gifSrc" class="gif" @mouseover="startGif" @mouseout="stopGif">        
            </div>
            <textarea v-text="explanation" readonly></textarea>      
          </div>
        </div>
      </div>
    </div>
    <div v-if="isLoading" class="loading-overlay">
      <img src="/static/assets/loading-icon.png" class="loading-icon">
      <p>Loading...</p>
    </div>
  </div>
</template>


<script setup>
import axios from 'axios';
</script>

<script>
export default {
  name: 'HomePage',
  icon: '/static/assets/icon-HomePage.png',
  data() {
    return {
      showInitialScreen: true,
      isNewCourse: false,
      courseName: '',
      quarter: 'Fall',
      year: 2024,
      isLoading: false,
      loadingCompleted: false, // New flag for loading completion
      instructor: '',
      subject: '',
      template: '',
      difficulty: '1',
      files: [],
      explanation: 'Insert Explanatory Text Here',
      instructors: ['John Doe', 'Jane Smith', 'Alice Johnson', 'Bob Brown'],
      courses: ['Math 101', 'Physics 202', 'Chemistry 303', 'Biology 404'],
      subjects: ['Mathematics', 'Physics', 'Chemistry', 'Biology'],
      templates: [
        { name: 'Template 1', content: 'Content for Template 1' },
        { name: 'Template 2', content: 'Content for Template 2' },
        { name: 'Template 3', content: 'Content for Template 3' },
        { name: 'Template 4', content: 'Content for Template 4' },
      ],
      showInstructorSuggestions: false,
      showCourseSuggestions: false,
      showSubjectSuggestions: false,
      showTemplateSuggestions: false,
      gifSrc: '/static/assets/rick-roll.png',
      existingCourse: '',
      existingQuarter: 'Fall',
      existingYear: 2024,
      showExistingCourseSuggestions: false,
      existingCourses: ['Math 101', 'Physics 202', 'Chemistry 303', 'Biology 404'],
      selectedTemplate: null,
    };
  },
  computed: {
    filteredInstructors() {
      if (this.instructor === '') {
        return this.instructors;
      }
      const searchTerm = this.instructor.toLowerCase();
      return this.instructors.filter(instructor => {
        const nameParts = instructor.toLowerCase().split(' ');
        return nameParts.some(part => part.startsWith(searchTerm));
      });
    },
    filteredCourses() {
      if (this.courseName === '') {
        return this.courses;
      }
      const searchTerm = this.courseName.toLowerCase();
      return this.courses.filter(course => {
        const nameParts = course.toLowerCase().split(' ');
        return nameParts.some(part => part.startsWith(searchTerm));
      });
    },
    filteredSubjects() {
      if (this.subject === '') {
        return this.subjects;
      }
      const searchTerm = this.subject.toLowerCase();
      return this.subjects.filter(subject => {
        const nameParts = subject.toLowerCase().split(' ');
        return nameParts.some(part => part.startsWith(searchTerm));
      });
    },
    filteredTemplates() {
      if (this.templates === '') {
        return this.templates;
      }
      const searchTerm = this.template.toLowerCase();
      return this.templates.filter(template => {
        const nameParts = template.name.toLowerCase().split(' ');
        return nameParts.some(part => part.startsWith(searchTerm));
      });
    },
    filteredExistingCourses() {
      if (this.existingCourse === '') {
        return this.existingCourses;
      }
      const searchTerm = this.existingCourse.toLowerCase();
      return this.existingCourses.filter(course => {
        const nameParts = course.toLowerCase().split(' ');
        return nameParts.some(part => part.startsWith(searchTerm));
      });
    },
  },
  methods: {
    async submitForm() {
      this.isLoading = true;
      const formData = new FormData();
      const quarterToMonthMapping = {
        'Fall': '09',
        'Winter': '01',
        'Spring': '04',
        'Summer Session I': '07',
        'Summer Session II': '08',
      };
      const month = quarterToMonthMapping[this.quarter];
      const date = `${this.year}-${month}-01`;
      formData.append('quarter', date);
      formData.append('courseName', this.courseName);
      formData.append('instructor', this.instructor);
      formData.append('subject', this.subject);
      formData.append('template', this.template);
      formData.append('difficulty', this.difficulty);
      formData.append('domain_id', '');
      formData.append('name', '');
      this.files.forEach(file => {
        formData.append('content_files', file);
      });

      // Log formData entries
      for (let pair of formData.entries()) {
        console.log(pair[0] + ', ' + pair[1]);
      }
      try {
        const response = await axios.post(`http://localhost:8080/qas/register?model_name=gpt-3.5-turbo`, formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        });
        console.log('Form submitted successfully:', response.data);
      } catch (error) {
        console.error('Error submitting form:', error);
      } finally {
        this.isLoading = false;
        this.loadingCompleted = true; // Set loadingCompleted to true
      }
    },
    async submitExistingCourseForm() {
      const formData = new FormData();
      const quarterToMonthMapping = {
        'Fall': '09',
        'Winter': '01',
        'Spring': '04',
        'Summer Session I': '07',
        'Summer Session II': '08',
      };
      const month = quarterToMonthMapping[this.quarter];
      const date = `${this.year}-${month}-01`;
      formData.append('quarter', date);
      formData.append('courseName', this.courseName);
      formData.append('instructor', this.instructor);
      formData.append('subject', this.subject);
      formData.append('template', this.template);
      formData.append('difficulty', this.difficulty);
      formData.append('domain_id', '');
      formData.append('name', '');
      this.files.forEach(file => {
        formData.append('content_files', file);
      });

      // Log formData entries
      for (let pair of formData.entries()) {
        console.log(pair[0] + ', ' + pair[1]);
      }
      try {
        const response = await axios.post(`http://localhost:8080/qas/register?model_name=gpt-3.5-turbo`, formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        });
        console.log('Form submitted successfully:', response.data);
      } catch (error) {
        console.error('Error submitting form:', error);
      }
    },
    startGif() {
      this.gifSrc = '/static/assets/rick-roll.gif';
    },
    stopGif() {
      this.gifSrc = '/static/assets/rick-roll.png';
    },
    handleFilesUpload(event) {
      const uploadedFiles = Array.from(event.target.files);
      this.files = [...this.files, ...uploadedFiles];
    },
    removeFile(index) {
      this.files.splice(index, 1);
    },
    fetchInstructors() {
      this.showInstructorSuggestions = this.filteredInstructors.length > 0;
    },
    showAllInstructors() {
      this.showInstructorSuggestions = this.instructors.length > 0;
    },
    hideInstructorSuggestions() {
      setTimeout(() => {
        this.showInstructorSuggestions = false;
      }, 200);
    },
    selectInstructor(instructor) {
      this.instructor = instructor;
      this.showInstructorSuggestions = false;
    },
    fetchCourses() {
      this.showCourseSuggestions = this.filteredCourses.length > 0;
    },
    showAllCourses() {
      this.showCourseSuggestions = this.courses.length > 0;
    },
    hideCourseSuggestions() {
      setTimeout(() => {
        this.showCourseSuggestions = false;
      }, 200);
    },
    selectCourse(course) {
      this.courseName = course;
      this.showCourseSuggestions = false;
    },
    fetchTemplates() {
      this.showTemplateSuggestions = this.filteredTemplates.length > 0;
    },
    showAllTemplates() {
      this.showTemplateSuggestions = this.templates.length > 0;
    },
    hideTemplateSuggestions() {
      setTimeout(() => {
        this.showTemplateSuggestions = false;
      }, 200);
    },
    fetchSubjects() {
      this.showSubjectSuggestions = this.filteredSubjects.length > 0;
    },
    showAllSubjects() {
      this.showSubjectSuggestions = this.subjects.length > 0;
    },
    hideSubjectSuggestions() {
      setTimeout(() => {
        this.showSubjectSuggestions = false;
      }, 200);
    },
    selectSubject(subject) {
      this.subject = subject;
      this.showSubjectSuggestions = false;
    },
    setSelectedTemplate(template) {
      this.template = template;
      this.showTemplateSuggestions = false;
    },
    selectOption(option) {
      this.showInitialScreen = false;
      this.isNewCourse = option === 'create';
    },
    fetchExistingCourses() {
      this.showExistingCourseSuggestions = this.filteredExistingCourses.length > 0;
    },
    showAllExistingCourses() {
      this.showExistingCourseSuggestions = this.existingCourses.length > 0;
    },
    hideExistingCourseSuggestions() {
      setTimeout(() => {
        this.showExistingCourseSuggestions = false;
      }, 200);
    },
    selectExistingCourse(course) {
      this.existingCourse = course;
      this.showExistingCourseSuggestions = false;
    },
  }
};
</script>

<style scoped>
.home-page-wrapper {
  position: relative;
}

.home-page {
  padding: 20px;
  display: flex;
  flex-direction: row;
  width: 100%;
  min-height: calc(100vh - 170px);
  transition: filter 0.3s ease;
}

.initial-screen {
  display: flex;
  flex: 1;
  justify-content: center;
  align-items: center;
  gap: 20px;
  width: 100%;
  height: 100vh-170px;
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

.left-half {
  flex: 1 1 45%;
  padding: 10px;
  display: flex;
  flex-direction: column;
  border-right: 2px solid #000000;
}

.right-half {
  flex: 1 1 45%;
  padding: 10px;
  display: flex;
  flex-direction: column;
}

.course-details, .existing-course-details {
  display: grid;
  grid-template-columns: 1fr 1fr;
  grid-template-rows: repeat(3, auto);
  gap: 20px;
  padding: auto;
}

.blurred {
  filter: blur(5px);
  pointer-events: none;
}

.loading-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(255, 255, 255, 0.7);
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.input-box {
  position: relative; /* Add relative positioning for the suggestions list */
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  padding: 10px;
  border: 2px solid #ccc;
  border-radius: 8px;
  background-color: #fff;
  box-sizing: border-box;
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

.input-box input, .input-box select, .quarter-inputs input {
  padding: 10px;
  font-size: 0.6em;
  border: 1px solid #ccc;
  border-radius: 4px;
  box-sizing: border-box;
  width: 100%;
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
  height: 91%;
  padding: 10px;
  border: 2px solid #ccc;
  border-radius: 8px;
  background-color: #fff;
  box-sizing: border-box;
  width: 100%;
  font-size: 1em;
}

.form-container {
  display: flex;
  width: 100%; 
}

.file-upload input[type="file"] {
  display: none;
}

.file-upload ul {
  list-style: none;
  padding: 0;
  margin-top: 10px;
  width: 100%;
  max-height: 350px; /* Set max-height to control the height of the upload section */
  overflow-y: auto; /* Add scrollbar if the content exceeds max-height */
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
}

.center-text {
  text-align: center;
}

.tutorial-section p {
  font-size: 1.2em;
  font-weight: bold;
  margin-bottom: 10px;
}

.tutorial-gif {
  height: 400px;
  background-color: #f0f0f0;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 20px;
}

.search-bar-inst {
  width: 20px;
  height: 20px;
  margin-left: 237px;
}

.submit-button {
  position: fixed;
  justify-content: flex-end;
  margin-top: 530px;
  margin-left: 650px;
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
  margin-top: 20px;
  padding: 15px 30px;
  font-size: 1em;
  background-color: #007BFF;
  color: #fff;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  align-self: flex-end;
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

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}
</style>