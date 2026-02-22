<template>
  <div class="floating-wrapper" :class="{ 'hidden': isChatVisible }">
    
    <button class="sub-btn digital-btn" @click="openDigitalHuman">
      <span class="btn-text">数字人</span>
      <i class="fas fa-user-tie"></i>
    </button>

    <button class="main-btn chat-btn" @click="toggleChat">
      <i class="fas fa-robot"></i> 
      <span class="btn-text">法律顾问</span>
    </button>

  </div>

  <div 
    id="chat-container" 
    :class="{ 'show': isChatVisible }" 
    :style="{ width: containerWidth + 'px', height: containerHeight + 'px' }"
  >
    
    <div class="resize-handle handle-left" @mousedown.prevent="startResize($event, 'left')"></div>
    <div class="resize-handle handle-top" @mousedown.prevent="startResize($event, 'top')"></div>
    <div class="resize-handle handle-top-left" @mousedown.prevent="startResize($event, 'both')"></div>

    <div class="chat-header">
      <span><i class="fas fa-balance-scale"></i> 智能法律助手</span>
      <div class="header-actions">
        <button class="icon-btn" @click="clearHistory" title="清空记录"><i class="fas fa-trash-alt"></i></button>
        <button class="icon-btn" @click="toggleChat" title="最小化"><i class="fas fa-minus"></i></button>
      </div>
    </div>

    <div id="chat" ref="chatRef">
      <div v-for="(msg, index) in messages" :key="index" :class="['message', msg.role]">
        <img v-if="msg.role === 'ai'" src="@/assets/img/lawyer-logo.png" class="avatar">
        <div class="text-wrapper">
            <div class="text" v-html="renderMarkdown(msg.content)"></div>
        </div>
      </div>

      <div v-if="isLoading" class="message ai">
        <img src="@/assets/img/lawyer-logo.png" class="avatar">
        <div class="text spinner-box">
          <div class="typing-dot"></div>
          <div class="typing-dot"></div>
          <div class="typing-dot"></div>
        </div>
      </div>
    </div>

    <form id="question-form" @submit.prevent="sendMessage">
      <input 
        type="text" 
        v-model="inputQuery" 
        placeholder="请输入您的法律问题..." 
        :disabled="isLoading"
        autocomplete="off"
      >
      <button type="submit" :disabled="isLoading || !inputQuery.trim()">
        <i class="fas fa-paper-plane"></i>
      </button>
    </form>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick, defineEmits } from 'vue'; // 新增 defineEmits
import { marked } from 'marked';
import DOMPurify from 'dompurify';

// --- 新增：定义事件 ---
// 用于通知父组件 (Home.vue) 打开数字人
const emit = defineEmits(['open-digital-human']);

const openDigitalHuman = () => {
  emit('open-digital-human');
};

// --- 状态管理 ---
const isChatVisible = ref(false);
const containerWidth = ref(350); 
const containerHeight = ref(500); 
const inputQuery = ref('');
const messages = ref([]);
const isLoading = ref(false);
const chatRef = ref(null);

// --- 核心逻辑 ---
const sendMessage = async () => {
  if (!inputQuery.value.trim() || isLoading.value) return;
  const userText = inputQuery.value;
  messages.value.push({ role: 'user', content: userText });
  inputQuery.value = '';
  scrollToBottom();
  isLoading.value = true;
  
  try {
    const response = await fetch('http://127.0.0.1:8000/api/ask', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ question: userText }) 
    });
    if (!response.ok) throw new Error('Network response was not ok');
    
    const reader = response.body.getReader();
    const decoder = new TextDecoder();
    let aiMessageIndex = -1;

    while (true) {
      const { value, done } = await reader.read();
      if (done) break;
      if (aiMessageIndex === -1) {
          isLoading.value = false;
          aiMessageIndex = messages.value.push({ role: 'ai', content: '' }) - 1;
      }
      const chunk = decoder.decode(value, { stream: true });
      if (aiMessageIndex !== -1) {
          messages.value[aiMessageIndex].content += chunk;
          scrollToBottom();
      }
    }
  } catch (error) {
    console.error('Chat error:', error);
    messages.value.push({ role: 'ai', content: '**[系统错误]** 连接服务器超时。' });
  } finally {
    isLoading.value = false;
    saveHistory();
    scrollToBottom();
  }
};

