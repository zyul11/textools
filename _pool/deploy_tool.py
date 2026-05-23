#!/usr/bin/env python3
"""
deploy_tool.py — Post-generation pipeline for new textools.site tools.

Usage: python3 _pool/deploy_tool.py <slug>

What it does:
1. Copies {slug}.html from root → versions/dev/
2. Updates EN index.html: adds card to correct grid section + footer link + seo list
3. Updates ja/ko/zh-hk index.html: adds coming-soon card
4. Regenerates sitemap.xml
5. Marks tool as done=true in pool
6. Runs deploy.sh textools
"""

import json
import os
import re
import sys
import subprocess
from pathlib import Path
from datetime import datetime

ROOT = '/home/ubuntu/textools'
POOL_FILE = os.path.join(ROOT, '_pool', 'tool-ideas.json')
DEV_DIR = os.path.join(ROOT, 'versions', 'dev')
LANGUAGES = ['ja', 'ko', 'zh-hk']
CATEGORY_LABELS = {
    'text-analysis': '📝 文字分析',
    'text-processing': '🔧 文字處理',
    'encoding-conversion': '🔣 編碼與轉換',
    'utilities': '🛠️ 工具',
}
# Order matters — these map to the English sec-title labels
EN_CATEGORY_MAP = {
    '📝 Text Analysis': 'text-analysis',
    '📝 文字分析': 'text-analysis',
    '📝 テキスト分析': 'text-analysis',
    '📝 텍스트 분석': 'text-analysis',
    '🔧 Text Processing': 'text-processing',
    '🔧 文字處理': 'text-processing',
    '🔧 テキスト処理': 'text-processing',
    '🔧 텍스트 처리': 'text-processing',
    '🔣 Encoding & Conversion': 'encoding-conversion',
    '🔣 編碼與轉換': 'encoding-conversion',
    '🔣 エンコード・変換': 'encoding-conversion',
    '🔣 인코딩 및 변환': 'encoding-conversion',
    '🛠️ Utilities': 'utilities',
    '🛠️ 工具': 'utilities',
    '🛠️ ユーティリティ': 'utilities',
    '🛠️ 유틸리티': 'utilities',
}


def get_pool_item(slug):
    with open(POOL_FILE) as f:
        pool = json.load(f)
    for item in pool:
        if item['slug'] == slug:
            return item, pool
    return None, None


def save_pool(pool):
    with open(POOL_FILE, 'w') as f:
        json.dump(pool, f, indent=2, ensure_ascii=False)


def card_html(slug, emoji, keyword, desc, lang=''):
    prefix = '/' + lang + '/' if lang else '/'
    return f'''    <a href="{prefix}{slug}.html" class="card">
      <div class="icon">{emoji}</div>
      <h3>{keyword}</h3>
      <p>{desc}</p>
    </a>'''


def coming_soon_card(name, lang=''):
    labels = {
        'ja': {'badge': '準備中'},
        'ko': {'badge': '준비 중'},
        'zh-hk': {'badge': '即將推出'},
    }
    badge = labels.get(lang, {}).get('badge', 'Coming Soon')
    return f'''    <a href="#" class="card coming-soon">
      <div class="icon">🚧</div>
      <h3>{name}</h3>
      <p>{badge}</p>
    </a>'''


def insert_into_grid(html, category, card_text):
    """
    Find the correct category's grid div and insert card before closing </div>.
    Pattern: sec-title line followed by grid div.
    """
    # Find all sec-title lines with their positions
    sec_pattern = re.compile(r'<div class="sec-title">([^<]+)</div>\s*<div class="grid">')
    
    matches = list(sec_pattern.finditer(html))
    found = False
    for m in matches:
        title_text = m.group(1).strip()
        if title_text in EN_CATEGORY_MAP and EN_CATEGORY_MAP[title_text] == category:
            # Found the right category grid
            grid_start = m.end()
            # Find the closing </div> of this grid
            # Count nested divs from grid_start
            depth = 1
            pos = grid_start
            while depth > 0 and pos < len(html):
                next_open = html.find('<div', pos)
                next_close = html.find('</div>', pos)
                if next_close == -1:
                    break
                if next_open != -1 and next_open < next_close:
                    depth += 1
                    pos = next_open + 5
                else:
                    depth -= 1
                    if depth == 0:
                        # Insert card before this closing </div>
                        insert_pos = next_close
                        html = html[:insert_pos] + card_text + '\n  ' + html[insert_pos:]
                        found = True
                        break
                    pos = next_close + 6
            break
    
    return html, found


def insert_footer_link(html, slug, keyword):
    """Add a link to the footer link list, before the <br><br>."""
    link = f'<a href="/{slug}.html">{keyword}</a> ·'
    # Find <br><br> in footer div
    footer_match = re.search(r'(<div class="footer">.*?)<br>\s*<br>', html, re.DOTALL)
    if footer_match:
        pos = footer_match.start(1)
        # Find the end of the first line of links (before <br>)
        footer_content = footer_match.group(1)
        # Insert after the last · link
        insert_after = footer_content.rstrip()
        old = insert_after
        new = insert_after + '\n    ' + link
        html = html.replace(old, new, 1)
    return html


