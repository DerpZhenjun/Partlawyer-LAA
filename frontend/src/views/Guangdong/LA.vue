<template>
  <div class="la-page">
    <QA />
    <QA @open-digital-human="showDigitalLawyer = true" />

    <div class="container mt-4 mb-5 p-4 bg-light rounded shadow-sm">
      <h2 class="text-center mb-4">劳动仲裁申请书 (广东省)</h2>

      <form @submit.prevent="submitForm">
        
        <h4 class="section-title">申请人信息</h4>
        
        <div class="row mb-3 align-items-center">
          <label class="col-sm-3 col-form-label fw-bold">申请书提交至：</label>
          <div class="col-sm-9 d-flex align-items-center">
            <input type="text" class="form-control me-2" v-model="form.submitCity" style="width: 120px;" placeholder="城市">
            <span>劳动人事争议仲裁委员会</span>
          </div>
        </div>

        <div class="row mb-3">
          <label class="col-sm-3 col-form-label fw-bold">申请人姓名：</label>
          <div class="col-sm-9">
            <input type="text" class="form-control" v-model="form.applicantName" style="width: 200px;" placeholder="申请人姓名">
          </div>
        </div>

        <div class="row mb-3">
          <label class="col-sm-3 col-form-label fw-bold">性别：</label>
          <div class="col-sm-9">
            <div class="form-check form-check-inline">
              <input class="form-check-input" type="radio" value="男" v-model="form.gender">
              <label class="form-check-label">男</label>
            </div>
            <div class="form-check form-check-inline">
              <input class="form-check-input" type="radio" value="女" v-model="form.gender">
              <label class="form-check-label">女</label>
            </div>
          </div>
        </div>

        <div class="row mb-3">
          <label class="col-sm-3 col-form-label fw-bold">出生日期：</label>
          <div class="col-sm-9 d-flex">
            <input type="number" class="form-control me-2" v-model="form.birthYear" placeholder="年" style="width: 100px;">
            <input type="number" class="form-control me-2" v-model="form.birthMonth" placeholder="月" style="width: 80px;">
            <input type="number" class="form-control" v-model="form.birthDay" placeholder="日" style="width: 80px;">
          </div>
        </div>

        <div class="row mb-3">
          <label class="col-sm-3 col-form-label fw-bold">公民身份号码：</label>
          <div class="col-sm-9">
            <input type="text" class="form-control" v-model="form.idNumber" maxlength="18">
          </div>
        </div>

        <div class="row mb-3">
          <label class="col-sm-3 col-form-label fw-bold">联系电话：</label>
          <div class="col-sm-9">
            <input type="text" class="form-control" v-model="form.phone">
          </div>
        </div>

        <div class="row mb-3">
          <label class="col-sm-3 col-form-label fw-bold">住址：</label>
          <div class="col-sm-9">
            <input type="text" class="form-control" v-model="form.address">
          </div>
        </div>

        <div class="row mb-3">
          <label class="col-sm-3 col-form-label fw-bold">通讯地址：</label>
          <div class="col-sm-9">
            <div class="form-check">
              <input class="form-check-input" type="radio" value="confirmation_of_partie" v-model="form.addressOption">
              <label class="form-check-label">以《当事人有效送达地址确认书》为准</label>
            </div>
            <div class="form-check">
              <input class="form-check-input" type="radio" value="other" v-model="form.addressOption">
              <label class="form-check-label">其他</label>
              <input v-if="form.addressOption === 'other'" type="text" class="form-control mt-2" v-model="form.addressAdditionalInput" placeholder="请输入具体地址">
            </div>
          </div>
        </div>

        <h4 class="section-title mt-5">被申请人信息</h4>
        
        <div class="row mb-3">
          <label class="col-sm-3 col-form-label fw-bold">被申请人名称：</label>
          <div class="col-sm-9">
            <input type="text" class="form-control" v-model="form.respondentName">
          </div>
        </div>

        <div class="row mb-3">
          <label class="col-sm-3 col-form-label fw-bold">住所：</label>
          <div class="col-sm-9">
            <input type="text" class="form-control" v-model="form.respondentAddress">
          </div>
        </div>

        <div class="row mb-3">
          <label class="col-sm-3 col-form-label fw-bold">通讯地址：</label>
          <div class="col-sm-9">
            <div class="form-check">
              <input class="form-check-input" type="radio" value="same_as_residence" v-model="form.respondentAddressOption">
              <label class="form-check-label">与被申请人住所相同</label>
            </div>
            <div class="form-check">
              <input class="form-check-input" type="radio" value="other" v-model="form.respondentAddressOption">
              <label class="form-check-label">其他</label>
              <input v-if="form.respondentAddressOption === 'other'" type="text" class="form-control mt-2" v-model="form.respondentAddressAdditionalInput" placeholder="请输入具体地址">
            </div>
          </div>
        </div>

        <div class="row mb-3">
          <label class="col-sm-3 col-form-label fw-bold">法定代表人：</label>
          <div class="col-sm-3">
            <input type="text" class="form-control mb-2" v-model="form.legalRepName" placeholder="姓名">
          </div>
          <div class="col-sm-3">
            <input type="text" class="form-control mb-2" v-model="form.legalRepPosition" placeholder="职务">
          </div>
          <div class="col-sm-3">
            <input type="text" class="form-control" v-model="form.legalRepContact" placeholder="联系电话">
          </div>
        </div>

        <h4 class="section-title mt-5">仲裁请求</h4>
        <div class="alert alert-secondary fs-7">
          <small><i class="fas fa-info-circle"></i> 示例：（1）请求确认2018年8月20日至2018年11月19日期间双方存在劳动关系...</small>
        </div>

        <div v-for="(item, index) in form.arbitrationRequest" :key="'req-'+index" class="mb-3 d-flex align-items-start">
          <label class="me-2 mt-2 fw-bold">{{ index + 1 }}、</label>
          <textarea class="form-control" v-model="form.arbitrationRequest[index]" rows="3" placeholder="请输入仲裁请求"></textarea>
          <button type="button" class="btn btn-outline-danger btn-sm ms-2 mt-2" @click="removeRequest(index)" v-if="form.arbitrationRequest.length > 1">
            <i class="fas fa-minus"></i>
          </button>
        </div>
        <button type="button" class="btn btn-primary btn-sm" @click="addRequest"><i class="fas fa-plus"></i> 添加请求</button>


        <h4 class="section-title mt-5">仲裁请求计算公式</h4>
        <div class="alert alert-secondary fs-7">
          <small><i class="fas fa-info-circle"></i> 示例：（1）违法解除劳动关系赔偿金5000元=月工资5000元×0.5个月×2倍</small>
        </div>
        
        <div v-for="(item, index) in form.requestCalculation" :key="'calc-'+index" class="mb-3 d-flex align-items-start">
          <label class="me-2 mt-2 fw-bold">{{ index + 1 }}、</label>
          <textarea class="form-control" v-model="form.requestCalculation[index]" rows="3" placeholder="请输入计算公式"></textarea>
          <button type="button" class="btn btn-outline-danger btn-sm ms-2 mt-2" @click="removeCalculation(index)" v-if="form.requestCalculation.length > 1">
            <i class="fas fa-minus"></i>
          </button>
        </div>
        <button type="button" class="btn btn-primary btn-sm" @click="addCalculation"><i class="fas fa-plus"></i> 添加公式</button>


        <h4 class="section-title mt-5">基本事实和理由</h4>
        
        <div class="row mb-3">
          <label class="col-sm-3 col-form-label fw-bold">入职时间：</label>
          <div class="col-sm-9 d-flex">
            <input type="number" class="form-control me-2" v-model="form.hireYear" placeholder="年" style="width: 100px;">
            <input type="number" class="form-control me-2" v-model="form.hireMonth" placeholder="月" style="width: 80px;">
            <input type="number" class="form-control" v-model="form.hireDay" placeholder="日" style="width: 80px;">
          </div>
        </div>

        <div class="row mb-3">
          <label class="col-sm-3 col-form-label fw-bold">岗位及职务：</label>
          <div class="col-sm-9">
            <input type="text" class="form-control" v-model="form.jobPosition">
          </div>
        </div>

        <div class="row mb-3">
          <label class="col-sm-3 col-form-label fw-bold">签订劳动合同：</label>
          <div class="col-sm-9">
            <div class="form-check form-check-inline">
              <input class="form-check-input" type="radio" value="yes" v-model="form.contractOption">
              <label class="form-check-label">有</label>
            </div>
            <div class="form-check form-check-inline">
              <input class="form-check-input" type="radio" value="no" v-model="form.contractOption">
              <label class="form-check-label">无</label>
            </div>
          </div>
        </div>

        <div class="row mb-3">
            <label class="col-sm-3 col-form-label fw-bold">最后一期合同期限：</label>
            <div class="col-sm-9">
                <div class="d-flex mb-2 align-items-center">
                    <input type="number" class="form-control me-1" style="width:80px" v-model="form.contractStartYear"><span class="me-2">年</span>
                    <input type="number" class="form-control me-1" style="width:60px" v-model="form.contractStartMonth"><span class="me-2">月</span>
                    <input type="number" class="form-control me-1" style="width:60px" v-model="form.contractStartDay"><span class="me-2">日</span>
                    <span class="mx-2 fw-bold">至</span>
                    <input type="number" class="form-control me-1" style="width:80px" v-model="form.contractEndYear"><span class="me-2">年</span>
                    <input type="number" class="form-control me-1" style="width:60px" v-model="form.contractEndMonth"><span class="me-2">月</span>
                    <input type="number" class="form-control me-1" style="width:60px" v-model="form.contractEndDay"><span>日</span>
                </div>
            </div>
        </div>

        <div class="row mb-3">
          <label class="col-sm-3 col-form-label fw-bold">工作地点：</label>
          <div class="col-sm-9">
            <input type="text" class="form-control" v-model="form.workLocation">
          </div>
        </div>

        <div class="row mb-3">
            <label class="col-sm-3 col-form-label fw-bold">工作时间：</label>
            <div class="col-sm-9">
                <div class="form-check mb-2">
                    <input class="form-check-input" type="radio" value="specific_time" v-model="form.workTimeOption">
                    <label class="form-check-label">
                        每周工作 <input type="number" class="form-control d-inline-block px-1 py-0 text-center" style="width:50px; height:25px" v-model="form.workDaysPerWeek"> 天，
                        每天 <input type="number" class="form-control d-inline-block px-1 py-0 text-center" style="width:50px; height:25px" v-model="form.workHoursPerDay"> 小时
                    </label>
                </div>
                <div class="form-check">
                    <input class="form-check-input" type="radio" value="other" v-model="form.workTimeOption">
                    <label class="form-check-label">其他</label>
                    <input v-if="form.workTimeOption === 'other'" type="text" class="form-control mt-1" v-model="form.workTimeAdditionalInput" placeholder="请输入">
                </div>
            </div>
        </div>

        <div class="row mb-3">
            <label class="col-sm-3 col-form-label fw-bold">是否考勤：</label>
            <div class="col-sm-9">
                <div class="form-check form-check-inline">
                    <input class="form-check-input" type="radio" value="yes" v-model="form.attendanceOption">
                    <label class="form-check-label">是</label>
                </div>
                <div class="form-check form-check-inline">
                    <input class="form-check-input" type="radio" value="no" v-model="form.attendanceOption">
                    <label class="form-check-label">否</label>
                </div>
            </div>
        </div>

        <div class="row mb-3">
            <label class="col-sm-3 col-form-label fw-bold">考勤方式：</label>
            <div class="col-sm-9">
                <input type="text" class="form-control" v-model="form.attendanceMethod">
            </div>
        </div>

        <div class="row mb-3">
            <label class="col-sm-3 col-form-label fw-bold">工资发放方式：</label>
            <div class="col-sm-9">
                <div class="form-check">
                    <input class="form-check-input" type="checkbox" v-model="form.salaryOptions.cash">
                    <label class="form-check-label">现金</label>
                </div>
                <div class="form-check">
                    <input class="form-check-input" type="checkbox" v-model="form.salaryOptions.transfer">
                    <label class="form-check-label">转账</label>
                </div>
                <div class="form-check">
                    <input class="form-check-input" type="checkbox" v-model="form.salaryOptions.signature">
                    <label class="form-check-label">需要签收</label>
                </div>
                <div class="form-check">
                    <input class="form-check-input" type="checkbox" v-model="form.salaryOptions.noSignature">
                    <label class="form-check-label">不需要签收</label>
                </div>
            </div>
        </div>

        <div class="mb-3">
            <label class="form-label fw-bold">入职时工资标准：</label>
            <textarea class="form-control" rows="2" v-model="form.initialSalary"></textarea>
        </div>

        <div class="mb-3">
            <label class="form-label fw-bold">工资标准调整情况：</label>
            <textarea class="form-control" rows="2" v-model="form.salaryAdjustment"></textarea>
        </div>

        <div class="row mb-3">
            <label class="col-sm-3 col-form-label fw-bold">现是否在职：</label>
            <div class="col-sm-9">
                <div class="form-check form-check-inline">
                    <input class="form-check-input" type="radio" value="yes" v-model="form.currentEmploymentStatus">
                    <label class="form-check-label">是</label>
                </div>
                <div class="form-check form-check-inline">
                    <input class="form-check-input" type="radio" value="no" v-model="form.currentEmploymentStatus">
                    <label class="form-check-label">否</label>
                </div>
            </div>
        </div>

        <div class="row mb-3">
            <label class="col-sm-3 col-form-label fw-bold">离职时间：</label>
            <div class="col-sm-9 d-flex">
                <input type="number" class="form-control me-2" v-model="form.leaveYear" placeholder="年" style="width: 100px;">
                <input type="number" class="form-control me-2" v-model="form.leaveMonth" placeholder="月" style="width: 80px;">
                <input type="number" class="form-control" v-model="form.leaveDay" placeholder="日" style="width: 80px;">
            </div>
        </div>

        <div class="mb-3">
            <label class="form-label fw-bold">离职原因：</label>
            <textarea class="form-control" rows="2" v-model="form.leaveReason" placeholder="若在职不用填写"></textarea>
        </div>

        <div class="row mb-3">
            <label class="col-sm-4 col-form-label fw-bold">离职前12个月月平均工资：</label>
            <div class="col-sm-8">
                <input type="text" class="form-control" v-model="form.avgMonthlySalary" placeholder="元/月" style="width: 150px;">
            </div>
        </div>

        <div class="mb-5">
            <label class="form-label fw-bold">其他需要说明的事实和理由：</label>
            <textarea class="form-control" rows="4" v-model="form.additionalFacts"></textarea>
        </div>

        <div class="text-center">
            <button type="submit" class="btn btn-primary btn-lg px-5" :disabled="isSubmitting">
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
import { reactive, ref } from 'vue';
import axios from 'axios';
import QA from '@/components/QA.vue';

