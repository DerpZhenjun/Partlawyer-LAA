<template>
  <div class="wia-page">
    <QA />

    <div class="container mt-4 mb-5 p-4 bg-light rounded shadow-sm">
      <h2 class="text-center mb-4">工伤仲裁申请书</h2>

      <form @submit.prevent="submitForm">
        
        <h4 class="section-title">申请人信息</h4>
        
        <div class="row mb-3">
          <label class="col-sm-3 col-form-label fw-bold">姓名：</label>
          <div class="col-sm-9">
            <input type="text" class="form-control" v-model="form.claimantName">
          </div>
        </div>

        <div class="row mb-3">
          <label class="col-sm-3 col-form-label fw-bold">民族：</label>
          <div class="col-sm-9">
            <select class="form-select" v-model="form.claimantNationality">
              <option value="" disabled>请选择民族</option>
              <option v-for="nation in nations" :key="nation" :value="nation">{{ nation }}</option>
            </select>
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
          <label class="col-sm-3 col-form-label fw-bold">职业：</label>
          <div class="col-sm-9">
            <input type="text" class="form-control" v-model="form.occupation">
          </div>
        </div>

        <div class="row mb-3">
          <label class="col-sm-3 col-form-label fw-bold">出生日期：</label>
          <div class="col-sm-9 d-flex">
            <input type="number" class="form-control me-2" v-model="form.birthdayYear" placeholder="年" style="width: 100px;">
            <input type="number" class="form-control me-2" v-model="form.birthdayMonth" placeholder="月" style="width: 80px;">
            <input type="number" class="form-control" v-model="form.birthdayDay" placeholder="日" style="width: 80px;">
          </div>
        </div>

        <div class="row mb-3">
          <label class="col-sm-3 col-form-label fw-bold">身份证号：</label>
          <div class="col-sm-9">
            <input type="text" class="form-control" v-model="form.idNumber" maxlength="18">
          </div>
        </div>

        <div class="row mb-3">
          <label class="col-sm-3 col-form-label fw-bold">户籍地：</label>
          <div class="col-sm-9">
            <input type="text" class="form-control" v-model="form.registeredAddress">
          </div>
        </div>

        <div class="row mb-3">
          <label class="col-sm-3 col-form-label fw-bold">现居住地：</label>
          <div class="col-sm-9">
            <textarea class="form-control" v-model="form.residenceAddress" rows="2"></textarea>
          </div>
        </div>

        <div class="row mb-3">
          <label class="col-sm-3 col-form-label fw-bold">联系电话：</label>
          <div class="col-sm-9">
            <input type="text" class="form-control" v-model="form.claimantPhone">
          </div>
        </div>

        <h4 class="section-title mt-5">被申请公司信息</h4>
        
        <div class="row mb-3">
          <label class="col-sm-3 col-form-label fw-bold">公司名称：</label>
          <div class="col-sm-9">
            <input type="text" class="form-control" v-model="form.respondentCompany">
          </div>
        </div>

        <div class="row mb-3">
          <label class="col-sm-3 col-form-label fw-bold">公司地址：</label>
          <div class="col-sm-9">
            <textarea class="form-control" v-model="form.respondentAddress" rows="2"></textarea>
          </div>
        </div>

        <div class="row mb-3">
          <label class="col-sm-3 col-form-label fw-bold">法定代表人：</label>
          <div class="col-sm-9">
            <input type="text" class="form-control" v-model="form.legalRepresentative">
          </div>
        </div>

        <div class="row mb-3">
          <label class="col-sm-3 col-form-label fw-bold">联系电话：</label>
          <div class="col-sm-9">
            <input type="text" class="form-control" v-model="form.respondentPhone">
          </div>
        </div>

        <h4 class="section-title mt-5">工伤待遇请求</h4>
        <div class="alert alert-info fs-7">
          <i class="fas fa-info-circle"></i> 点击左侧 <span class="badge bg-primary rounded-pill"><i class="fas fa-plus"></i></span> 按钮可展开填写该项费用。
        </div>

        <div class="card mb-3 border-0 shadow-sm bg-white">
          <div class="card-body py-2">
            <div class="row align-items-center">
              <label class="col-sm-4 col-form-label">医疗费：</label>
              <div class="col-sm-8 d-flex align-items-center">
                <input type="number" class="form-control me-2" v-model="form.medicalFees" style="width: 120px;"> 元
              </div>
            </div>
          </div>
        </div>

        <div v-for="(item, key) in requestItems" :key="key" class="card mb-3 border-0 shadow-sm bg-white">
          <div class="card-header bg-transparent d-flex align-items-center py-2 border-0">
            <button 
              type="button" 
              class="btn btn-sm btn-icon me-3" 
              :class="visibility[key] ? 'btn-danger' : 'btn-primary'"
              @click="toggleItem(key)"
            >
              <i class="fas" :class="visibility[key] ? 'fa-minus' : 'fa-plus'"></i>
            </button>
            <span class="fw-bold">{{ item.label }}</span>
          </div>
          
          <div v-show="visibility[key]" class="card-body pt-0 pb-3 ps-5">
            <div v-if="item.type === 'amount'" class="d-flex align-items-center">
              <input type="number" class="form-control me-2" v-model="form[key]" style="width: 120px;"> 元
            </div>

            <div v-else-if="item.type === 'complex'" class="row g-2 align-items-center">
              <div class="col-auto d-flex align-items-center mb-2">
                <input type="number" class="form-control me-2" v-model="form[key]" style="width: 120px;"> 元
              </div>
              <div class="col-12 text-muted small">
                自
                <input type="number" class="form-control d-inline-block px-1 py-0 text-center mx-1" style="width:50px;height:25px" v-model="form[key+'Year']">年
                <input type="number" class="form-control d-inline-block px-1 py-0 text-center mx-1" style="width:40px;height:25px" v-model="form[key+'Month']">月
                <input type="number" class="form-control d-inline-block px-1 py-0 text-center mx-1" style="width:40px;height:25px" v-model="form[key+'Day']">日
                起支付至申请人退休日
              </div>
            </div>
          </div>
        </div>

        <div class="card mb-3 border-0 shadow-sm bg-warning bg-opacity-10">
          <div class="card-body py-2">
            <div class="row align-items-center">
              <label class="col-sm-4 col-form-label fw-bold text-dark">合计费用：</label>
              <div class="col-sm-8 d-flex align-items-center">
                <input type="number" class="form-control me-2" v-model="form.totalFees" style="width: 120px;"> 元
              </div>
            </div>
          </div>
        </div>

        <h4 class="section-title mt-5">详细事实与理由</h4>

        <div class="row mb-3">
          <label class="col-sm-3 col-form-label fw-bold">入职时间：</label>
          <div class="col-sm-9 d-flex">
            <input type="number" class="form-control me-2" v-model="form.hiredateYear" placeholder="年" style="width: 100px;">
            <input type="number" class="form-control me-2" v-model="form.hiredateMonth" placeholder="月" style="width: 80px;">
            <input type="number" class="form-control" v-model="form.hiredateDay" placeholder="日" style="width: 80px;">
          </div>
        </div>

        <div class="row mb-3">
          <label class="col-sm-3 col-form-label fw-bold">工作岗位：</label>
          <div class="col-sm-9">
            <input type="text" class="form-control" v-model="form.job">
          </div>
        </div>

        <div class="row mb-3">
          <label class="col-sm-3 col-form-label fw-bold">月工资标准：</label>
          <div class="col-sm-9 d-flex align-items-center">
            <input type="number" class="form-control me-2" v-model="form.monthlySalaryStandard" style="width: 120px;"> 元
          </div>
        </div>

        <div class="mb-3">
          <label class="form-label fw-bold">伤情认证：</label>
          <div class="p-3 bg-white border rounded">
            <div class="d-flex align-items-center mb-2 flex-wrap">
              <span>申请人于</span>
              <input type="number" class="form-control mx-1" style="width:60px" v-model="form.injuryCertYear">年
              <input type="number" class="form-control mx-1" style="width:50px" v-model="form.injuryCertMonth">月
              <input type="number" class="form-control mx-1" style="width:50px" v-model="form.injuryCertDay">日
              <span>受伤经过：</span>
              <input type="text" class="form-control mx-1" style="width:150px" v-model="form.certOrganization">
            </div>
            <div class="d-flex align-items-center mb-2 flex-wrap">
              <span>伤情诊断：</span>
              <input type="text" class="form-control mx-1" style="width:150px" v-model="form.injuryCondition">
            </div>
            <div class="d-flex align-items-center mb-2 flex-wrap">
              <span>后于</span>
              <input type="number" class="form-control mx-1" style="width:60px" v-model="form.govCertYear">年
              <input type="number" class="form-control mx-1" style="width:50px" v-model="form.govCertMonth">月
              <input type="number" class="form-control mx-1" style="width:50px" v-model="form.govCertDay">日
            </div>
            <div class="d-flex align-items-center flex-wrap">
              <span>经</span>
              <input type="text" class="form-control mx-1" style="width:80px" v-model="form.govCity">市
              <input type="text" class="form-control mx-1" style="width:80px" v-model="form.govRegion">
              <select class="form-select mx-1" style="width:70px" v-model="form.govRegionType">
                <option value="区">区</option>
                <option value="县">县</option>
              </select>
              <span>人社局认定为工伤，伤残等级：</span>
              <input type="number" class="form-control mx-1" style="width:60px" v-model="form.disabilityLevel">级
            </div>
          </div>
        </div>

        <div class="row mb-3">
          <label class="col-sm-3 col-form-label fw-bold">申请提交至：</label>
          <div class="col-sm-9 d-flex align-items-center">
            <input type="text" class="form-control me-2" v-model="form.appCity" style="width: 100px;">市
            <input type="text" class="form-control me-2" v-model="form.appRegion" style="width: 100px;">
            <select class="form-select me-2" v-model="form.appRegionType" style="width: 80px;">
              <option value="区">区</option>
              <option value="县">县</option>
            </select>
          </div>
        </div>

        <div class="text-center mt-5">
          <button type="submit" class="btn btn-primary btn-lg px-5" :disabled="isSubmitting">
            <span v-if="isSubmitting" class="spinner-border spinner-border-sm me-2"></span>
            {{ isSubmitting ? '生成中...' : '生成文档' }}
          </button>
        </div>

      </form>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue';
