# Skills 目录

本目录包含所有可用的 Trae Agent Skills。

## 快速导航

| Skill | 描述 | 版本 |
|-------|------|------|
| [coros-activity-downloader](coros-activity-downloader/) | 从 COROS Training Hub 下载跑步活动记录 | v2.0.0 |

## 安装 Skill

### 方式一：复制整个 skills 目录

```bash
# Windows
xcopy /E /I skills %USERPROFILE%\.trae\skills

# macOS/Linux
cp -r skills ~/.trae/skills
```

### 方式二：安装单个 Skill

```bash
# 复制特定 Skill
cp -r skills/coros-activity-downloader ~/.trae/skills/
```

## 开发新 Skill

1. 创建新的 Skill 目录
   ```bash
   mkdir skills/your-skill-name
   ```

2. 复制模板文件
   ```bash
   cp docs/SKILL_TEMPLATE.md skills/your-skill-name/SKILL.md
   ```

3. 按照 [Skill 开发指南](../docs/SKILL_DEVELOPMENT_GUIDE.md) 开发

4. 运行验证
   ```bash
   python scripts/validate-skills.py
   ```

## Skill 结构

每个 Skill 应遵循以下结构：

```
skill-name/
├── README.md          # 用户文档
├── SKILL.md           # Skill 定义（Trae 规范）
├── CHANGELOG.md       # 版本历史（可选）
├── scripts/           # 执行脚本
│   └── script.py
├── docs/              # 详细文档（可选）
└── tests/             # 测试（可选）
```
