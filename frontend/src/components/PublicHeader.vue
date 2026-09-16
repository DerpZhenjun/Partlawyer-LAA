<template>
  <header class="public-header">
    <div class="header-inner">
      <RouterLink to="/" class="public-brand" aria-label="LabourLawyer 首页">
        <span>法</span><div><strong>LabourLawyer</strong><small>劳动仲裁文书助手</small></div>
      </RouterLink>
      <nav aria-label="网站导航">
        <RouterLink to="/">选择省份</RouterLink>
        <a href="/#process">申请流程</a>
        <a href="/#faq">常见问题</a>
      </nav>
      <RouterLink to="/admin" class="admin-entry"><i class="fa-regular fa-user"></i> 管理后台</RouterLink>
    </div>
  </header>
</template>
<script setup>import { RouterLink } from 'vue-router'</script>
<style scoped>
.public-header{position:sticky;top:0;z-index:40;border-bottom:1px solid #e5e9ee;background:rgba(255,255,255,.96);backdrop-filter:blur(15px)}.header-inner{max-width:1180px;height:72px;margin:auto;padding:0 24px;display:flex;align-items:center}.public-brand{display:flex;align-items:center;gap:11px}.public-brand>span{width:38px;height:38px;display:grid;place-items:center;border-radius:10px;color:#fff;background:#16665f;font:700 20px serif}.public-brand strong,.public-brand small{display:block}.public-brand strong{color:#17324b;font-size:17px}.public-brand small{margin-top:1px;color:#7c8996;font-size:11px}.public-header nav{display:flex;gap:34px;margin-left:auto}.public-header nav a{color:#49586a;font-size:14px}.public-header nav a:hover{color:#0f766e}.admin-entry{margin-left:34px;padding:9px 13px;border:1px solid #dce3e8;border-radius:8px;color:#667587;font-size:12px}.admin-entry i{margin-right:5px}@media(max-width:700px){.header-inner{height:62px;padding:0 16px}.public-header nav{display:none}.admin-entry{margin-left:auto;padding:8px;font-size:0}.admin-entry i{margin:0;font-size:14px}.public-brand small{display:none}}
</style>
