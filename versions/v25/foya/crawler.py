#!/usr/bin/env python3
"""
myfoya.com 全面爬虫
- 爬取全部页面（首页、关于、产品列表、产品详情）
- 下载所有图片
- 提取所有文本内容
"""

import requests
import re
import os
import time
import json
import urllib.parse
from collections import deque

BASE_URL = "http://www.myfoya.com/"
IMAGE_DIR = "/home/ubuntu/textools/foya/images"
OUTPUT_FILE = "/home/ubuntu/textools/foya/crawl_result.json"
PAGE_LIST_FILE = "/home/ubuntu/textools/foya/all_pages.txt"
PRODUCTS_FILE = "/home/ubuntu/textools/foya/products.txt"
SECTIONS_FILE = "/home/ubuntu/textools/foya/sections.txt"

visited = set()
all_pages = []
all_images = []
all_products = []
all_sections = []
failed = []

session = requests.Session()
session.headers.update({
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
})


def normalize_url(href, base=BASE_URL):
    """Convert relative URLs to absolute"""
    if not href or href.startswith('#') or href.startswith('javascript:'):
        return None
    absolute = urllib.parse.urljoin(base, href)
    # Remove fragment
    absolute = urllib.parse.urldefrag(absolute)[0]
    # Filter out external links and non-html resources
    parsed = urllib.parse.urlparse(absolute)
    if parsed.netloc and parsed.netloc != 'www.myfoya.com' and parsed.netloc != 'myfoya.com':
        return None
    # Only keep http/https
    if parsed.scheme not in ('http', 'https'):
        return None
    return absolute


def extract_links(html, base_url):
    """Extract all <a href> links from HTML"""
    links = set()
    for match in re.finditer(r'<a[^>]*href\s*=\s*["\']([^"\']+)["\']', html, re.IGNORECASE):
        url = normalize_url(match.group(1), base_url)
        if url:
            links.add(url)
    return links


def extract_images(html, base_url):
    """Extract all image URLs from HTML"""
    imgs = set()
    # <img src="...">
    for match in re.finditer(r'<img[^>]*src\s*=\s*["\']([^"\']+)["\']', html, re.IGNORECASE):
        url = normalize_url(match.group(1), base_url)
        if url and not url.startswith('data:'):
            imgs.add(url)
    # background-image: url(...)
    for match in re.finditer(r'background(?:-image)?\s*:\s*[^;]*?url\s*\(\s*["\']?([^"\')\s]+)["\']?\s*\)', html, re.IGNORECASE):
        url = normalize_url(match.group(1), base_url)
        if url and not url.startswith('data:'):
            imgs.add(url)
    return imgs


def extract_title(html):
    """Extract page title"""
    m = re.search(r'<title[^>]*>([^<]+)</title>', html, re.IGNORECASE)
    return m.group(1).strip() if m else "No Title"


def extract_sections(html):
    """Extract text content from each section/div on the page"""
    sections = []
    # Find all div sections with text content
    divs = re.finditer(r'<(div|section|header|footer|article)[^>]*>(.*?)</\1>', html, re.IGNORECASE | re.DOTALL)
    for i, m in enumerate(divs):
        tag = m.group(1)
        inner = m.group(2)
        # Get any heading
        heading = ''
        hm = re.search(r'<h[1-6][^>]*>([^<]+)</h[1-6]>', inner, re.IGNORECASE)
        if hm:
            heading = hm.group(1).strip()
        # Extract visible text (strip tags)
        text = re.sub(r'<[^>]+>', ' ', inner)
        text = re.sub(r'\s+', ' ', text).strip()
        if text and len(text) > 20:
            sections.append({
                'tag': tag,
                'heading': heading,
                'text': text[:500],
            })
    return sections


def extract_products(html, url):
    """Extract product info from a page"""
    products = []
    
    # Look for product items (common patterns)
    product_items = re.finditer(
        r'<(?:div|li|article)[^>]*class\s*=\s*["\'][^"\']*product[^"\']*["\'][^>]*>'
        r'(.*?)</(?:div|li|article)>',
        html, re.IGNORECASE | re.DOTALL
    )
    
    for m in product_items:
        block = m.group(1)
        name = ''
        desc = ''
        
        # Name from heading or alt or title
        nm = re.search(r'<h[1-6][^>]*>([^<]+)</h[1-6]>', block, re.IGNORECASE)
        if nm:
            name = nm.group(1).strip()
        if not name:
            nm = re.search(r'<img[^>]*alt\s*=\s*["\']([^"\']+)["\']', block, re.IGNORECASE)
            if nm:
                name = nm.group(1).strip()
        if not name:
            nm = re.search(r'class\s*=\s*["\'][^"\']*name[^"\']*["\'][^>]*>([^<]+)<', block, re.IGNORECASE)
            if nm:
                name = nm.group(1).strip()
        
        # Description (text after name, first substantial text)
        desc_text = re.sub(r'<[^>]+>', ' ', block)
        desc_text = re.sub(r'\s+', ' ', desc_text).strip()
        if name and name in desc_text:
            desc_text = desc_text.replace(name, '', 1).strip()
        desc_text = desc_text.strip(':- \t\n')
        if desc_text and len(desc_text) > 10:
            desc = desc_text[:300]
        elif desc_text:
            desc = desc_text
        
        if name:
            products.append({'name': name, 'description': desc, 'source_url': url})
    
    # Also try simpler pattern: any h2/h3/h4 followed by a paragraph
    if not products:
        headings = re.finditer(r'<h([2-4])[^>]*>([^<]+)</h[2-4]>', html, re.IGNORECASE)
        for hm in headings:
            name = hm.group(2).strip()
            # Look for the next paragraph
            after = html[hm.end():]
            pm = re.search(r'<p[^>]*>(.*?)</p>', after, re.IGNORECASE | re.DOTALL)
            desc = ''
            if pm:
                desc = re.sub(r'<[^>]+>', ' ', pm.group(1))
                desc = re.sub(r'\s+', ' ', desc).strip()[:300]
            if name and len(name) > 2:
                products.append({'name': name, 'description': desc, 'source_url': url})
    
    return products


