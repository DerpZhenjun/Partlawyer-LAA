<template>
  <main v-if="province" class="province-page">
    <section class="province-banner">
      <div class="breadcrumb"><RouterLink to="/">首页</RouterLink><i class="fa-solid fa-chevron-right"></i><span>{{ province.name }}</span></div>
      <div class="province-title"><span>{{ province.shortName.slice(0,1) }}</span><div><small>{{ province.status === 'ready' ? '本省文书可以在线生成' : '省份办事入口' }}</small><h1>{{ province.name }}劳动仲裁</h1><p>先生成申请材料，再按本省官方流程提交。</p></div></div>
      <div v-if="isZhejiang" class="official-facts"><div><i class="fa-solid fa-laptop-file"></i><span>现场办理次数<strong>0 次</strong></span></div><div><i class="fa-regular fa-clock"></i><span>官方承诺时间<strong>44 个工作日</strong></span></div><div><i class="fa-solid fa-phone"></i><span>办事咨询<strong>0571-85119566</strong></span></div></div>
      <div v-else-if="isGuangdong" class="official-facts"><div><i class="fa-solid fa-laptop-file"></i><span>办理方式<strong>网上 / 窗口</strong></span></div><div><i class="fa-regular fa-clock"></i><span>是否受理<strong>5 个工作日</strong></span></div><div><i class="fa-solid fa-phone"></i><span>办事咨询<strong>020-12345</strong></span></div></div>
    </section>

    <section class="action-area">
      <div class="document-panel">
        <div class="panel-heading"><span>先准备文书</span><h2>你需要填写这两份材料</h2><p>生成后请核对姓名、金额、日期和你的要求，再打印签字。</p></div>
        <div class="document-options">
          <RouterLink v-if="province.applicationRoute" :to="province.applicationRoute" class="document-option primary"><span><i class="fa-solid fa-file-signature"></i></span><div><small>申请时需要</small><h3>劳动人事争议仲裁申请书</h3><p>填写你的信息、公司信息、你的要求和事情经过</p></div><b>开始填写 <i class="fa-solid fa-arrow-right"></i></b></RouterLink>
          <div v-else class="document-option disabled"><span><i class="fa-solid fa-file-signature"></i></span><div><small>该省文书还在准备中</small><h3>劳动人事争议仲裁申请书</h3><p>请先查看右侧官方入口</p></div><b>暂未开放</b></div>
          <RouterLink v-if="province.evidenceRoute" :to="province.evidenceRoute" class="document-option"><span><i class="fa-solid fa-list-check"></i></span><div><small>与证据一起提交</small><h3>证据清单</h3><p>逐项填写材料名称、来源和能说明的事情</p></div><b>开始填写 <i class="fa-solid fa-arrow-right"></i></b></RouterLink>
          <div v-else class="document-option disabled"><span><i class="fa-solid fa-list-check"></i></span><div><small>该省文书还在准备中</small><h3>证据清单</h3><p>可先按下方清单整理材料</p></div><b>暂未开放</b></div>
        </div>
        <div v-if="province.status!=='ready'" class="template-notice"><i class="fa-solid fa-circle-info"></i>{{ province.name }}专用文书还在准备中。请以政府网站和当地仲裁委员会的最新要求为准。</div>
      </div>

      <aside class="official-card">
        <span class="official-label"><i class="fa-solid fa-building-columns"></i> 政府官方网站</span>
        <h2>{{ province.officialName }}</h2><p>{{ province.note }}</p>
        <div class="search-term"><small>办理事项</small><strong>“{{ province.searchKeyword }}”</strong></div>
        <a :href="province.officialUrl" target="_blank" rel="noopener noreferrer">打开官方办理页 <i class="fa-solid fa-arrow-up-right-from-square"></i></a>
        <small class="external-note">账号登录和材料提交都在政府网站完成，本网站不会代替你提交。</small>
      </aside>
    </section>

    <section class="guide-content">
      <div class="guide-main">
        <div class="content-heading"><span>提交步骤</span><h2>{{ province.shortName }}劳动仲裁怎么申请</h2></div>
        <div v-if="isGuangdong" class="jurisdiction-alert"><i class="fa-solid fa-location-dot"></i><div><strong>先确认该交到哪个仲裁委员会</strong><p>这个官方链接是广东省级仲裁院的页面，主要处理部分省直、中央驻穗单位和符合条件的大型企业争议。大多数劳动者应向实际工作地或公司所在地的市、区仲裁委员会申请。</p></div></div>
        <div class="flow-list"><article v-for="(item,index) in displayProcess" :key="item.title"><b>{{index+1}}</b><div><h3>{{item.title}}</h3><p>{{item.text}}</p></div></article></div>
        <div v-if="isZhejiang" class="conditions"><h3><i class="fa-regular fa-circle-check"></i> 提交前简单确认</h3><div><span v-for="item in zhejiangConditions" :key="item"><i class="fa-solid fa-check"></i>{{ item }}</span></div></div>
        <div class="official-reminder"><i class="fa-solid fa-triangle-exclamation"></i><p>不同城市的受理地点和具体要求可能不同。正式提交前，请在官方页面选择办理地点，并以当地仲裁委员会的要求为准。</p></div>
      </div>
      <aside class="material-card">
        <div class="content-heading"><span>提交前检查</span><h2>{{ isZhejiang ? '官方列出的 5 类材料' : isGuangdong ? '广东官方列出的材料' : '常用材料' }}</h2></div>
        <ul><li v-for="item in displayMaterials" :key="item"><i class="fa-regular fa-square-check"></i><span>{{item}}</span></li></ul>
        <div><strong>{{ isZhejiang ? '浙江官方页面说明' : isGuangdong ? '广东官方页面说明' : '材料小提示' }}</strong><p>{{ isZhejiang ? '以上材料页面均标注为 A4 纸、原件、2 份。线上或现场提交时，请再按具体办理地点核对。' : isGuangdong ? '申请书需要本人签名，副本按公司一方人数准备；证据材料页面标注为 2 份。提交前请再按实际受理机构核对。' : '聊天记录、邮件、考勤截图等电子材料尽量保留原始设备和完整上下文。' }}</p></div>
      </aside>
    </section>
  </main>
  <main v-else class="not-found"><h1>暂未找到该省份</h1><RouterLink to="/">返回选择省份</RouterLink></main>
