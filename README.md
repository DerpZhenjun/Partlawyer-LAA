<p align="center">
  <img src="./ChatVRM/public/logo.png" alt="PartLawyer Logo" width="400">
</p>

<h1 align="center">PartLawyer-Labor Arbitration Assistant</h1>

<p align="center">
  <strong>劳动仲裁文书生成——辅助平台</strong>
</p>

<p align="center">
  <a href="https://github.com/pixiv/ChatVRM">
    <img src="https://img.shields.io/badge/Digital%20Human-ChatVRM-FF4081?style=flat&logo=pixiv" alt="ChatVRM">
  </a>
  <a href="https://github.com/RVC-Boss/GPT-SoVITS">
    <img src="https://img.shields.io/badge/Voice%20Cloning-GPT--SoVITS-FF5722?style=flat&logo=github" alt="GPT-SoVITS">
  </a>
  <a href="https://hub.vroid.com/en/characters/6317386427492305874/models/6271821272125919618">
    <img src="https://img.shields.io/badge/3D%20Model-VRoid%20Hub-00B0FF?style=flat&logo=vroid" alt="VRM Model">
  </a>
  <a href="https://www.ai-hobbyist.com/thread-938-1-1.html">
    <img src="https://img.shields.io/badge/TTS%20Weights-AI%20Hobbyist-9E9E9E?style=flat" alt="TTS Weights">
  </a>
  <img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="license">
</p>

---

## 📖 项目简介

**PartLawyer** 是一款针对劳动仲裁场景设计的智能化辅助平台。项目通过微调的 **DeepSeek-Qwen** 大模型提供专业的法律逻辑支持，并集成 **ChatVRM** 3D数字人交互与 **GPT-SoVITS** 语音克隆技术，为非法律专业用户提供直观、温馨的法律咨询与文书生成体验。

## 📺 演示视频

*(此处可粘贴你的 Bilibili 演示视频链接)*

## 📖 部署流程

```bash
# 克隆仓库
git clone [https://github.com/你的用户名/Partlawyer-LAA.git](https://github.com/你的用户名/Partlawyer-LAA.git)
cd Partlawyer-LAA

# 创建并激活虚拟环境
conda create -n pl python=3.10 -y
conda activate pl
