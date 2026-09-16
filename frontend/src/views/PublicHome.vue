<template>
  <main class="public-home">
    <section class="public-hero">
      <div class="hero-copy">
        <span class="service-label"><i class="fa-solid fa-scale-balanced"></i> 劳动者办事助手</span>
        <h1>申请劳动仲裁，<br><em>先把文书和证据准备好</em></h1>
        <p>选择你实际工作地或公司所在地的省份，查看当地办理流程，并生成对应格式的仲裁申请书和证据清单。</p>
        <label class="province-search">
          <i class="fa-solid fa-location-dot"></i>
          <input v-model="query" placeholder="输入省份名称，例如：浙江、广东" aria-label="搜索省份">
          <button v-if="query" @click="query=''" aria-label="清空"><i class="fa-solid fa-xmark"></i></button>
        </label>
        <div class="jurisdiction-tip"><i class="fa-solid fa-circle-info"></i><span><strong>不知道该选哪里？</strong>一般可选择实际工作地或用人单位所在地。</span></div>
      </div>
      <div class="simple-steps" aria-label="使用步骤">
        <div class="steps-head"><span><i class="fa-solid fa-wand-magic-sparkles"></i></span><div><strong>从这里开始</strong><small>准备材料不走弯路</small></div></div>
        <div class="step-item"><b><i class="fa-solid fa-map-location-dot"></i></b><span><strong>选择办理省份</strong><small>匹配当地模板和要求</small></span></div>
        <div class="step-item"><b><i class="fa-solid fa-pen-to-square"></i></b><span><strong>填写并生成文书</strong><small>申请书与证据清单</small></span></div>
        <div class="step-item"><b><i class="fa-solid fa-building-columns"></i></b><span><strong>前往官方平台</strong><small>在线提交或窗口办理</small></span></div>
      </div>
    </section>

    <section class="province-section" id="provinces">
      <div class="section-heading"><div><span><i class="fa-solid fa-compass"></i> 按省份办理</span><h2>{{ query ? '搜索结果' : '请选择办理省份' }}</h2></div><p><i class="fa-solid fa-circle-check"></i> 标有“可以生成文书”的省份可直接填写并下载</p></div>
      <div v-if="query && !filteredProvinces.length" class="no-result">暂未找到该地区，请换一个名称试试。</div>
      <template v-if="query">
        <div class="province-grid"><ProvinceCard v-for="item in filteredProvinces" :key="item.slug" :province="item" /></div>
      </template>
      <template v-else>
        <div class="ready-grid">
          <ProvinceCard v-for="item in readyProvinces" :key="item.slug" :province="item" featured />
        </div>
        <details class="all-provinces">
          <summary>查看全国其他省份 <span>{{ provinces.length - readyProvinces.length }} 个地区</span><i class="fa-solid fa-chevron-down"></i></summary>
          <div v-for="group in provinceGroups" :key="group" class="province-group">
            <h3>{{ group }}</h3><div><RouterLink v-for="item in byGroup(group)" :key="item.slug" :to="`/province/${item.slug}`">{{ item.shortName }}<i v-if="item.status==='guide'" class="fa-solid fa-circle-check"></i></RouterLink></div>
          </div>
        </details>
      </template>
    </section>

    <section class="process-section" id="process">
      <div class="section-heading"><div><span>办理前先了解</span><h2>劳动仲裁一般怎么申请</h2></div><p>各地细节可能不同，请以所选省份官方办事指南为准</p></div>
      <div class="process-list"><article v-for="(item,index) in commonProcess" :key="item.title"><b>{{ index+1 }}</b><div><h3>{{ item.title }}</h3><p>{{ item.text }}</p></div></article></div>
      <div class="deadline-warning"><i class="fa-regular fa-clock"></i><div><strong>注意仲裁时效</strong><p>一般劳动争议的仲裁时效为一年，从知道或应当知道权利被侵害之日起计算；拖欠劳动报酬等情形存在特别规则。</p></div></div>
    </section>

    <section class="faq-section" id="faq">
      <div class="section-heading"><div><span>常见问题</span><h2>第一次申请，先看这几项</h2></div></div>
      <div class="faq-list"><details v-for="item in faqs" :key="item.q"><summary>{{ item.q }}<i class="fa-solid fa-plus"></i></summary><p>{{ item.a }}</p></details></div>
    </section>
  </main>
</template>

<script setup>
import { computed, ref } from 'vue'
import { RouterLink } from 'vue-router'
import ProvinceCard from '@/components/ProvinceCard.vue'
import { commonProcess, provinceGroups, provinces } from '@/data/provinces'

