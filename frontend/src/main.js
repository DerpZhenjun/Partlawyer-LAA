import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

// 1. 引入 Bootstrap (CSS 和 JS)
import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap/dist/js/bootstrap.bundle.min.js' // 使用 bundle 版本以支持下拉菜单等交互组件

// 2. 引入 FontAwesome 图标库 (Home.vue 里用了 fas fa-search 等图标)
// 如果您还没安装，请在终端运行: npm install @fortawesome/fontawesome-free
import '@fortawesome/fontawesome-free/css/all.min.css'

// 3. 引入全局样式
import './style.css'

const app = createApp(App)

app.use(router) // 挂载路由
app.mount('#app')