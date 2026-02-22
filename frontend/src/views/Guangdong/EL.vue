<template>
  <div class="el-page min-vh-100 bg-light">
    <QA />
    <QA @open-digital-human="showDigitalLawyer = true" />

    <div class="container-lg py-4">
      
      <div class="text-center mb-5">
        <h2 class="fw-bold text-dark">证据清单 (广东省)</h2>
        <p class="text-muted">请添加并完善您的证据信息</p>
      </div>

      <form @submit.prevent="submitForm">
        
        <div class="evidence-list mb-5">
          <transition-group name="list" tag="div" class="row g-4">
            
            <div 
              v-for="(group, index) in evidenceList" 
              :key="group.id" 
              :class="[
                'col-12', 
                // 核心逻辑：1组时全宽，>1组时半宽
                evidenceList.length > 1 ? 'col-md-6' : 'col-md-12'
              ]"
              class="transition-item"
            >
              <div class="card h-100 border-0 shadow-sm hover-shadow transition-all">
                <div class="card-header bg-white border-bottom-0 pt-3 px-3 d-flex justify-content-between align-items-center">
                  <span class="badge bg-primary bg-opacity-10 text-primary px-3 py-2 rounded-pill fs-6">
                    <i class="fas fa-folder-open me-1"></i>
                    第 {{ toChineseNum(index + 1) }} 组证据
                  </span>
                  
                  <button 
                    type="button" 
                    class="btn btn-link text-danger text-decoration-none p-0" 
                    @click="removeGroup(index)" 
                    v-if="evidenceList.length > 0"
                    title="删除此组"
                  >
                    <i class="fas fa-trash-alt"></i> <span class="small d-none d-sm-inline">删除</span>
                  </button>
                </div>

                <div class="card-body px-3 pb-3 pt-2">
                  <div class="row g-3">
                    
                    <div class="col-12">
                      <label class="form-label text-secondary small fw-bold mb-1">证据名称</label>
                      <input 
                        type="text" 
                        class="form-control bg-light border-0" 
                        v-model="group.name" 
                        placeholder="请输入证据名称"
                      >
                    </div>
                    
                    <div class="col-12">
                      <label class="form-label text-secondary small fw-bold mb-1">证明内容</label>
                      <textarea 
                        class="form-control bg-light border-0" 
                        v-model="group.content" 
                        rows="5" 
                        placeholder="请输入该证据想要证明的内容..."
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
            <i class="fas fa-plus-circle me-2"></i> 增加证据组
          </button>
          
          <button type="submit" class="btn btn-primary btn-lg w-100 w-md-auto px-5 shadow" :disabled="isSubmitting">
            <span v-if="isSubmitting" class="spinner-border spinner-border-sm me-2"></span>
            {{ isSubmitting ? '生成中...' : '生成文档' }}
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

const isSubmitting = ref(false);

// 证据列表状态
const evidenceList = ref([
  { id: Date.now(), name: '', content: '' }
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

// --- 动态增删逻辑 ---
const addGroup = () => {
  evidenceList.value.push({
    id: Date.now(),
    name: '',
    content: ''
  });
};

const removeGroup = (index) => {
  evidenceList.value.splice(index, 1);
};

// --- 提交逻辑 ---
const submitForm = async () => {
  // 防止空数组提交
  if (evidenceList.value.length === 0) {
    evidenceList.value.push({ id: Date.now(), name: '', content: '' });
  }

  // 如果需要严格校验非空，可取消下行注释。这里为了灵活体验暂不强制校验。
  // if (evidenceList.value.some(item => !item.name.trim())) { alert('请填写名称'); return; }

  isSubmitting.value = true;
  try {
    const response = await axios.post('http://127.0.0.1:8000/api/guangdong/el/generate', {
      evidence_list: evidenceList.value
    }, {
      responseType: 'blob'
    });

    const url = window.URL.createObjectURL(new Blob([response.data]));
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', '广东证据清单.docx');
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);

  } catch (error) {
    console.error('Submission failed', error);
    alert('生成失败，请检查后端服务是否启动');
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
  transition: all 0.5s cubic-bezier(0.55, 0, 0.1, 1);
}

/* 2. 列表元素进入/离开 */
.list-enter-from,
.list-leave-to {
  opacity: 0;
  transform: scale(0.9);
}

/* 3. 确保离开的元素脱离文档流 */
.list-leave-active {
  position: absolute;
  width: 100%;
  z-index: 0;
}

/* 4. 剩余元素移动 */
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