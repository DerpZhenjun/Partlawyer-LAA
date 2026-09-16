Page({
  data: { input: '', loading: false, messages: [{ role: 'ai', content: '你好，我可以帮你梳理请求事项、关键证据、仲裁时效和下一步行动。请先简单描述发生了什么。' }], prompts: ['公司口头辞退怎么办？', '仲裁需要哪些证据？', '赔偿金怎么计算？'] },
  onInput(e) { this.setData({ input: e.detail.value }) }, usePrompt(e) { this.setData({ input: e.currentTarget.dataset.text }) },
  send() {
    const text = this.data.input.trim(); if (!text || this.data.loading) return
    const messages = [...this.data.messages, { role: 'user', content: text }]; this.setData({ messages, input: '', loading: true })
    const history = messages.slice(-12).map(item => ({ role: item.role === 'ai' ? 'assistant' : 'user', content: item.content }))
    wx.request({ url: `${getApp().globalData.apiBase}/api/ask`, method: 'POST', data: { question: text, history }, timeout: 60000,
      success: res => this.setData({ messages: [...messages, { role: 'ai', content: typeof res.data === 'string' ? res.data : '已收到，请继续补充关键事实。' }] }),
      fail: () => this.setData({ messages: [...messages, { role: 'ai', content: '当前无法连接模型服务。你仍可继续查看办理指南和准备文书。' }] }),
      complete: () => this.setData({ loading: false })
    })
  }
})