</template>

<script setup>
import { computed } from 'vue'
import { RouterLink, useRoute } from 'vue-router'
import { commonMaterials, commonProcess, findProvince } from '@/data/provinces'
const route=useRoute()
const province=computed(()=>findProvince(route.params.slug))
const isZhejiang=computed(()=>province.value?.slug==='zhejiang')
const isGuangdong=computed(()=>province.value?.slug==='guangdong')
const zhejiangProcess=[
  {title:'准备并提交申请',text:'可以到公布的省、市、县劳动人事争议仲裁委员会提交，也可以邮寄，或通过“浙里办”APP中的“智慧仲裁”办理。'},
  {title:'等待是否受理的通知',text:'仲裁委员会收到申请后，会在 5 个工作日内决定是否受理，并通知申请人。'},
  {title:'参加调解或开庭',text:'受理后按通知参加调解或开庭。办结后，仲裁委员会会送达调解书、裁决书或决定书。'},
]
const zhejiangMaterials=['用人单位登记注册材料','劳动者身份证','《劳动人事争议仲裁申请书》','《证据清单》','能说明劳动关系和支持你要求的证据']
const zhejiangConditions=['争议属于劳动人事仲裁处理范围','你的要求以及事情经过写得清楚','申请人与争议有直接关系，公司信息明确','申请材料填写规范并准备齐全']
const guangdongProcess=[
  {title:'确认正确的仲裁委员会',text:'一般选择实际工作地或公司所在地的市、区仲裁委员会。只有符合省级受理范围时，才使用本页链接对应的广东省级仲裁院。'},
  {title:'准备并提交材料',text:'准备申请书、证据材料和身份证明等，可以按受理机构要求网上提交或到窗口办理。'},
  {title:'等待是否受理的通知',text:'官方页面显示，收到申请后会在 5 个工作日内决定是否受理并通知申请人。'},
  {title:'参加调解或开庭',text:'受理后按通知参加调解或开庭。通常自受理之日起 45 日内办结，复杂案件可依法延长 15 日。'},
]
const guangdongMaterials=['本人签名的《劳动人事争议仲裁申请书》','证据材料和《证据清单》（官方页面标注 2 份）','身份证复印件，并携带原件供核对','公司登记资料（按官方页面要求准备近期资料）','委托他人办理时另备授权委托书等材料']
const displayProcess=computed(()=>isZhejiang.value?zhejiangProcess:isGuangdong.value?guangdongProcess:commonProcess)
const displayMaterials=computed(()=>isZhejiang.value?zhejiangMaterials:isGuangdong.value?guangdongMaterials:commonMaterials)
</script>

