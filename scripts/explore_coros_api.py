#!/usr/bin/env python3
"""深入探索 COROS API 端点"""

import json
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
USER_ID = "445542372294541312"

def try_api(url, method="GET", headers=None):
    """尝试访问 API 端点"""
    try:
        req_headers = {'User-Agent': USER_AGENT}
        if headers:
            req_headers.update(headers)
        req = Request(url, headers=req_headers, method=method)
        with urlopen(req, timeout=10) as response:
            data = response.read()
            content_type = response.headers.get('Content-Type', '')
            if 'json' in content_type:
                text = data.decode('utf-8')
                return True, content_type, text[:1000]
            elif 'html' in content_type:
                return True, content_type, f"HTML页面, {len(data)} bytes"
            else:
                return True, content_type, f"{len(data)} bytes"
    except HTTPError as e:
        return False, f"HTTP {e.code}", str(e.reason)
    except Exception as e:
        return False, "Error", str(e)

def main():
    print("=" * 70)
    print("COROS API 深度探索")
    print("=" * 70)
    
    # 尝试各种 API 端点
    endpoints = [
        # Training Hub API 变体
        ("https://t.coros.com/admin/activity/list", "POST", {"Content-Type": "application/json"}, '{"sportType":100,"page":1,"size":15}'),
        ("https://t.coros.com/gateway/activity/list", "POST", {"Content-Type": "application/json"}, '{"sportType":100,"page":1,"size":15}'),
        
        # COROS 开放平台 API
        (f"https://s.coros.com/activity/getActivityList?userId={USER_ID}&sportType=100&page=1&pageSize=15", "GET", None, None),
        (f"https://s.coros.com/v1/activity/list?userId={USER_ID}", "GET", None, None),
        
        # oss.coros.com 相关
        (f"https://oss.coros.com/fit/{USER_ID}/", "GET", None, None),
        
        # API 子域名
        (f"https://api.coros.com/activity/list?userId={USER_ID}&sportType=100", "GET", None, None),
        (f"https://api.coros.cn/activity/list?userId={USER_ID}&sportType=100", "GET", None, None),
        
        # Training Hub 其他路径
        ("https://t.coros.com/admin/api/v1/activity/list", "GET", None, None),
        ("https://t.coros.com/traininghub/api/activity/list", "GET", None, None),
    ]
    
    for url, method, headers, body in endpoints:
        print(f"\n[{method}] {url}")
        if body:
            print(f"  Body: {body}")
        
        # 对于 POST 请求，需要编码 body
        if method == "POST" and body:
            try:
                from urllib.request import Request
                data = body.encode('utf-8')
                req = Request(url, data=data, headers=headers or {}, method=method)
                with urlopen(req, timeout=10) as response:
                    resp_data = response.read()
                    content_type = response.headers.get('Content-Type', '')
                    print(f"  ✓ {response.status} - {content_type}")
                    if 'json' in content_type:
                        print(f"  响应: {resp_data.decode('utf-8')[:500]}")
            except Exception as e:
                print(f"  ✗ {e}")
        else:
            success, status, info = try_api(url, method, headers)
            if success:
                print(f"  ✓ {status}")
                print(f"  {info}")
            else:
                print(f"  ✗ {status}: {info}")

if __name__ == '__main__':
    main()
