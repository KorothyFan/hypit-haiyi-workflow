# 新机器安装与迁移

适用：在另一台电脑或新的Codex任务中开始制作，不要求搬历史作品、库存、统计表或云机账号。先将当前Release源码ZIP解压到任意可写目录，用终端进入解压后的 `hypit-haiyi-workflow`；不要直接在ZIP内运行。路径可有中文、空格，不要求特定盘符或用户名。

## 按实际路径安装依赖

| 路径 | 需要准备 | 执行入口及边界 |
| --- | --- | --- |
| 文字策划／方法交接 | Codex能读取技能或文档；用Node安装器时需要Node ≥22.15 | `node scripts/workflow.mjs install-skill --director-only`，无需海艺或Hypit |
| 本地记录／迁移检查 | Python ≥3.11；迁移脚本只用标准库，Windows缺IANA时区时 `python -m pip install tzdata` | `python -X utf8 scripts/migration.py --help`；记录核心为 `scripts/koroflow.py`，都不是生成器 |
| 直接海艺技能 | 从可信来源另装 `haiyi-aigc`；按它当前SKILL核对Python及依赖，现有入口需requests；媒体处理需FFmpeg/FFprobe | 该技能的 `scripts/generate.py`；源码ZIP不含海艺原技能或登录程序，不依赖旧机器的批次脚本 |
| 海艺＋Hypit Provider | Node ≥22.15、Git、pnpm 10.33.0、FFmpeg/FFprobe、upstream.json固定的Hypit及其依赖 | 本仓库 `scripts/workflow.mjs`，图片/视频能力按Provider实际覆盖；其他海艺操作仍由原技能提供 |

Python图像检查可按需要安装Pillow；OpenCV、yt-dlp、rg等是采样／取片／检索辅助，非所有路径的强依赖。不要动态导入旧电脑的单批脚本或依赖历史工程才能做新片。

PowerShell先发现本机命令：

```powershell
Get-Command python,node,git,ffmpeg,ffprobe -ErrorAction SilentlyContinue
python --version
node --version
```

若 `python` 是Store别名，选实际Python解释器；路径含空格时用 `& "<解释器完整路径>"` 调用。macOS/Linux按实际 `python3` 与命令发现工具替换。不要复制旧电脑的缓存运行时路径。

## 安装技能及配置实际执行器

只装统筹技能可运行 `node scripts/workflow.mjs install-skill --core-only`，不需先setup。只装导演同理。完整Hypit路线：

```text
npm install -g pnpm@10.33.0
node scripts/workflow.mjs setup --install --ffmpeg "<本机ffmpeg路径>" --ffprobe "<本机ffprobe路径>"
node scripts/workflow.mjs install-skill
node scripts/workflow.mjs info
node scripts/workflow.mjs verify
```

已有固定版本Hypit时，改用 `setup --hypit-root "<本机Hypit目录>"`；完整选项与调用见[适配器安装说明](../skills/hypit-haiyi/references/setup.md)。setup下载／编译并写本机 `.local/config.json`；install-skill写入当前CODEX_HOME/skills（默认用户的 `.codex/skills`）并重建local-setup。移动目录后重跑配置，别复制旧绝对路径JSON冒充安装完成。已有技能建议先备份再更新；重新开启或刷新Codex任务确认技能被发现。

Python工具可直接从源码运行，或使用已安装koroflow技能的 `scripts/migration.py`；后者自包含，不依赖源码根。直接海艺路线另按该技能当前说明安装及授权，不要运行Hypit setup来代替安装海艺原技能。

## 新机重新授权

海艺原技能的当前入口支持 `python "<本机海艺技能>/scripts/generate.py" '{"action":"login"}'` 与 `check-auth`；以新安装技能说明为准。Node Provider凭据顺序为 `HAIYI_API_TOKEN` → `HAIYI_TOKEN_FILE` → 系统用户配置目录的haiyi-skills存储，详见适配器说明。直接海艺路径核对它自己的优先级，不推定所有执行器一致。

不要迁移Token、旧.env、上传缓存或私有请求，也不要把值粘到交接或截图里。`auth_source`只记录变量／安全存储方式的名称；离线检查不读取或验证凭据。登录及check-auth会联网；模型、价格、余额也须在新机单独只读核对。

## 私有配置与无付费自检

将下列空模板复制到源码外的私人目录：

- [machine.example.json](../skills/koroflow/assets/templates/machine.example.json) → `machine.json`。
- [asset-manifest.example.json](../skills/koroflow/assets/templates/asset-manifest.example.json) → `assets.json`。
- [request-preflight.example.json](../skills/koroflow/assets/templates/request-preflight.example.json) → 需要时填本次请求。

创建workspace、assets、deliveries目录；machine内相对路径从machine.json所在目录解析，资产路径从asset_root解析。填写本机工具、执行器、时区、工作根和交付根；route先为planning，实际制作前切到direct-haiyi或hypit并填写入口。偏好策略是可配置的：若本地要求海艺原生声音，将 `policy.require_native_audio` 设为true；不加BGM、输入参考去声、换背景、准备合回旧音轨都不取消该策略。此时Seedance实际请求须 `generateAudio: true`；当次明确静音须false及单独的用户依据。其他模型的等效开关按实时接口核对，不能硬套字段。

资产清单每项填写id、相对路径、SHA256、核准身份／比例材质、完整叫声、真实发声部位、声音参考采用依据与是否默认绑定。音频存在不代表被采用。文件搬家按指纹重新定位，不退回同名旧资产。只携带下一次要用的核准图和可选已采用音色；个人清单、偏好、媒体与路径不上传公共库。

```text
python -X utf8 scripts/migration.py --config "<私人目录>/machine.json"
python -X utf8 scripts/migration.py --config "<私人目录>/machine.json" --request "<私人目录>/request.json"
python -X utf8 -m unittest discover -s tests -p "test_*.py"
```

工具只读本地文件、计算指纹并运行工具版本/requests导入检查，无网络、无上传、无生成。请求JSON是包裹实际payload的检查交接格式，不能直接提交平台；覆盖最新真实请求再检查，不拿示例占位符当可用模型。它核对本地策略、字段、附件索引／指纹和纯图引用；不会认证远程URL内容、自动观看素材、听音、查模型/报价/授权或替代平台schema校验，也不能阻止绕过工具的提交。

## 首个新项目

1. 把个人启动词和当前偏好交给Codex，明确“先自检、不生成”；核对资产完整画幅及指纹。只查本次可访问记录，不宣称全历史未用。
2. 按[执行流程](../skills/koroflow/references/reference-production-runbook.md)分析参考，列保留/替换元素、初始在场状态、揭示机制和结尾；选视频参考或纯图重建，核对当前模型能力与价格。
3. Hypit路线使用 `node scripts/workflow.mjs init "<全新工程目录>"`，改写演示Source/Run及Runtime，再check/plan；直接海艺路线按其SKILL准备实际请求。不要为了安装验证执行演示生成。
4. `check/plan`不提交生成；`verify`是离线mock与计划验证；`doctor/pricing`或原技能check-auth/model-info可能联网，实际行为按当前工具说明。`prepare`写本地记录，不代表已提交。
5. 用户具体委托覆盖后完成正式请求、模型价档、费用和授权预检，才执行 `build` 或海艺 `generate` 等收费动作。未知结果查询原任务，平台错误文本不授权重试。

本机干净目录自检与CI不是笔记本实机安装、登录或媒体质量验证；这些尚需新机按步骤核实。
