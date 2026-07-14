#!/usr/bin/env python3
"""尝试访问 COROS API 获取活动列表"""

import json
import sys
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
USER_ID = "445542372294541312"

def try_api(url, desc):
    """尝试访问 API 端点"""
    print(f"\n尝试: {desc}")
    print(f"URL: {url}")
    try:
        req = Request(url, headers={'User-Agent': USER_AGENT})
        with urlopen(req, timeout=10) as response:
            data = response.read()
            print(f"状态: {response.status}")
            print(f"Content-Type: {response.headers.get('Content-Type', 'unknown')}")
            try:
                text = data.decode('utf-8')
                if len(text) > 500:
                    print(f"响应内容 (前500字符): {text[:500]}")
                else:
                    print(f"响应内容: {text}")
            except:
                print(f"响应大小: {len(data)} bytes")
            return True
    except HTTPError as e:
        print(f"HTTP 错误: {e.code} - {e.reason}")
        return False
    except URLError as e:
        print(f"URL 错误: {e.reason}")
        return False
    except Exception as e:
        print(f"错误: {e}")
        return False

def main():
    print("=" * 60)
    print("COROS API 探测")
    print("=" * 60)
    
    # 尝试常见的活动列表 API 端点
    endpoints = [
        (f"https://t.coros.com/admin/api/activity/list?sportType=100&page=1&size=15", "活动列表 API (admin/api)"),
        (f"https://t.coros.com/api/activity/list?sportType=100&page=1&size=15", "活动列表 API (api)"),
        (f"https://t.coros.com/gateway/activity/list?sportType=100&page=1&size=15", "活动列表 API (gateway)"),
        (f"https://s.coros.com/activity/getActivityList?sportType=100&pageSize=15", "活动列表 API (s.coros.com)"),
        (f"https://t.coros.com/admin/views/activities", "活动列表页面 (HTML)"),
    ]
    
    for url, desc in endpoints:
        try_api(url, desc)
    
    # 测试 FIT 文件下载 URL 格式
    test_label_id = "478503150718845430"
    fit_url = f"https://oss.coros.com/fit/{USER_ID}/{test_label_id}.fit"
    print(f"\n测试 FIT 下载 URL: {fit_url}")
    try:
        req = Request(fit_url, headers={'User-Agent': USER_AGENT})
        with urlopen(req, timeout=10) as response:
            data = response.read()
            print(f"状态: {response.status}, 大小: {len(data)} bytes")
    except Exception as e:
        print(f"错误: {e}")

if __name__ == '__main__':
    main()
