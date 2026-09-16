<template>
  <Transition name="panel">
    <section v-if="open" class="assistant-panel" role="dialog" aria-modal="true" aria-label="AI 法律助手">
      <header>
        <div class="assistant-identity"><span><i class="fa-solid fa-scale-balanced"></i></span><div><strong>AI 劳动法律助手</strong><small><i></i> 本地模型服务</small></div></div>
        <div class="header-actions"><button class="digital-entry" title="打开法律数字人" @click="$emit('open-digital-human')"><i class="fa-solid fa-user-tie"></i><span>数字人</span></button><button title="清空对话" aria-label="清空对话" @click="clearHistory"><i class="fa-regular fa-trash-can"></i></button><button title="关闭" aria-label="关闭" @click="$emit('close')"><i class="fa-solid fa-xmark"></i></button></div>
      </header>
      <div class="assistant-context"><i class="fa-solid fa-circle-info"></i>回答仅用于辅助梳理，不替代执业律师意见；重要结论请结合原始材料核验。</div>
      <div ref="chatRef" class="chat-stream">
        <div v-for="(msg,index) in messages" :key="index" class="message" :class="msg.role">
          <span v-if="msg.role==='ai'" class="assistant-avatar">法</span>
          <div><small>{{ msg.role==='ai' ? 'AI 助手' : '你' }}</small><div class="bubble" v-html="renderMarkdown(msg.content)"></div></div>
        </div>
        <div v-if="isLoading" class="message ai"><span class="assistant-avatar">法</span><div><small>AI 助手</small><div class="bubble typing"><i></i><i></i><i></i></div></div></div>
      </div>
      <div v-if="messages.length<2" class="suggestions"><button v-for="item in prompts" :key="item" @click="inputQuery=item">{{ item }}</button></div>
      <form @submit.prevent="sendMessage">
        <textarea v-model="inputQuery" rows="2" placeholder="描述案情，例如：公司口头辞退但不给书面通知……" :disabled="isLoading" @keydown.enter.exact.prevent="sendMessage"></textarea>
        <div><span><i class="fa-solid fa-lock"></i> 敏感信息建议脱敏</span><button type="submit" :disabled="isLoading||!inputQuery.trim()"><i class="fa-solid fa-arrow-up"></i></button></div>
      </form>
    </section>
  </Transition>
  <Transition name="fade"><div v-if="open" class="assistant-mask" @click="$emit('close')"></div></Transition>
