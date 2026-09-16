# LabourLawyer

面向普通劳动者的劳动仲裁文书与办事助手。

LabourLawyer 按省份提供劳动人事争议仲裁申请书、证据清单和官方办理指南。用户无需理解复杂法律术语，只需选择办理地区、按照提示填写事实和诉求，即可生成对应地区格式的 Word 文书，并前往当地政务平台提交申请。

> 本项目提供文书和办事信息辅助，不替代执业律师的正式法律意见。办理材料、受理条件和提交方式以当地劳动人事争议仲裁委员会的最新要求为准。

## 核心流程

1. 选择实际工作地或用人单位所在地。
2. 选择生成仲裁申请书或证据清单。
3. 按通俗提示填写当事人信息、仲裁请求和证据。
4. 确认内容并下载 Word 文书。
5. 查看当地办理指南，前往官方政务平台申请。

## 当前能力

- 全国 31 个省级地区入口与搜索。
- 浙江、广东官方格式的仲裁申请书和证据清单生成。
- 浙江、广东、江苏、辽宁、福建官方办理入口与流程说明。
- 表单草稿自动保存、必填项提示和生成前确认。
- 空白表单也可直接下载官方模板。
- AI 劳动法律顾问，支持本地 Ollama 模型和多轮对话。
- 法律数字人入口。
- 群众服务首页与管理后台分离。
- Web、Android、微信小程序及可选桌面客户端工程。

未完成专用模板适配的地区会明确显示“适配中”，不会套用其他省份模板。

## 项目结构

```text
backend/          FastAPI 接口、文书生成和管理平台数据
frontend/         Vue 3 群众服务网页与管理后台
llm_service/      独立的本地大模型问答服务逻辑
templates_docx/   按省份分类的官方 Word 模板
mobile/           Capacitor Android 应用
miniprogram/      微信小程序
desktop/          可选 Electron 桌面客户端
ChatVRM/          法律数字人页面
scripts/          启动、停止和手机安装脚本
```

## 快速启动

### Windows 一键启动

双击根目录的 `start-web.bat`。首次运行会自动准备依赖，随后启动：

- 群众服务网页：`http://127.0.0.1:5173`
- 后端接口：`http://127.0.0.1:8000`
- API 文档：`http://127.0.0.1:8000/docs`
- 法律数字人：`http://127.0.0.1:3000`

停止全部本地服务时双击 `stop-web.bat`。日志保存在 `.runtime/`。

更完整的网页、Android 和微信小程序操作步骤见 [启动与使用说明](./启动与使用说明.md)。

### Android USB 安装

1. 手机开启开发者选项和 USB 调试，并允许当前电脑调试。
2. 保持 `start-web.bat` 启动的服务运行。
3. 双击 `install-mobile.bat`。

脚本会构建最新网页资源、生成 APK、设置 USB 端口转发、安装并打开应用。生成的调试 APK 位于 `mobile/android/app/build/outputs/apk/debug/app-debug.apk`。

### 微信小程序

使用微信开发者工具导入 `miniprogram/`。发布前需要配置正式 AppID、HTTPS API 地址及微信公众平台的 `request` 合法域名。

## 文书模板

模板统一放在仓库根目录：

```text
templates_docx/
├─ ZheJiangSheng/
└─ GuangDongSheng/
```

浙江使用带书名号的官方申请书和证据清单文件；广东使用 `仲裁申请书.docx` 和 `证据清单.docx`。如需使用其他模板目录，可设置 `LABOURLAWYER_TEMPLATE_DIR`。

## AI 法律顾问

AI 默认连接本机 Ollama。推荐安装兼顾响应速度和本地资源占用的模型：

```powershell
ollama pull qwen3.5:4b
ollama serve
```

可通过 `backend/.env` 调整：

```dotenv
OLLAMA_API_BASE=http://127.0.0.1:11434
LABOURLAWYER_LLM_MODEL=ollama/qwen3.5:4b
LABOURLAWYER_LLM_REASONING=none
LABOURLAWYER_LLM_MAX_TOKENS=1200
```

模型回答仅用于信息梳理。涉及仲裁请求、金额、时效和重要程序选择时，应结合原始材料并向当地仲裁委员会、12333 或执业律师核实。

## 开发与验证

后端文书测试：

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s backend/tests -v
```

前端生产构建：

```powershell
npm run build --prefix frontend
```

Android 同步与构建：

```powershell
npm run sync --prefix mobile
cd mobile/android
.\gradlew.bat assembleDebug
```

## 官方办理入口

- [国家 12333 公共服务平台](https://www.12333.gov.cn/)
- [浙江政务服务网·劳动人事争议仲裁申请](https://www.zjzwfw.gov.cn/zjservice-fe/#/workguide?localInnerCode=2510b7af-2402-4502-837c-14eb4a71177d)
- [广东政务服务网·劳动人事争议仲裁申请](https://www.gdzwfw.gov.cn/portal/v3/guide/11440000553612461J244211105N00302)
- [江苏政务服务劳动争议专题](https://www.jszwfw.gov.cn/col/col172703/index.html)
- [辽宁政务服务劳动人事争议仲裁申请](https://center.lnzwfw.gov.cn/api/web/matter/getContent?id=65dbb98b-35ef-47a5-b7ff-1a4f5c914e11)
- [福建省人社厅劳动仲裁办事指南](https://www.fujian.gov.cn/nrrh/srst/202509/t20250910_7003551.htm)

## 上线前检查

- 使用 HTTPS 并将跨域来源限制为正式域名。
- 为身份证号、电话、住址和证据文件提供加密、删除和备份机制。
- 接入身份认证、权限控制、租户隔离和审计日志。
- 定期核验各地区模板、办理链接、材料要求和更新时间。
- 使用正式 Android 签名生成 release APK/AAB。
- 完成隐私政策、用户协议、数据处理说明及必要的合规评估。

## License

[MIT](./LICENSE)
