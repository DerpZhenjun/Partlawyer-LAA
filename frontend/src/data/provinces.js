const nationalPortal = 'https://www.12333.gov.cn/'

export const provinces = [
  { slug: 'zhejiang', name: '浙江省', shortName: '浙江', region: '华东', status: 'ready', officialUrl: 'https://www.zjzwfw.gov.cn/zjservice-fe/#/workguide?localInnerCode=2510b7af-2402-4502-837c-14eb4a71177d', officialName: '浙江政务服务网', searchKeyword: '劳动人事争议仲裁申请', applicationRoute: '/documents/zhejiang/application', evidenceRoute: '/documents/zhejiang/evidence', note: '支持网上申请，官方页面显示现场办理 0 次、承诺 44 个工作日办结。' },
  { slug: 'guangdong', name: '广东省', shortName: '广东', region: '华南', status: 'ready', officialUrl: 'https://www.gdzwfw.gov.cn/portal/v3/guide/11440000553612461J244211105N00302', officialName: '广东政务服务网', searchKeyword: '劳动人事争议仲裁申请', applicationRoute: '/documents/guangdong/application', evidenceRoute: '/documents/guangdong/evidence', note: '支持网上和窗口办理，官方承诺 5 个工作日内决定是否受理。这个链接对应省级仲裁院，提交前请先确认应由哪个仲裁委员会受理。' },
  { slug: 'jiangsu', name: '江苏省', shortName: '江苏', region: '华东', status: 'guide', officialUrl: 'https://www.jszwfw.gov.cn/col/col172703/index.html', officialName: '江苏政务服务·劳动争议', searchKeyword: '劳动人事争议仲裁申请', note: '官方专题提供仲裁委员会查询、仲裁申请等服务。' },
  { slug: 'liaoning', name: '辽宁省', shortName: '辽宁', region: '东北', status: 'guide', officialUrl: 'https://center.lnzwfw.gov.cn/api/web/matter/getContent?id=65dbb98b-35ef-47a5-b7ff-1a4f5c914e11', officialName: '辽宁省政务服务网', searchKeyword: '劳动人事争议仲裁申请', note: '官方指南列明申请条件、材料、办理流程与受理时限。' },
  { slug: 'fujian', name: '福建省', shortName: '福建', region: '华东', status: 'guide', officialUrl: 'https://www.fujian.gov.cn/nrrh/srst/202509/t20250910_7003551.htm', officialName: '福建省人民政府·劳动人事争议仲裁', searchKeyword: '劳动人事争议仲裁申请', note: '可通过福建人社、闽政通或福建省网上办事大厅预申请。' },
  { slug: 'beijing', name: '北京市', shortName: '北京', region: '华北' },
  { slug: 'tianjin', name: '天津市', shortName: '天津', region: '华北' },
  { slug: 'hebei', name: '河北省', shortName: '河北', region: '华北' },
  { slug: 'shanxi', name: '山西省', shortName: '山西', region: '华北' },
  { slug: 'neimenggu', name: '内蒙古自治区', shortName: '内蒙古', region: '华北' },
  { slug: 'jilin', name: '吉林省', shortName: '吉林', region: '东北' },
  { slug: 'heilongjiang', name: '黑龙江省', shortName: '黑龙江', region: '东北' },
  { slug: 'shanghai', name: '上海市', shortName: '上海', region: '华东' },
  { slug: 'anhui', name: '安徽省', shortName: '安徽', region: '华东' },
  { slug: 'jiangxi', name: '江西省', shortName: '江西', region: '华东' },
  { slug: 'shandong', name: '山东省', shortName: '山东', region: '华东' },
  { slug: 'henan', name: '河南省', shortName: '河南', region: '华中' },
  { slug: 'hubei', name: '湖北省', shortName: '湖北', region: '华中' },
  { slug: 'hunan', name: '湖南省', shortName: '湖南', region: '华中' },
  { slug: 'guangxi', name: '广西壮族自治区', shortName: '广西', region: '华南' },
  { slug: 'hainan', name: '海南省', shortName: '海南', region: '华南' },
  { slug: 'chongqing', name: '重庆市', shortName: '重庆', region: '西南' },
  { slug: 'sichuan', name: '四川省', shortName: '四川', region: '西南' },
  { slug: 'guizhou', name: '贵州省', shortName: '贵州', region: '西南' },
  { slug: 'yunnan', name: '云南省', shortName: '云南', region: '西南' },
  { slug: 'xizang', name: '西藏自治区', shortName: '西藏', region: '西南' },
  { slug: 'shaanxi', name: '陕西省', shortName: '陕西', region: '西北' },
  { slug: 'gansu', name: '甘肃省', shortName: '甘肃', region: '西北' },
  { slug: 'qinghai', name: '青海省', shortName: '青海', region: '西北' },
  { slug: 'ningxia', name: '宁夏回族自治区', shortName: '宁夏', region: '西北' },
  { slug: 'xinjiang', name: '新疆维吾尔自治区', shortName: '新疆', region: '西北' },
].map(item => ({
  status: 'pending',
  officialUrl: nationalPortal,
  officialName: '全国人社政务服务平台',
  searchKeyword: '劳动人事争议仲裁申请',
  note: '本省专用模板正在核对，可先查看全国办事入口。',
  ...item,
}))

export const provinceGroups = ['华东', '华南', '华北', '华中', '东北', '西南', '西北']

export const commonMaterials = [
  '仲裁申请书：本人签字，并按被申请人人数准备副本',
  '身份证明：身份证复印件；委托办理还需授权委托书',
  '劳动关系证明：劳动合同、工资流水、社保记录、工牌等',
  '支持仲裁请求的证据，并附上按顺序整理的证据清单',
  '用人单位主体信息：企业名称、统一社会信用代码和注册地址',
]

export const commonProcess = [
  { title: '确认管辖', text: '一般向实际工作地或用人单位所在地的劳动人事争议仲裁委员会申请。' },
  { title: '准备材料', text: '填写仲裁申请书，整理身份证明、劳动关系证明、证据和证据清单。' },
  { title: '线上或现场申请', text: '通过当地政务服务网提交，或前往有管辖权的仲裁委员会窗口办理。' },
  { title: '等待受理', text: '仲裁委员会收到申请后依法审查；材料不完整的，会通知一次性补正。' },
  { title: '调解或开庭', text: '受理后可能先行调解；未达成调解的，依法安排开庭并作出裁决。' },
]

export const findProvince = slug => provinces.find(item => item.slug === slug)
