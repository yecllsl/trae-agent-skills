#!/usr/bin/env python3
"""尝试通过 COROS API 获取活动列表"""

import json
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"

def try_api(url, headers=None, method="GET", data=None):
    """尝试访问 API"""
    try:
        req_headers = {'User-Agent': USER_AGENT}
        if headers:
            req_headers.update(headers)
        
        req = Request(url, headers=req_headers, method=method)
        if data:
            req.data = data.encode('utf-8')
        
        with urlopen(req, timeout=15) as response:
            result = response.read().decode('utf-8')
            content_type = response.headers.get('Content-Type', '')
            return True, response.status, content_type, result
    except HTTPError as e:
        try:
            body = e.read().decode('utf-8')
        except:
            body = ''
        return False, e.code, '', body
    except Exception as e:
        return False, 0, '', str(e)

def main():
    print("=" * 70)
    print("COROS API 测试")
    print("=" * 70)
    
    user_id = "445542372294541312"
    
    endpoints = [
        # COROS Training Hub API
        ("https://t.coros.com/admin/activity/list", "POST", 
         {"Content-Type": "application/json", "Accept": "application/json"},
         json.dumps({"sportType": 100, "page": 1, "size": 15})),
        
        # teamcnapi
        ("https://teamcnapi.coros.com/activity/query?size=15&pageNumber=1&modeList=", 
         "GET", {"Accept": "application/json"}, None),
        
        # 尝试带 userId 的参数
        (f"https://teamcnapi.coros.com/activity/query?size=15&pageNumber=1&userId={user_id}", 
         "GET", {"Accept": "application/json"}, None),
        
        # s.coros.com API
        ("https://s.coros.com/activity/getActivityList?sportType=100&pageSize=15&page=1",
         "GET", {"Accept": "application/json"}, None),
    ]
    
    for url, method, headers, body in endpoints:
        print(f"\n[{method}] {url}")
        if body:
            print(f"  Body: {body[:100]}")
        
        success, status, content_type, result = try_api(url, headers, method, body)
        
        if success:
            print(f"  ✓ 状态: {status}, Content-Type: {content_type}")
            if 'json' in content_type.lower():
                try:
                    data = json.loads(result)
                    print(f"  JSON 响应 (前500字符): {json.dumps(data, ensure_ascii=False)[:500]}")
                except:
                    print(f"  响应 (前500字符): {result[:500]}")
            else:
                print(f"  响应 (前300字符): {result[:300]}")
        else:
            print(f"  ✗ 状态: {status}")
            if result:
                print(f"  响应 (前300字符): {result[:300]}")

if __name__ == '__main__':
    main()
