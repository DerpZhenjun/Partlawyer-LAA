<template>
  <main class="document-page">
    <header class="page-hero">
      <div class="hero-inner">
        <RouterLink :to="config.backRoute" class="back-link"><i class="fa-solid fa-arrow-left"></i> 返回{{ config.shortName }}办理页</RouterLink>
        <div class="hero-copy">
          <span class="document-icon"><i class="fa-regular fa-file-lines"></i></span>
          <div><p class="eyebrow">{{ config.name }}官方格式</p><h1>劳动人事争议仲裁申请书</h1><p>按提示填写，我们会把内容放进{{ config.name }}官方申请书模板，并下载为 Word 文档。</p></div>
        </div>
        <div class="progress-strip" aria-label="填写步骤">
          <span v-for="(label, index) in steps" :key="label" :class="{ active: index === activeStep, done: index < activeStep }"><b>{{ index + 1 }}</b>{{ label }}</span>
        </div>
      </div>
    </header>

    <div class="page-grid">
      <form class="form-column" novalidate @submit.prevent="requestGeneration">
        <section class="form-section">
          <div class="section-heading"><span><i class="fa-regular fa-user"></i></span><div><small>第 1 步</small><h2>填写你的信息</h2><p>请按身份证上的内容填写。</p></div></div>
          <div class="fields two-columns">
            <label class="field full"><span>提交给哪个仲裁委员会 <em>必填</em></span><input v-model.trim="form.committeeName" type="text" placeholder="例如：杭州市劳动人事争议仲裁委员会" autocomplete="organization"><small>一般选择工作地或公司所在地的劳动人事争议仲裁委员会。</small></label>
            <label class="field"><span>姓名 <em>必填</em></span><input v-model.trim="form.applicantName" type="text" placeholder="身份证上的姓名" autocomplete="name"></label>
            <label class="field"><span>出生日期</span><input v-model="form.birthDate" type="date"></label>
            <fieldset class="field"><legend>性别</legend><div class="choice-row"><label v-for="item in ['男','女','其他']" :key="item"><input v-model="form.gender" type="radio" :value="item"><span>{{ item }}</span></label></div></fieldset>
            <label class="field"><span>民族</span><input v-model.trim="form.nationality" type="text" placeholder="例如：汉族"></label>
            <label class="field"><span>身份证号码 <em>必填</em></span><input v-model.trim="form.idNumber" type="text" maxlength="30" placeholder="请核对后再填写" autocomplete="off"></label>
            <label class="field"><span>联系电话 <em>必填</em></span><input v-model.trim="form.phone" type="tel" placeholder="能接到通知的手机号" autocomplete="tel"></label>
            <label class="field"><span>户口类型</span><select v-model="form.householdType"><option value="">请选择</option><option v-for="item in householdOptions" :key="item">{{ item }}</option></select></label>
            <label class="field full"><span>身份证住址 <em>必填</em></span><input v-model.trim="form.idAddress" type="text" placeholder="身份证上写的住址" autocomplete="street-address"></label>
            <label v-if="props.province==='guangdong'" class="field full"><span>你的收件地址</span><div class="field-action"><input v-model.trim="form.applicantMailingAddress" type="text" placeholder="用于接收仲裁材料，不填则使用身份证住址"><button type="button" @click="form.applicantMailingAddress=form.idAddress">同身份证住址</button></div></label>
          </div>
        </section>

        <section class="form-section">
          <div class="section-heading"><span><i class="fa-regular fa-building"></i></span><div><small>第 2 步</small><h2>填写公司信息</h2><p>不确定时，可查看劳动合同或公司的营业执照信息。</p></div></div>
          <div class="fields two-columns">
            <label class="field full"><span>公司全称 <em>必填</em></span><input v-model.trim="form.respondentName" type="text" placeholder="请填写营业执照上的完整名称" autocomplete="organization"></label>
            <label class="field"><span>统一社会信用代码</span><input v-model.trim="form.socialCreditCode" type="text" maxlength="30" placeholder="营业执照上的 18 位代码"></label>
            <label class="field"><span>法定代表人姓名</span><input v-model.trim="form.legalRepName" type="text" placeholder="不知道可以暂时留空"></label>
            <label class="field full"><span>公司注册地址 <em>必填</em></span><input v-model.trim="form.registeredAddress" type="text" placeholder="营业执照上的住所"></label>
            <label class="field full"><span>实际工作地址 <em>必填</em></span><input v-model.trim="form.workAddress" type="text" placeholder="你平时上班的具体地址"></label>
            <label class="field full"><span>公司收件地址</span><div class="field-action"><input v-model.trim="form.mailingAddress" type="text" placeholder="用于接收仲裁材料，不清楚可与注册地址相同"><button type="button" @click="form.mailingAddress=form.registeredAddress">同注册地址</button></div></label>
            <label class="field"><span>法定代表人职务</span><input v-model.trim="form.legalRepPosition" type="text" placeholder="例如：执行董事"></label>
            <label class="field"><span>法定代表人电话</span><input v-model.trim="form.legalRepPhone" type="tel" placeholder="不知道可以留空"></label>
            <label class="field"><span>公司联系人</span><input v-model.trim="form.companyContact" type="text" placeholder="例如：人事负责人"></label>
            <label class="field"><span>联系人电话</span><input v-model.trim="form.companyContactPhone" type="tel" placeholder="不知道可以留空"></label>
          </div>
        </section>

        <section class="form-section">
          <div class="section-heading"><span><i class="fa-solid fa-list-check"></i></span><div><small>第 3 步</small><h2>你希望公司怎么处理</h2><p>一条写一件事，并写清时间和金额。最多填写 4 条。</p></div></div>
          <div class="example-box"><i class="fa-regular fa-lightbulb"></i><p><strong>参考写法：</strong>请求公司支付 2026 年 1 月至 3 月拖欠的工资共计 15,000 元。</p></div>
          <div class="request-list">
            <div v-for="(item,index) in form.requests" :key="index" class="request-item"><b>{{ index + 1 }}</b><textarea v-model.trim="form.requests[index]" rows="3" maxlength="300" :placeholder="index === 0 ? '请写明你的第一项要求' : '继续填写另一项要求'"></textarea><button v-if="form.requests.length > 1" type="button" aria-label="删除这一项" @click="removeRequest(index)"><i class="fa-regular fa-trash-can"></i></button></div>
          </div>
          <button v-if="form.requests.length < 4" type="button" class="add-button" @click="form.requests.push('')"><i class="fa-solid fa-plus"></i> 再加一项要求</button>
          <label v-if="props.province==='guangdong'" class="field calculation-field"><span>金额是怎么算的</span><textarea v-model.trim="form.claimCalculation" rows="5" maxlength="240" placeholder="例如：拖欠工资＝5000元/月 × 3个月＝15000元；经济补偿＝5000元/月 × 2个月＝10000元。没有金额的请求可以留空。"></textarea><small>广东官方申请书单独留有“仲裁请求计算公式”区域。</small></label>

          <div v-if="props.province==='guangdong'" class="guangdong-details">
            <div class="subsection-title"><span><i class="fa-solid fa-briefcase"></i></span><div><h3>补充工作基本情况</h3><p>这些内容来自广东官方申请书。知道多少填多少，不确定的可以先留空。</p></div></div>
            <div class="fields two-columns">
              <label class="field"><span>入职日期</span><input v-model="form.employmentDate" type="date"></label>
              <label class="field"><span>岗位或职务</span><input v-model.trim="form.jobTitle" type="text" placeholder="例如：运营专员"></label>
              <label class="field"><span>有没有签劳动合同</span><select v-model="form.signedContract"><option value="">请选择</option><option>有</option><option>无</option></select></label>
              <label class="field"><span>最后一份劳动合同期限</span><div class="date-range"><input v-model="form.contractStartDate" type="date"><b>至</b><input v-model="form.contractEndDate" type="date"></div></label>
              <label class="field full"><span>平时怎么上班</span><input v-model.trim="form.workSchedule" type="text" placeholder="例如：每周工作5天，每天8小时；或写明排班情况"></label>
              <label class="field"><span>是否需要考勤</span><select v-model="form.attendanceRequired"><option value="">请选择</option><option>是</option><option>否</option></select></label>
              <label class="field"><span>考勤方式</span><input v-model.trim="form.attendanceMethod" type="text" placeholder="例如：钉钉打卡、指纹"></label>
              <label class="field"><span>工资怎么发</span><select v-model="form.salaryPaymentMethod"><option value="">请选择</option><option>现金</option><option>转账</option></select></label>
              <label class="field"><span>领工资是否签收</span><select v-model="form.salaryReceiptRequired"><option value="">请选择</option><option>需要签收</option><option>不需要签收</option></select></label>
              <label class="field"><span>入职时工资标准</span><input v-model.trim="form.startingSalary" type="text" placeholder="例如：5000元/月"></label>
              <label class="field"><span>后来工资有没有调整</span><input v-model.trim="form.salaryAdjustments" type="text" placeholder="没有可写“无”"></label>
              <label class="field"><span>现在是否还在职</span><select v-model="form.currentlyEmployed"><option value="">请选择</option><option>是</option><option>否</option></select></label>
              <label class="field"><span>离职日期</span><input v-model="form.departureDate" type="date" :disabled="form.currentlyEmployed==='是'"></label>
              <label class="field full"><span>离职原因</span><input v-model.trim="form.departureReason" type="text" :disabled="form.currentlyEmployed==='是'" placeholder="仍在职不用填写；已离职请简单说明"></label>
              <label class="field"><span>离职前12个月平均工资</span><input v-model.trim="form.averageMonthlySalary" type="text" :disabled="form.currentlyEmployed==='是'" placeholder="例如：5200元/月"></label>
            </div>
          </div>
        </section>

        <section class="form-section">
          <div class="section-heading"><span><i class="fa-regular fa-pen-to-square"></i></span><div><small>第 4 步</small><h2>说明事情经过</h2><p>按时间顺序写清楚，不用写复杂的法律用语。</p></div></div>
          <div class="writing-tips"><span>建议写清</span><ul><li>什么时候入职、做什么工作</li><li>工资约定和实际发放情况</li><li>争议是怎样发生的</li><li>与上面各项要求有关的事实</li></ul></div>
          <label class="field"><span>事情经过和理由 <em>必填</em></span><textarea v-model.trim="form.factsReason" class="facts-area" rows="10" :maxlength="factsLimit" placeholder="例如：我于2024年3月1日入职该公司，担任……双方约定每月工资……从……开始，公司……"></textarea><small class="count">{{ form.factsReason.length }} / {{ factsLimit }}</small></label>
          <div class="fields two-columns compact-fields">
            <label class="field"><span>申请日期</span><input v-model="form.applicationDate" type="date"></label>
            <label class="field"><span>申请书副本份数</span><input v-model.number="form.copyCount" type="number" min="1" max="20"><small>通常按公司一方准备 1 份，现场要求以当地为准。</small></label>
          </div>
        </section>

        <div v-if="status.message" class="status-message" :class="status.type" role="status"><i :class="status.type==='success'?'fa-solid fa-circle-check':'fa-solid fa-circle-exclamation'"></i>{{ status.message }}</div>
        <div class="submit-area"><div><strong>生成{{ config.name }}官方格式 Word 文档</strong><small><i class="fa-solid fa-circle-info"></i> 可以直接下载空白模板；正式提交前请补全标为必填的内容。</small></div><button type="submit" :disabled="isSubmitting"><i :class="isSubmitting?'fa-solid fa-spinner fa-spin':'fa-regular fa-file-word'"></i>{{ isSubmitting ? '正在生成…' : '生成并下载申请书' }}</button></div>
      </form>

      <aside class="side-column">
        <div class="side-card official-info"><span class="side-label"><i class="fa-solid fa-building-columns"></i> {{ config.shortName }}官方办事信息</span><h2>提交前先准备这些</h2><ul><li><i class="fa-regular fa-id-card"></i><span><strong>身份证明</strong>身份证等有效证件</span></li><li><i class="fa-regular fa-building"></i><span><strong>公司登记信息</strong>公司全称、代码和地址</span></li><li><i class="fa-solid fa-link"></i><span><strong>劳动关系材料</strong>合同、工资流水、社保记录等</span></li><li><i class="fa-regular fa-folder-open"></i><span><strong>支持你要求的证据</strong>并另外制作证据清单</span></li></ul><RouterLink :to="config.evidenceRoute"><i class="fa-solid fa-list-check"></i> 接着制作证据清单</RouterLink></div>
        <div class="side-card online-card"><div><span>官方承诺</span><strong>{{ config.promise }}</strong><small>{{ config.handleNote }}</small></div><a :href="config.officialUrl" target="_blank" rel="noopener noreferrer">查看{{ config.shortName }}官方办理页 <i class="fa-solid fa-arrow-up-right-from-square"></i></a></div>
        <div class="draft-note"><i class="fa-regular fa-floppy-disk"></i><div><strong>内容已自动保存在这台设备</strong><p>刷新页面后仍可继续填写。下载完成后可用下方按钮清除。</p><button type="button" @click="clearDraft">清除已保存内容</button></div></div>
      </aside>
    </div>
  </main>

  <Teleport to="body">
    <div v-if="showConfirm" class="confirm-backdrop" @click.self="showConfirm=false">
      <section class="confirm-dialog" role="dialog" aria-modal="true" aria-labelledby="application-confirm-title">
        <button class="confirm-close" type="button" aria-label="取消生成" @click="showConfirm=false"><i class="fa-solid fa-xmark"></i></button>
        <span class="confirm-icon"><i class="fa-regular fa-file-word"></i></span>
        <h2 id="application-confirm-title">确认生成申请书？</h2>
        <template v-if="missingFields.length">
          <p>当前还有 <strong>{{ missingFields.length }} 项</strong>内容没有填写。确认后仍会生成官方模板，空白处可以在 Word 中继续填写。</p>
          <div class="missing-preview"><i class="fa-solid fa-circle-info"></i><span>{{ missingFields.slice(0, 5).join('、') }}<template v-if="missingFields.length > 5">等</template></span></div>
        </template>
        <p v-else>内容已填写完成。确认后将生成并下载 {{ config.name }}官方格式 Word 文档。</p>
        <div class="confirm-actions"><button type="button" class="cancel-button" @click="showConfirm=false">取消</button><button type="button" class="confirm-button" @click="confirmGeneration"><i class="fa-solid fa-download"></i> 确认生成</button></div>
      </section>
    </div>
  </Teleport>