import axios from 'axios';
import QA from '@/components/QA.vue';

// 民族列表
const nations = ["汉族", "回族", "藏族", "苗族", "彝族", "壮族", "满族", "侗族", "瑶族", "白族", "土家族", "哈尼族", "哈萨克族", "傣族", "黎族", "傈僳族", "佤族", "畲族", "高山族", "拉祜族", "水族", "东乡族", "纳西族", "景颇族", "柯尔克孜族", "土族", "达斡尔族", "仫佬族", "羌族", "布朗族", "撒拉族", "毛南族", "仡佬族", "锡伯族", "阿昌族", "普米族", "朝鲜族", "塔吉克族", "怒族", "乌孜别克族", "俄罗斯族", "鄂温克族", "德昂族", "保安族", "裕固族", "京族", "塔塔尔族", "独龙族", "鄂伦春族", "赫哲族", "门巴族", "珞巴族", "基诺族"];

const isSubmitting = ref(false);

// 表单数据
const form = reactive({
  claimantName: '', claimantNationality: '', gender: '男', occupation: '',
  birthdayYear: '', birthdayMonth: '', birthdayDay: '',
  idNumber: '', registeredAddress: '', residenceAddress: '', claimantPhone: '',
  
  respondentCompany: '', respondentAddress: '', legalRepresentative: '', respondentPhone: '',
  
  medicalFees: '',
  // 可选项对应字段
  foodAllowanc: '', treatmentOuttown: '', workstoppageSalary: '', nursingFee: '',
  rehabilitationFee: '', onetimeDisability: '', onetimeWorkinjury: '', onetimeDisabilityemployment: '',
  
  // 复杂可选项
  monthlyDisabilityallowance: '', monthlyDisabilityallowanceYear: '', monthlyDisabilityallowanceMonth: '', monthlyDisabilityallowanceDay: '',
  monthlyLivingcare: '', monthlyLivingcareYear: '', monthlyLivingcareMonth: '', monthlyLivingcareDay: '',
  
  totalFees: '',
  
  hiredateYear: '', hiredateMonth: '', hiredateDay: '',
  job: '', monthlySalaryStandard: '',
  
  // 伤情认证
  injuryCertYear: '', injuryCertMonth: '', injuryCertDay: '',
  certOrganization: '', injuryCondition: '',
  govCertYear: '', govCertMonth: '', govCertDay: '',
  govCity: '', govRegion: '', govRegionType: '区',
  disabilityLevel: '',
  
  // 提交地
  appCity: '', appRegion: '', appRegionType: '区'
});

