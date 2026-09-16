import { createRouter, createWebHistory } from 'vue-router'
import PublicHome from '@/views/PublicHome.vue'
import ProvinceGuide from '@/views/ProvinceGuide.vue'
import Dashboard from '@/views/Dashboard.vue'
import CaseCenter from '@/views/CaseCenter.vue'
import EvidenceCenter from '@/views/EvidenceCenter.vue'
import DocumentCenter from '@/views/DocumentCenter.vue'
import DeadlineCenter from '@/views/DeadlineCenter.vue'
import KnowledgeCenter from '@/views/KnowledgeCenter.vue'
import ZhejiangLA from '@/views/Zhejiang/LA.vue'
import ZhejiangEL from '@/views/Zhejiang/EL.vue'
import GuangdongLA from '@/views/Guangdong/LA.vue'
import GuangdongEL from '@/views/Guangdong/EL.vue'
import WIA from '@/views/others/WIA.vue'

const adminMeta = (eyebrow, title) => ({ layout: 'admin', eyebrow, title })

const routes = [
  { path: '/', name: 'public-home', component: PublicHome, meta: { title: '劳动仲裁文书助手' } },
  { path: '/province/:slug', name: 'province-guide', component: ProvinceGuide, meta: { title: '各省劳动仲裁办理指南' } },
  { path: '/documents/zhejiang/application', component: ZhejiangLA, meta: { title: '浙江省劳动仲裁申请书' } },
  { path: '/documents/zhejiang/evidence', component: ZhejiangEL, meta: { title: '浙江省证据清单' } },
  { path: '/documents/guangdong/application', component: GuangdongLA, meta: { title: '广东省劳动仲裁申请书' } },
  { path: '/documents/guangdong/evidence', component: GuangdongEL, meta: { title: '广东省证据清单' } },
  { path: '/documents/injury', component: WIA, meta: { title: '工伤仲裁申请书' } },

  { path: '/admin', name: 'admin-dashboard', component: Dashboard, meta: adminMeta('数据概览', '管理后台') },
  { path: '/admin/cases', name: 'admin-cases', component: CaseCenter, meta: adminMeta('案件管理', '案件中心') },
  { path: '/admin/evidence', name: 'admin-evidence', component: EvidenceCenter, meta: adminMeta('材料管理', '证据中心') },
  { path: '/admin/documents', name: 'admin-documents', component: DocumentCenter, meta: adminMeta('模板与生成', '文书管理') },
  { path: '/admin/deadlines', name: 'admin-deadlines', component: DeadlineCenter, meta: adminMeta('时效管理', '时效与日程') },
  { path: '/admin/knowledge', name: 'admin-knowledge', component: KnowledgeCenter, meta: adminMeta('内容管理', '法规知识库') },

  { path: '/documents', redirect: '/' },
  { path: '/cases', redirect: '/admin/cases' },
  { path: '/evidence', redirect: '/admin/evidence' },
  { path: '/deadlines', redirect: '/admin/deadlines' },
  { path: '/knowledge', redirect: '/admin/knowledge' },
  { path: '/zhejiang/la', redirect: '/documents/zhejiang/application' },
  { path: '/zhejiang/el', redirect: '/documents/zhejiang/evidence' },
  { path: '/guangdong/la', redirect: '/documents/guangdong/application' },
  { path: '/guangdong/el', redirect: '/documents/guangdong/evidence' },
  { path: '/wia', redirect: '/documents/injury' },
]

const router=createRouter({history:createWebHistory(import.meta.env.BASE_URL),routes,scrollBehavior(to){return to.hash?{el:to.hash,behavior:'smooth'}:{top:0}}})
router.afterEach(to=>{document.title=to.meta.title?`${to.meta.title} · LabourLawyer`:'LabourLawyer · 劳动仲裁文书助手'})
export default router
