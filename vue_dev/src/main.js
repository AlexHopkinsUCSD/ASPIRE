import { createApp, ref } from 'vue'
import App from './App.vue'
import VNetworkGraph from "v-network-graph"
import "v-network-graph/lib/style.css"
// import HelloWorld from "./components/HelloWorld.vue"
// import RegisterDomainModel from "./components/RegisterDomainModel.vue"
// import CreateModule from "./components/CreateModule.vue"
// import QuizCreation from "./components/QuizCreation.vue"
// import QuizEditing from "./components/QuizEditing.vue"
import HomePage from "./components/HomePage.vue"
import DomainEditor from "./pages/DomainEditor.vue"
import QuizAuthoring from "./components/QuizAuthoring.vue"
import AdaptiveTutor from "./components/AdaptiveTutor.vue"
import SettingsPage from "./components/SettingsPage.vue"
import "./styles/fonts.css"
import "./styles/body.css"

const app = createApp(App)
app.use(VNetworkGraph)

app.component(HomePage.name, HomePage)
   .component(DomainEditor.name, DomainEditor)
   .component(QuizAuthoring.name, QuizAuthoring)
   .component(AdaptiveTutor.name, AdaptiveTutor)
   .component(SettingsPage.name, SettingsPage)
   
   
// app.component(HelloWorld.name, HelloWorld)
//     .component(RegisterDomainModel.name, RegisterDomainModel)
//     .component(CreateModule.name, CreateModule)
//     .component(QuizCreation.name, QuizCreation)
//     .component(QuizEditing.name, QuizEditing)

app.provide("currentTab", ref("CourseSelection"));
app.mount('#app')