// --- 辅助功能 ---
const renderMarkdown = (text) => text ? DOMPurify.sanitize(marked.parse(text.trim())) : '';

const scrollToBottom = async () => {
  await nextTick();
  if (chatRef.value) chatRef.value.scrollTop = chatRef.value.scrollHeight;
};

const toggleChat = () => {
  isChatVisible.value = !isChatVisible.value;
  if (isChatVisible.value) scrollToBottom();
};

const clearHistory = () => {
  if(confirm('确定清空所有聊天记录吗？')) {
    messages.value = [];
    localStorage.removeItem('chatHistoryV2');
    messages.value.push({ role: 'ai', content: '您好，我是您的法律顾问，欢迎提问！' });
  }
};

const saveHistory = () => localStorage.setItem('chatHistoryV2', JSON.stringify(messages.value));

onMounted(() => {
  const saved = localStorage.getItem('chatHistoryV2');
  if (saved) messages.value = JSON.parse(saved);
  else messages.value.push({ role: 'ai', content: '您好，我是您的法律顾问，欢迎提问您在填写表格中遇到的任何问题。'});
});

// --- 拖拽调整大小 ---
const startResize = (e, direction) => {
  const startX = e.clientX;
  const startY = e.clientY;
  const startWidth = containerWidth.value;
  const startHeight = containerHeight.value;
  const maxScreenWidth = window.innerWidth;
  const maxScreenHeight = window.innerHeight;

  const doDrag = (dragEvent) => {
    if (direction === 'left' || direction === 'both') {
        const deltaX = startX - dragEvent.clientX; 
        const newWidth = startWidth + deltaX;
        if (newWidth > 300 && newWidth < (maxScreenWidth - 20)) {
            containerWidth.value = newWidth;
        }
    }

    if (direction === 'top' || direction === 'both') {
        const deltaY = startY - dragEvent.clientY; 
        const newHeight = startHeight + deltaY;
        if (newHeight > 400 && newHeight < (maxScreenHeight - 100)) {
            containerHeight.value = newHeight;
        }
    }
  };

  const stopDrag = () => {
    document.removeEventListener('mousemove', doDrag);
    document.removeEventListener('mouseup', stopDrag);
  };

  document.addEventListener('mousemove', doDrag);
  document.addEventListener('mouseup', stopDrag);
};
</script>

<style scoped>
/* ======================================================== */
/* 新增：悬浮按钮组样式 (核心交互逻辑) */
/* ======================================================== */

.floating-wrapper {
  position: fixed;
  bottom: 25px;
  right: 25px;
  z-index: 9998;
  display: flex;
  align-items: center;
  /* 增加透明 padding，防止鼠标在两个按钮间隙移动时触发mouseleave */
  padding: 10px 0 10px 20px; 
}

/* 当聊天窗口打开时隐藏按钮组 */
.floating-wrapper.hidden {
  opacity: 0;
  pointer-events: none;
}

/* 通用按钮样式 */
.main-btn, .sub-btn {
  border: none;
  border-radius: 50px;
  font-weight: bold;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  box-shadow: 0 4px 15px rgba(0,0,0,0.2);
  transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  white-space: nowrap;
}

/* --- 主按钮 (法律顾问 - 蓝色) --- */
.main-btn {
  background: #2563eb;
  color: white;
  padding: 12px 24px;
  font-size: 1rem;
  z-index: 2; /* 保证在最上层 */
  position: relative;
}

.main-btn:hover {
  transform: scale(1.05);
  background: #1d4ed8;
  box-shadow: 0 6px 20px rgba(37,99,235,0.4);
}

