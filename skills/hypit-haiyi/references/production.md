# 执行、复用与交付

## 提交前核对方案、参数与消耗

先读本地原生音频策略。要求海艺带声时Seedance最终实际请求必须generateAudio为true，同时生成动作声、环境声与正常角色反应；无BGM、输入去声、背景修改、准备复用旧音轨不构成关闭理由。只有当次明确静音才例外。其他接口按当前等效字段核对；通用工具保留明确无声能力。

付费生成前展示可直接核对的确认单：作品与请求数量、正式提示词、实际上传附件及用途、平台与扣费来源、精确模型ID和价格/速度档位、生成模式、时长、画幅、分辨率、音频设置和特殊输入开关。相同720p的不同价档不能混称。预检文件格式、编码、尺寸、时长及平台自适应要求。

按本次真实配置查询实时价格，注明计费单位、查询时间、单项及批量合计、图片/视频等依赖阶段和复用项、预算上限；能查余额才报告余额，读不到保留未知。积分不无依据换算人民币，空费用不证明免费或退款。

先完成check/plan/pricing及必要doctor，再在本次明确委托及既有约定范围内执行build；直接制作指令可以构成授权，不要求固定确认口令。已明确授权的同一请求/批次不重复询问；“只分析／先看方案／暂停”优先。换模型或升档、增加数量/时长/付费步骤、切换扣费来源、实质改方案或超预算时，未被原授权覆盖的部分重新确认。未授权付费重试不自动执行，未知结果先查原任务。完整通用规范由相邻koroflow技能的`references/production-standard.md`提供；单独使用本技能时仍执行本节。

参考复刻批次可按相邻koroflow技能的[执行流程](../../koroflow/references/reference-production-runbook.md)交接：先核对重复产出，固定源角色职责与目标身份、声音，按需补资产；检查后将正式提示词标签与实际请求数组、文件指纹逐项对应。按当前模型实际限制判断整段或分段，不把历史上限、图数或价档当跨平台默认。

上述为操作者流程，当前代码并未实现统一预算审批弹窗或全部提交路径的费用锁。

## 执行与实际交付

制作前使用已安装 Hypit 的对应参考：

- 项目边界与跨会话记录：`references/creation/project-files.md`。
- 图片方向：`references/playbooks/craft/image-direction.md`；视频方向：`references/playbooks/craft/video-direction.md`；连续角色与道具：`references/playbooks/craft/generated-dependencies.md`。
- Source / Run：`references/production/authoring.md`、`runs.md`；检查 `plan` 后仅执行所需生成。
- 付费范围、Build id、超时及失败恢复：`references/production/builds.md`。
- 本地程序准备：`references/environment/local-tools.md`；Provider 调整：`references/environment/model-and-provider.md`。
- 渲染、看成片与编辑预览：`references/production/rendering.md`、`review.md`、`studio.md`。

`PROGRESS.md` 至少保留项目根目录、Source/Run 路径、Runtime Profile、当前 Build id、已接受 Output 的名称及对应 Result、剩余工作与授权范围。不要写入凭据或带签名的私有素材 URL。

执行脚本不自动重试生成。观察超时后查询 Runtime/Build，不能再调用 `build` 来“继续等待”。处理失败时保留成功素材，将要复用的 Output 写入新的 Run Candidates，再检查剩余请求。已经提交的请求若无法确定状态，先查询海艺任务记录。

交付前观看并听完真实最终文件；留意人脸/手/产品变形、镜头间一致性、跳帧与音画同步、字幕遮挡、响度和时长。生成结果需修复时，先用可编辑 Source 或本地处理解决适合的问题；模型重生成按已授权预算执行。现有 mock/plan 验证不等于画面或声音质量验证。
