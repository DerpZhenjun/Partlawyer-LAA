<template>
  <main class="evidence-page">
    <header class="page-hero">
      <div class="hero-inner">
        <RouterLink :to="config.backRoute" class="back-link"><i class="fa-solid fa-arrow-left"></i> 返回{{ config.shortName }}办理页</RouterLink>
        <div class="title-row"><span><i class="fa-solid fa-list-check"></i></span><div><small>{{ config.name }}官方格式</small><h1>证据清单</h1><p>把准备提交的材料逐项列出来，我们会生成可直接检查和打印的 Word 清单。</p></div></div>
      </div>
    </header>

    <div class="page-grid">
      <form novalidate @submit.prevent="requestGeneration">
        <section class="form-card basic-card">
          <div class="section-title"><span>1</span><div><h2>填写清单信息</h2><p>案件编号还没有时可以留空。</p></div></div>
          <div class="field-grid">
            <label v-if="props.province==='zhejiang'" class="field full"><span>仲裁委员会 <em>必填</em></span><input v-model.trim="form.committeeName" placeholder="例如：杭州市劳动人事争议仲裁委员会"></label>
            <label class="field"><span>提交人姓名 <em>必填</em></span><input v-model.trim="form.submitterName" placeholder="你的姓名"></label>
            <label v-if="props.province==='zhejiang'" class="field"><span>案件编号</span><input v-model.trim="form.caseNumber" placeholder="尚未立案可留空"></label>
            <label class="field"><span>提交日期</span><input v-model="form.submitDate" type="date"></label>
            <label v-if="props.province==='zhejiang'" class="field"><span>清单份数</span><input v-model.number="form.copyCount" type="number" min="1" max="20"><small>{{ config.copyHint }}</small></label>
          </div>
        </section>

        <section class="form-card evidence-card">
          <div class="section-title"><span>2</span><div><h2>添加你的证据</h2><p>一份材料填写一行，按你准备提交的顺序排列。</p></div><b>{{ evidenceList.length }} 项</b></div>
          <div class="tip"><i class="fa-regular fa-lightbulb"></i><span><strong>怎么写“能说明什么”？</strong>例如工资流水可以写“说明每月工资金额和公司发薪情况”。</span></div>

          <div class="evidence-list">
            <article v-for="(item,index) in evidenceList" :key="item.id" class="evidence-item">
              <div class="item-number"><b>{{ index + 1 }}</b><span>第 {{ index + 1 }} 项</span></div>
              <div class="item-fields">
                <label class="field wide"><span>材料名称 <em>必填</em></span><input v-model.trim="item.name" placeholder="例如：劳动合同、工资流水、考勤记录"></label>
                <label class="field short"><span>页数</span><input v-model.trim="item.pageCount" placeholder="例如：3页"></label>
                <label class="field"><span>材料从哪里取得 <em>必填</em></span><input v-model.trim="item.source" placeholder="例如：本人保存、银行下载、公司提供"></label>
                <label class="field wide"><span>这份材料能说明什么 <em>必填</em></span><textarea v-model.trim="item.purpose" rows="2" placeholder="用一句话说明这份材料与哪项要求有关"></textarea></label>
              </div>
              <button v-if="evidenceList.length > 1" type="button" class="remove" aria-label="删除这一项" @click="removeItem(index)"><i class="fa-regular fa-trash-can"></i></button>
            </article>
          </div>
          <button type="button" class="add-evidence" :disabled="evidenceList.length >= 30" @click="addItem"><i class="fa-solid fa-plus"></i> 添加一项证据</button>
        </section>

        <div v-if="status.message" class="message" :class="status.type" role="status"><i :class="status.type==='success'?'fa-solid fa-circle-check':'fa-solid fa-circle-exclamation'"></i>{{ status.message }}</div>
        <div class="submit-bar"><div><strong>生成{{ config.name }}官方格式证据清单</strong><small><i class="fa-solid fa-circle-info"></i> 可以直接下载空白模板；正式提交前请补全标为必填的内容。</small></div><button type="submit" :disabled="isSubmitting"><i :class="isSubmitting?'fa-solid fa-spinner fa-spin':'fa-regular fa-file-word'"></i>{{ isSubmitting ? '正在生成…' : '生成并下载证据清单' }}</button></div>
      </form>

      <aside>
        <div class="side-card">
          <span class="side-label"><i class="fa-regular fa-folder-open"></i> 常见证据</span>
          <h2>不知道从哪里开始？</h2>
          <p>点一下即可添加，再按你的实际情况修改。</p>
          <button v-for="preset in presets" :key="preset.name" type="button" @click="addPreset(preset)"><i :class="preset.icon"></i><span><strong>{{ preset.name }}</strong>{{ preset.help }}</span><i class="fa-solid fa-plus"></i></button>
        </div>
        <div class="notice-card"><i class="fa-solid fa-circle-info"></i><div><strong>别只留截图</strong><p>聊天、邮件、考勤等电子材料尽量保留原始设备和完整上下文，提交要求以当地仲裁委员会为准。</p></div></div>
        <div class="draft-card"><i class="fa-regular fa-floppy-disk"></i><span>已自动保存在这台设备</span><button type="button" @click="clearDraft">清除</button></div>
      </aside>
    </div>
  </main>

  <Teleport to="body">
    <div v-if="showConfirm" class="confirm-backdrop" @click.self="showConfirm=false">
      <section class="confirm-dialog" role="dialog" aria-modal="true" aria-labelledby="evidence-confirm-title">
        <button class="confirm-close" type="button" aria-label="取消生成" @click="showConfirm=false"><i class="fa-solid fa-xmark"></i></button>
        <span class="confirm-icon"><i class="fa-solid fa-list-check"></i></span>
        <h2 id="evidence-confirm-title">确认生成证据清单？</h2>
        <template v-if="missingFields.length">
          <p>当前还有 <strong>{{ missingFields.length }} 项</strong>内容没有填写。确认后仍会生成官方模板，空白处可以在 Word 中继续填写。</p>
          <div class="missing-preview"><i class="fa-solid fa-circle-info"></i><span>{{ missingFields.slice(0, 5).join('、') }}<template v-if="missingFields.length > 5">等</template></span></div>
        </template>
        <p v-else>内容已填写完成。确认后将生成并下载 {{ config.name }}官方格式证据清单。</p>
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

