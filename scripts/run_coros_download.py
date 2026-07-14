#!/usr/bin/env python3
"""
COROS 活动下载执行脚本
从现有文件提取 labelId，尝试发现新活动并下载
"""

import json
import os
import sys
import subprocess
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

# 配置
SCRIPT_DIR = Path(__file__).parent.resolve()
DOWNLOAD_DIR = "D:/yecll/Downloads/coros/test-fit-files"
USER_ID = "445542372294541312"
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
PYTHON_PATH = r"d:\yecll\Documents\LocalCode\testskills\.venv\Scripts\python.exe"
DOWNLOAD_SCRIPT = r"d:\yecll\Documents\LocalCode\testskills\skills\coros-activity-downloader\scripts\download_coros.py"

def scan_existing_label_ids(download_dir):
    """扫描现有 FIT 文件，提取 labelId 列表"""
    label_ids = []
    try:
        files = [f for f in os.listdir(download_dir) if f.endswith('.fit')]
    except FileNotFoundError:
        return label_ids
    
    for f in files:
        base = f.replace('.fit', '')
        if '_' in base:
            lid = base.rsplit('_', 1)[-1]
            if lid.isdigit():
                label_ids.append(lid)
        elif base.isdigit():
            label_ids.append(base)
    
    return sorted(set(label_ids), key=lambda x: int(x), reverse=True)

def check_activity_exists(user_id, label_id):
    """检查活动 FIT 文件是否存在（通过 HEAD 请求）"""
    url = f"https://oss.coros.com/fit/{user_id}/{label_id}.fit"
    try:
        req = Request(url, headers={'User-Agent': USER_AGENT}, method='HEAD')
        with urlopen(req, timeout=10) as response:
            return response.status == 200, response.headers.get('Content-Length', 'unknown')
    except HTTPError as e:
        if e.code == 404:
            return False, None
        return False, f"HTTP {e.code}"
    except Exception as e:
        return False, str(e)

def discover_new_activities(user_id, existing_ids, try_count=50, step=1):
    """
    通过递增 labelId 尝试发现新活动。
    
    从最大的 labelId 开始，尝试后续的 labelId。
    """
    if not existing_ids:
        print("没有现有文件，无法发现新活动")
        return []
    
    max_id = max(int(lid) for lid in existing_ids)
    print(f"当前最大 labelId: {max_id}")
    print(f"尝试发现新活动（从 {max_id + 1} 开始，尝试 {try_count} 个）...")
    
    new_activities = []
    for i in range(1, try_count + 1):
        test_id = str(max_id + i * step)
        exists, size = check_activity_exists(user_id, test_id)
        if exists:
            print(f"  ✓ 发现新活动: {test_id} (大小: {size} bytes)")
            new_activities.append({
                "labelId": test_id,
                "name": f"Activity_{test_id}",
                "sportType": 100
            })
        else:
            print(f"  ✗ {test_id}: 不存在 ({size})")
        
        if i % 10 == 0:
            print(f"  已检查 {i}/{try_count}...")
    
    return new_activities

def run_download_script(activities, download_dir, json_output=True):
    """调用下载脚本执行下载"""
    if not activities:
        print("没有需要下载的活动")
        return None
    
    activities_json = json.dumps(activities, ensure_ascii=False)
    
    cmd = [
        PYTHON_PATH,
        DOWNLOAD_SCRIPT,
        "--activities-json", activities_json,
        "--download-dir", download_dir,
    ]
    if json_output:
        cmd.append("--json-output")
    
    print(f"\n执行下载脚本，下载 {len(activities)} 个活动...")
    print(f"命令: {' '.join(cmd[:4])} ...")
    
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            encoding='utf-8'
        )
        
        if result.stderr:
            print("STDERR:", result.stderr, file=sys.stderr)
        
        if json_output and result.stdout:
            try:
                return json.loads(result.stdout)
            except json.JSONDecodeError:
                print("解析 JSON 输出失败")
                print("STDOUT:", result.stdout)
                return None
        else:
            print(result.stdout)
            return None
    except Exception as e:
        print(f"执行脚本失败: {e}")
        return None

def main():
    print("=" * 60)
    print("COROS 跑步活动下载任务")
    print("=" * 60)
    
    # Step 1: 扫描现有文件
    print(f"\n[步骤1] 扫描下载目录: {DOWNLOAD_DIR}")
    existing_ids = scan_existing_label_ids(DOWNLOAD_DIR)
    print(f"现有 FIT 文件: {len(existing_ids)} 个")
    
    if existing_ids:
        print(f"最新的 10 个 labelId:")
        for lid in existing_ids[:10]:
            print(f"  - {lid}")
    
    # Step 2: 尝试发现新活动
    print(f"\n[步骤2] 尝试发现新活动...")
    print("注意: 由于 Chrome DevTools MCP 不可用，使用 labelId 递增探测方式")
    
    new_activities = discover_new_activities(USER_ID, existing_ids, try_count=30, step=1)
    print(f"\n发现 {len(new_activities)} 个新活动")
    
    # 如果没有发现新活动，使用已有的前 15 个 labelId 测试去重功能
    if not new_activities:
        print("\n未发现新活动，使用现有活动测试去重功能...")
        test_activities = []
        for lid in existing_ids[:15]:
            test_activities.append({
                "labelId": lid,
                "name": f"Activity_{lid}",
                "sportType": 100
            })
        
        # 再加一个不存在的 labelId 来测试下载失败场景
        test_activities.append({
            "labelId": "999999999999999999",
            "name": "Test_Nonexistent",
            "sportType": 100
        })
        
        activities = test_activities
        print(f"测试活动数: {len(activities)} (15个已有 + 1个不存在)")
    else:
        activities = new_activities
    
    # Step 3: 执行下载
    print(f"\n[步骤3] 执行下载脚本...")
    result = run_download_script(activities, DOWNLOAD_DIR, json_output=True)
    
    # Step 4: 输出结果
    print(f"\n[步骤4] 下载结果:")
    if result:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print("无法获取 JSON 结果")
    
    # 统计最终文件数
    final_count = len(scan_existing_label_ids(DOWNLOAD_DIR))
    print(f"\n最终 FIT 文件总数: {final_count}")

if __name__ == '__main__':
    main()
