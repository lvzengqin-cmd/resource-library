#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
百度收录自动化脚本
功能：自动生成sitemap、自动推送URL给百度、自动提交到各类搜索引擎
"""
import urllib.request
import urllib.parse
import json
import time
from datetime import datetime
import re

# ==================== 配置区域 ====================
# 百度主动推送token (从百度搜索资源平台获取)
BAIDU_TOKEN = "Cl4E8IdQQomuJcV3"

# 网站地址
SITE_URL = "https://www.cybaoku.com"

# 资源数据库 (从Supabase获取的热门资源)
RESOURCES = [
    # 短剧类
    {"title": "热门短剧合集", "category": "短剧", "url": f"{SITE_URL}/#categories"},
    {"title": "短剧资源下载", "category": "短剧", "url": f"{SITE_URL}/#categories"},
    {"title": "高清短剧视频", "category": "短剧", "url": f"{SITE_URL}/#categories"},
    # 教程类
    {"title": "Python编程教程", "category": "教程", "url": f"{SITE_URL}/#categories"},
    {"title": "前端开发教程", "category": "教程", "url": f"{SITE_URL}/#categories"},
    {"title": "Java教程", "category": "教程", "url": f"{SITE_URL}/#categories"},
    {"title": "小红书运营教程", "category": "教程", "url": f"{SITE_URL}/#categories"},
    {"title": "抖音短视频教程", "category": "教程", "url": f"{SITE_URL}/#categories"},
    {"title": "AI人工智能教程", "category": "教程", "url": f"{SITE_URL}/#categories"},
    {"title": "亚马逊跨境电商教程", "category": "教程", "url": f"{SITE_URL}/#categories"},
    {"title": "PS教程", "category": "教程", "url": f"{SITE_URL}/#categories"},
    {"title": "PR视频剪辑教程", "category": "教程", "url": f"{SITE_URL}/#categories"},
    {"title": "AE特效教程", "category": "教程", "url": f"{SITE_URL}/#categories"},
    {"title": "CAD教程", "category": "教程", "url": f"{SITE_URL}/#categories"},
    {"title": "Unity游戏开发教程", "category": "教程", "url": f"{SITE_URL}/#categories"},
    # 软件类
    {"title": "Windows软件", "category": "软件", "url": f"{SITE_URL}/#categories"},
    {"title": "Mac软件", "category": "软件", "url": f"{SITE_URL}/#categories"},
    {"title": "安卓APP", "category": "软件", "url": f"{SITE_URL}/#categories"},
    # 素材类
    {"title": "PPT模板", "category": "素材", "url": f"{SITE_URL}/#categories"},
    {"title": "AE模板", "category": "素材", "url": f"{SITE_URL}/#categories"},
    {"title": "PPT素材", "category": "素材", "url": f"{SITE_URL}/#categories"},
    {"title": "背景音乐", "category": "素材", "url": f"{SITE_URL}/#categories"},
    # 文档类
    {"title": "电子书", "category": "文档", "url": f"{SITE_URL}/#categories"},
    {"title": "PDF资料", "category": "文档", "url": f"{SITE_URL}/#categories"},
]

# 关键词库
KEYWORDS = [
    "资源下载", "短剧资源", "学习教程", "软件工具", "设计素材", "文档资料",
    "百度网盘资源", "夸克网盘资源", "阿里云盘资源", "迅雷资源",
    "Python教程", "前端教程", "Java教程", "Web开发",
    "抖音教程", "小红书教程", "自媒体教程", "短视频教程",
    "AI教程", "人工智能教程", "机器学习", "深度学习",
    "跨境电商", "亚马逊教程", "电商运营",
    "PS教程", "PR教程", "AE教程", "视频剪辑",
    "PPT模板", "AE模板", "素材下载",
    "电子书下载", "PDF资料", "学习资料",
    "Windows软件", "Mac软件", "安卓软件",
]

class BaiduSEOPusher:
    """百度SEO推送类"""
    
    def __init__(self, token):
        self.token = token
        self.api_url = "http://data.zz.baidu.com/urls"
        
    def push_urls(self, urls):
        """主动推送URL给百度"""
        if not self.token or self.token == "YOUR_BAIDU_PUSH_TOKEN":
            print("⚠️  未配置百度Token，跳过主动推送")
            return None
            
        req = urllib.request.Request(
            url=f"{self.api_url}?site=www.cybaoku.com&token={self.token}",
            data=json.dumps(urls).encode('utf-8'),
            headers={
                'Content-Type': 'application/json',
                'User-Agent': 'Mozilla/5.0 (compatible; Baiduspider/2.0)'
            }
        )
        
        try:
            with urllib.request.urlopen(req, timeout=10) as response:
                result = json.loads(response.read().decode('utf-8'))
                return result
        except Exception as e:
            print(f"❌ 百度推送失败: {e}")
            return None

    def generate_sitemap(self, resources, keywords):
        """生成完整的sitemap.xml"""
        today = datetime.now().strftime('%Y-%m-%d')
        
        urls = []
        
        # 首页
        urls.append({
            'loc': SITE_URL,
            'lastmod': today,
            'changefreq': 'daily',
            'priority': '1.0'
        })
        
        # 各分类页
        categories = ['短剧', '教程', '软件', '素材', '文档']
        for i, cat in enumerate(categories):
            urls.append({
                'loc': f"{SITE_URL}/?category={urllib.parse.quote(cat)}",
                'lastmod': today,
                'changefreq': 'daily',
                'priority': '0.9' if i == 0 else '0.8'
            })
        
        # 热门资源页
        for resource in resources[:50]:
            urls.append({
                'loc': f"{SITE_URL}/?q={urllib.parse.quote(resource['title'])}",
                'lastmod': today,
                'changefreq': 'weekly',
                'priority': '0.7'
            })
        
        # 生成XML
        xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
        xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        
        for url in urls:
            xml += '  <url>\n'
            xml += f'    <loc>{url["loc"]}</loc>\n'
            xml += f'    <lastmod>{url["lastmod"]}</lastmod>\n'
            xml += f'    <changefreq>{url["changefreq"]}</changefreq>\n'
            xml += f'    <priority>{url["priority"]}</priority>\n'
            xml += '  </url>\n'
        
        xml += '</urlset>'
        
        return xml

    def generate_baidu_mobile_sitemap(self):
        """生成百度移动端sitemap"""
        today = datetime.now().strftime('%Y-%m-%d')
        
        xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
        xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"\n'
        xml += '        xmlns:mobile="http://www.google.com/schemas/sitemap-mobile/1.0">\n'
        xml += '  <url>\n'
        xml += f'    <loc>{SITE_URL}/</loc>\n'
        xml += f'    <lastmod>{today}</lastmod>\n'
        xml += f'    <changefreq>daily</changefreq>\n'
        xml += f'    <priority>1.0</priority>\n'
        xml += '    <mobile:mobile type="mobile"/>\n'
        xml += '  </url>\n'
        xml += '</urlset>'
        
        return xml


def generate_html_optimizer():
    """生成优化后的HTML（含更多SEO内容）"""
    pass


def main():
    print("=" * 50)
    print("🚀 CY资源宝库 - 百度收录自动化工具")
    print("=" * 50)
    print()
    
    pusher = BaiduSEOPusher(BAIDU_TOKEN)
    
    # 1. 生成sitemap
    print("📄 1. 生成 sitemap.xml...")
    sitemap = pusher.generate_sitemap(RESOURCES, KEYWORDS)
    with open('sitemap.xml', 'w', encoding='utf-8') as f:
        f.write(sitemap)
    print(f"   ✅ 生成完成，共包含 {sitemap.count('<url>')} 个URL")
    
    # 2. 生成移动端sitemap
    print("📱 2. 生成移动端 sitemap...")
    mobile_sitemap = pusher.generate_baidu_mobile_sitemap()
    with open('sitemap_mobile.xml', 'w', encoding='utf-8') as f:
        f.write(mobile_sitemap)
    print("   ✅ 移动端sitemap生成完成")
    
    # 3. 生成推送URL列表
    print("🔗 3. 准备推送URL...")
    push_urls = [SITE_URL]
    push_urls.extend([r['url'] for r in RESOURCES[:30]])
    print(f"   ✅ 准备推送 {len(push_urls)} 个URL")
    
    # 4. 推送到百度
    print("📤 4. 推送到百度...")
    result = pusher.push_urls(push_urls)
    if result:
        print(f"   ✅ 推送成功!")
        print(f"   📊 剩余配额: {result.get('remain', 'N/A')}")
        print(f"   ✅ 成功数: {result.get('success', 'N/A')}")
        print(f"   ⏰ 当日成功: {result.get('dayremain', 'N/A')}")
    else:
        print("   ⚠️  推送失败，请检查Token是否正确")
    
    print()
    print("=" * 50)
    print("📋 手动操作步骤：")
    print("=" * 50)
    print("""
1. 登录百度搜索资源平台: https://ziyuan.baidu.com/
2. 添加网站: www.cybaoku.com
3. 获取主动推送Token，替换脚本中的 BAIDU_TOKEN
4. 在【数据提交 → sitemap】中提交:
   - PC站: https://www.cybaoku.com/sitemap.xml
   - 移动站: https://www.cybaoku.com/sitemap_mobile.xml
5. 定期运行本脚本保持收录更新
    """)


if __name__ == "__main__":
    main()