const props=defineProps({province:{type:String,default:'zhejiang'}})
const provinceConfigs={
  zhejiang:{name:'浙江省',shortName:'浙江',backRoute:'/province/zhejiang',apiPath:'/api/zhejiang/el/generate',downloadName:'浙江省劳动仲裁证据清单.docx',copyHint:'浙江官方指南所列材料通常为 2 份。'},
  guangdong:{name:'广东省',shortName:'广东',backRoute:'/province/guangdong',apiPath:'/api/guangdong/el/generate',downloadName:'广东省劳动仲裁证据清单.docx',copyHint:'广东官方页面将证据材料列为 2 份。'},
}
const config=computed(()=>provinceConfigs[props.province]||provinceConfigs.zhejiang)
const API_BASE=(import.meta.env.VITE_API_BASE_URL||'http://127.0.0.1:8000').replace(/\/$/,'')
const DRAFT_KEY=`labourlawyer-${props.province}-evidence-draft-v5`
const makeItem=(data={})=>({id:`${Date.now()}-${Math.random()}`,name:'',pageCount:'',source:'',purpose:'',...data})
const defaults={committeeName:'',caseNumber:'',copyCount:2,submitterName:'',submitDate:'',evidenceList:[makeItem()]}
const loadDraft=()=>{try{return {...defaults,...JSON.parse(localStorage.getItem(DRAFT_KEY)||'{}')}}catch{return {...defaults,evidenceList:[makeItem()]}}}
const saved=loadDraft()
const form=reactive({committeeName:saved.committeeName||'',caseNumber:saved.caseNumber||'',copyCount:saved.copyCount||2,submitterName:saved.submitterName||'',submitDate:saved.submitDate||''})
const evidenceList=ref(Array.isArray(saved.evidenceList)&&saved.evidenceList.length?saved.evidenceList.map(makeItem):[makeItem()])
const isSubmitting=ref(false),showConfirm=ref(false),missingFields=ref([]),status=reactive({type:'',message:''})
const presets=[
  {name:'劳动合同',help:'说明劳动关系和双方约定',icon:'fa-regular fa-file-lines',source:'本人保存',purpose:'说明我与公司存在劳动关系以及双方约定的工作内容、工资等事项。'},
  {name:'工资流水',help:'说明工资金额和发放情况',icon:'fa-solid fa-money-check-dollar',source:'银行下载',purpose:'说明公司向我支付工资的金额、时间和拖欠情况。'},
  {name:'考勤记录',help:'说明出勤时间和工作情况',icon:'fa-regular fa-calendar-check',source:'本人保存',purpose:'说明我的出勤时间和实际工作情况。'},
  {name:'聊天记录',help:'说明工作安排或争议经过',icon:'fa-regular fa-comments',source:'本人手机',purpose:'说明公司对我的工作安排以及双方沟通过程。'},
  {name:'社保记录',help:'帮助说明劳动关系',icon:'fa-solid fa-shield-heart',source:'政务平台下载',purpose:'说明公司为我缴纳社会保险以及劳动关系存续时间。'},
]
let timer
watch([form,evidenceList],()=>{clearTimeout(timer);timer=setTimeout(()=>localStorage.setItem(DRAFT_KEY,JSON.stringify({...form,evidenceList:evidenceList.value})),350)},{deep:true})
onBeforeUnmount(()=>clearTimeout(timer))
const addItem=()=>{if(evidenceList.value.length<30)evidenceList.value.push(makeItem())}
const removeItem=index=>evidenceList.value.splice(index,1)
const addPreset=preset=>{const existing=evidenceList.value.find(item=>!item.name&&!item.source&&!item.purpose);const target=existing||makeItem();Object.assign(target,{name:preset.name,source:preset.source,purpose:preset.purpose});if(!existing)evidenceList.value.push(target)}
const clearDraft=()=>{localStorage.removeItem(DRAFT_KEY);Object.assign(form,{committeeName:'',caseNumber:'',copyCount:2,submitterName:'',submitDate:''});evidenceList.value=[makeItem()];status.type='success';status.message='已清除这台设备上保存的内容。'}
const collectMissingFields=()=>{const list=[];if(props.province==='zhejiang'&&!form.committeeName)list.push('仲裁委员会');if(!form.submitterName)list.push('提交人姓名');evidenceList.value.forEach((item,index)=>{if(!item.name&&!item.source&&!item.purpose&&!item.pageCount)list.push(index===0?'至少一项证据':`第 ${index+1} 项证据`);else{if(!item.name)list.push(`第 ${index+1} 项材料名称`);if(!item.source)list.push(`第 ${index+1} 项材料来源`);if(!item.purpose)list.push(`第 ${index+1} 项材料说明`)}});return list}
const parseError=async error=>{if(error.response?.data instanceof Blob){try{const data=JSON.parse(await error.response.data.text());return data.detail||'生成失败，请检查填写内容。'}catch{}}return error.code==='ERR_NETWORK'?'无法连接文书生成服务，请确认后端已经启动。':'生成失败，请稍后再试。'}
const requestGeneration=()=>{status.message='';missingFields.value=collectMissingFields();showConfirm.value=true}
const confirmGeneration=()=>{showConfirm.value=false;submitForm()}
const submitForm=async()=>{status.message='';isSubmitting.value=true;try{const payload={...form,evidenceList:evidenceList.value.map(({name,pageCount,source,purpose})=>({name,pageCount,source,purpose}))};const response=await axios.post(`${API_BASE}${config.value.apiPath}`,payload,{responseType:'blob',timeout:30000});await downloadDocument(response.data,config.value.downloadName);status.type='success';status.message='证据清单已生成。请核对顺序、页数和说明后再打印。'}catch(error){status.type='error';status.message=await parseError(error)}finally{isSubmitting.value=false}}
</script>

