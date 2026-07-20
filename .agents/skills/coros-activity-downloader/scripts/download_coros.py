#!/usr/bin/env python3
"""
COROS Activity Downloader

Downloads running activity records from COROS Training Hub in FIT format.
Supports duplicate prevention, file integrity validation, and configurable parameters.

Usage:
    python download_coros.py --count 15 --sport-type 100
    python download_coros.py --label-ids 476855911038615862,476786357002338514
    python download_coros.py --validate-only
"""

import argparse
import json
import os
import sys
import time
from datetime import datetime
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
from pathlib import Path


# ============================================================
# Configuration
# ============================================================

# 获取脚本所在目录，用于查找 config.json
SCRIPT_DIR = Path(__file__).parent.resolve()
CONFIG_FILE = SCRIPT_DIR.parent / "config.json"

# 默认配置
DEFAULT_CONFIG = {
    "userId": "445542372294541312",
    "downloadDir": "D:/yecll/Downloads/coros/test-fit-files",
    "sportType": 100,
    "defaultCount": 10,
    "downloadDelayMs": 500,
    "minFileSize": 1024
}

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"


def load_config():
    """加载配置文件，如果不存在则使用默认配置"""
    config = DEFAULT_CONFIG.copy()
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                user_config = json.load(f)
                config.update(user_config)
        except (json.JSONDecodeError, IOError) as e:
            print(f"警告: 无法加载配置文件 {CONFIG_FILE}: {e}", file=sys.stderr)
    return config


def setup_download_dir(path):
    """创建下载目录（如果不存在）"""
    os.makedirs(path, exist_ok=True)
    return path


def scan_existing_files(download_dir):
    """
    扫描现有 FIT 文件并提取其 labelId。
    
    支持任意命名格式：
        "上海市跑步_476786357002338514.fit" -> "476786357002338514"
        "Shanghai_Run_476786357002338514.fit" -> "476786357002338514"
        "476786357002338514.fit" -> "476786357002338514"
    
    Returns:
        dict: {labelId: {"filename": ..., "size": ..., "size_kb": ...}}
    """
    existing = {}
    try:
        files = [f for f in os.listdir(download_dir) if f.endswith('.fit')]
    except FileNotFoundError:
        return existing
    
    for f in files:
        base = f.replace('.fit', '')
        if '_' in base:
            # 提取下划线后的最后一段（labelId）
            lid = base.rsplit('_', 1)[-1]
            if lid.isdigit():
                fpath = os.path.join(download_dir, f)
                size = os.path.getsize(fpath)
                existing[lid] = {
                    "filename": f,
                    "size": size,
                    "size_kb": round(size / 1024, 2)
                }
        elif base.isdigit():
            # 文件名就是 labelId.fit
            fpath = os.path.join(download_dir, f)
            size = os.path.getsize(fpath)
            existing[base] = {
                "filename": f,
                "size": size,
                "size_kb": round(size / 1024, 2)
            }
    
    return existing


def build_download_url(user_id, label_id):
    """构建 FIT 文件下载 URL"""
    return f"https://oss.coros.com/fit/{user_id}/{label_id}.fit"


def sanitize_filename(name):
    """移除或替换 Windows 文件名中的非法字符"""
    for ch in r'\/:*?"<>|':
        name = name.replace(ch, '_')
    return name


def download_file(url, filepath):
    """
    从 URL 下载文件到指定路径。
    
    Returns:
        tuple: (success: bool, size_bytes: int, error_msg: str)
    """
    try:
        req = Request(url, headers={'User-Agent': USER_AGENT})
        with urlopen(req, timeout=30) as response, open(filepath, 'wb') as out_file:
            data = response.read()
            out_file.write(data)
        return True, os.path.getsize(filepath), ""
    except HTTPError as e:
        return False, 0, f"HTTP {e.code}: {e.reason}"
    except URLError as e:
        return False, 0, f"URL Error: {e.reason}"
    except Exception as e:
        return False, 0, str(e)


def validate_fit_file(filepath, min_size):
    """
    FIT 文件完整性基础检查。
    
    检查项：
        - 文件大小 >= min_size
        - 文件不为空
    
    Returns:
        tuple: (valid: bool, issues: list[str])
    """
    issues = []
    size = os.path.getsize(filepath)
    
    if size == 0:
        issues.append("文件为空")
    elif size < min_size:
        issues.append(f"文件过小 ({size} bytes, 最小 {min_size})")
    
    return len(issues) == 0, issues


