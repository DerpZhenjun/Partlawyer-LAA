<template>
  <div class="la-page">
    <QA />
    <QA @open-digital-human="showDigitalLawyer = true" />

    <div class="container mt-4 mb-5 p-4 bg-light rounded shadow-sm">
      <h2 class="text-center mb-4 text-primary fw-bold">劳动仲裁申请书 (浙江省)</h2>

      <form @submit.prevent="submitForm">
        
        <div class="card mb-4 border-0 shadow-sm">
          <div class="card-header bg-white border-bottom-0 pb-0">
            <h5 class="text-primary fw-bold border-bottom border-2 border-primary d-inline-block pb-1">申请人信息</h5>
          </div>
          <div class="card-body">
            <div class="form-group row align-items-center mb-3">
              <label class="col-sm-3 col-form-label">申请书提交至：</label>
              <div class="col-sm-9 d-flex align-items-center">
                <input type="text" class="form-control me-2" v-model="form.submitCity" style="width: 150px;" placeholder="例如：杭州市">
                <span class="fw-bold">劳动人事争议仲裁委员会</span>
              </div>
            </div>

            <div class="row mb-3">
              <label class="col-sm-3 col-form-label">申请人姓名：</label>
              <div class="col-sm-9">
                <input type="text" class="form-control" v-model="form.applicantName" placeholder="您的真实姓名">
              </div>
            </div>

            <div class="row mb-3">
              <label class="col-sm-3 col-form-label">性别：</label>
              <div class="col-sm-9">
                <div class="form-check form-check-inline">
                  <input class="form-check-input" type="radio" id="g_male" value="男" v-model="form.gender">
                  <label class="form-check-label" for="g_male">男</label>
                </div>
                <div class="form-check form-check-inline">
                  <input class="form-check-input" type="radio" id="g_female" value="女" v-model="form.gender">
                  <label class="form-check-label" for="g_female">女</label>
                </div>
              </div>
            </div>

            <div class="row mb-3">
              <label class="col-sm-3 col-form-label">出生日期：</label>
              <div class="col-sm-9 d-flex">
                <input type="number" class="form-control me-2" v-model="form.birthYear" placeholder="年">
                <input type="number" class="form-control me-2" v-model="form.birthMonth" placeholder="月">
                <input type="number" class="form-control" v-model="form.birthDay" placeholder="日">
              </div>
            </div>

            <div class="row mb-3">
              <label class="col-sm-3 col-form-label">身份证号：</label>
              <div class="col-sm-9">
                <input type="text" class="form-control" v-model="form.idNumber" maxlength="18">
              </div>
            </div>

            <div class="row mb-3">
              <label class="col-sm-3 col-form-label">联系电话：</label>
              <div class="col-sm-9">
                <input type="text" class="form-control" v-model="form.phone">
              </div>
            </div>
             <div class="row mb-3">
              <label class="col-sm-3 col-form-label">民族：</label>
              <div class="col-sm-9">
                <input type="text" class="form-control" v-model="form.nationality" placeholder="例如：汉">
              </div>
            </div>

            <div class="row mb-3">
              <label class="col-sm-3 col-form-label">住址：</label>
              <div class="col-sm-9">
                <input type="text" class="form-control" v-model="form.address" placeholder="身份证上的住址或现住址">
              </div>
            </div>
          </div>
        </div>

        <div class="card mb-4 border-0 shadow-sm">
          <div class="card-header bg-white border-bottom-0 pb-0">
             <h5 class="text-primary fw-bold border-bottom border-2 border-primary d-inline-block pb-1">被申请人信息</h5>
          </div>
          <div class="card-body">
            <div class="row mb-3">
              <label class="col-sm-3 col-form-label">公司名称：</label>
              <div class="col-sm-9">
                <input type="text" class="form-control" v-model="form.respondentName" placeholder="公司全称">
              </div>
            </div>

            <div class="row mb-3">
              <label class="col-sm-3 col-form-label">公司住所地：</label>
              <div class="col-sm-9">
                <input type="text" class="form-control" v-model="form.respondentAddress" placeholder="营业执照上的地址">
              </div>
            </div>

            <div class="row mb-3">
                <label class="col-sm-3 col-form-label">法定代表人：</label>
                <div class="col-sm-3">
                    <input type="text" class="form-control mb-2" v-model="form.legalRepName" placeholder="姓名">
                </div>
                <div class="col-sm-3">
                    <input type="text" class="form-control mb-2" v-model="form.legalRepPosition" placeholder="职务 (如: 总经理)">
                </div>
                <div class="col-sm-3">
                    <input type="text" class="form-control" v-model="form.legalRepContact" placeholder="联系电话 (选填)">
                </div>
            </div>
          </div>
        </div>

        <div class="card mb-4 border-0 shadow-sm">
          <div class="card-header bg-white border-bottom-0 pb-0">
             <h5 class="text-danger fw-bold border-bottom border-2 border-danger d-inline-block pb-1">欠薪与追索详情</h5>
          </div>
          <div class="card-body bg-light">
             <div class="alert alert-warning py-2">
               <small><i class="fas fa-exclamation-circle"></i> 此处信息将直接填入申请书正文，请准确填写。</small>
             </div>

             <div class="row mb-3">
                <label class="col-sm-3 col-form-label fw-bold">追索总金额：</label>
                <div class="col-sm-9 input-group">
                  <input type="text" class="form-control" v-model="form.recourseAmount" placeholder="例如：15000">
                  <span class="input-group-text">元</span>
                </div>
             </div>

             <div class="row mb-3">
                <label class="col-sm-3 col-form-label fw-bold">月工资标准：</label>
                <div class="col-sm-9 input-group">
                  <input type="text" class="form-control" v-model="form.monthlySalary" placeholder="例如：5000">
                  <span class="input-group-text">元</span>
                </div>
             </div>

             <div class="row mb-3">
               <label class="col-sm-3 col-form-label">欠薪起始日期：</label>
               <div class="col-sm-9 d-flex">
                  <input type="number" class="form-control me-1" v-model="form.debtYearStart" placeholder="年">
                  <input type="number" class="form-control me-1" v-model="form.debtMonthStart" placeholder="月">
                  <input type="number" class="form-control" v-model="form.debtDayStart" placeholder="日">
               </div>
             </div>

             <div class="row mb-3">
               <label class="col-sm-3 col-form-label">欠薪结束日期：</label>
               <div class="col-sm-9 d-flex">
                  <input type="number" class="form-control me-1" v-model="form.debtYearEnd" placeholder="年">
                  <input type="number" class="form-control me-1" v-model="form.debtMonthEnd" placeholder="月">
                  <input type="number" class="form-control" v-model="form.debtDayEnd" placeholder="日">
               </div>
             </div>
          </div>
        </div>

        <div class="card mb-4 border-0 shadow-sm">
           <div class="card-header bg-white border-bottom-0 pb-0">
             <h5 class="text-primary fw-bold border-bottom border-2 border-primary d-inline-block pb-1">基本事实</h5>
          </div>
          <div class="card-body">
            <div class="row mb-3">
                <label class="col-sm-3 col-form-label">入职时间：</label>
                <div class="col-sm-9 d-flex">
                  <input type="number" class="form-control me-2" v-model="form.hireYear" placeholder="年">
                  <input type="number" class="form-control me-2" v-model="form.hireMonth" placeholder="月">
                  <input type="number" class="form-control" v-model="form.hireDay" placeholder="日">
                </div>
            </div>

            <div class="row mb-3">
                <label class="col-sm-3 col-form-label">岗位及职务：</label>
                <div class="col-sm-9">
                  <input type="text" class="form-control" v-model="form.jobPosition" placeholder="例如：销售经理">
                </div>
            </div>

            <div class="row mb-3">
                <label class="col-sm-3 col-form-label">劳动合同：</label>
                <div class="col-sm-9 pt-2">
                  <div class="form-check form-check-inline">
                      <input class="form-check-input" type="radio" id="contractYes" value="yes" v-model="form.contractOption">
                      <label class="form-check-label" for="contractYes">有签订</label>
                  </div>
                  <div class="form-check form-check-inline">
                      <input class="form-check-input" type="radio" id="contractNo" value="no" v-model="form.contractOption">
                      <label class="form-check-label" for="contractNo">无</label>
                  </div>
                </div>
            </div>
          </div>
        </div>

        <div class="text-center mt-5">
            <button type="submit" class="btn btn-primary btn-lg px-5 rounded-pill shadow" :disabled="isSubmitting">
                <span v-if="isSubmitting" class="spinner-border spinner-border-sm me-2"></span>
                <i v-else class="fas fa-file-word me-2"></i>
                {{ isSubmitting ? '正在生成文档...' : '生成仲裁申请书' }}
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

