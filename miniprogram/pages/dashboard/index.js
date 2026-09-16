const featured = [
  { slug: 'zhejiang', mark: '浙', name: '浙江省', meta: '申请书 · 证据清单', ready: true },
  { slug: 'guangdong', mark: '粤', name: '广东省', meta: '申请书 · 证据清单', ready: true },
  { slug: 'jiangsu', mark: '苏', name: '江苏省', meta: '官方申请入口与流程', ready: false },
  { slug: 'liaoning', mark: '辽', name: '辽宁省', meta: '材料与办理时限', ready: false },
  { slug: 'fujian', mark: '闽', name: '福建省', meta: '网上预申请指南', ready: false }
]

const names = [
  ['beijing','北京'],['tianjin','天津'],['hebei','河北'],['shanxi','山西'],['neimenggu','内蒙古'],
  ['jilin','吉林'],['heilongjiang','黑龙江'],['shanghai','上海'],['anhui','安徽'],['jiangxi','江西'],
  ['shandong','山东'],['henan','河南'],['hubei','湖北'],['hunan','湖南'],['guangxi','广西'],
  ['hainan','海南'],['chongqing','重庆'],['sichuan','四川'],['guizhou','贵州'],['yunnan','云南'],
  ['xizang','西藏'],['shaanxi','陕西'],['gansu','甘肃'],['qinghai','青海'],['ningxia','宁夏'],['xinjiang','新疆']
]

Page({
  data: { featured, others: names.map(([slug, name]) => ({ slug, name })) },
  openProvince(event) {
    wx.navigateTo({ url: `/pages/province/index?slug=${event.currentTarget.dataset.slug}` })
  }
})