import DigitalLawyer from '@/components/DigitalLawyer.vue'; 
const showDigitalLawyer = ref(false); 

const isSubmitting = ref(false);

// 初始化表单数据，所有单选/多选/输入框默认值均为空，确保无默认选中
const form = reactive({
    // 申请人
    submitCity: '',
    applicantName: '', 
    gender: '', // 移除默认 '男'
    birthYear: '', birthMonth: '', birthDay: '',
    idNumber: '',
    phone: '',
    address: '',
    addressOption: '', // 移除默认 'confirmation_of_partie'
    addressAdditionalInput: '',

    // 被申请人
    respondentName: '',
    respondentAddress: '',
    respondentAddressOption: '', // 移除默认 'same_as_residence'
    respondentAddressAdditionalInput: '',
    legalRepName: '', legalRepPosition: '', legalRepContact: '',

    // 动态数组
    arbitrationRequest: [''],
    requestCalculation: [''],

    // 事实与理由
    hireYear: '', hireMonth: '', hireDay: '',
    jobPosition: '',
    contractOption: '', // 移除默认 'yes'
    // 合同期限
    contractStartYear: '', contractStartMonth: '', contractStartDay: '',
    contractEndYear: '', contractEndMonth: '', contractEndDay: '',
    
    workLocation: '',
    workTimeOption: '', // 移除默认 'specific_time'
    workDaysPerWeek: '', workHoursPerDay: '', workTimeAdditionalInput: '',
    
    attendanceOption: '', // 移除默认 'yes'
    attendanceMethod: '',
    
    // 工资发放 (复选框映射对象)
    salaryOptions: {
        cash: false,
        transfer: false,
        signature: false,
        noSignature: false
    },
    
    initialSalary: '',
    salaryAdjustment: '',
    
    currentEmploymentStatus: '', // 移除默认 'yes'
    leaveYear: '', leaveMonth: '', leaveDay: '',
    leaveReason: '',
    avgMonthlySalary: '',
    
    additionalFacts: ''
});

