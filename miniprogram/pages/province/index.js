const national = { portal: '国家 12333 公共服务平台', url: 'https://www.12333.gov.cn/', search: '劳动人事争议调解仲裁' }
const provinces = {
  zhejiang: { name: '浙江省', short: '浙江', ready: true, official: true, portal: '浙江政务服务网', url: 'https://www.zjzwfw.gov.cn/zjservice-fe/#/workguide?localInnerCode=2510b7af-2402-4502-837c-14eb4a71177d', search: '劳动人事争议仲裁申请', note: '支持网上申请，官方页面显示现场办理 0 次、承诺 44 个工作日办结。' },
  guangdong: { name: '广东省', short: '广东', ready: true, guangdong: true, portal: '广东政务服务网', url: 'https://www.gdzwfw.gov.cn/portal/v3/guide/11440000553612461J244211105N00302', search: '劳动人事争议仲裁申请', note: '支持网上和窗口办理，5 个工作日内决定是否受理。省级页面有特定受理范围，提交前请先确认仲裁委员会。' },
  jiangsu: { name: '江苏省', short: '江苏', ready: false, portal: '江苏政务服务劳动争议专题', url: 'https://www.jszwfw.gov.cn/col/col172703/index.html', search: '劳动人事争议仲裁申请', note: '专题页提供仲裁委员会查询和仲裁申请入口。' },
  liaoning: { name: '辽宁省', short: '辽宁', ready: false, portal: '辽宁政务服务网', url: 'https://center.lnzwfw.gov.cn/api/web/matter/getContent?id=65dbb98b-35ef-47a5-b7ff-1a4f5c914e11', search: '劳动人事争议仲裁申请', note: '官方事项列明受理条件、材料和办理时限。' },
  fujian: { name: '福建省', short: '福建', ready: false, portal: '福建省人社厅办事指南', url: 'https://www.fujian.gov.cn/nrrh/srst/202509/t20250910_7003551.htm', search: '劳动仲裁预申请', note: '可通过福建人社微信、网上办事大厅或闽政通进行预申请。' }
}
const names = { beijing:'北京市',tianjin:'天津市',hebei:'河北省',shanxi:'山西省',neimenggu:'内蒙古自治区',jilin:'吉林省',heilongjiang:'黑龙江省',shanghai:'上海市',anhui:'安徽省',jiangxi:'江西省',shandong:'山东省',henan:'河南省',hubei:'湖北省',hunan:'湖南省',guangxi:'广西壮族自治区',hainan:'海南省',chongqing:'重庆市',sichuan:'四川省',guizhou:'贵州省',yunnan:'云南省',xizang:'西藏自治区',shaanxi:'陕西省',gansu:'甘肃省',qinghai:'青海省',ningxia:'宁夏回族自治区',xinjiang:'新疆维吾尔自治区' }

Page({
  data: {
    province: {}, mode: 'application', generated: '',
    form: { applicant: '', respondent: '', requests: '', facts: '', evidence: '' },
    process: ['确认管辖地区', '准备申请书和证据', '在线或窗口提交', '等待受理并按通知参加调解或庭审'],
    materials: ['申请人身份证明', '用人单位主体信息', '仲裁申请书及副本', '劳动关系证明', '按编号整理的证据及证据清单']
  },
  onLoad(options) {
    const base = provinces[options.slug] || { name: names[options.slug] || '其他地区', short: names[options.slug] || '当地', ready: false, ...national, note: '专用文书模板正在核对，请先通过官方平台查询当地要求。' }
    const zhejiangProcess = ['到仲裁委员会、邮寄或通过“浙里办”智慧仲裁提交', '仲裁委员会在 5 个工作日内决定是否受理并通知', '按通知参加调解或开庭，并接收办理文书']
    const zhejiangMaterials = ['用人单位登记注册材料', '劳动者身份证', '《劳动人事争议仲裁申请书》', '《证据清单》', '能说明劳动关系和支持请求的证据']
    const guangdongProcess = ['先确认实际工作地或公司所在地的仲裁委员会', '准备并网上或窗口提交申请书、证据和身份证明', '5 个工作日内等待是否受理的通知', '按通知参加调解或开庭']
    const guangdongMaterials = ['本人签名的仲裁申请书', '证据材料和证据清单（官方页面标注 2 份）', '身份证复印件并带原件核对', '公司登记资料', '委托办理时另备授权材料']
    const localGuide = base.official ? { process: zhejiangProcess, materials: zhejiangMaterials } : base.guangdong ? { process: guangdongProcess, materials: guangdongMaterials } : {}
    this.setData({ province: base, ...localGuide })
    wx.setNavigationBarTitle({ title: `${base.short}劳动仲裁` })
  },
  setMode(event) { this.setData({ mode: event.currentTarget.dataset.mode, generated: '' }) },
  updateField(event) { this.setData({ [`form.${event.currentTarget.dataset.field}`]: event.detail.value }) },
  generate() {
    const { province, mode, form } = this.data
    if (mode === 'application' && (!form.applicant.trim() || !form.respondent.trim())) {
      wx.showToast({ title: '请填写申请人和被申请人', icon: 'none' }); return
    }
    let generated
    if (mode === 'application') {
      generated = `劳动人事争议仲裁申请书\n\n申请人：${form.applicant}\n被申请人：${form.respondent}\n\n仲裁请求：\n${form.requests || '请补充具体仲裁请求'}\n\n事实和理由：\n${form.facts || '请补充事实经过和理由'}\n\n此致\n${province.short}有管辖权的劳动人事争议仲裁委员会\n\n申请人：${form.applicant}\n日期：____年__月__日`
    } else {
      const lines = form.evidence.split('\n').map(item => item.trim()).filter(Boolean)
      generated = `证据清单\n\n申请人：${form.applicant || '________'}\n被申请人：${form.respondent || '________'}\n\n${lines.length ? lines.map((line, index) => `${index + 1}. ${line}`).join('\n') : '1. 请按“证据名称｜来源｜证明目的”逐行补充'}\n\n提交人：${form.applicant || '________'}\n日期：____年__月__日`
    }
    this.setData({ generated })
  },
  copyGenerated() { wx.setClipboardData({ data: this.data.generated }) },
  copyPortal() { wx.setClipboardData({ data: this.data.province.url, success: () => wx.showToast({ title: '官方链接已复制' }) }) }
})
