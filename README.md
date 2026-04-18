# Trae Agent Skills

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Skills Count](https://img.shields.io/badge/skills-1-blue.svg)]()

一组用于 [Trae IDE](https://www.trae.ai/) 的 Agent Skills，增强 AI 助手的功能能力。

## 🚀 快速开始

### 安装整个 Skill 集合

```bash
# 克隆仓库
git clone https://github.com/你的用户名/trae-agent-skills.git

# 复制到 Trae 配置目录（Windows）
# 注意：请根据实际路径调整
xcopy /E /I trae-agent-skills\.trae %USERPROFILE%\.trae

# 或手动复制 skills 目录到 .trae/skills/
```

### 安装单个 Skill

```bash
# 复制单个 Skill 到 Trae 配置目录
cp -r trae-agent-skills/skills/coros-activity-downloader ~/.trae/skills/
```

## 📦 包含的 Skills

| Skill | 描述 | 版本 | 状态 |
|-------|------|------|------|
| [coros-activity-downloader](skills/coros-activity-downloader/) | 从 COROS Training Hub 下载跑步活动记录 | v2.0.0 | ✅ 稳定 |

## 🛠️ 开发新 Skill

查看 [Skill 开发指南](docs/SKILL_DEVELOPMENT_GUIDE.md) 了解如何创建和贡献新 Skill。

## 📁 项目结构

```
trae-agent-skills/
├── skills/                    # Skill 集合
│   └── coros-activity-downloader/
├── docs/                      # 项目文档
├── scripts/                   # 工具脚本
└── .trae/                     # Trae IDE 配置
```

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

查看 [CONTRIBUTING.md](CONTRIBUTING.md) 了解贡献指南。

## 📄 许可证

[MIT](LICENSE) © 2026

## ⚠️ 免责声明

这些 Skills 仅供个人学习和使用。使用这些 Skills 时，请确保遵守相关服务的使用条款。