const form = reactive({
    // --- 申请人信息 ---
    submitCity: '',
    applicantName: '', // 后端对应 claimant
    gender: '男',
    birthYear: '', birthMonth: '', birthDay: '',
    idNumber: '',
    phone: '',
    nationality: '汉', // 新增：民族
    address: '',
    addressOption: 'confirmation_of_partie', // 暂时保留，虽然后端目前没用上
    addressAdditionalInput: '',

    // --- 被申请人信息 ---
    respondentName: '', // 后端对应 respondent
    respondentAddress: '',
    respondentAddressOption: 'same_as_residence',
    legalRepName: '',
    legalRepPosition: '',
    legalRepContact: '',

    // --- 核心诉求 & 工资 (新增，匹配后端 LAdocx) ---
    recourseAmount: '',   // 追索总金额
    monthlySalary: '',    // 月工资标准
    
    // --- 欠薪时间段 (新增) ---
    debtYearStart: '', debtMonthStart: '', debtDayStart: '',
    debtYearEnd: '', debtMonthEnd: '', debtDayEnd: '',

    // --- 事实与理由 ---
    hireYear: '', hireMonth: '', hireDay: '',
    jobPosition: '',
    contractOption: 'yes',
    
    // --- 预留字段 ---
    all_date_ranges: [] // 如果未来需要支持多段欠薪，可用这个
});