def download_image(img_url, page_url):
    """Download a single image"""
    try:
        parsed = urllib.parse.urlparse(img_url)
        path = parsed.path
        if not path or path == '/':
            return None
        
        # Create filename from path
        basename = os.path.basename(path)
        if not basename or '.' not in basename:
            basename = f"img_{hash(img_url) & 0xFFFFFFFF:08x}.jpg"
        
        # Avoid duplicate names by prepending directory hash
        dir_hash = hashlib.md5(os.path.dirname(path).encode()).hexdigest()[:6]
        filename = f"{dir_hash}_{basename}"
        filepath = os.path.join(IMAGE_DIR, filename)
        
        # Skip if already downloaded
        if os.path.exists(filepath) and os.path.getsize(filepath) > 0:
            return filepath
        
        r = session.get(img_url, timeout=15, stream=True)
        if r.status_code == 200:
            ct = r.headers.get('Content-Type', '')
            if 'image' not in ct:
                return None
            with open(filepath, 'wb') as f:
                for chunk in r.iter_content(1024):
                    f.write(chunk)
            time.sleep(0.1)
            return filepath
    except Exception as e:
        return None


import hashlib

def crawl():
    queue = deque([BASE_URL])
    visited.add(BASE_URL)
    
    while queue:
        url = queue.popleft()
        print(f"\n[{len(visited)}] Crawling: {url}")
        
        try:
            r = session.get(url, timeout=20)
            r.encoding = r.apparent_encoding or 'utf-8'
            
            if r.status_code != 200:
                print(f"  FAILED: HTTP {r.status_code}")
                failed.append({'url': url, 'status': r.status_code})
                continue
            
            html = r.text
            title = extract_title(html)
            print(f"  Title: {title}")
            
            page_info = {
                'url': url,
                'title': title,
                'content_length': len(html),
            }
            all_pages.append(page_info)
            
            # Extract sections
            sections = extract_sections(html)
            all_sections.extend([{**s, 'page_url': url} for s in sections])
            
            # Extract products
            products = extract_products(html, url)
            all_products.extend(products)
            
            # Extract images
            imgs = extract_images(html, url)
            print(f"  Found {len(imgs)} images")
            
            for img_url in imgs:
                filepath = download_image(img_url, url)
                all_images.append({
                    'url': img_url,
                    'page_url': url,
                    'filepath': filepath,
                    'downloaded': filepath is not None,
                })
                if filepath:
                    print(f"    Downloaded: {os.path.basename(filepath)}")
            
            # Extract links for further crawling
            links = extract_links(html, url)
            for link in links:
                if link not in visited:
                    # Only crawl same domain paths
                    parsed = urllib.parse.urlparse(link)
                    if parsed.path and not parsed.path.endswith(('.pdf', '.zip', '.rar', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx', '.exe')):
                        visited.add(link)
                        queue.append(link)
            
            time.sleep(0.3)  # Be polite
            
        except Exception as e:
            print(f"  ERROR: {e}")
            failed.append({'url': url, 'error': str(e)})


def save_results():
    result = {
        'total_pages': len(all_pages),
        'total_images_found': len(all_images),
        'total_images_downloaded': sum(1 for i in all_images if i['downloaded']),
        'total_products': len(all_products),
        'total_sections': len(all_sections),
        'failed_pages': len(failed),
        'pages': all_pages,
        'images': all_images,
        'products': all_products,
        'sections': all_sections,
        'failed': failed,
    }
    
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    
    # Pages list
    with open(PAGE_LIST_FILE, 'w', encoding='utf-8') as f:
        for p in all_pages:
            f.write(f"{p['url']}\n  Title: {p['title']}\n\n")
    
    # Products list
    with open(PRODUCTS_FILE, 'w', encoding='utf-8') as f:
        for p in all_products:
            f.write(f"Product: {p['name']}\n")
            f.write(f"  URL: {p['source_url']}\n")
            f.write(f"  Description: {p['description']}\n\n")
    
    # Sections
    with open(SECTIONS_FILE, 'w', encoding='utf-8') as f:
        for s in all_sections:
            f.write(f"[{s['tag']}] ({s['page_url']})\n")
            if s['heading']:
                f.write(f"  Heading: {s['heading']}\n")
            f.write(f"  Text: {s['text'][:500]}\n\n")
    
    print(f"\n{'='*60}")
    print(f"爬取完成!")
    print(f"总计页面: {len(all_pages)}")
    print(f"图片发现/下载: {len(all_images)} / {sum(1 for i in all_images if i['downloaded'])}")
    print(f"产品/板块: {len(all_products)} / {len(all_sections)}")
    print(f"失败: {len(failed)}")
    print(f"{'='*60}")
    print(f"结果文件: {OUTPUT_FILE}")
    print(f"页面列表: {PAGE_LIST_FILE}")
    print(f"产品列表: {PRODUCTS_FILE}")
    print(f"板块内容: {SECTIONS_FILE}")
    print(f"图片目录: {IMAGE_DIR}")


if __name__ == '__main__':
    crawl()
    save_results()
