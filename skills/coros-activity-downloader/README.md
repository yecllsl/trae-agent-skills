# COROS Activity Downloader

从 [COROS Training Hub](https://t.coros.com) 下载跑步活动记录（FIT格式）。

## 功能特性

- ✅ **自动下载** - 从 COROS 云端自动下载跑步活动
- ✅ **智能去重** - 基于 `labelId` 自动跳过已下载文件
- ✅ **完整性验证** - 下载后验证文件完整性
- ✅ **中文支持** - 完美支持中文活动名称
- ✅ **JSON 输出** - 支持程序化调用
- ✅ **断点续传** - 中断后可安全重试

## 使用方法

### 在 Trae IDE 中使用

直接告诉 Trae：

```
下载我最近15条COROS跑步记录
```

或：

```
帮我备份所有COROS活动到本地
```

### 命令行使用

```bash
# 基本用法（需要活动列表JSON）
python scripts/download_coros.py --count 15 --activities-json '[{"labelId":"xxx","name":"跑步","sportType":100}]'

# 指定下载目录
python scripts/download_coros.py --count 10 --activities-json '<JSON>' --download-dir "D:\COROS_Backup"

# 仅验证现有文件
python scripts/download_coros.py --validate-only

# JSON 输出模式
python scripts/download_coros.py --count 10 --activities-json '<JSON>' --json-output
```

## 参数说明

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `--count` | int | 10 | 下载数量 |
| `--activities-json` | string | - | 活动列表JSON（从浏览器提取） |
| `--label-ids` | string | - | 直接指定labelId（逗号分隔） |
| `--download-dir` | string | `~/.nanobot-runner/download` | 下载目录 |
| `--sport-type` | int | 100 | 运动类型（100=跑步） |
| `--validate-only` | flag | false | 仅验证，不下载 |
| `--json-output` | flag | false | JSON格式输出 |

## 依赖要求

- Python 3.6+
- Chrome DevTools MCP（用于浏览器自动化）
- 有效的 COROS 账号和登录会话

## 工作原理

1. **浏览器提取** - 使用 Chrome DevTools MCP 从 COROS 网页提取活动列表
2. **智能匹配** - 扫描本地已有文件，跳过重复
3. **下载执行** - 从 COROS CDN 下载 FIT 文件
4. **完整性检查** - 验证文件大小和有效性

## 文件命名

下载的文件使用以下命名格式：

```
{活动名称}_{labelId}.fit
```

例如：
- `恢复跑_476855911038615862.fit`
- `上海市跑步_476786357002338514.fit`

## 常见问题

### Q: 下载失败（HTTP 404）

**原因**：活动可能已被删除或 userId 不正确

**解决**：检查活动是否存在于 COROS 账号中

### Q: 文件大小为0

**原因**：网络中断或权限问题

**解决**：重新运行脚本，会自动重试

### Q: 中文文件名乱码

**原因**：Python 3 默认 UTF-8，通常不会出现问题

**解决**：确保使用 Python 3.6+

## 详细文档

查看 [SKILL.md](SKILL.md) 获取完整的技术文档和架构说明。

## 更新日志

查看 [CHANGELOG.md](CHANGELOG.md) 了解版本历史。

## 许可证

[MIT](../../LICENSE)
