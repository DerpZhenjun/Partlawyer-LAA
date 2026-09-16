<template>
  <RouterLink
    :to="`/province/${province.slug}`"
    class="province-card"
    :class="[`state-${province.status}`, { featured }]"
    :style="cardTheme"
  >
    <div class="card-topline">
      <span class="region-label"><i :class="topLabel.icon"></i>{{ topLabel.text }}</span>
      <span class="status-label">
        <i :class="province.status === 'ready' ? 'fa-solid fa-circle-check' : province.status === 'guide' ? 'fa-solid fa-landmark' : 'fa-regular fa-clock'"></i>
        {{ statusText }}
      </span>
    </div>

    <div class="province-title-row">
      <span class="province-icon"><i :class="visual.icon"></i></span>
      <div>
        <h3>{{ province.name }}</h3>
        <p>{{ description }}</p>
      </div>
    </div>

    <div class="service-list" aria-label="可用服务">
      <template v-if="province.status === 'ready'">
        <span><i class="fa-regular fa-file-lines"></i>仲裁申请书</span>
        <span><i class="fa-solid fa-list-check"></i>证据清单</span>
      </template>
      <template v-else-if="province.status === 'guide'">
        <span><i class="fa-solid fa-building-columns"></i>官方入口</span>
        <span><i class="fa-solid fa-route"></i>办理流程</span>
      </template>
      <template v-else>
        <span><i class="fa-solid fa-circle-info"></i>全国办事入口</span>
      </template>
    </div>

    <div class="card-action">
      <span>进入{{ province.shortName }}办理</span>
      <i class="fa-solid fa-arrow-right"></i>
    </div>
    <span class="province-watermark" aria-hidden="true">{{ province.shortName.slice(0, 1) }}</span>
  </RouterLink>
</template>

<script setup>
import { computed } from 'vue'
import { RouterLink } from 'vue-router'

const props = defineProps({ province: { type: Object, required: true }, featured: Boolean })

const visuals = {
  zhejiang: { icon: 'fa-solid fa-water', accent: '#0b7a72', soft: '#e5f5f2' },
  guangdong: { icon: 'fa-solid fa-sun', accent: '#b96424', soft: '#fff0df' },
  jiangsu: { icon: 'fa-solid fa-landmark-dome', accent: '#356789', soft: '#e8f1f7' },
  liaoning: { icon: 'fa-solid fa-industry', accent: '#526a82', soft: '#edf1f5' },
  fujian: { icon: 'fa-solid fa-mountain-sun', accent: '#33735d', soft: '#e9f3ee' },
}
const visual = computed(() => visuals[props.province.slug] || { icon: 'fa-solid fa-location-dot', accent: '#557083', soft: '#eef3f5' })
const cardTheme = computed(() => ({ '--card-accent': visual.value.accent, '--card-soft': visual.value.soft }))
const topLabel = computed(() => props.province.status === 'ready'
  ? { icon: 'fa-regular fa-file-lines', text: '本省专用模板' }
  : props.province.status === 'guide'
    ? { icon: 'fa-solid fa-building-columns', text: '官方办事信息' }
    : { icon: 'fa-solid fa-location-dot', text: '省份办事入口' })
const statusText = computed(() => props.province.status === 'ready' ? '可以生成文书' : props.province.status === 'guide' ? '可查看办理指南' : '文书正在准备')
const description = computed(() => props.province.status === 'ready' ? '在线填写并生成当地仲裁材料' : props.province.status === 'guide' ? '查看当地官方申请入口和材料要求' : '先查看通用流程和全国办理入口')
</script>

<style scoped>
.province-card{position:relative;min-width:0;min-height:208px;padding:22px 22px 0;display:flex;flex-direction:column;overflow:hidden;border:1px solid #dfe7ea;border-radius:18px;background:linear-gradient(145deg,#fff 50%,var(--card-soft));box-shadow:0 8px 28px rgba(28,54,70,.055);transition:transform .22s ease,border-color .22s ease,box-shadow .22s ease}.province-card:before{content:'';position:absolute;inset:0 auto 0 0;width:4px;background:var(--card-accent);opacity:.86}.province-card:hover{transform:translateY(-4px);border-color:color-mix(in srgb,var(--card-accent) 32%,#dfe7ea);box-shadow:0 18px 42px rgba(25,52,68,.12)}.province-card:focus-visible{outline:3px solid color-mix(in srgb,var(--card-accent) 30%,transparent);outline-offset:3px}.card-topline{position:relative;z-index:1;display:flex;align-items:center;justify-content:space-between;gap:12px}.region-label,.status-label{display:inline-flex;align-items:center;gap:6px;font-size:12px;font-weight:650}.region-label{color:#6f7f8e}.region-label i{color:var(--card-accent)}.status-label{padding:6px 9px;border-radius:999px;color:var(--card-accent);background:color-mix(in srgb,var(--card-soft) 82%,#fff);white-space:nowrap}.state-pending .status-label{color:#71808d;background:#f0f3f5}.province-title-row{position:relative;z-index:1;margin-top:20px;display:flex;align-items:center;gap:14px}.province-icon{width:50px;height:50px;flex:0 0 50px;display:grid;place-items:center;border:1px solid color-mix(in srgb,var(--card-accent) 14%,transparent);border-radius:15px;color:var(--card-accent);background:var(--card-soft);font-size:20px;box-shadow:inset 0 1px rgba(255,255,255,.8)}h3{margin:0;color:#17324a;font-size:22px;line-height:1.25;letter-spacing:-.025em}p{margin:5px 0 0;color:#6e7e8c;font-size:13px;line-height:1.5}.service-list{position:relative;z-index:1;margin:18px 0 20px;display:flex;gap:8px;flex-wrap:wrap}.service-list span{padding:7px 10px;display:inline-flex;align-items:center;gap:6px;border:1px solid rgba(113,135,148,.13);border-radius:8px;color:#536778;background:rgba(255,255,255,.72);font-size:12px}.service-list i{color:var(--card-accent)}.card-action{position:relative;z-index:1;margin-top:auto;height:49px;display:flex;align-items:center;justify-content:space-between;border-top:1px solid rgba(115,135,145,.16);color:#2c4b5f;font-size:13px;font-weight:700}.card-action i{width:28px;height:28px;display:grid;place-items:center;border-radius:50%;color:#fff;background:var(--card-accent);font-size:11px;transition:transform .2s ease}.province-card:hover .card-action i{transform:translateX(3px)}.province-watermark{position:absolute;right:-8px;bottom:-42px;color:var(--card-accent);font-family:serif;font-size:132px;font-weight:900;line-height:1;opacity:.035;pointer-events:none}.state-ready{border-color:color-mix(in srgb,var(--card-accent) 17%,#dfe7ea)}
@media(max-width:620px){.province-card{min-height:196px;padding:19px 18px 0}.status-label{font-size:11px}.province-title-row{margin-top:17px}.province-icon{width:46px;height:46px;flex-basis:46px}h3{font-size:20px}.service-list{margin:15px 0}.card-action{height:46px}}
</style>
