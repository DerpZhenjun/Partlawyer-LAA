import { createRouter, createWebHistory } from 'vue-router'

// ==========================================
// 1. 引入页面组件 (Page Components)
// ==========================================

// 首页
import Home from '@/views/Home.vue'

// [已删除] QA 组件现在直接在 Home.vue 中引入，不需要在这里配置路由了
// import QA from '@/views/QA.vue'  <-- 这一行删掉

// 浙江省相关文书页面
import ZhejiangLA from '@/views/Zhejiang/LA.vue' // 劳动仲裁申请书
import ZhejiangEL from '@/views/Zhejiang/EL.vue' // 证据清单

// 广东省相关文书页面
import GuangdongLA from '@/views/Guangdong/LA.vue' // 劳动仲裁申请书
import GuangdongEL from '@/views/Guangdong/EL.vue' // 证据清单

// --- 工伤仲裁 (通用文书) ---
import WIA from '@/views/others/WIA.vue' 

// ==========================================
// 2. 创建路由实例
// ==========================================
const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  
  // ==========================================
  // 3. 定义路由规则 (Routes)
  // ==========================================
  routes: [
    // --- 首页 (根路径) ---
    {
      path: '/',
      name: 'home',
      component: Home
    },

    // [已删除] 原来的 /qa 路由块删掉，因为现在它是 Home 页面的一部分
    // 如果你以后非要一个独立的测试页，记得把 import 路径改成 '@/components/QA.vue'

    // ==========================
    // 浙江省 (Zhejiang)
    // ==========================
    {
      path: '/zhejiang/la',
      name: 'zhejiang-la',
      component: ZhejiangLA
    },
    {
      path: '/zhejiang/el',
      name: 'zhejiang-el',
      component: ZhejiangEL
    },

    // ==========================
    // 广东省 (Guangdong)
    // ==========================
    {
      path: '/guangdong/la',
      name: 'guangdong-la',
      component: GuangdongLA
    },
    {
      path: '/guangdong/el',
      name: 'guangdong-el',
      component: GuangdongEL
    },

    // ==========================
    // 其他 / 通用文书 (Others)
    // ==========================
    {
      path: '/wia', 
      name: 'wia',
      component: WIA
    }
  ]
})

export default router