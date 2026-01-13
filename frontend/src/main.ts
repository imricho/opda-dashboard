import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import './style.css'

import "@tabler/core/dist/css/tabler.min.css"
import "@tabler/core/dist/js/tabler.min.js";
import "tabulator-tables/dist/css/tabulator.min.css";// optional, for some tabler behaviors

createApp(App).use(router).mount('#app')