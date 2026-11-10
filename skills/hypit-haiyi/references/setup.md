# 安装与调用

首次换电脑先读仓库 `docs/laptop-setup.md`，区分直接海艺技能与Hypit Provider的依赖，重新配置并授权，不复制旧机器的Token或绝对路径配置。

此代码库提供统一技能、Provider 和模板，使用固定版本 Hypit 工具，不复制完整 Hypit 核心或海艺原插件。最低 Node.js 22.15；完整新机器准备另需 Git、pnpm 10.33.0、FFmpeg 和 FFprobe。Windows、macOS 与 Linux 均可使用 Node 入口；本次实际验证环境为 Windows。

已有安装：

```text
node scripts/workflow.mjs setup --hypit-root /absolute/path/to/hypit --ffmpeg /absolute/path/to/ffmpeg --ffprobe /absolute/path/to/ffprobe
node scripts/workflow.mjs install-skill
node scripts/workflow.mjs info
```

从零安装固定版本工具：

```text
node scripts/workflow.mjs setup --install --ffmpeg /absolute/path/to/ffmpeg --ffprobe /absolute/path/to/ffprobe
node scripts/workflow.mjs install-skill
```

`setup --install` 克隆 upstream.json 指定的 Hypit 版本到 `.local/hypit` 并安装依赖，只下载和配置，不生成媒体。pnpm 需预先安装；缺失时可用 `npm install -g pnpm@10.33.0`。已有其他版本 Hypit 不会被重置。FFmpeg/FFprobe 未传路径时查 PATH；未发现则停止并说明缺失项。

`install-skill` 一并安装统一入口 `hypit-haiyi` 和导演剧本模块 `video-director`。只需要文字策划时运行 `node scripts/workflow.mjs install-skill --director-only`：无需先 setup，也无需 Hypit 工具、FFmpeg 或海艺账号。文字策划使用当前对话模型，平台自身的计费方式仍适用。

`install-skill` 安装到 CODEX_HOME/skills，未设置 CODEX_HOME 时使用用户 `.codex/skills`。缺失的 Hypit 基础技能从工具目录补装，不整篇替换已有基础技能。给已安装 Hypit 与海艺的技能入口补充统一视频路由说明，原文先备份到 `.local/skill-backups`，重复安装不会重复追加。插件更新可能覆盖此路由说明，重新运行 install-skill 可补回。原海艺插件只用于补充操作，直接 Provider 的图片和视频生成无需它的 Python 脚本，但需要有效海艺 Token。

以下从代码库根目录调用，项目和输入路径都相对当前终端目录，而非相对技能目录：

```text
node scripts/workflow.mjs init /path/to/new-video-project
node scripts/workflow.mjs check /path/to/new-video-project/haiyi-text-video.svml --project /path/to/new-video-project
node scripts/workflow.mjs plan /path/to/new-video-project/haiyi-text-video.svrun --project /path/to/new-video-project
node scripts/workflow.mjs doctor --project /path/to/new-video-project
node scripts/workflow.mjs pricing /path/to/new-video-project/haiyi-text-video.svrun --project /path/to/new-video-project
node scripts/workflow.mjs build /path/to/new-video-project/haiyi-text-video.svrun --project /path/to/new-video-project --follow
```

`build` 会产生海艺费用；其余示例不提交生成任务，`pricing` 会读取账号的实时模型价格。演示模板只有图片与四秒视频，创作项目必须改写提示词和编排。

命令包装器添加代码库的 `--package-root` 和项目的 Runtime Profile；这是复用 Provider 的入口，不要求每个视频项目安装完整工具。更多命令使用 `hypit` 子命令透传，例如：

```text
node scripts/workflow.mjs hypit runtime status /path/to/project/hypit.runtime.json --project /path/to/project
node scripts/workflow.mjs hypit builds --project /path/to/project
node scripts/workflow.mjs hypit help studio
```

凭据优先级：`HAIYI_API_TOKEN` > `HAIYI_TOKEN_FILE` > 系统用户配置目录 `haiyi-skills/tokens.json`。包装器按 Profile 中的海艺地址选择存储的 Token，且仅注入子进程，不回显。没有 Token 时可以创作和检查，不能生成；可通过海艺原技能显式登录，或设置环境变量。

机器路径仅保存到被 Git 忽略的 `.local/config.json` 和已安装技能的 `references/local-setup.json`。移动代码库或工具目录后重新执行 `setup`、`install-skill`。移到新机器后不要复制 Token，重新授权。