<style scoped>
.province-page{color:#26394d;background:#fff}.province-banner{padding:26px max(24px,calc((100% - 1132px)/2)) 31px;background:linear-gradient(135deg,#edf7f5,#f9fbfa)}.breadcrumb{display:flex;align-items:center;gap:8px;color:#778694;font-size:12px}.breadcrumb i{font-size:8px}.province-title{margin-top:24px;display:flex;align-items:center;gap:17px}.province-title>span{width:64px;height:64px;display:grid;place-items:center;border-radius:17px;color:#fff;background:linear-gradient(145deg,#188479,#105e5b);font-size:25px;font-weight:800;box-shadow:0 10px 24px rgba(19,115,106,.18)}.province-title small{color:#178076;font-size:11px;font-weight:700}.province-title h1{margin:3px 0 4px;font-size:32px}.province-title p{margin:0;color:#71808e;font-size:13px}.official-facts{margin-top:25px;max-width:680px;display:grid;grid-template-columns:repeat(3,1fr);gap:10px}.official-facts>div{padding:11px 12px;display:flex;align-items:center;gap:9px;border:1px solid #d3e5e1;border-radius:10px;background:rgba(255,255,255,.72)}.official-facts i{color:#187b72}.official-facts span,.official-facts strong{display:block}.official-facts span{color:#77878a;font-size:9px}.official-facts strong{margin-top:2px;color:#304a50;font-size:12px}.action-area,.guide-content{max-width:1180px;margin:auto;padding:34px 24px;display:grid;grid-template-columns:minmax(0,1fr) 330px;gap:22px}.document-panel,.official-card,.guide-main,.material-card{border:1px solid #e0e6e9;border-radius:15px;background:#fff}.document-panel{padding:25px}.panel-heading>span,.content-heading>span{color:#128077;font-size:11px;font-weight:800}.panel-heading h2,.content-heading h2{margin:5px 0 6px;font-size:21px}.panel-heading p{margin:0;color:#74828f;font-size:12px}.document-options{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-top:20px}.document-option{min-height:190px;padding:18px;display:flex;flex-direction:column;border:1px solid #dde4e7;border-radius:13px;background:#fbfcfc}.document-option:hover:not(.disabled){transform:translateY(-2px);border-color:#8bbdb8;box-shadow:0 10px 28px rgba(34,70,78,.08)}.document-option>span{width:43px;height:43px;display:grid;place-items:center;border-radius:11px;color:#14776f;background:#e4f4f1}.document-option small{display:block;margin-top:13px;color:#7a8896;font-size:10px}.document-option h3{margin:3px 0 5px;font-size:16px}.document-option p{margin:0;color:#687887;font-size:11px;line-height:1.55}.document-option>b{margin-top:auto;padding-top:14px;color:#0f766e;font-size:11px}.document-option.primary{border-color:#abd0cc;background:#f5fbfa}.document-option.disabled{opacity:.66}.template-notice{margin-top:14px;padding:11px 13px;border-radius:8px;color:#6f654e;background:#fff8e9;font-size:11px}.template-notice i{margin-right:7px;color:#a97420}.official-card{align-self:start;padding:25px;color:#fff;background:linear-gradient(145deg,#102f47,#105f5d);border:0}.official-label{font-size:11px;color:#9ee1da}.official-label i{margin-right:6px}.official-card h2{margin:15px 0 9px;font-size:19px}.official-card>p{margin:0;color:#b9cbd2;font-size:12px;line-height:1.65}.search-term{margin:20px 0;padding:12px;border:1px solid rgba(255,255,255,.14);border-radius:9px;background:rgba(255,255,255,.06)}.search-term small,.search-term strong{display:block}.search-term small{color:#9eb4bf;font-size:9px}.search-term strong{margin-top:4px;font-size:12px}.official-card>a{height:42px;display:flex;align-items:center;justify-content:center;border-radius:8px;color:#133a42;background:#fff;font-size:12px;font-weight:800}.official-card>a i{margin-left:7px}.external-note{display:block;margin-top:10px;color:#95aeb8;font-size:9px;line-height:1.6}.guide-content{padding-top:8px;align-items:start}.guide-main,.material-card{padding:24px}.flow-list{margin-top:20px}.flow-list article{display:grid;grid-template-columns:34px 1fr;gap:13px;padding:16px 0;border-top:1px solid #e7ebed}.flow-list article>b{width:30px;height:30px;display:grid;place-items:center;border-radius:8px;color:#0f766e;background:#e7f5f2;font-size:11px}.flow-list h3{margin:0 0 5px;font-size:14px}.flow-list p{margin:0;color:#697988;font-size:12px;line-height:1.7}.conditions{margin:12px 0 16px;padding:16px;border-radius:10px;background:#f3f8f7}.conditions h3{margin:0 0 11px;color:#31544f;font-size:12px}.conditions h3 i{margin-right:7px;color:#167b72}.conditions>div{display:grid;grid-template-columns:1fr 1fr;gap:8px}.conditions span{display:flex;gap:7px;color:#607478;font-size:10px;line-height:1.5}.conditions span i{margin-top:3px;color:#22877d;font-size:8px}.official-reminder{padding:13px;display:flex;gap:10px;border-radius:9px;color:#75674b;background:#fff8e9;font-size:11px;line-height:1.6}.official-reminder i{margin-top:3px;color:#af781e}.official-reminder p{margin:0}.material-card ul{margin:18px 0;padding:0;list-style:none}.material-card li{padding:11px 0;display:flex;gap:9px;border-top:1px solid #e8ecee;color:#4e6072;font-size:11px;line-height:1.55}.material-card li i{margin-top:3px;color:#168177}.material-card>div:last-child{padding:13px;border-radius:9px;background:#f3f7f6}.material-card>div:last-child strong{font-size:11px}.material-card>div:last-child p{margin:5px 0 0;color:#6e7e8b;font-size:10px;line-height:1.6}.not-found{padding:100px 24px;text-align:center}.not-found a{color:#0f766e}
@media(max-width:850px){.action-area,.guide-content{grid-template-columns:1fr}.official-card{order:-1}.official-facts{max-width:none}}
@media(max-width:580px){.province-banner{padding:22px 16px 28px}.province-title>span{width:52px;height:52px}.province-title h1{font-size:25px}.official-facts{grid-template-columns:1fr}.action-area,.guide-content{padding:22px 16px}.document-panel,.official-card,.guide-main,.material-card{padding:18px}.document-options{grid-template-columns:1fr}.document-option{min-height:165px}.conditions>div{grid-template-columns:1fr}}
.jurisdiction-alert{margin:18px 0 4px;padding:14px 15px;display:flex;gap:11px;border:1px solid #ecd8ad;border-radius:10px;color:#6b5c3f;background:#fff9eb}.jurisdiction-alert>i{margin-top:3px;color:#b2781d}.jurisdiction-alert strong{font-size:12px}.jurisdiction-alert p{margin:5px 0 0;font-size:11px;line-height:1.65}
</style>
