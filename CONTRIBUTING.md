# 贡献指南

感谢你对 Trae Agent Skills 项目的兴趣！本文档将帮助你了解如何为项目做出贡献。

## 🎯 贡献方式

### 1. 报告 Bug

如果你发现了 Bug，请通过 [GitHub Issues](../../issues) 提交，并包含以下信息：

- 问题描述
- 复现步骤
- 期望行为 vs 实际行为
- 环境信息（OS、Python版本、Trae版本）
- 相关日志或截图

### 2. 提交新 Skill

想要添加新的 Skill？太棒了！请遵循以下流程：

1. **Fork 仓库** 并创建你的分支
2. **复制模板** 从 `docs/SKILL_TEMPLATE.md`
3. **开发 Skill** 遵循我们的规范
4. **运行验证** 使用 `python scripts/validate-skills.py`
5. **提交 PR** 并描述你的 Skill

### 3. 改进文档

文档改进同样受欢迎！包括：

- 修正错别字
- 改进说明清晰度
- 添加示例
- 翻译

## 📋 Skill 开发规范

### 目录结构

```
skills/your-skill-name/
├── README.md          # 用户文档（必需）
├── SKILL.md           # Skill定义（必需）
├── CHANGELOG.md       # 版本历史（推荐）
├── scripts/           # 执行脚本
│   └── script.py
├── docs/              # 详细文档（可选）
└── tests/             # 测试（可选）
```

### 命名规范

- **Skill目录名**：小写，短横线连接
  - ✅ `coros-activity-downloader`
  - ❌ `CorosActivityDownloader`
  
- **脚本文件名**：小写，下划线连接
  - ✅ `download_coros.py`
  - ❌ `downloadCoros.py`

- **函数名**：snake_case
  - ✅ `download_file()`
  - ❌ `downloadFile()`

### SKILL.md 规范

必须包含以下 frontmatter：

```yaml
---
name: "skill-name"
description: "简短描述，50字以内"
---
```

必须包含以下章节：

1. **Purpose** - 功能目的
2. **Prerequisites** - 依赖要求
3. **Usage** - 使用方法
4. **Architecture** - 架构说明
5. **Error Handling** - 错误处理

### 代码规范

- 使用 Python 3.6+ 语法
- 添加中文注释解释复杂逻辑
- 遵循 PEP 8 风格指南
- 不要硬编码敏感信息

## 🔍 提交前检查清单

- [ ] Skill 可以在 Trae IDE 中正常工作
- [ ] 已添加 README.md 和 SKILL.md
- [ ] 已运行验证脚本并通过
- [ ] 代码中有适当的中文注释
- [ ] 没有硬编码的敏感信息
- [ ] 更新了 CHANGELOG.md（如适用）

## 📝 Pull Request 流程

1. **创建分支**
   ```bash
   git checkout -b feature/your-skill-name
   ```

2. **提交更改**
   ```bash
   git add .
   git commit -m "Add skill: your-skill-name v1.0.0"
   ```

3. **推送到你的 Fork**
   ```bash
   git push origin feature/your-skill-name
   ```

4. **创建 Pull Request**
   - 标题格式：`Add skill: skill-name vX.X.X`
   - 描述中包含 Skill 的功能说明
   - 关联相关 Issue（如有）

## 💬 沟通指南

- 保持友善和尊重
- 提供建设性的反馈
- 接受不同的观点
- 专注于技术讨论

## 📞 获取帮助

如果你需要帮助：

1. 查看 [Skill 开发指南](docs/SKILL_DEVELOPMENT_GUIDE.md)
2. 参考现有的 Skill 实现
3. 在 Issue 中提问
4. 发起 Discussion（如启用）

再次感谢你的贡献！