<style scoped>
.evidence-page{min-height:100vh;color:#263c4b;background:#f5f8f7}.page-hero{padding:27px 24px 34px;border-bottom:1px solid #dbe7e4;background:linear-gradient(135deg,#f9fcfb,#eaf6f3)}.hero-inner{max-width:1180px;margin:auto}.back-link{display:inline-flex;align-items:center;gap:7px;color:#60766f;font-size:13px}.title-row{margin-top:25px;display:flex;align-items:center;gap:17px}.title-row>span{width:64px;height:64px;display:grid;place-items:center;border-radius:18px;color:#fff;background:linear-gradient(145deg,#16847a,#105f5b);font-size:24px;box-shadow:0 12px 25px rgba(22,103,96,.17)}.title-row small{color:#147c72;font-size:11px;font-weight:800}.title-row h1{margin:3px 0 5px;font-size:35px;letter-spacing:-.04em}.title-row p{margin:0;color:#657980;font-size:13px}.page-grid{max-width:1180px;margin:auto;padding:30px 24px 75px;display:grid;grid-template-columns:minmax(0,1fr) 300px;gap:22px;align-items:start}.form-card{margin-bottom:17px;padding:27px;border:1px solid #dfe7e5;border-radius:17px;background:#fff;box-shadow:0 8px 26px rgba(31,57,64,.035)}.section-title{display:flex;align-items:center;gap:12px;padding-bottom:19px;border-bottom:1px solid #e8eeec}.section-title>span{width:36px;height:36px;flex:0 0 36px;display:grid;place-items:center;border-radius:11px;color:#fff;background:#187c72;font-size:12px;font-weight:800}.section-title h2{margin:0;font-size:19px}.section-title p{margin:3px 0 0;color:#78898d;font-size:11px}.section-title>b{margin-left:auto;padding:5px 9px;border-radius:999px;color:#17746c;background:#eaf6f3;font-size:11px}.field-grid{margin-top:21px;display:grid;grid-template-columns:1fr 1fr;gap:18px}.field{min-width:0;display:flex;flex-direction:column;gap:7px}.field.full{grid-column:1/-1}.field span{color:#354b55;font-size:12px;font-weight:700}.field em{margin-left:3px;color:#c55242;font-size:9px;font-style:normal}.field input,.field textarea{width:100%;box-sizing:border-box;padding:10px 12px;border:1px solid #cedbd8;border-radius:9px;outline:0;color:#2a414d;background:#fff;font:inherit;font-size:13px}.field input{height:43px}.field textarea{resize:vertical;line-height:1.6}.field input:focus,.field textarea:focus{border-color:#20867b;box-shadow:0 0 0 3px rgba(32,134,123,.1)}.field input::placeholder,.field textarea::placeholder{color:#9facae}.field small{color:#829195;font-size:10px}.tip{margin:18px 0 13px;padding:12px 14px;display:flex;gap:10px;border-radius:9px;color:#6c624e;background:#fff8ea;font-size:11px;line-height:1.55}.tip i{margin-top:2px;color:#ae771f}.tip strong{display:block}.evidence-list{display:grid;gap:11px}.evidence-item{position:relative;padding:17px;display:grid;grid-template-columns:55px 1fr 28px;gap:13px;border:1px solid #dce6e3;border-radius:12px;background:#fbfdfc}.item-number b,.item-number span{display:block}.item-number b{width:31px;height:31px;display:grid;place-items:center;border-radius:9px;color:#14766e;background:#e5f4f1;font-size:12px}.item-number span{margin-top:6px;color:#809093;font-size:9px}.item-fields{display:grid;grid-template-columns:1fr 115px;gap:13px}.item-fields .wide{grid-column:1/-1}.remove{width:28px;height:28px;border:0;border-radius:8px;color:#a85d50;background:#fff0ed;cursor:pointer}.add-evidence{margin-top:14px;width:100%;height:43px;border:1px dashed #8fbdb6;border-radius:9px;color:#11766c;background:#f3faf8;font-size:12px;font-weight:800;cursor:pointer}.add-evidence:disabled{opacity:.5}.message{margin:15px 0;padding:14px 16px;display:flex;gap:10px;border-radius:10px;font-size:11px;line-height:1.6}.message span strong{display:block}.message.success{border:1px solid #bbddd4;color:#17645b;background:#ecf8f5}.message.error{border:1px solid #efc8c2;color:#854a41;background:#fff2ef}.submit-bar{padding:20px 22px;display:flex;align-items:center;justify-content:space-between;gap:18px;border-radius:14px;color:#fff;background:linear-gradient(135deg,#143d4e,#116b65);box-shadow:0 16px 36px rgba(22,74,73,.16)}.submit-bar strong,.submit-bar small{display:block}.submit-bar strong{font-size:13px}.submit-bar small{margin-top:5px;color:#acd0cc;font-size:10px}.submit-bar button{height:45px;min-width:205px;border:0;border-radius:9px;color:#15564f;background:#fff;font-weight:800;cursor:pointer}.submit-bar button i{margin-right:7px}.submit-bar button:disabled{opacity:.7}aside{position:sticky;top:22px;display:grid;gap:14px}.side-card{padding:20px;border:1px solid #dce6e3;border-radius:15px;background:#fff}.side-label{color:#14766d;font-size:11px;font-weight:800}.side-label i{margin-right:6px}.side-card h2{margin:10px 0 5px;font-size:17px}.side-card>p{margin:0 0 16px;color:#7a898d;font-size:11px}.side-card>button{width:100%;padding:10px 0;display:grid;grid-template-columns:31px 1fr 16px;align-items:center;gap:9px;border:0;border-top:1px solid #e8edec;color:#627479;background:#fff;text-align:left;cursor:pointer}.side-card>button>i:first-child{width:29px;height:29px;display:grid;place-items:center;border-radius:8px;color:#17786f;background:#edf7f5}.side-card>button>i:last-child{color:#7d9691;font-size:9px}.side-card button strong,.side-card button span{display:block}.side-card button strong{color:#344b55;font-size:11px}.side-card button span{font-size:9px}.notice-card{padding:16px;display:flex;gap:10px;border-radius:13px;color:#6a604a;background:#fff9ed}.notice-card>i{margin-top:2px;color:#a8721f}.notice-card strong{font-size:11px}.notice-card p{margin:4px 0 0;font-size:10px;line-height:1.6}.draft-card{padding:5px 4px;display:flex;align-items:center;gap:7px;color:#708185;font-size:10px}.draft-card i{color:#43857d}.draft-card button{margin-left:auto;border:0;color:#ae5a4d;background:transparent;font-size:10px;text-decoration:underline;cursor:pointer}
@media(max-width:880px){.page-grid{grid-template-columns:1fr}aside{position:static;grid-template-columns:1fr 1fr}.draft-card{grid-column:1/-1}}
@media(max-width:620px){.page-hero{padding:20px 16px 27px}.title-row>span{width:53px;height:53px;border-radius:15px}.title-row h1{font-size:28px}.title-row p{font-size:11px}.page-grid{padding:20px 14px 60px}.form-card{padding:20px 16px}.field-grid{grid-template-columns:1fr}.field.full{grid-column:auto}.evidence-item{grid-template-columns:35px 1fr}.item-number span{display:none}.item-fields{grid-template-columns:1fr}.item-fields .wide{grid-column:auto}.remove{grid-column:2;justify-self:end}.submit-bar{align-items:stretch;flex-direction:column}.submit-bar button{width:100%}aside{grid-template-columns:1fr}}
.confirm-backdrop{position:fixed;inset:0;z-index:1000;padding:20px;display:grid;place-items:center;background:rgba(14,35,45,.52);backdrop-filter:blur(5px)}.confirm-dialog{position:relative;width:min(460px,100%);box-sizing:border-box;padding:31px;border:1px solid rgba(255,255,255,.7);border-radius:20px;background:#fff;box-shadow:0 28px 80px rgba(9,35,45,.28);text-align:center}.confirm-close{position:absolute;top:14px;right:14px;width:34px;height:34px;border:0;border-radius:9px;color:#738489;background:#f2f6f5;cursor:pointer}.confirm-icon{width:60px;height:60px;margin:0 auto 17px;display:grid;place-items:center;border-radius:17px;color:#fff;background:linear-gradient(145deg,#19887d,#0e625d);font-size:24px;box-shadow:0 12px 25px rgba(20,113,105,.2)}.confirm-dialog h2{margin:0;color:#203b49;font-size:22px}.confirm-dialog>p{margin:12px auto 0;max-width:380px;color:#667a82;font-size:13px;line-height:1.75}.confirm-dialog>p strong{color:#b35646}.missing-preview{margin:16px 0 0;padding:12px 14px;display:flex;align-items:flex-start;gap:9px;border-radius:10px;color:#756145;background:#fff8eb;font-size:11px;line-height:1.6;text-align:left}.missing-preview i{margin-top:3px;color:#b77a20}.confirm-actions{margin-top:23px;display:grid;grid-template-columns:1fr 1.35fr;gap:10px}.confirm-actions button{height:45px;border-radius:10px;font-weight:800;cursor:pointer}.cancel-button{border:1px solid #d4dfdc;color:#566b71;background:#fff}.confirm-button{border:0;color:#fff;background:linear-gradient(135deg,#178277,#105f5b);box-shadow:0 9px 20px rgba(17,105,98,.18)}.confirm-button i{margin-right:7px}
@media(max-width:520px){.confirm-dialog{padding:27px 20px 21px}.confirm-actions{grid-template-columns:1fr}.confirm-button{grid-row:1}}
</style>