def main():
    # 加载配置
    config = load_config()
    
    parser = argparse.ArgumentParser(description='COROS Activity Downloader')
    parser.add_argument('--count', type=int, default=config.get("defaultCount", 10),
                        help=f'下载活动数量 (默认: {config.get("defaultCount", 10)})')
    parser.add_argument('--sport-type', type=int, default=config.get("sportType", 100),
                        help=f'运动类型筛选 (100=跑步, 默认: {config.get("sportType", 100)})')
    parser.add_argument('--download-dir', type=str, default=config.get("downloadDir"),
                        help=f'下载目录 (默认: {config.get("downloadDir")})')
    parser.add_argument('--user-id', type=str, default=config.get("userId"),
                        help='COROS 用户 ID')
    parser.add_argument('--label-ids', type=str, default=None,
                        help='直接指定 labelId 列表（逗号分隔）')
    parser.add_argument('--activities-json', type=str, default=None,
                        help='活动列表 JSON 字符串（从浏览器或 MCP 工具获取）')
    parser.add_argument('--validate-only', action='store_true',
                        help='仅验证现有文件，不下载')
    parser.add_argument('--json-output', action='store_true',
                        help='以 JSON 格式输出结果')
    parser.add_argument('--show-config', action='store_true',
                        help='显示当前配置并退出')
    
    args = parser.parse_args()
    
    # 显示配置模式
    if args.show_config:
        print(json.dumps(config, indent=2, ensure_ascii=False))
        return
    
    download_dir = setup_download_dir(args.download_dir)
    min_file_size = config.get("minFileSize", 1024)
    download_delay = config.get("downloadDelayMs", 500) / 1000
    
    # Step 1: 扫描现有文件
    existing = scan_existing_files(download_dir)
    
    if args.json_output:
        print(f"已扫描 {len(existing)} 个现有 FIT 文件", file=sys.stderr)
    else:
        print(f"\n{'='*50}")
        print(f"  COROS Activity Downloader")
        print(f"  下载目录: {download_dir}")
        print(f"  现有文件: {len(existing)}")
        print(f"{'='*50}\n")
    
    # Step 2: 确定要下载的活动
    activities = []
    
    if args.activities_json:
        # 使用提供的活动列表 JSON
        activities = json.loads(args.activities_json)
    elif args.label_ids:
        # 使用显式 labelId 列表
        for lid in args.label_ids.split(','):
            lid = lid.strip()
            if lid:
                activities.append({"labelId": lid, "name": f"Activity_{lid}", "sportType": args.sport_type})
    else:
        print("错误: 未指定活动。请使用 --activities-json 或 --label-ids 参数。",
              file=sys.stderr)
        print("提示: 使用 MCP 工具 mcp_coros_list_activities 获取活动列表。",
              file=sys.stderr)
        sys.exit(1)
    
    # Step 3: 分类 - 待下载 vs 已存在
    to_download = []
    skipped = []
    
    for act in activities:
        lid = act["labelId"]
        if lid in existing:
            skipped.append({**act, "existing_size_kb": existing[lid]["size_kb"]})
        else:
            to_download.append(act)
    
    if not args.json_output:
        print(f"分类结果:")
        for s in skipped:
            print(f"  [跳过] {s['name']} (已存在: {s.get('existing_size_kb', '?')} KB)")
        for t in to_download:
            print(f"  [待下载] {t['name']}")
        print(f"\n摘要: {len(to_download)} 待下载, {len(skipped)} 已跳过, {len(activities)} 总计\n")
    
    # Step 4: 仅验证模式
    if args.validate_only:
        if args.json_output:
            result = {
                "success": True,
                "mode": "validate_only",
                "existingCount": len(existing),
                "files": [
                    {"labelId": lid, **info}
                    for lid, info in existing.items()
                ]
            }
            print(json.dumps(result, indent=2, ensure_ascii=False))
        return
    
    # Step 5: 下载文件
    downloaded = []
    failed = []
    
    for i, act in enumerate(to_download):
        lid = act["labelId"]
        name = act.get("name", f"Activity_{lid}") or f"Activity_{lid}"
        url = build_download_url(args.user_id, lid)
        filename = sanitize_filename(f"{name}_{lid}.fit")
        filepath = os.path.join(download_dir, filename)
        
        if not args.json_output:
            print(f"[{i+1}/{len(to_download)}] 下载中: {name}...", end=" ")
        
        success, size, error = download_file(url, filepath)
        
        if success:
            is_valid, issues = validate_fit_file(filepath, min_file_size)
            if is_valid:
                downloaded.append({
                    "labelId": lid,
                    "name": name,
                    "fileName": filename,
                    "filePath": filepath,
                    "fileSize": size,
                    "fileSizeKB": round(size / 1024, 2),
                    "downloadUrl": url,
                    "status": "success",
                    "timestamp": datetime.utcnow().isoformat() + "Z"
                })
                if not args.json_output:
                    print(f"成功 ({size/1024:.2f} KB)")
            else:
                failed.append({
                    "labelId": lid,
                    "name": name,
                    "error": f"验证失败: {'; '.join(issues)}",
                    "errorCode": "VALIDATION_FAILED",
                    "timestamp": datetime.utcnow().isoformat() + "Z"
                })
                if not args.json_output:
                    print(f"警告: {'; '.join(issues)}")
        else:
            failed.append({
                "labelId": lid,
                "name": name,
                "error": error,
                "errorCode": "DOWNLOAD_FAILED",
                "timestamp": datetime.utcnow().isoformat() + "Z"
            })
            if not args.json_output:
                print(f"失败: {error}")
        
        # 延迟以避免限速
        time.sleep(download_delay)
    
    # Step 6: 最终摘要
    total_fit = len([f for f in os.listdir(download_dir) if f.endswith('.fit')])
    
    if args.json_output:
        result = {
            "success": len(failed) == 0,
            "totalCount": len(activities),
            "downloadedCount": len(downloaded),
            "skippedCount": len(skipped),
            "failedCount": len(failed),
            "downloadDir": download_dir,
            "totalFitFiles": total_fit,
            "files": downloaded,
            "skipped": [
                {"labelId": s["labelId"], "name": s["name"], "existingSizeKB": s.get("existing_size_kb")}
                for s in skipped
            ],
            "errors": failed,
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(f"\n{'='*50}")
        print(f"  下载完成!")
        print(f"{'='*50}")
        print(f"  总活动数:      {len(activities)}")
        print(f"  已下载:        {len(downloaded)}")
        print(f"  已跳过(存在):  {len(skipped)}")
        print(f"  失败:          {len(failed)}")
        print(f"  FIT 文件总数:  {total_fit}")
        print(f"{'='*50}")
        
        if failed:
            print(f"\n失败详情:")
            for f_item in failed:
                print(f"  - {f_item['name']} ({f_item['labelId']}): {f_item['error']}")


if __name__ == '__main__':
    main()