/* --- 子按钮 (数字人 - 橙色/渐变) --- */
.sub-btn {
  /* 使用橙色区分，或者你可以改回蓝色 */
  background: linear-gradient(135deg, #ebab62, #e69138); 
  color: white;
  padding: 10px 18px;
  font-size: 0.9rem;
  
  /* 初始隐藏状态：位于主按钮后面 */
  position: absolute;
  right: 10px; /* 藏在主按钮下面 */
  z-index: 1;
  opacity: 0;
  transform: translateX(0) scale(0.8);
  pointer-events: none;
}

/* --- 核心交互：Hover 容器时 -> 子按钮向左弹出 --- */
.floating-wrapper:hover .sub-btn {
  opacity: 1;
  /* 向左平移：主按钮宽度 + 间距 */
  transform: translateX(-130px) scale(1); 
  pointer-events: auto;
}

/* 子按钮悬停效果 */
.sub-btn:hover {
  background: linear-gradient(135deg, #f0b670, #eb9c4d);
  transform: translateX(-130px) scale(1.1); /* 保持位移同时放大 */
}

/* ======================================================== */
/* 以下为原有样式，保持不变 (只删除了 #chat-toggle-btn 相关) */
/* ======================================================== */

#chat-container {
  position: fixed;
  bottom: 80px;
  right: 20px;
  background-color: #fff;
  border-radius: 12px;
  box-shadow: 0 5px 25px rgba(0,0,0,0.15);
  display: flex;
  flex-direction: column;
  z-index: 9999;
  overflow: visible;
  transition: opacity 0.3s ease, transform 0.3s ease;
  opacity: 0;
  pointer-events: none;
  transform: translateY(20px);
}

#chat-container.show {
  opacity: 1;
  pointer-events: auto;
  transform: translateY(0);
}

.resize-handle {
  position: absolute;
  z-index: 100;
  background: transparent;
}
.handle-left { left: -5px; top: 0; bottom: 0; width: 10px; cursor: w-resize; }
.handle-top { top: -5px; left: 0; right: 0; height: 10px; cursor: n-resize; }
.handle-top-left { top: -8px; left: -8px; width: 20px; height: 20px; cursor: nw-resize; border-radius: 50%; }

.chat-header {
  background: linear-gradient(135deg, #2563eb, #1d4ed8);
  color: white;
  padding: 12px 15px;
  display: flex; justify-content: space-between; align-items: center; font-weight: bold;
  border-top-left-radius: 12px;
  border-top-right-radius: 12px;
}
.icon-btn { background: none; border: none; color: white; cursor: pointer; padding: 5px; }

#chat { flex: 1; overflow-y: auto; padding: 15px; background-color: #f8fafc; scroll-behavior: smooth; }

.message { display: flex; margin-bottom: 15px; align-items: flex-start; }
.avatar { width: 36px; height: 36px; border-radius: 50%; border: 2px solid #fff; box-shadow: 0 2px 4px rgba(0,0,0,0.1); flex-shrink: 0; }
.text { padding: 10px 14px; border-radius: 10px; font-size: 14px; line-height: 1.5; word-wrap: break-word; max-width: 100%; text-align: left; }
.message.ai .avatar { margin-right: 10px; }
.message.ai .text { background-color: #fff; color: #333; border: 1px solid #e2e8f0; border-top-left-radius: 2px; }
.message.user { flex-direction: row-reverse; }
.message.user .text { background-color: #2563eb; color: white; margin-right: 10px; border-bottom-right-radius: 2px; }

#question-form { padding: 12px; background: #fff; border-top: 1px solid #eee; display: flex; gap: 8px; }
#question-form input { flex: 1; padding: 10px 15px; border: 1px solid #ddd; border-radius: 20px; outline: none; }
#question-form input:focus { border-color: #2563eb; }
#question-form button { width: 40px; height: 40px; border-radius: 50%; background: #2563eb; color: white; border: none; cursor: pointer; display: flex; align-items: center; justify-content: center; }
#question-form button:disabled { background: #ccc; }

.spinner-box { display: flex; gap: 6px; align-items: center; justify-content: center; padding: 16px 20px !important; min-height: 40px; width: fit-content; }
.typing-dot { width: 8px; height: 8px; background-color: #2563eb; border-radius: 50%; animation: typing-wave 1.4s infinite ease-in-out both; }
.typing-dot:nth-child(1) { animation-delay: -0.32s; }
.typing-dot:nth-child(2) { animation-delay: -0.16s; }
.typing-dot:nth-child(3) { animation-delay: 0s; }
@keyframes typing-wave { 0%, 80%, 100% { transform: scale(0); opacity: 0.5; } 40% { transform: scale(1); opacity: 1; } }

:deep(.text *) { text-align: left; }
:deep(.text p) { margin: 0 0 8px 0; line-height: 1.6; }
:deep(.text p:last-child) { margin-bottom: 0; }
:deep(.text ul), :deep(.text ol) { margin: 0 0 8px 0; padding-left: 20px; }
:deep(.text pre) { background: #f1f5f9; padding: 8px; border-radius: 4px; overflow-x: auto; margin-bottom: 8px; }
</style>