// 可选项目的配置 (用于 v-for 循环渲染)
const requestItems = {
  foodAllowanc: { label: '伙食补助费', type: 'amount' },
  treatmentOuttown: { label: '交通费和食宿费（外地治疗）', type: 'amount' },
  workstoppageSalary: { label: '停工留薪期工资', type: 'amount' },
  nursingFee: { label: '护理费用', type: 'amount' },
  rehabilitationFee: { label: '工伤康复费用', type: 'amount' },
  onetimeDisability: { label: '一次性伤残补助金', type: 'amount' },
  onetimeWorkinjury: { label: '一次性工伤医疗补助金', type: 'amount' },
  onetimeDisabilityemployment: { label: '一次性伤残就业补助金', type: 'amount' },
  monthlyDisabilityallowance: { label: '每月伤残津贴', type: 'complex' },
  monthlyLivingcare: { label: '每月生活护理费', type: 'complex' }
};

// 控制显示/隐藏的状态对象
const visibility = reactive({});
// 初始化所有可选项为隐藏 (false)
Object.keys(requestItems).forEach(key => visibility[key] = false);

// 切换显示状态
const toggleItem = (key) => {
  visibility[key] = !visibility[key];
  if (!visibility[key]) {
    // 如果是隐藏，清空对应的数据
    form[key] = '';
    // 如果是复杂项，清空日期字段
    if (requestItems[key].type === 'complex') {
      form[key + 'Year'] = '';
      form[key + 'Month'] = '';
      form[key + 'Day'] = '';
    }
  }
};

const submitForm = async () => {
  isSubmitting.value = true;
  try {
    const response = await axios.post('http://127.0.0.1:8000/api/wia/generate', form, {
      responseType: 'blob'
    });

    const url = window.URL.createObjectURL(new Blob([response.data]));
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', '工伤仲裁申请书.docx');
    document.body.appendChild(link);
    link.click();
  } catch (error) {
    console.error('Submission failed', error);
    alert('生成失败，请检查填写内容');
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
.btn-icon {
  width: 24px;
  height: 24px;
  padding: 0;
  border-radius: 50%;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}
.fs-7 { font-size: 0.85rem; }
</style>