Page({
  data: { cases: [], query: '', showCreate: false, form: { title: '', client: '', employer: '' } },
  onShow() { this.setData({ cases: getApp().globalData.cases }) },
  onSearch(e) { this.setData({ query: e.detail.value }) },
  openCreate() { this.setData({ showCreate: true }) }, closeCreate() { this.setData({ showCreate: false }) },
  field(e) { this.setData({ [`form.${e.currentTarget.dataset.key}`]: e.detail.value }) },
  createCase() {
    const form = this.data.form
    if (!form.title || !form.client || !form.employer) return wx.showToast({ title: '请完整填写', icon: 'none' })
    const cases = [{ id: `PL-2026-${String(Date.now()).slice(-3)}`, title: form.title, client: form.client, employer: form.employer, stage: '案情梳理', deadline: '待计算', progress: 0 }, ...getApp().globalData.cases]
    getApp().globalData.cases = cases; wx.setStorageSync('labourlawyer_cases', cases); this.setData({ cases, showCreate: false, form: { title: '', client: '', employer: '' } }); wx.showToast({ title: '案件已创建' })
  }
})
