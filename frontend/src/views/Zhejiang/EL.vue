<template>
  <div class="el-page min-vh-100 bg-light">
    <QA />
    <QA @open-digital-human="showDigitalLawyer = true" />

    <div class="container-lg py-4">
      
      <div class="text-center mb-5">
        <h2 class="fw-bold text-dark">证据清单 (浙江省)</h2>
        <p class="text-muted">请添加并完善您的证据信息</p>
      </div>

      <form @submit.prevent="submitForm">
        
        <div class="evidence-list mb-5">
          <transition-group name="list" tag="div" class="row g-4">
            
            <div 
              v-for="(group, index) in evidenceGroups" 
              :key="group.id" 
              :class="[
                'col-12', 
                // 核心修改：如果只有1组证据，占满全宽(12)；如果有>1组，每行两列(6)
                evidenceGroups.length > 1 ? 'col-md-6' : 'col-md-12'
              ]"
              class="transition-item"
            >
              <div class="card h-100 border-0 shadow-sm hover-shadow transition-all">
                <div class="card-header bg-white border-bottom-0 pt-3 px-3 d-flex justify-content-between align-items-center">
                  <span class="badge bg-primary bg-opacity-10 text-primary px-3 py-2 rounded-pill fs-6">
                    <i class="fas fa-file-contract me-1"></i> 
                    第 {{ toChineseNum(index + 1) }} 组证据
                  </span>
                  
                  <button 
                    type="button" 
                    class="btn btn-link text-danger text-decoration-none p-0" 
                    @click="removeGroup(index)" 
                    v-if="evidenceGroups.length > 0" 
                    title="删除此组"
                  >
                    <i class="fas fa-trash-alt"></i> <span class="small d-none d-sm-inline">删除</span>
                  </button>
                </div>

                <div class="card-body px-3 pb-3 pt-2">
                  <div class="row g-3">
                    
                    <div class="col-12 col-lg-8">
                      <label class="form-label text-secondary small fw-bold mb-1">证据名称</label>
                      <input 
                        type="text" 
                        class="form-control bg-light border-0" 
                        v-model="group.name" 
                        placeholder="例如：劳动合同书"
                      >
                    </div>

                    <div class="col-12 col-lg-4">
                      <label class="form-label text-secondary small fw-bold mb-1">来源</label>
                      <input 
                        type="text" 
                        class="form-control bg-light border-0" 
                        v-model="group.source" 
                        placeholder="如：原件"
                      >
                    </div>

                    <div class="col-12">
                      <label class="form-label text-secondary small fw-bold mb-1">证明对象</label>
                      <textarea 
                        class="form-control bg-light border-0" 
                        v-model="group.object" 
                        rows="4" 
                        placeholder="说明该证据证明了什么事实..."
                        style="resize: none;"
                      ></textarea>
                    </div>

                  </div>
                </div>
              </div>
            </div>
          </transition-group>
        </div>

        <div class="action-area text-center">
          <button type="button" class="btn btn-outline-primary btn-lg border-dashed me-md-3 mb-3 mb-md-0 w-100 w-md-auto" @click="addGroup">
            <i class="fas fa-plus-circle me-2"></i> 增加一组证据
          </button>
          
          <button type="submit" class="btn btn-primary btn-lg w-100 w-md-auto px-5 shadow" :disabled="isSubmitting">
            <span v-if="isSubmitting" class="spinner-border spinner-border-sm me-2"></span>
            {{ isSubmitting ? '生成中...' : '生成证据清单' }}
          </button>
        </div>

      </form>
    </div>
  </div>
<transition name="fade-slide">
      <DigitalLawyer
        v-if="showDigitalLawyer"
        @close="showDigitalLawyer = false"
      />
</transition>
</template>

<script setup>
import { ref } from 'vue';
import axios from 'axios';
import QA from '@/components/QA.vue';

import DigitalLawyer from '@/components/DigitalLawyer.vue'; 
const showDigitalLawyer = ref(false); 

// --- 状态定义 ---
const isSubmitting = ref(false);

