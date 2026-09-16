# Soha Skills 仓库入口

- 本仓负责 Soha 官方 skills、MCP presets、agent profiles 和发布目录；与本仓 `.agents/skills/` 下的开发协作技能区分，不复制 Core 业务逻辑。
- 在 OpenSoha 多仓工作区中读取 `../AGENTS.md` 一次；独立克隆时使用本仓规则，不要求初始化相邻仓库或规划工具。
- 资产实现或审查按需使用 [soha-skills](.agents/skills/soha-skills/SKILL.md)。技能描述限定真实能力和触发条件，不把安装技能视为外部操作授权。
- 资产验证入口为 `python3 tools/validate_assets.py`；发布参数和包验证以 [CI](.github/workflows/ci.yml) 与发布流程为准。
- 仅修改开发协作说明时检查元数据、链接和内容一致性；相关内容和环境未变化时复用成功验证，保留用户未提交改动。