def insert_seo_list_item(html, slug, keyword, lang=''):
    """Add a link to the SEO section's ul, before closing </ul>."""
    prefix = '/' + lang + '/' if lang else '/'
    li = f'      <li><a href="{prefix}{slug}.html">{keyword}</a></li>\n'
    # Find the last </ul> before closing </div> of seo-section
    # Actually just find the last </ul>
    ul_end = html.rfind('</ul>')
    if ul_end != -1:
        html = html[:ul_end] + li + html[ul_end:]
    return html


def update_en_index(slug, emoji, keyword, desc, category):
    path = os.path.join(ROOT, 'index.html')
    with open(path) as f:
        html = f.read()
    
    card = card_html(slug, emoji, keyword, desc)
    
    # Insert card into correct grid section
    html, found = insert_into_grid(html, category, card)
    if not found:
        print(f"  ⚠️  Could not find category '{category}' grid in EN index, appending to last grid")
        # Append to last grid as fallback
        last_grid_end = html.rfind('</div>\n\n  <div class="sec-title"')
        if last_grid_end == -1:
            last_grid_end = html.rfind('</div>\n\n  <div class="lang-links"')
        if last_grid_end != -1:
            # Go back to find the grid before this
            grid_end = html.rfind('</div>', 0, last_grid_end)
            if grid_end != -1:
                grid_start = html.rfind('<div class="grid">', 0, grid_end)
                if grid_start != -1:
                    insert_pos = html.rfind('</div>', grid_start, grid_end)
                    html = html[:insert_pos] + card + '\n  ' + html[insert_pos:]
                    found = True
    
    # Insert footer link
    html = insert_footer_link(html, slug, keyword)
    
    # Insert SEO section list item
    html = insert_seo_list_item(html, slug, keyword)
    
    with open(path, 'w') as f:
        f.write(html)
    print(f"  ✅ EN index.html updated ({'found grid' if found else 'fallback'})")


def update_lang_index(lang, slug, keyword):
    """Add a coming-soon card to a language index page."""
    path = os.path.join(ROOT, lang, 'index.html')
    if not os.path.exists(path):
        print(f"  ⚠️  {lang}/index.html not found, skipping")
        return
    
    with open(path) as f:
        html = f.read()
    
    # Map language-specific category names
    lang_cat_map = {
        'ja': {
            '📝 テキスト分析': 'text-analysis',
            '🔧 テキスト処理': 'text-processing',
            '🔣 エンコード・変換': 'encoding-conversion',
            '🛠️ ユーティリティ': 'utilities',
        },
        'ko': {
            '📝 텍스트 분석': 'text-analysis',
            '🔧 텍스트 처리': 'text-processing',
            '🔣 인코딩 및 변환': 'encoding-conversion',
            '🛠️ 유틸리티': 'utilities',
        },
        'zh-hk': {
            '📝 文字分析': 'text-analysis',
            '🔧 文字處理': 'text-processing',
            '🔣 編碼與轉換': 'encoding-conversion',
            '🛠️ 工具': 'utilities',
        },
    }
    
    # Try to insert in the last grid section (Utilities)
    cat_map = lang_cat_map.get(lang, {})
    target_cat = 'utilities'
    card = coming_soon_card(keyword, lang)
    
    found_cat = None
    for title, cat in cat_map.items():
        if cat == target_cat:
            found_cat = title
            break
    
    if found_cat:
        sec_pattern = re.compile(r'<div class="sec-title">([^<]+)</div>\s*<div class="grid">')
        matches = list(sec_pattern.finditer(html))
        for m in matches:
            if m.group(1).strip() == found_cat:
                grid_start = m.end()
                depth = 1
                pos = grid_start
                while depth > 0 and pos < len(html):
                    next_open = html.find('<div', pos)
                    next_close = html.find('</div>', pos)
                    if next_close == -1:
                        break
                    if next_open != -1 and next_open < next_close:
                        depth += 1
                        pos = next_open + 5
                    else:
                        depth -= 1
                        if depth == 0:
                            html = html[:next_close] + card + '\n  ' + html[next_close:]
                            break
                        pos = next_close + 6
                break
    
    with open(path, 'w') as f:
        f.write(html)
    print(f"  ✅ {lang}/index.html updated")