// --- 提交逻辑 ---
const submitForm = async () => {
    isSubmitting.value = true;
    try {
        // 1. 发送请求 (确保后端 app.py 注册了 /api/zhejiang/la)
        const response = await axios.post('http://127.0.0.1:8000/api/zhejiang/la/generate', form, {
            responseType: 'blob' 
        });

        // 2. 下载文件
        const fileName = `${form.applicantName || '申请人'}的劳动仲裁申请书.docx`;
        const url = window.URL.createObjectURL(new Blob([response.data]));
        const link = document.createElement('a');
        link.href = url;
        link.setAttribute('download', fileName);
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link); 
        
    } catch (error) {
        console.error('提交失败:', error);
        alert('生成文档失败，请检查：\n1. 后端 (app.py) 是否运行 \n2. 接口路径 /api/zhejiang/la 是否正确');
    } finally {
        isSubmitting.value = false;
    }
};
</script>

<style scoped>
.la-page {
  /* 给页面加个底色，让白色卡片更突出 */
  background-color: #f8f9fa; 
  min-height: 100vh;
  padding-bottom: 50px;
}

.card {
  transition: transform 0.2s;
}
.card:hover {
  /* 鼠标悬停时轻微浮起 */
  transform: translateY(-2px);
}

.form-control:focus {
  border-color: #86b7fe;
  box-shadow: 0 0 0 0.25rem rgba(13, 110, 253, 0.25);
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