</template>
<script setup>
import { nextTick, onMounted, ref, watch } from 'vue'; import { marked } from 'marked'; import DOMPurify from 'dompurify'
defineProps({ open:{type:Boolean,default:false} }); defineEmits(['close','open-digital-human'])
const API_BASE=(import.meta.env.VITE_API_BASE_URL||'http://127.0.0.1:8000').replace(/\/$/,'')
const inputQuery=ref(''); const messages=ref([]); const isLoading=ref(false); const chatRef=ref(null)
const prompts=['公司没有签劳动合同，我能主张什么？','帮我梳理申请劳动仲裁需要的证据','违法解除赔偿金怎么计算？']
const welcome={role:'ai',content:'你好，我可以帮你梳理劳动争议中的 **请求事项、关键证据、仲裁时效和下一步行动**。请先用一句话描述发生了什么。'}
const renderMarkdown=text=>DOMPurify.sanitize(marked.parse(text||'')); const scroll=async()=>{await nextTick();if(chatRef.value)chatRef.value.scrollTop=chatRef.value.scrollHeight}; const save=()=>localStorage.setItem('labourlawyer.chat.v1',JSON.stringify(messages.value))
const clearHistory=()=>{messages.value=[welcome];save()}
const sendMessage=async()=>{
  const text=inputQuery.value.trim(); if(!text||isLoading.value)return; messages.value.push({role:'user',content:text});inputQuery.value='';isLoading.value=true;scroll()
  try{const history=messages.value.filter(item=>item!==welcome).slice(-12).map(item=>({role:item.role==='ai'?'assistant':'user',content:item.content}));const response=await fetch(`${API_BASE}/api/ask`,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({question:text,history})});if(!response.ok)throw new Error('服务暂不可用');const reader=response.body.getReader();const decoder=new TextDecoder();const index=messages.value.push({role:'ai',content:''})-1;isLoading.value=false;while(true){const{value,done}=await reader.read();if(done)break;messages.value[index].content+=decoder.decode(value,{stream:true});scroll()}}
  catch{messages.value.push({role:'ai',content:'当前无法连接本地模型服务。你仍可继续整理案件和生成文书；启动后端与 Ollama 后再重试。'})}finally{isLoading.value=false;save();scroll()}
}
onMounted(()=>{try{messages.value=JSON.parse(localStorage.getItem('labourlawyer.chat.v1'))||[welcome]}catch{messages.value=[welcome]}});watch(messages,save,{deep:true})
</script>
<style scoped>
.assistant-panel{position:fixed;inset:18px 18px 18px auto;z-index:90;width:min(440px,calc(100vw - 36px));display:flex;flex-direction:column;border:1px solid #d8e0e7;border-radius:17px;background:#fff;box-shadow:0 30px 90px rgba(5,19,36,.24);overflow:hidden}.assistant-mask{position:fixed;inset:0;z-index:80;background:rgba(9,24,42,.22);backdrop-filter:blur(1px)}header{min-height:70px;padding:13px 16px;display:flex;align-items:center;justify-content:space-between;color:#fff;background:#0b213c}.assistant-identity{display:flex;align-items:center;gap:10px}.assistant-identity>span{width:38px;height:38px;display:grid;place-items:center;border-radius:10px;color:#d7fff9;background:#0f736d}.assistant-identity strong,.assistant-identity small{display:block}.assistant-identity strong{font-size:13px}.assistant-identity small{margin-top:3px;color:#9fb2c8;font-size:9px}.assistant-identity small i{display:inline-block;width:6px;height:6px;margin-right:5px;border-radius:50%;background:#47c9a9}.header-actions{display:flex;gap:3px}.header-actions button{width:32px;height:32px;border:0;border-radius:7px;color:#aebdd0;background:transparent}.header-actions button:hover{color:#fff;background:rgba(255,255,255,.1)}.assistant-context{padding:9px 14px;color:#6d7785;background:#fff9e9;border-bottom:1px solid #eee4ca;font-size:9px}.assistant-context i{margin-right:6px;color:#ad741b}.chat-stream{flex:1;overflow:auto;padding:18px;background:#f5f7f9}.message{display:flex;gap:9px;margin-bottom:17px}.message.user{justify-content:flex-end}.message.user>div{max-width:84%;text-align:right}.message small{display:block;margin:0 0 5px;color:#8b97a4;font-size:9px}.assistant-avatar{flex:0 0 31px;height:31px;display:grid;place-items:center;border-radius:9px;color:#fff;background:#0f766e;font-family:serif;font-size:12px}.bubble{padding:11px 13px;border:1px solid #e1e6eb;border-radius:4px 12px 12px;background:#fff;color:#34445a;text-align:left;font-size:12px;line-height:1.7;box-shadow:0 3px 12px rgba(30,50,70,.03)}.user .bubble{border-color:#0f766e;border-radius:12px 4px 12px 12px;color:#fff;background:#0f766e}.bubble :deep(p){margin:0 0 7px}.bubble :deep(p:last-child){margin-bottom:0}.bubble :deep(ul),.bubble :deep(ol){margin:6px 0;padding-left:18px}.typing{display:flex;gap:4px;padding:16px}.typing i{width:6px;height:6px;border-radius:50%;background:#77909e;animation:pulse 1.2s infinite}.typing i:nth-child(2){animation-delay:.15s}.typing i:nth-child(3){animation-delay:.3s}.suggestions{padding:0 14px 10px;display:flex;gap:6px;overflow:auto;background:#f5f7f9}.suggestions button{padding:7px 9px;border:1px solid #d8e2e3;border-radius:8px;color:#48666b;background:#fff;white-space:nowrap;font-size:9px}form{padding:12px 14px;border-top:1px solid var(--line);background:#fff}textarea{width:100%;resize:none;border:0;outline:0;color:#24354b;font-size:12px;line-height:1.5}form>div{display:flex;align-items:center;justify-content:space-between}form span{color:#929da8;font-size:8px}form span i{margin-right:4px;color:#0d8a7f}form button{width:32px;height:32px;border:0;border-radius:9px;color:#fff;background:#0f766e}form button:disabled{background:#c5ced3}.panel-enter-active,.panel-leave-active{transition:.25s ease}.panel-enter-from,.panel-leave-to{opacity:0;transform:translateX(25px)}.fade-enter-active,.fade-leave-active{transition:.2s}.fade-enter-from,.fade-leave-to{opacity:0}@keyframes pulse{0%,100%{opacity:.25;transform:translateY(0)}50%{opacity:1;transform:translateY(-3px)}}@media(max-width:560px){.assistant-panel{inset:0;width:100%;border-radius:0}.assistant-mask{display:none}}
.header-actions .digital-entry{width:auto;padding:0 9px;display:flex;align-items:center;gap:5px;color:#d7fff9;background:rgba(27,150,139,.2);font-size:10px}.header-actions .digital-entry span{color:inherit;font-size:10px}
</style>