def generate_sitemap():
    """Regenerate sitemap.xml by scanning filesystem."""
    urls = []
    base = 'https://textools.site'
    
    # Root tool pages
    for f in sorted(os.listdir(ROOT)):
        if f.endswith('.html') and f != '404.html':
            slug = f[:-5]
            if slug in ('privacy', 'terms', 'fortuna-preview'):
                continue
            urls.append(f'{base}/{f}')
            # Language versions
            for lang in LANGUAGES:
                lang_path = os.path.join(ROOT, lang, f)
                if os.path.exists(lang_path):
                    urls.append(f'{base}/{lang}/{f}')
    
    # Language homepages
    for lang in LANGUAGES:
        if os.path.exists(os.path.join(ROOT, lang, 'index.html')):
            urls.append(f'{base}/{lang}/')
    
    # Articles
    articles_dir = os.path.join(ROOT, 'articles')
    for root, dirs, files in os.walk(articles_dir):
        for f in sorted(files):
            if f.endswith('.html'):
                rel = os.path.relpath(os.path.join(root, f), ROOT)
                urls.append(f'{base}/{rel}')
    
    # SEO audit subdirectory
    seo_dir = os.path.join(ROOT, 'seo-audit')
    if os.path.exists(seo_dir):
        for root, dirs, files in os.walk(seo_dir):
            for f in sorted(files):
                if f.endswith('.html'):
                    rel = os.path.relpath(os.path.join(root, f), ROOT)
                    urls.append(f'{base}/{rel}')
    
    # Homepage
    if '/index.html' in urls[0] if urls else '':
        pass
    
    # Build XML
    lines = ['<?xml version="1.0" encoding="UTF-8"?>']
    lines.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')
    lines.append(f'  <url>\n    <loc>{base}/</loc>\n    <priority>0.9</priority>\n  </url>')
    
    for url in sorted(set(urls)):
        if url == f'{base}/':
            continue
        if url.endswith('index.html'):
            continue
        prio = '0.6' if '/articles/' in url else '0.8'
        lines.append(f'  <url>\n    <loc>{url}</loc>\n    <priority>{prio}</priority>\n  </url>')
    
    lines.append('</urlset>')
    
    xml = '\n'.join(lines)
    with open(os.path.join(ROOT, 'sitemap.xml'), 'w') as f:
        f.write(xml)
    
    url_count = len(set(urls))
    print(f"  ✅ Sitemap regenerated: {url_count} URLs")


def copy_to_dev(slug):
    """Copy new tool HTML and updated index.html to versions/dev/."""
    src = os.path.join(ROOT, f'{slug}.html')
    dst = os.path.join(DEV_DIR, f'{slug}.html')
    if os.path.exists(src):
        subprocess.run(['cp', src, dst], check=True)
        print(f"  ✅ {slug}.html copied to dev/")
    else:
        print(f"  ⚠️  {slug}.html not found at root, skipping dev copy")
    
    # Copy updated index pages
    for lang in [''] + LANGUAGES:
        src_idx = os.path.join(ROOT, lang, 'index.html')
        dst_dir = os.path.join(DEV_DIR, lang)
        os.makedirs(dst_dir, exist_ok=True)
        dst_idx = os.path.join(dst_dir, 'index.html')
        if os.path.exists(src_idx):
            subprocess.run(['cp', src_idx, dst_idx], check=True)
    
    # Copy sitemap
    subprocess.run(['cp', os.path.join(ROOT, 'sitemap.xml'), os.path.join(DEV_DIR, 'sitemap.xml')], check=True)
    
    print(f"  ✅ Index files and sitemap synced to dev/")


def run_deploy():
    """Run deploy.sh textools."""
    result = subprocess.run(
        ['bash', os.path.join(ROOT, 'versions', 'deploy.sh'), 'textools'],
        capture_output=True, text=True
    )
    print(f"  📦 deploy.sh: {result.stdout.strip()}")
    if result.stderr:
        print(f"  ⚠️  stderr: {result.stderr.strip()}")


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 _pool/deploy_tool.py <slug>")
        sys.exit(1)
    
    slug = sys.argv[1]
    item, pool = get_pool_item(slug)
    if not item:
        print(f"❌ Tool '{slug}' not found in pool")
        sys.exit(1)
    
    print(f"\n🚀 Deploying new tool: {item['keyword']} ({slug})")
    
    emoji = item.get('emoji', '🔧')
    keyword = item.get('keyword', slug)
    desc = item.get('desc', '')
    category = item.get('category', 'text-processing')
    
    # Step 1: Update EN index
    print("\n📝 Updating EN index...")
    update_en_index(slug, emoji, keyword, desc, category)
    
    # Step 2: Update language indexes
    print("\n🌐 Updating language indexes...")
    for lang in LANGUAGES:
        update_lang_index(lang, slug, keyword)
    
    # Step 3: Regenerate sitemap
    print("\n🗺️ Regenerating sitemap...")
    generate_sitemap()
    
    # Step 4: Copy to dev
    print("\n📋 Syncing to dev...")
    copy_to_dev(slug)
    
    # Step 5: Mark done in pool
    print("\n✅ Marking done in pool...")
    item['done'] = True
    save_pool(pool)
    
    # Step 6: Deploy
    print("\n🚢 Deploying...")
    run_deploy()
    
    print(f"\n🎉 Done! {item['keyword']} is now live at https://textools.site/{slug}.html")


if __name__ == '__main__':
    main()