// 证据组数据
const evidenceGroups = ref([
  { id: Date.now(), name: '', source: '', object: '' }
]);

// --- 辅助函数：数字转中文 ---
const toChineseNum = (num) => {
  const changeNum = ['零', '一', '二', '三', '四', '五', '六', '七', '八', '九'];
  const unit = ["", "十", "百", "千", "万"];
  num = parseInt(num);
  let getWan = (temp) => {
    let strArr = temp.toString().split("").reverse();
    let newNum = "";
    for (var i = 0; i < strArr.length; i++) {
      newNum = (i == 0 && strArr[i] == 0 ? "" : (i > 0 && strArr[i] == 0 && strArr[i - 1] == 0 ? "" : changeNum[strArr[i]] + (strArr[i] == 0 ? unit[0] : unit[i]))) + newNum;
    }
    return newNum;
  }
  return getWan(num);
};

// --- 操作逻辑 ---
const addGroup = () => {
  evidenceGroups.value.push({
    id: Date.now(),
    name: '',
    source: '',
    object: ''
  });
};

const removeGroup = (index) => {
  evidenceGroups.value.splice(index, 1);
};

// --- 提交逻辑 ---
const submitForm = async () => {
  if (evidenceGroups.value.length === 0) {
    evidenceGroups.value.push({ 
      id: Date.now(), 
      name: '', 
      source: '', 
      object: '' 
    });
  }

  isSubmitting.value = true;
  try {
    const response = await axios.post('http://127.0.0.1:8000/api/zhejiang/el/generate', {
      evidence_list: evidenceGroups.value 
    }, {
      responseType: 'blob'
    });

    const url = window.URL.createObjectURL(new Blob([response.data]));
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', '证据清单.docx');
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link); 

  } catch (error) {
    console.error('提交失败:', error);
    alert('生成失败，请检查后端服务是否运行');
  } finally {
    isSubmitting.value = false;
  }
};
</script>

<style scoped>
/* 悬浮上浮效果 */
.hover-shadow:hover {
  transform: translateY(-3px);
  box-shadow: 0 0.5rem 1rem rgba(0,0,0,0.1) !important;
}
.transition-all {
  transition: all 0.3s ease;
}

/* 输入框聚焦样式 */
.form-control:focus {
  background-color: #fff;
  box-shadow: 0 0 0 0.25rem rgba(13, 110, 253, 0.15);
}

/* 虚线按钮 */
.border-dashed {
  border-style: dashed;
  border-width: 2px;
}
.border-dashed:hover {
  background-color: #f0f8ff;
}

/* --- 列表与布局动画关键 CSS --- */

/* 1. 列表项目的过渡效果 */
.transition-item {
  /* 确保宽度变化(col-12 -> col-6)时有平滑过渡 */
  transition: all 0.5s cubic-bezier(0.55, 0, 0.1, 1);
}

/* 2. 列表元素进入/离开 */
.list-enter-from,
.list-leave-to {
  opacity: 0;
  transform: scale(0.9); /* 轻微缩放效果 */
}

/* 3. 确保离开的元素脱离文档流，让后面的元素可以平滑补位 */
.list-leave-active {
  position: absolute;
  width: 100%; /* 防止脱离文档流后宽度坍塌 */
  z-index: 0;
}

/* 4. Vue 的 v-move 特性：处理剩余元素的位置移动（当上面的元素删除或布局改变时） */
.list-move {
  transition: all 0.5s cubic-bezier(0.55, 0, 0.1, 1);
}

/* 移动端适配调整 */
@media (max-width: 768px) {
  .w-md-auto {
    width: 100% !important;
  }
}

/* DigitalLawyer 组件的入场动画 */
.fade-slide-enter-active,
.fade-slide-leave-active {
  transition: all 0.4s cubic-bezier(0.19, 1, 0.22, 1);
}

.fade-slide-enter-from,
.fade-slide-leave-to {
  opacity: 0;
  transform: translateY(20px) scale(0.95);
}
</style>