<template>
  <div 
    class="digital-lawyer-modal"
    :style="{ width: boxWidth + 'px', height: boxHeight + 'px' }"
    :class="{ 'is-resizing': isResizing }"
  >
    <div class="resize-handle-tl" @mousedown="startResize">
      </div>

    <div class="header-bar">
      <button class="close-btn" @click="$emit('close')">
        <span>✕</span>
      </button>
    </div>
    
    <iframe 
      ref="vrmFrame"
      src="http://localhost:3000" 
      class="vrm-iframe"
      :style="{ pointerEvents: isResizing ? 'none' : 'auto' }"
      allow="microphone; camera"
      frameborder="0"
    ></iframe>
    
    <div class="loading-tips">正在连线阿律律师...</div>
  </div>
</template>

<script setup>
import { ref, onUnmounted } from 'vue';

const emit = defineEmits(['close']);

// --- 状态定义 ---
const boxWidth = ref(360);  // 初始宽度
const boxHeight = ref(600); // 初始高度
const isResizing = ref(false);

// 拖拽相关临时变量
let startX = 0;
let startY = 0;
let startW = 0;
let startH = 0;

// --- 拖拽逻辑 ---

const startResize = (e) => {
  e.preventDefault(); 
  isResizing.value = true;
  
  // 记录鼠标按下时的位置
  startX = e.clientX;
  startY = e.clientY;
  
  // 记录当前的宽高
  startW = boxWidth.value;
  startH = boxHeight.value;

  // 添加全局监听
  window.addEventListener('mousemove', handleResize);
  window.addEventListener('mouseup', stopResize);
};

const handleResize = (e) => {
  if (!isResizing.value) return;
  
  // --- 核心修改点：计算逻辑反转 ---
  // 因为是拖动左上角：
  // 鼠标向左移 (clientX 变小) -> 宽度变大 (diff > 0)
  // 鼠标向上移 (clientY 变小) -> 高度变大 (diff > 0)
  const dx = startX - e.clientX; 
  const dy = startY - e.clientY;

  const newWidth = startW + dx;
  const newHeight = startH + dy;

  // 限制最小尺寸 (宽300, 高400)
  if (newWidth > 300) boxWidth.value = newWidth;
  if (newHeight > 400) boxHeight.value = newHeight;
};

const stopResize = () => {
  isResizing.value = false;
  window.removeEventListener('mousemove', handleResize);
  window.removeEventListener('mouseup', stopResize);
};

onUnmounted(() => {
  window.removeEventListener('mousemove', handleResize);
  window.removeEventListener('mouseup', stopResize);
});
</script>

<style scoped>
/* 容器样式 */
.digital-lawyer-modal {
  position: fixed;
  bottom: 20px;
  right: 20px; /* 固定在右下角 */
  background: white;
  border-radius: 12px;
  /* 左上角圆角设为0，为了让手柄贴合（可选） */
  border-top-left-radius: 0; 
  box-shadow: 0 8px 30px rgba(0,0,0,0.2);
  z-index: 9999;
  border: 1px solid #e0e0e0;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  transition: box-shadow 0.3s;
}

.digital-lawyer-modal.is-resizing {
  box-shadow: 0 15px 50px rgba(0,0,0,0.4);
  user-select: none;
}

/* --- 左上角拖拽手柄样式 --- */
.resize-handle-tl {
  position: absolute;
  top: 0;
  left: 0;
  width: 25px;
  height: 25px;
  cursor: nwse-resize; /* 鼠标样式：左上-右下箭头 */
  z-index: 20; 
  
  /* 用渐变画一个左上角的三角形 */
  background: linear-gradient(135deg, rgba(235, 171, 98, 0.9) 50%, transparent 50%);
  
  /* 增加一点阴影让它浮起来 */
  box-shadow: 2px 2px 4px rgba(0,0,0,0.1);
  
  /* 过渡效果 */
  transition: width 0.2s, height 0.2s;
}

/* 鼠标悬停时手柄变大一点，提示可点击 */
.resize-handle-tl:hover {
  width: 30px;
  height: 30px;
  background: linear-gradient(135deg, #e69138 50%, transparent 50%);
}

/* 顶部栏样式 */
.header-bar {
  position: absolute;
  top: 0;
  right: 0; /* 靠右对齐，避开左边的手柄 */
  width: 100%; 
  height: 40px;
  z-index: 10;
  display: flex;
  justify-content: flex-end; /* 内容靠右 */
  align-items: center;
  padding: 0 10px;
  pointer-events: none; /* 让鼠标事件穿透 header，除非点到按钮 */
}

/* 关闭按钮 */
.close-btn {
  pointer-events: auto; /* 恢复按钮点击 */
  background: rgba(0, 0, 0, 0.4);
  color: white;
  border: none;
  width: 24px;
  height: 24px;
  border-radius: 50%;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
  backdrop-filter: blur(4px);
  transition: all 0.2s;
}

.close-btn:hover {
  background: rgba(200, 50, 50, 0.9);
}

.vrm-iframe {
  width: 100%;
  height: 100%;
  background: transparent;
  position: relative;
  z-index: 2;
  border: none;
}

.loading-tips {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  color: #999;
  font-size: 14px;
  z-index: 1;
}
</style>