const query=ref('')
const readyProvinces=computed(()=>provinces.filter(item=>item.status==='ready'||item.status==='guide'))
const filteredProvinces=computed(()=>{const keyword=query.value.trim();return keyword?provinces.filter(item=>`${item.name}${item.shortName}`.includes(keyword)):provinces})
const byGroup=group=>provinces.filter(item=>item.region===group&&!readyProvinces.value.includes(item))
const faqs=[
  {q:'应该向哪里的仲裁委员会申请？',a:'一般由劳动合同履行地（实际工作地）或者用人单位所在地的劳动人事争议仲裁委员会管辖。两地不一致时，可先查看当地官方指南或拨打 12333 咨询。'},
  {q:'没有劳动合同，还能申请仲裁吗？',a:'可以。可用工资流水、社保缴费记录、工牌、考勤、工作聊天记录等材料证明劳动关系。请尽量保留原始载体。'},
  {q:'申请劳动仲裁收费吗？',a:'劳动争议仲裁不收费。委托律师、打印复印、鉴定等其他费用需按实际情况承担。'},
  {q:'网上提交以后多久知道是否受理？',a:'通常仲裁委员会在收到申请后五日内审查是否符合受理条件；材料不完整的，会通知补正。各地平台展示时间可能不同。'},
]

</script>

