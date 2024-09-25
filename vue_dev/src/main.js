import { createApp, ref } from "vue"
import App from "./App.vue"
import VNetworkGraph from "v-network-graph"
import VueApexCharts from "vue3-apexcharts";
import "v-network-graph/lib/style.css"
import axios from "axios"

import HomePage from "./components/HomePage.vue"
import DomainEditor from "./pages/DomainEditor.vue"
import StudentQuiz from "./pages/StudentQuiz.vue"
import QuizAuthoring from "./components/QuizAuthoring.vue"
import AdaptiveTutor from "./components/AdaptiveTutor.vue"
import SettingsPage from "./components/SettingsPage.vue"
import StudentModel from "./pages/StudentModel.vue"

import "./styles/fonts.css"
import "./styles/body.css"

if (!window.contextData) {
   const urlParams = new URLSearchParams(window.location.search);
   const token = urlParams.get('token');
   window.contextData = JSON.parse(token)
}

const app = createApp(App)
app.use(VNetworkGraph)
app.use(VueApexCharts)

// ADD STUDENT VIEW COMPONENTS BELLOW
if (window.contextData.roles.split(",").includes("StudentEnrollment")) {
   app.component(StudentModel.name, StudentModel)
   .component(StudentQuiz.name, StudentQuiz)
   .component(SettingsPage.name, SettingsPage)
} else {
   app.component(HomePage.name, HomePage)
      .component(DomainEditor.name, DomainEditor)
      .component(QuizAuthoring.name, QuizAuthoring)
      .component(AdaptiveTutor.name, AdaptiveTutor)
      .component(SettingsPage.name, SettingsPage)

}

app.provide("currentTab", ref("CourseSelection"));


function getSessionConfig() {
   return new Promise((resolve, reject) => {
      const contextData = window.contextData

      if (contextData.storage_target === "cookie") {
         resolve({key: "withCredentials", value: true})

      } else {
         let platformOrigin = new URL(contextData.oidc_auth_domain).origin
         let parent = window.parent || window.opener
         let targetFrame = contextData.storage_target === "_parent" ? parent : parent.frames[contextData.storage_target];
         const messageId = crypto.randomUUID()

         targetFrame.postMessage({
            "subject": "lti.get_data",
            "message_id": messageId,
            "key": "aspire_session_id",
         }, platformOrigin)

         window.addEventListener('message', function handleResponse(event) {
            if (event.data.subject === "lti.get_data.response") {
               window.removeEventListener('message', handleResponse);
               resolve({key: "headers", value: {"x-session-cookie": event.data.value}})
            }

            if (event.data.error) {
               reject(new Error(`${event.data.error.code} - ${event.data.error.message}`))
            }
         })

         setTimeout(() => {
            reject(new Error("Error: Session ID retrieval timed out"))
         }, 5000)
      }
   })
}

axios.interceptors.request.use(async (config) => {
   try {
      const sessionConfig = await getSessionConfig()
      config[sessionConfig.key] = sessionConfig.value

      return config

   } catch (error) {
      return Promise.reject(error)
   }
})

app.mount("#app")