// 动态增删
const addRequest = () => form.arbitrationRequest.push('');
const removeRequest = (index) => form.arbitrationRequest.splice(index, 1);

const addCalculation = () => form.requestCalculation.push('');
const removeCalculation = (index) => form.requestCalculation.splice(index, 1);

const submitForm = async () => {
    isSubmitting.value = true;
    try {
        // 数据处理
        const payload = {
            ...form,
            salaryOption1: form.salaryOptions.cash ? 'yes' : 'no',
            salaryOption2: form.salaryOptions.signature ? 'yes' : 'no',
            salaryOption3: form.salaryOptions.transfer ? 'yes' : 'no', 
            salaryOption4: form.salaryOptions.noSignature ? 'yes' : 'no',
        };

        // 发送请求
        const response = await axios.post('http://127.0.0.1:8000/api/guangdong/la/generate', payload, {
            responseType: 'blob'
        });

        // 提取文件名逻辑
        let fileName = '劳动仲裁申请书.docx'; 
        const disposition = response.headers['content-disposition'];
        
        if (disposition) {
            let match = disposition.match(/filename\*=utf-8''(.+)/i);
            if (match && match[1]) {
                fileName = decodeURIComponent(match[1]);
            } else {
                match = disposition.match(/filename="?([^"]+)"?/i);
                if (match && match[1]) {
                    fileName = match[1];
                }
            }
        }

        // 触发下载
        const url = window.URL.createObjectURL(new Blob([response.data]));
        const link = document.createElement('a');
        link.href = url;
        link.setAttribute('download', fileName);
        document.body.appendChild(link);
        link.click();
        
        // 清理内存
        document.body.removeChild(link);
        window.URL.revokeObjectURL(url);

    } catch (error) {
        console.error('Submission failed', error);
        alert('生成失败，请检查网络或联系管理员');
    } finally {
        isSubmitting.value = false;
    }
};
</script>

<style scoped>
.section-title {
    margin-top: 30px;
    padding-bottom: 10px;
    border-bottom: 2px solid #0d6efd;
    color: #333;
}
.fs-7 {
    font-size: 0.85rem;
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