<style scoped>
.public-home{color:#24364a}.public-hero{max-width:1180px;margin:auto;padding:34px 24px 30px;display:grid;grid-template-columns:minmax(0,1.4fr) 310px;gap:58px;align-items:center}.service-label{display:inline-flex;align-items:center;gap:7px;color:#0f766e;font-size:14px;font-weight:700}.hero-copy h1{margin:10px 0 12px;color:#182b40;font-size:clamp(34px,4.1vw,52px);line-height:1.18;letter-spacing:-.04em}.hero-copy h1 em{color:#147c72;font-style:normal}.hero-copy>p{max-width:670px;margin:0 0 18px;color:#596a7b;font-size:16px;line-height:1.7}.province-search{max-width:650px;height:54px;padding:0 17px;display:flex;align-items:center;gap:12px;border:2px solid #d7e2e3;border-radius:13px;background:#fff;box-shadow:0 12px 35px rgba(30,61,79,.08)}.province-search>i{color:#178278}.province-search input{flex:1;border:0;outline:0;color:#21354a;font-size:16px}.province-search button{width:30px;height:30px;border:0;border-radius:50%;color:#748391;background:#edf1f3}.jurisdiction-tip{margin-top:11px;display:flex;align-items:flex-start;gap:8px;color:#687787;font-size:13px}.jurisdiction-tip i{margin-top:3px;color:#2a8d84}.jurisdiction-tip strong{color:#374b60}.simple-steps{padding:20px;border:1px solid #dfe6e9;border-radius:16px;background:#f7faf9;box-shadow:0 16px 45px rgba(34,65,77,.06)}.step-title{display:block;margin-bottom:13px;color:#758493;font-size:13px}.simple-steps>div{display:flex;align-items:center;gap:13px}.simple-steps b{width:34px;height:34px;display:grid;place-items:center;border-radius:10px;color:#fff;background:#167a72}.simple-steps strong,.simple-steps small{display:block}.simple-steps strong{font-size:15px}.simple-steps small{margin-top:2px;color:#7a8997;font-size:12px}.simple-steps>i{margin:6px 0 6px 12px;color:#aebbc1;font-size:11px}.province-section,.process-section,.faq-section{max-width:1180px;margin:auto;padding:38px 24px}.province-section{border-top:1px solid #e7ebee}.section-heading{display:flex;align-items:flex-end;justify-content:space-between;gap:30px;margin-bottom:20px}.section-heading span{color:#138076;font-size:13px;font-weight:700}.section-heading h2{margin:5px 0 0;color:#1b3046;font-size:30px}.section-heading>p{margin:0;color:#7b8997;font-size:13px}.ready-grid,.province-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}.province-card{position:relative;min-height:104px;padding:18px;display:grid;grid-template-columns:46px 1fr auto;align-items:center;gap:13px;border:1px solid #e0e6e9;border-radius:13px;background:#fff;transition:.18s}.province-card:hover{transform:translateY(-2px);border-color:#9fc8c3;box-shadow:0 13px 32px rgba(27,62,74,.08)}.province-mark{width:46px;height:46px;display:grid;place-items:center;border-radius:12px;color:#0d716a;background:#e4f4f1;font-size:18px;font-weight:800}.province-info h3{margin:0;color:#22364b;font-size:16px}.province-info p{margin:5px 0 0;color:#7c8996;font-size:12px}.availability{padding:5px 8px;border-radius:20px;font-size:11px}.availability.ready{color:#087267;background:#e6f6f3}.availability.guide{color:#86601d;background:#fff5df}.availability.pending{color:#75818d;background:#f0f3f5}.card-arrow{display:none}.all-provinces{margin-top:20px;border:1px solid #e1e6e9;border-radius:13px;background:#fff}.all-provinces summary{padding:17px 20px;display:flex;align-items:center;cursor:pointer;color:#34495e;font-size:14px;font-weight:700;list-style:none}.all-provinces summary span{margin-left:8px;color:#8996a2;font-size:12px;font-weight:400}.all-provinces summary i{margin-left:auto}.province-group{padding:17px 20px;border-top:1px solid #e7ebee;display:grid;grid-template-columns:70px 1fr;gap:20px}.province-group h3{margin:5px 0;color:#697888;font-size:13px}.province-group>div{display:flex;gap:8px;flex-wrap:wrap}.province-group a{min-width:72px;padding:7px 10px;border-radius:7px;color:#405367;background:#f5f7f8;text-align:center;font-size:13px}.province-group a:hover{color:#0f766e;background:#eaf5f3}.province-group a i{margin-left:4px;color:#1a8d82;font-size:9px}.no-result{padding:45px;border:1px dashed #ccd6db;border-radius:12px;color:#7b8895;text-align:center}.process-section{max-width:none;padding-left:max(24px,calc((100% - 1132px)/2));padding-right:max(24px,calc((100% - 1132px)/2));background:#f4f8f7}.process-list{display:grid;grid-template-columns:repeat(5,1fr);gap:10px}.process-list article{position:relative;min-height:180px;padding:20px;border:1px solid #dde6e5;border-radius:12px;background:#fff}.process-list b{width:30px;height:30px;display:grid;place-items:center;border-radius:8px;color:#11746c;background:#e5f4f2}.process-list h3{margin:20px 0 8px;font-size:15px}.process-list p{margin:0;color:#697988;font-size:13px;line-height:1.65}.deadline-warning{margin-top:16px;padding:17px 20px;display:flex;align-items:flex-start;gap:13px;border:1px solid #efd9ad;border-radius:11px;background:#fff9ec}.deadline-warning>i{margin-top:3px;color:#ad761e}.deadline-warning strong{font-size:14px}.deadline-warning p{margin:4px 0 0;color:#77694e;font-size:13px;line-height:1.6}.faq-list{display:grid;grid-template-columns:1fr 1fr;gap:12px}.faq-list details{border:1px solid #e0e6e9;border-radius:11px;background:#fff}.faq-list summary{padding:17px 18px;display:flex;justify-content:space-between;cursor:pointer;color:#2b3e52;font-size:14px;font-weight:700;list-style:none}.faq-list summary i{color:#72908d;font-size:12px}.faq-list p{margin:0;padding:0 18px 18px;color:#667687;font-size:13px;line-height:1.75}@media(max-width:900px){.public-hero{grid-template-columns:1fr;gap:25px;padding-top:36px}.simple-steps{display:grid;grid-template-columns:1fr auto 1fr auto 1fr;align-items:center}.simple-steps .step-title{grid-column:1/-1}.simple-steps>i{margin:0 10px;transform:rotate(-90deg)}.ready-grid,.province-grid{grid-template-columns:1fr 1fr}.process-list{grid-template-columns:1fr 1fr}}@media(max-width:620px){.public-hero{padding:26px 16px 28px}.hero-copy h1{font-size:34px}.hero-copy>p{font-size:15px}.simple-steps{display:none}.province-section,.faq-section{padding:32px 16px}.section-heading{align-items:flex-start;flex-direction:column;gap:8px}.section-heading h2{font-size:24px}.ready-grid,.province-grid{grid-template-columns:1fr}.province-card{grid-template-columns:42px 1fr 20px}.province-mark{width:42px;height:42px}.availability{position:absolute;right:15px;top:13px}.card-arrow{display:block;color:#a0abb4}.province-group{grid-template-columns:1fr}.process-section{padding:38px 16px}.process-list{grid-template-columns:1fr}.process-list article{min-height:0}.faq-list{grid-template-columns:1fr}.province-group a{min-width:65px}}
/* Refined public-service visual system */
.public-home{overflow:hidden;background:linear-gradient(180deg,#fbfdfd 0,#fff 34%,#fff 100%)}
.public-hero{position:relative;isolation:isolate;padding-top:42px;padding-bottom:40px}
.public-hero:before{content:'';position:absolute;z-index:-1;width:620px;height:420px;right:-220px;top:-170px;border-radius:50%;background:radial-gradient(circle,rgba(23,137,126,.11),rgba(23,137,126,0) 68%);pointer-events:none}
.service-label{padding:6px 10px;border:1px solid #d6e9e6;border-radius:999px;background:rgba(238,249,247,.82);font-size:13px}
.hero-copy h1{max-width:720px;font-size:clamp(38px,4.3vw,56px)}
.province-search{height:58px;border-color:#ccdddf;border-width:1px;box-shadow:0 16px 40px rgba(33,65,77,.09)}
.province-search:focus-within{border-color:#45a198;box-shadow:0 0 0 4px rgba(20,124,114,.09),0 16px 40px rgba(33,65,77,.09)}
.simple-steps{position:relative;padding:22px 23px;border-color:#d8e6e5;border-radius:20px;background:rgba(250,253,252,.92);box-shadow:0 22px 60px rgba(27,65,72,.09)}
.steps-head{padding-bottom:17px!important;border-bottom:1px solid #e2eae9}
.steps-head>span{width:40px;height:40px;display:grid;place-items:center;border-radius:12px;color:#fff;background:linear-gradient(145deg,#188d82,#0b6865);box-shadow:0 8px 18px rgba(15,118,110,.18)}
.steps-head strong,.steps-head small{display:block}.steps-head strong{color:#233a4e;font-size:14px}.steps-head small{margin-top:3px;color:#81909c;font-size:12px}
.simple-steps .step-item{position:relative;padding:15px 0 0;align-items:center;gap:13px}
.simple-steps .step-item:not(:last-child):after{content:'';position:absolute;left:16px;top:48px;width:1px;height:14px;background:#cbdedb}
.simple-steps .step-item b{width:33px;height:33px;flex:0 0 33px;border:1px solid #d1e6e2;border-radius:10px;color:#13766e;background:#eaf7f5;font-size:13px}
.simple-steps .step-item strong{color:#30465a;font-size:14px}.simple-steps .step-item small{color:#81909d;font-size:12px}
.province-section{position:relative;padding-top:44px;border-top:1px solid #e5ecee}
.section-heading span i{margin-right:5px}.section-heading>p i{margin-right:6px;color:#128177}
.ready-grid{grid-template-columns:repeat(6,minmax(0,1fr));gap:16px}
.ready-grid :deep(.province-card){grid-column:span 2;display:flex;grid-template-columns:none;align-items:stretch;gap:0;padding:22px 22px 0;min-height:208px;border-radius:18px;background:linear-gradient(145deg,#fff 50%,var(--card-soft))}
.ready-grid :deep(.province-card:nth-child(-n+2)){grid-column:span 3;min-height:222px}
.province-grid :deep(.province-card){display:flex;grid-template-columns:none;align-items:stretch;gap:0;padding:22px 22px 0;min-height:208px;border-radius:18px;background:linear-gradient(145deg,#fff 50%,var(--card-soft))}
.ready-grid :deep(.province-card:hover),.province-grid :deep(.province-card:hover){transform:translateY(-4px);border-color:color-mix(in srgb,var(--card-accent) 32%,#dfe7ea);box-shadow:0 18px 42px rgba(25,52,68,.12)}
.all-provinces{margin-top:22px;border-color:#dce5e8;border-radius:16px;box-shadow:0 8px 26px rgba(31,56,70,.035)}
.all-provinces summary{min-height:58px;padding:16px 22px}.all-provinces summary i{width:28px;height:28px;display:grid;place-items:center;border-radius:50%;background:#eff5f5;color:#54716e;font-size:11px;transition:transform .2s}.all-provinces[open] summary i{transform:rotate(180deg)}
.province-group a{border:1px solid transparent;transition:.17s}.province-group a:hover{border-color:#cfe4e1}
@media(max-width:900px){.ready-grid{grid-template-columns:repeat(2,minmax(0,1fr))}.ready-grid :deep(.province-card),.ready-grid :deep(.province-card:nth-child(-n+2)){grid-column:span 1}.public-hero:before{right:-330px}.simple-steps{display:block}.simple-steps .steps-head{display:flex}.simple-steps .step-item{display:flex}.simple-steps .step-item b{display:grid}.simple-steps .step-item:not(:last-child):after{display:block}}
@media(max-width:620px){.public-hero{padding-top:28px}.hero-copy h1{font-size:35px}.province-search{height:54px}.ready-grid{grid-template-columns:1fr;gap:13px}.ready-grid :deep(.province-card),.ready-grid :deep(.province-card:nth-child(-n+2)){grid-column:1}.section-heading>p{font-size:12px}.simple-steps{display:none}}
</style>
