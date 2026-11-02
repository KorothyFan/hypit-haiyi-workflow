# KoroFlow

**把内容策划、AI 制作、质量检查、版本交付和发布运营，整理成可以持续复用的工作流。**

KoroFlow 面向需要持续制作角色短视频、参考复刻和图文内容的创作者与团队。从理解参考素材，到选择生成方式、修订画面和声音，再到整理库存与准备发布，每个环节都保留明确的要求、版本和执行依据，方便在不同任务或工具之间接着做。

项目提供 Codex 技能、本地记录工具、制作规范和可扩展的平台交接方式。现有制作适配器连接海艺与 Hypit；使用其他生成平台、无限画布或发布工具时，也可以沿用作品、素材和交付记录，另外接入实际可用的执行工具。

[快速开始](#快速开始) · [制作路径](#按不同制作路径使用) · [能力边界](#目前实现到哪一步) · [详细文档](#文档导航)

**下载 v0.7.1 预览版：** [完整源码与技能包 ZIP](https://github.com/KorothyFan/Koroflow/releases/download/v0.7.1/koroflow-v0.7.1-source.zip) · [发布说明与校验文件](https://github.com/KorothyFan/Koroflow/releases/tag/v0.7.1)。包内包含四个技能、完整制作规范、七条制作路径和最新使用指南，安装依赖仍按下文准备。

## 一套工作流怎样使用

一个典型的项目会经过以下环节：

1. **明确内容**：分析参考片或整理原创想法，确定角色、剧情、镜头、声音，以及本次要保留和改变的内容。
2. **选择制作路径**：根据目标决定直接编辑原片、依据参考重建，还是先做场景图再生成视频。需要保留原声、另做配音或制作漫画时，使用对应的方法。
3. **准备并执行**：核对实际附件、模型版本与价档、输出参数和预计消耗，在用户委托的范围内调用已连接的平台，保存任务回执。
4. **检查与修订**：对照方案看画面、听声音，检查角色、动作、接触、表情与口型。保留原生输出和历史版本，明确哪些问题已经解决、哪些仍未确认。
5. **交付与运营**：选择正式版本，准备英文标题和标签，整理库存与统计。发布前核对账号、文件和历史，通过实际发布工具执行，再保存结果与回填记录。

每个独立作品使用稳定的作品编号 `work_id`。同一作品换声音、改画面或重新交付时沿用原编号，避免把多个修订误算成多条产出。成功生成、独立交付和用户确认采用分别记录。

可以这样开始一个任务：

> 使用 $koroflow，参考这段视频，把主角换成我提供的角色，保留剧情、镜头和原声。先分析适合的制作路径，暂不生成。

也可以只调用其中一个环节，例如写分镜、检查已有作品，或者为已交付视频准备发布文案。实际生成和发布按照明确的委托范围执行；阅读文档或安装技能不会自动启动任务。

## 按不同制作路径使用

同样是“做一个视频”，具体方法可能很不同。KoroFlow 按路径保存经验，让每种方法保留自己的适用条件。

| 制作路径 | 适合的情况 | 重点 |
| --- | --- | --- |
| [A · 原视频参考／编辑](skills/koroflow/references/production-paths/source-video-edit.md) | 希望保留原片剧情、动作和镜头，只改变指定元素 | 真实视频参考、角色映射、动作时序与接触关系 |
| [B · 解读复写](skills/koroflow/references/production-paths/reference-rebuild.md) | 不上传原片，根据已理解的剧情与表达重建 | 分清参考事实与本次改编，明确重建的取舍 |
| [C · 场景资产驱动视频](skills/koroflow/references/production-paths/scene-to-video.md) | 先确定新空间、立体风格或原创画面，再生成动作 | 分阶段确认身份、场景、动作空间和连续性 |
| [D · 只改画面，保留原音轨](skills/koroflow/references/production-paths/visual-only-audio-preserve.md) | 原声已经合适，只需要修订形象或背景 | 原音轨复用、时间匹配、原生版与本地处理版区分 |
| [E · 独立声音修订](skills/koroflow/references/production-paths/audio-repair.md) | 需要调整音色、情绪或另做配音 | 完整发声回合、表演、声音空间与音画同步 |
| [F · 连续图文漫画](skills/koroflow/references/production-paths/sequential-comic.md) | 制作多页角色故事与轮播内容 | 跨页身份和道具连续性、对白、分页与交付校验 |
| [G · 外部成片与合集](skills/koroflow/references/production-paths/intake-and-compilation.md) | 接收外包或用户成片，整理库存，或编排合集 | 来源、采用版本、父片段关系与去重 |

这些路径可以组合。例如“编辑原视频并保留原声”采用 `A + D`；“先做新场景，再单独配音”可以采用 `C + E`。字母是文档检索标识，不是命令参数。

角色缺件、修补或持久道具容易漂移时，可以用 `A + C`：原片控制故事和动作，必要的状态资产控制身份、材质、道具归属及变化前后。见[状态资产方法](skills/koroflow/references/production-paths/state-and-prop-continuity.md)、[素材绑定表](skills/koroflow/assets/templates/state-asset-binding.md)与[针织玩偶互助案例](skills/koroflow/references/cases/knitted-dolls.md)。资产数量按剧情决定，案例保留已知瑕疵与证据范围。

某个参考素材的时长、切点、笑点和特殊对白仍保存在它自己的项目中，不会因为一次效果不错就变成所有作品的默认要求。路径选择与适用范围见[制作路径总览](skills/koroflow/references/production-paths.md)；新经验可用[路径经验模板](templates/path-experience.md)记录。

## 四个技能如何配合

| 技能 | 负责什么 | 什么时候使用 |
| --- | --- | --- |
| `koroflow` | 统筹需求、路径、制作、检查、交付和运营 | 开始完整项目，或接续已有工作 |
| `video-director` | 剧本、分镜、参考片拆解与角色替换方案 | 需要先把内容和镜头想清楚 |
| `hypit-haiyi` | 海艺生成与 Hypit 编排、渲染的具体交接 | 已选择海艺／Hypit 制作路径 |
| `koro-operations` | 核对既有工程、统计快照、账号与发布历史 | 整理作品、核对库存或准备发布 |

只做剧本时可以直接使用 `$video-director`；完整项目通常从 `$koroflow` 进入，再按需要调用其他技能。各技能按职责配合，不要求每个小任务走完所有环节。

## 目前实现到哪一步

KoroFlow 包含三部分，它们各自承担不同的工作：

- **技能与制作规范**：指导助手分析素材、写方案、选择路径、检查结果和交接任务。完整音画质量仍需实际观看与听审，文档和技术检查不能替代审片。
- **本地记录核心**：保存作品、素材职责、文件 SHA256、修订、检查结果和任务状态。交付时检查必检项；保存发布占用和未知结果，帮助避免重复分配或重复提交。
- **平台执行工具**：现有海艺 Provider 支持图片／视频 API，Hypit 负责相应编排与本地渲染。其他生成、编辑、音频及发布能力，需要通过已验证的工具或接口接入。

本地核心的 `route` 和 `prepare` 用于核对能力、准备交接和保存记录，本身不调用外部平台。仓库尚未内置通用社交平台发布执行器，也不附带原有 Excel 刷新器；可以与使用者现有的发布工具、台账和整理脚本衔接。

参考编辑是否能严格保留动作、模型是否支持声音控制，以及某个平台当前是否连通，都需要针对实际服务验证。整合流程可以改善约束、复用和检查方式，不能保证模型画质提升或逐帧复刻成功。

## 快速开始

### 1. 获取代码并安装需要的技能

使用 Git、Node.js ≥22.15；运行本地记录核心另需 Python ≥3.11。Windows Python 如果缺少 IANA 时区数据，可安装 `tzdata`。

```powershell
git clone https://github.com/KorothyFan/Koroflow.git
cd Koroflow
node scripts/workflow.mjs install-skill --core-only
```

这会安装独立的 `koroflow` 技能，不要求先准备 Hypit、FFmpeg 或生成账号。只需要导演或运营技能时，可以分别运行：

```powershell
node scripts/workflow.mjs install-skill --director-only
node scripts/workflow.mjs install-skill --operations-only
```

### 2. 使用本地记录核心

以下工作空间路径为示例，请替换为自己的目录。`init` 创建本地配置，不搬迁已有素材，也不覆盖已初始化的工作空间。

```powershell
python -X utf8 scripts/koroflow.py --workspace "D:/my-video-workspace" init
python -X utf8 scripts/koroflow.py --workspace "D:/my-video-workspace" adapters
python -X utf8 scripts/koroflow.py --help
```

工作空间的 `.koroflow` 保存配置和事件记录，其中 `quality.json`、`targets.json`、`adapters.json` 分别配置质量检查、制作目标和平台能力。角色资产、账号、时区和临时安排按使用者的实际情况设置。

新作品可从[作品清单模板](skills/koroflow/assets/templates/work.example.json)开始：登记作品与参考，保存真实任务，选定输出版本，实际检查后再交付。完整命令见[核心记录与执行](skills/koroflow/references/workflow.md)。已有工程可以先核对旧记录，需要时显式导入，保留原作品编号和首次交付日，不必重新建成新作。

### 3. 需要海艺／Hypit 制作时再配置

本仓库包含整合技能、Provider 和配置脚本。完整 Hypit 工具、海艺原 Skill、账号与生成额度需要另外准备。

已有 `upstream.json` 固定版本的 Hypit 和媒体工具时：

```powershell
node scripts/workflow.mjs setup --hypit-root "D:/tools/hypit" --ffmpeg "D:/tools/ffmpeg/bin/ffmpeg.exe" --ffprobe "D:/tools/ffmpeg/bin/ffprobe.exe"
node scripts/workflow.mjs install-skill
node scripts/workflow.mjs info
```

没有 Hypit 时可使用 `setup --install` 下载 `upstream.json` 固定的版本并安装依赖；这一步另需 Git、pnpm 10.33.0，以及 FFmpeg／FFprobe 等运行依赖。完整 `install-skill` 会安装四个 KoroFlow 技能，并补装缺失的 Hypit 原技能。

海艺原技能 `haiyi-aigc` 从其提供渠道单独安装。已持有效 Token、仅使用 Provider 支持的图片／视频接口时，可以不依赖它；需要其登录、语音、音乐或增强等功能时，再按对应说明安装。凭据保存在本机，可使用 `HAIYI_API_TOKEN` 或海艺原技能已保存的登录授权。

详细依赖、费用说明与操作步骤见[海艺／Hypit 制作适配器](docs/haiyi-hypit.md)。云端任务按实际平台、模型和额度计费，安装本仓库不提供免费生成额度。参数与费用预检后，在已授权范围内执行；`build` 会提交真实生成任务。

## 使用自己的平台与整理方式

制作平台和发布平台分别配置。接入新服务时，先确认实际可用的 API、MCP、浏览器、CLI 或人工操作方式，验证输入输出和任务查询，再用[适配器模板](skills/koroflow/assets/templates/adapter.example.json)描述能力与交接方式。填写配置并不代表服务已经接通。

已有项目、台账和统计工具可以继续使用：`koro-operations` 负责读取和预检，核心可显式导入旧作品并通过 `bridge` 导出兼容事件。核心自身的报表只覆盖其日志，不冒充已有工程的全量统计；Excel 手工字段仍通过原有刷新机制按稳定编号保留。

发布时保留准备、提交、预约、完成和结果未知的区别。用户确认、平台回执与台账展示可以有不同依据，记录时分别说明。制作授权不自动包含发布授权；结果未知先查原任务，不能直接重复提交。

## 文件与数据放在哪里

```text
Koroflow/                 本仓库：可分享的技能、规范、模板和工具
  skills/                 四个技能及对应参考资料
  templates/              制作确认、复刻委托和路径经验模板
  scripts/                安装、记录、预检和打包入口
  packages/provider-haiyi/ 海艺制作适配器
  docs/                   架构、运营和依赖说明

自己的工作空间/           个人资产、视频工程和真实运行记录
  .koroflow/              本地核心配置与事件
  作品工程/               Brief、分镜、输入素材、任务与交付版本
```

仓库 `.local` 仅保存本机工具配置。凭据、账号设备清单、私人素材、运行日志和本机路径索引不进入 Git 或源码包；原文案例可在自己的项目中保留，公开部分只沉淀可迁移的方法。

## 文档导航

| 想了解什么 | 从这里开始 |
| --- | --- |
| 一条作品怎样制作、检查和交付 | [完整制作规范](skills/koroflow/references/production-standard.md) |
| 不同素材该采用什么方法 | [制作路径与经验](skills/koroflow/references/production-paths.md) |
| 原片复刻中如何稳定特殊状态和道具 | [状态资产方法](skills/koroflow/references/production-paths/state-and-prop-continuity.md) · [针织案例](skills/koroflow/references/cases/knitted-dolls.md) |
| 记录本次方案、附件、参数和费用 | [提交确认单](templates/production-confirmation.md) |
| 给出多角色、多版本复刻委托 | [复刻委托模板](templates/replication-brief.md) |
| 本地核心命令、旧工程接续 | [核心记录与执行](skills/koroflow/references/workflow.md) |
| 既有统计、账号和发布预检 | [运营模块](docs/operations.md) |
| 海艺、Hypit 与可选 H3 技能的关系 | [制作适配器说明](docs/haiyi-hypit.md) |
| 接其他平台和发布工具 | [适配器契约](skills/koroflow/references/adapters.md) · [架构说明](docs/architecture.md) |

## 版本、开发与来源

当前下载包为 [v0.7.1 预览版](https://github.com/KorothyFan/Koroflow/releases/tag/v0.7.1)，包含完整制作规范、七条制作路径、经验模板与新版 README。Release 附件是固定版本快照；`main` 后续可能继续更新，附件不会随源码提交自动变化。更新记录见 [CHANGELOG](CHANGELOG.md)。

2026-11-02新增的状态资产方法、绑定表和针织案例目前仅在源码中，尚未进入v0.7.1附件；需要这些内容请获取当前源码。版本号与旧下载附件保持不变，下次获授权发版时再随新包分发。

开发验证：

```powershell
python -X utf8 -m unittest discover -s tests -p "test_*.py" -v
node scripts/workflow.mjs verify
node scripts/bundle.mjs
```

Python 测试与源码打包已配置 Windows／Linux CI；`verify` 另检查已准备好的 Hypit 与 Provider，执行离线 mock 和 Source／plan 验证。它们不提交付费生成，也不证明真实平台连接、音画质量或发布成功。源码包按白名单构建，为兼容保留顶层目录名 `hypit-haiyi-workflow`。插件入口为 `plugin.json` 和 `.agents/plugins/marketplace.json`。

Hypit 上游为 [hypit-ai/hypit](https://github.com/hypit-ai/hypit)，固定版本见 `upstream.json`。归属与适用范围见 [NOTICE](NOTICE.md)，上游许可证见 [HYPIT-LICENSE](third-party/HYPIT-LICENSE)。KoroFlow 是独立的工作流整合项目，上游工具与平台服务仍适用各自条款。