</template>

<script setup>
import { computed, onBeforeUnmount, reactive, ref, watch } from 'vue'
import axios from 'axios'
import { RouterLink } from 'vue-router'
import { downloadDocument } from '@/composables/downloadDocument'

const props = defineProps({ province: { type: String, default: 'zhejiang' } })
const provinceConfigs = {
  zhejiang: { name:'浙江省', shortName:'浙江', backRoute:'/province/zhejiang', evidenceRoute:'/documents/zhejiang/evidence', apiPath:'/api/zhejiang/la/generate', promise:'44 个工作日', handleNote:'页面显示现场办理 0 次', officialUrl:'https://www.zjzwfw.gov.cn/zjservice-fe/#/workguide?localInnerCode=2510b7af-2402-4502-837c-14eb4a71177d' },
  guangdong: { name:'广东省', shortName:'广东', backRoute:'/province/guangdong', evidenceRoute:'/documents/guangdong/evidence', apiPath:'/api/guangdong/la/generate', promise:'5 个工作日', handleNote:'支持网上办理和窗口办理', officialUrl:'https://www.gdzwfw.gov.cn/portal/v3/guide/11440000553612461J244211105N00302' },
}
const config = computed(() => provinceConfigs[props.province] || provinceConfigs.zhejiang)
const factsLimit = computed(() => props.province === 'guangdong' ? 700 : 8000)
const API_BASE = (import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000').replace(/\/$/, '')
const DRAFT_KEY = `labourlawyer-${props.province}-application-draft-v5`
const steps = ['你的信息', '公司信息', '你的要求', '事情经过']
const householdOptions = ['本省非农业户口','本省农业户口','外省非农业户口','外省农业户口','港澳台人员','外籍人员']
const defaults = { committeeName:'',applicantName:'',birthDate:'',gender:'',nationality:'',idNumber:'',phone:'',householdType:'',idAddress:'',applicantMailingAddress:'',respondentName:'',socialCreditCode:'',registeredAddress:'',mailingAddress:'',workAddress:'',legalRepName:'',legalRepPhone:'',legalRepPosition:'',companyContact:'',companyContactPhone:'',requests:[''],claimCalculation:'',employmentDate:'',jobTitle:'',signedContract:'',contractStartDate:'',contractEndDate:'',workSchedule:'',attendanceRequired:'',attendanceMethod:'',salaryPaymentMethod:'',salaryReceiptRequired:'',startingSalary:'',salaryAdjustments:'',currentlyEmployed:'',departureDate:'',departureReason:'',averageMonthlySalary:'',factsReason:'',copyCount:1,applicationDate:'' }
const loadDraft = () => { try { return { ...defaults, ...JSON.parse(localStorage.getItem(DRAFT_KEY) || '{}') } } catch { return { ...defaults } } }
const form = reactive(loadDraft())
if (!Array.isArray(form.requests) || !form.requests.length) form.requests = ['']
const isSubmitting = ref(false)
const showConfirm = ref(false)
const missingFields = ref([])
const status = reactive({ type:'', message:'' })
let saveTimer
watch(form, () => { clearTimeout(saveTimer); saveTimer = setTimeout(() => localStorage.setItem(DRAFT_KEY, JSON.stringify(form)), 350) }, { deep:true })
onBeforeUnmount(() => clearTimeout(saveTimer))
const activeStep = computed(() => !form.applicantName || !form.idNumber || !form.phone || !form.idAddress ? 0 : !form.respondentName || !form.registeredAddress || !form.workAddress ? 1 : !form.requests.some(item => item.trim()) ? 2 : 3)
const removeRequest = index => form.requests.splice(index, 1)
const clearDraft = () => { localStorage.removeItem(DRAFT_KEY); Object.assign(form, { ...defaults, requests:[''] }); status.type='success'; status.message='已清除这台设备上保存的填写内容。'; window.scrollTo({ top:0, behavior:'smooth' }) }
const collectMissingFields = () => {
  const missing=[]
  if(!form.committeeName) missing.push('仲裁委员会'); if(!form.applicantName) missing.push('姓名'); if(!form.idNumber) missing.push('身份证号码'); if(!form.phone) missing.push('联系电话'); if(!form.idAddress) missing.push('身份证住址'); if(!form.respondentName) missing.push('公司全称'); if(!form.registeredAddress) missing.push('公司注册地址'); if(!form.workAddress) missing.push('实际工作地址'); if(!form.requests.some(item=>item.trim())) missing.push('至少一项要求'); if(form.factsReason.length<10) missing.push('事情经过（至少填写 10 个字）')
  return missing
}
const parseError = async error => { if(error.response?.data instanceof Blob){try{const data=JSON.parse(await error.response.data.text());return data.detail||'生成失败，请检查填写内容。'}catch{}} return error.response?.data?.detail||(error.code==='ERR_NETWORK'?'无法连接文书生成服务，请确认后端已经启动。':'生成失败，请稍后再试。') }
const requestGeneration = () => { status.message=''; missingFields.value=collectMissingFields(); showConfirm.value=true }
const confirmGeneration = () => { showConfirm.value=false; submitForm() }
const submitForm = async () => {
  status.message=''; isSubmitting.value=true
  try { const payload={...form,requests:form.requests.map(item=>item.trim()).filter(Boolean)}; const response=await axios.post(`${API_BASE}${config.value.apiPath}`,payload,{responseType:'blob',timeout:30000}); const filename=form.applicantName?`${form.applicantName}的劳动人事争议仲裁申请书.docx`:`${config.value.name}劳动人事争议仲裁申请书.docx`;await downloadDocument(response.data,filename);status.type='success';status.message='申请书已生成。请打开 Word 仔细核对后再签字提交。' } catch(error){status.type='error';status.message=await parseError(error)} finally{isSubmitting.value=false}
}
</script>

<style scoped>
.document-page{min-height:100vh;color:#24394a;background:#f5f8f7}.page-hero{padding:28px 24px 0;border-bottom:1px solid #dce8e5;background:linear-gradient(135deg,#f8fcfb 0,#eaf6f3 100%)}.hero-inner{max-width:1180px;margin:auto}.back-link{display:inline-flex;align-items:center;gap:7px;color:#5f756f;font-size:13px}.hero-copy{padding:28px 0 30px;display:flex;align-items:center;gap:18px}.document-icon{width:68px;height:68px;flex:0 0 68px;display:grid;place-items:center;border:1px solid #c6e0db;border-radius:19px;color:#0d766c;background:#fff;font-size:27px;box-shadow:0 12px 28px rgba(26,91,80,.09)}.eyebrow{margin:0 0 5px!important;color:#0e7c70!important;font-size:12px!important;font-weight:800;letter-spacing:.08em}.hero-copy h1{margin:0;color:#17344a;font-size:clamp(27px,3vw,38px);letter-spacing:-.04em}.hero-copy p{margin:8px 0 0;color:#617680;font-size:14px}.progress-strip{display:grid;grid-template-columns:repeat(4,1fr);max-width:730px}.progress-strip span{position:relative;padding:13px 12px 15px;display:flex;align-items:center;gap:8px;border-bottom:3px solid transparent;color:#788a90;font-size:12px}.progress-strip span:after{content:'';position:absolute;right:-4px;width:8px;height:8px;border-top:1px solid #aebeba;border-right:1px solid #aebeba;transform:rotate(45deg)}.progress-strip span:last-child:after{display:none}.progress-strip b{width:25px;height:25px;display:grid;place-items:center;border-radius:50%;color:#647972;background:#dfe9e6;font-size:11px}.progress-strip .active{border-color:#157d72;color:#195f59;font-weight:700}.progress-strip .active b,.progress-strip .done b{color:#fff;background:#167d72}.page-grid{max-width:1180px;margin:auto;padding:32px 24px 80px;display:grid;grid-template-columns:minmax(0,1fr) 310px;gap:24px;align-items:start}.form-column{min-width:0}.form-section{margin-bottom:18px;padding:29px;border:1px solid #dfe7e5;border-radius:18px;background:#fff;box-shadow:0 8px 26px rgba(31,57,64,.035)}.section-heading{display:flex;align-items:center;gap:13px;padding-bottom:21px;border-bottom:1px solid #e8eeec}.section-heading>span{width:43px;height:43px;flex:0 0 43px;display:grid;place-items:center;border-radius:13px;color:#0f786e;background:#e8f5f2;font-size:17px}.section-heading small{color:#178076;font-size:11px;font-weight:800}.section-heading h2{margin:2px 0 3px;font-size:20px}.section-heading p{margin:0;color:#78888d;font-size:12px}.fields{margin-top:23px;display:grid;gap:19px}.two-columns{grid-template-columns:1fr 1fr}.field{min-width:0;margin:0;display:flex;flex-direction:column;gap:8px;border:0}.field.full{grid-column:1/-1}.field>span,.field legend{padding:0;color:#304650;font-size:13px;font-weight:700}.field em{margin-left:4px;color:#c65342;font-size:10px;font-style:normal}.field input,.field select,.field textarea,.request-item textarea{width:100%;padding:11px 13px;border:1px solid #cfdbd8;border-radius:9px;outline:0;color:#243b48;background:#fff;font:inherit;font-size:14px;transition:.18s;box-sizing:border-box}.field input,.field select{height:44px}.field textarea,.request-item textarea{resize:vertical;line-height:1.7}.field input:focus,.field select:focus,.field textarea:focus,.request-item textarea:focus{border-color:#19867b;box-shadow:0 0 0 3px rgba(25,134,123,.1)}.field input::placeholder,.field textarea::placeholder,.request-item textarea::placeholder{color:#a0adae}.field small{color:#819095;font-size:11px;line-height:1.55}.choice-row{height:44px;display:flex;gap:8px}.choice-row label{flex:1}.choice-row input{position:absolute;opacity:0}.choice-row span{height:42px;display:grid;place-items:center;border:1px solid #d2dcda;border-radius:9px;color:#5f7278;background:#fff;font-size:13px;cursor:pointer}.choice-row input:checked+span{border-color:#23877c;color:#0f756b;background:#eaf7f4;font-weight:700}.field-action{display:flex;gap:8px}.field-action button{flex:0 0 auto;padding:0 13px;border:1px solid #cfe1dd;border-radius:9px;color:#16796f;background:#eff8f6;font-size:12px;cursor:pointer}.example-box{margin:20px 0 14px;padding:12px 14px;display:flex;gap:10px;border:1px solid #f0dfba;border-radius:10px;color:#6d6045;background:#fffaf0;font-size:12px;line-height:1.6}.example-box i{margin-top:3px;color:#b67b20}.example-box p{margin:0}.request-list{display:grid;gap:10px}.request-item{display:grid;grid-template-columns:34px 1fr 34px;gap:10px;align-items:start}.request-item>b{width:31px;height:31px;display:grid;place-items:center;border-radius:9px;color:#fff;background:#247e75;font-size:12px}.request-item>button{width:34px;height:34px;border:0;border-radius:8px;color:#a45c50;background:#fff1ee;cursor:pointer}.add-button{margin:13px 0 0 44px;padding:9px 13px;border:1px dashed #8fbdb7;border-radius:8px;color:#0e776d;background:#f4fbfa;font-size:12px;font-weight:700;cursor:pointer}.writing-tips{margin:20px 0;padding:15px 17px;border-radius:11px;background:#f2f7f6}.writing-tips span{color:#1a615b;font-size:12px;font-weight:800}.writing-tips ul{margin:9px 0 0;padding-left:18px;display:grid;grid-template-columns:1fr 1fr;gap:7px;color:#607278;font-size:12px}.facts-area{min-height:230px}.count{align-self:flex-end}.compact-fields{margin-top:19px}.error-summary,.status-message{margin:18px 0;padding:15px 17px;display:flex;gap:11px;border-radius:11px;font-size:12px;line-height:1.65}.error-summary{border:1px solid #efc8c2;color:#854a41;background:#fff2ef}.error-summary i{margin-top:4px}.error-summary strong{display:block}.error-summary p{margin:2px 0 0}.status-message.success{border:1px solid #bbddd4;color:#17645b;background:#ecf8f5}.status-message.error{border:1px solid #efc8c2;color:#854a41;background:#fff2ef}.status-message i{margin-top:3px}.submit-area{padding:21px 23px;display:flex;align-items:center;justify-content:space-between;gap:20px;border-radius:15px;color:#fff;background:linear-gradient(135deg,#143d4e,#116b65);box-shadow:0 16px 36px rgba(22,74,73,.16)}.submit-area strong,.submit-area small{display:block}.submit-area strong{font-size:14px}.submit-area small{margin-top:6px;color:#acd0cc;font-size:10px}.submit-area button{min-width:200px;height:47px;padding:0 20px;border:0;border-radius:10px;color:#14534f;background:#fff;font-weight:800;cursor:pointer}.submit-area button:disabled{opacity:.7;cursor:wait}.submit-area button i{margin-right:8px}.side-column{position:sticky;top:22px;display:grid;gap:14px}.side-card{padding:21px;border:1px solid #dce6e4;border-radius:15px;background:#fff}.side-label{color:#13766d;font-size:11px;font-weight:800}.side-label i{margin-right:6px}.side-card h2{margin:10px 0 16px;font-size:17px}.official-info ul{margin:0;padding:0;display:grid;gap:13px;list-style:none}.official-info li{display:flex;gap:10px;color:#65777d;font-size:11px;line-height:1.5}.official-info li>i{width:29px;height:29px;flex:0 0 29px;display:grid;place-items:center;border-radius:8px;color:#187b72;background:#edf7f5}.official-info li strong{display:block;color:#344b54;font-size:12px}.official-info>a{margin-top:18px;height:42px;display:flex;align-items:center;justify-content:center;gap:8px;border:1px solid #c8e0db;border-radius:9px;color:#126f67;background:#f2faf8;font-size:12px;font-weight:800}.online-card{color:#fff;background:linear-gradient(145deg,#17384c,#126b66);border:0}.online-card div{display:grid}.online-card span{color:#a6cdc9;font-size:10px}.online-card strong{margin-top:3px;font-size:22px}.online-card small{color:#b6cecf;font-size:10px}.online-card a{margin-top:17px;padding-top:14px;display:flex;justify-content:space-between;border-top:1px solid rgba(255,255,255,.14);color:#fff;font-size:11px;font-weight:700}.draft-note{padding:5px 6px;display:flex;gap:10px;color:#6f7e82;font-size:10px;line-height:1.55}.draft-note>i{margin-top:4px;color:#45857e}.draft-note strong{color:#425960;font-size:11px}.draft-note p{margin:4px 0}.draft-note button{padding:0;border:0;color:#b05b4d;background:transparent;font-size:10px;text-decoration:underline;cursor:pointer}
.choice-row label{position:relative}.choice-row input{width:1px;height:1px}
@media(max-width:900px){.page-grid{grid-template-columns:1fr}.side-column{position:static;grid-template-columns:1fr 1fr}.draft-note{grid-column:1/-1}}
@media(max-width:640px){.page-hero{padding:20px 16px 0}.hero-copy{padding:22px 0}.document-icon{width:54px;height:54px;flex-basis:54px;border-radius:15px}.hero-copy h1{font-size:25px}.hero-copy p{font-size:12px}.progress-strip span{padding:10px 3px 12px;justify-content:center;font-size:0}.progress-strip span:after{display:none}.progress-strip b{font-size:11px}.page-grid{padding:20px 14px 60px}.form-section{padding:20px 17px;border-radius:14px}.two-columns{grid-template-columns:1fr}.field.full{grid-column:auto}.writing-tips ul{grid-template-columns:1fr}.field-action{flex-direction:column}.field-action button{height:37px}.request-item{grid-template-columns:29px 1fr}.request-item>b{width:29px}.request-item>button{grid-column:2;justify-self:end}.submit-area{align-items:stretch;flex-direction:column}.submit-area button{width:100%}.side-column{grid-template-columns:1fr}}
.calculation-field{margin-top:20px}.guangdong-details{margin-top:24px;padding-top:22px;border-top:1px solid #e4ecea}.subsection-title{display:flex;align-items:center;gap:11px}.subsection-title>span{width:39px;height:39px;display:grid;place-items:center;border-radius:11px;color:#12756c;background:#e8f5f2}.subsection-title h3{margin:0;font-size:17px}.subsection-title p{margin:4px 0 0;color:#78888d;font-size:11px}.date-range{display:grid;grid-template-columns:1fr auto 1fr;align-items:center;gap:7px}.date-range b{color:#7a898d;font-size:11px}.field input:disabled,.field select:disabled{color:#98a3a6;background:#f1f4f3}
.confirm-backdrop{position:fixed;inset:0;z-index:1000;padding:20px;display:grid;place-items:center;background:rgba(14,35,45,.52);backdrop-filter:blur(5px)}.confirm-dialog{position:relative;width:min(460px,100%);box-sizing:border-box;padding:31px;border:1px solid rgba(255,255,255,.7);border-radius:20px;background:#fff;box-shadow:0 28px 80px rgba(9,35,45,.28);text-align:center}.confirm-close{position:absolute;top:14px;right:14px;width:34px;height:34px;border:0;border-radius:9px;color:#738489;background:#f2f6f5;cursor:pointer}.confirm-icon{width:60px;height:60px;margin:0 auto 17px;display:grid;place-items:center;border-radius:17px;color:#fff;background:linear-gradient(145deg,#19887d,#0e625d);font-size:25px;box-shadow:0 12px 25px rgba(20,113,105,.2)}.confirm-dialog h2{margin:0;color:#203b49;font-size:22px}.confirm-dialog>p{margin:12px auto 0;max-width:380px;color:#667a82;font-size:13px;line-height:1.75}.confirm-dialog>p strong{color:#b35646}.missing-preview{margin:16px 0 0;padding:12px 14px;display:flex;align-items:flex-start;gap:9px;border-radius:10px;color:#756145;background:#fff8eb;font-size:11px;line-height:1.6;text-align:left}.missing-preview i{margin-top:3px;color:#b77a20}.confirm-actions{margin-top:23px;display:grid;grid-template-columns:1fr 1.35fr;gap:10px}.confirm-actions button{height:45px;border-radius:10px;font-weight:800;cursor:pointer}.cancel-button{border:1px solid #d4dfdc;color:#566b71;background:#fff}.confirm-button{border:0;color:#fff;background:linear-gradient(135deg,#178277,#105f5b);box-shadow:0 9px 20px rgba(17,105,98,.18)}.confirm-button i{margin-right:7px}
@media(max-width:520px){.confirm-dialog{padding:27px 20px 21px}.confirm-actions{grid-template-columns:1fr}.confirm-button{grid-row:1}}
</style>
