#!/usr/bin/env python3
"""Generate full categorized index pages for ja/ko language versions."""
import os

ROOT = '/home/ubuntu/textools'

TOOL_CATEGORIES = {
    'text-analysis': ['word-counter', 'char-counter', 'markdown-preview'],
    'text-processing': ['remove-duplicates', 'sort-lines', 'case-converter', 'find-replace', 'text-reverser', 'text-splitter', 'text-diff', 'whitespace-trimmer', 'line-numberer', 'template-tool'],
    'encoding-conversion': ['base64-encoder', 'url-encoder', 'slug-generator', 'timestamp-converter', 'json-formatter'],
    'utilities': ['password-generator', 'regex-tester', 'random-picker'],
}

JA = {
    'lang': 'ja', 'title': 'テキストツール 無料 — オンライン文字数カウント・重複行削除・行ソート | Textools',
    'desc': '無料のオンラインテキスト処理ツール。文字数カウンター、重複行削除、行ソートなど。100%プライバシー保護 — すべてブラウザ上で処理。',
    'h1': '🧰 テキストツール',
    'sub': '無料のオンラインテキスト処理 — すべてのツールはブラウザ上で動作し、データは端末から外部に出ません',
    'trust': '<strong>🔒 プライバシー完全保護</strong> — すべてのテキスト処理はお使いのブラウザ上でローカルに実行されます。サーバーにデータが送信されることは一切ありません。',
    'back': '← Textools ホーム',
    'cat': {
        'text-analysis': '📝 テキスト分析',
        'text-processing': '🔧 テキスト処理',
        'encoding-conversion': '🔣 エンコード・変換',
        'utilities': '🛠️ ユーティリティ',
    },
    'tools': {
        'word-counter': ['📊', '単語カウンター', '文字数・単語数・文章数・段落数・読了時間をリアルタイムで集計します。'],
        'char-counter': ['🔢', '文字数カウンター', 'スペースを含む／含まない文字数をカウント。Twitter・SMS・メタディスクリプションに最適。'],
        'markdown-preview': ['📝', 'Markdown プレビュー', 'リアルタイムでMarkdownを記述・プレビュー。テーブル・コードブロック・書式に対応。'],
        'remove-duplicates': ['🗑️', '重複行削除', 'テキストから重複行を削除。元の順序を保持したまま一括除去。'],
        'sort-lines': ['🔤', '行ソート', 'テキスト行を昇順（A-Z）または降順（Z-A）に並べ替え。'],
        'case-converter': ['🔄', '大文字小文字変換', '大文字・小文字・タイトルケース・キャメルケースなどに変換。'],
        'find-replace': ['🔍', '検索・置換', 'テキストを検索して置換。正規表現モード対応。'],
        'text-reverser': ['↩️', 'テキスト反転', '文字列・単語・行を反転。パリンドロームやパズルに。'],
        'text-splitter': ['✂️', 'テキスト分割', '区切り文字・改行・正規表現でテキストを分割。'],
        'text-diff': ['📋', '差分チェッカー', '2つのテキストを並べて比較。追加・削除・変更をハイライト。'],
        'whitespace-trimmer': ['🧹', '空白文字削除', '余分なスペース・タブ・改行を削除。テキストをクリーンアップ。'],
        'line-numberer': ['🔢', '行番号付与', 'テキストに行番号を追加。接頭辞・接尾辞・開始番号をカスタマイズ。'],
        'template-tool': ['📄', 'テンプレートツール', 'カスタム値でテキストテンプレートを埋め込み。再利用可能なパターンを作成。'],
        'base64-encoder': ['🔐', 'Base64 エンコーダ/デコーダ', 'テキストをBase64形式にエンコード／デコード。ファイル入力にも対応。'],
        'url-encoder': ['🔗', 'URL エンコーダ/デコーダ', 'URLパラメータをエンコード／デコード。特殊文字を処理。'],
        'slug-generator': ['📌', 'URL スラグ生成', 'テキストからURLに適したスラグを生成。ブログ記事やページに最適。'],
        'timestamp-converter': ['⏰', 'タイムスタンプ変換', 'Unixタイムスタンプと日付を相互変換。複数のタイムゾーン対応。'],
        'json-formatter': ['📋', 'JSON フォーマッター', 'JSONデータをフォーマット・検証・美化。ツリービューで折りたたみ可能。'],
        'password-generator': ['🔐', 'パスワード生成', '高強度ランダムパスワードを生成。長さ・記号・数字をカスタマイズ。'],
        'regex-tester': ['🔬', '正規表現テスター', 'リアルタイムで正規表現をテスト。マッチ・グループ・置換結果を表示。'],
        'random-picker': ['🎲', 'ランダム選択', 'リストからランダムに項目を選択。抽選・くじ引き・チーム分けに。'],
    },
    'seo_h2': 'ブラウザ完結の無料テキストツール',
    'seo_p': '当サイトのテキストツールはすべてブラウザ上で動作するため、データがサーバーに送信されることはありません。文字数カウント、重複行削除、行ソートなど、日々のテキスト処理を安全かつ高速に行えます。',
    'footer_copyright': '© 2026 Textools · すべてのツールはクライアントサイドで動作 · データのアップロードはありません',
    'footer_links': {'Home': '/', 'プライバシー': '/privacy.html', '記事': '/articles/'},
    'cat_seo_titles': {
        'text-analysis': ['単語カウンター', '文字数カウンター', 'Markdown プレビュー'],
        'text-processing': ['重複行削除', '行ソート', '大文字小文字変換', '検索・置換', 'テキスト反転', 'テキスト分割', '差分チェッカー', '空白文字削除', '行番号付与', 'テンプレートツール'],
        'encoding-conversion': ['Base64 エンコーダ/デコーダ', 'URL エンコーダ/デコーダ', 'URL スラグ生成', 'タイムスタンプ変換', 'JSON フォーマッター'],
        'utilities': ['パスワード生成', '正規表現テスター', 'ランダム選択'],
    },
}

KO = {
    'lang': 'ko', 'title': '텍스트 도구 모음 — 무료 온라인 텍스트 처리 도구 | Textools',
    'desc': '무료 온라인 텍스트 처리 도구 모음입니다. 단어 수 세기, 중복 줄 제거, 줄 정렬 등 모든 도구가 브라우저에서 실행되어 데이터가 서버로 전송되지 않습니다.',
    'h1': '🧰 텍스트 도구',
    'sub': '무료 온라인 텍스트 처리 — 모든 도구가 브라우저에서 실행되며, 데이터가 외부로 전송되지 않습니다',
    'trust': '<strong>🔒 100% 프라이버시 보호</strong> — 모든 텍스트 처리는 브라우저에서 로컬로 실행됩니다. 서버에 업로드되는 데이터는 없습니다.',
    'back': '← Textools 홈',
    'cat': {
        'text-analysis': '📝 텍스트 분석',
        'text-processing': '🔧 텍스트 처리',
        'encoding-conversion': '🔣 인코딩 및 변환',
        'utilities': '🛠️ 유틸리티',
    },
    'tools': {
        'word-counter': ['📊', '단어 카운터', '텍스트의 단어 수, 문자 수, 문장 수, 문단 수, 읽기 시간을 계산합니다.'],
        'char-counter': ['🔢', '문자 카운터', '공백 포함/미포함 문자 수 계산. Twitter, SMS, 메타 설명에 최적.'],
        'markdown-preview': ['📝', 'Markdown 미리보기', 'Markdown을 실시간 작성/미리보기. 표, 코드 블록, 서식 지원.'],
        'remove-duplicates': ['🗑️', '중복 줄 제거', '텍스트에서 중복된 줄을 제거합니다. 원래 순서 유지.'],
        'sort-lines': ['🔤', '줄 정렬', '텍스트 줄을 알파벳순으로 정렬 (A-Z 또는 Z-A).'],
        'case-converter': ['🔄', '대소문자 변환', '대문자, 소문자, 첫 글자 대문자, 카멜케이스 등으로 변환.'],
        'find-replace': ['🔍', '찾기 및 바꾸기', '텍스트 검색 및 바꾸기. 정규식 모드 지원.'],
        'text-reverser': ['↩️', '텍스트 뒤집기', '텍스트, 단어, 줄을 뒤집습니다. 회문과 퍼즐에 유용.'],
        'text-splitter': ['✂️', '텍스트 분할', '구분 기호, 줄 바꿈, 정규식 패턴으로 텍스트 분할.'],
        'text-diff': ['📋', '텍스트 차이 비교', '두 텍스트를 나란히 비교. 추가/삭제/변경 강조.'],
        'whitespace-trimmer': ['🧹', '공백 문자 제거', '여분의 공백, 탭, 줄 바꿈을 제거하여 텍스트 정리.'],
        'line-numberer': ['🔢', '줄 번호 매기기', '텍스트에 줄 번호를 추가. 접두사/접미사/시작 번호 사용자 지정.'],
        'template-tool': ['📄', '템플릿 도구', '사용자 지정 값으로 텍스트 템플릿 채우기. 재사용 가능한 패턴 생성.'],
        'fortuna-preview': ['🎯', '포르투나 미리보기', '랜덤 선택 결과 미리보기.'],
        'base64-encoder': ['🔐', 'Base64 인코더/디코더', '텍스트를 Base64로 인코딩/디코딩. 파일 입력 지원.'],
        'url-encoder': ['🔗', 'URL 인코더/디코더', 'URL 매개변수 인코딩/디코딩. 특수 문자 처리.'],
        'slug-generator': ['📌', 'URL 슬러그 생성기', '텍스트에서 URL 친화적 슬러그 생성. 블로그 게시물에 최적.'],
        'timestamp-converter': ['⏰', '타임스탬프 변환기', 'Unix 타임스탬프와 날짜 상호 변환. 여러 시간대 지원.'],
        'json-formatter': ['📋', 'JSON 포맷터', 'JSON 데이터 포맷팅, 검증 및 예쁘게 출력. 트리 뷰 접기 가능.'],
        'password-generator': ['🔐', '비밀번호 생성기', '강력한 랜덤 비밀번호 생성. 길이, 기호, 숫자 사용자 지정.'],
        'regex-tester': ['🔬', '정규식 테스터', '실시간 정규식 테스트. 일치, 그룹, 대체 결과 표시.'],
        'random-picker': ['🎲', '랜덤 선택', '목록에서 항목을 무작위로 선택. 추첨, 제비뽑기, 팀 구성에 유용.'],
    },
    'seo_h2': '브라우저에서 완전히 실행되는 무료 텍스트 도구',
    'seo_p': '당사 텍스트 도구는 모두 브라우저에서만 실행되므로 데이터가 서버로 전송되지 않습니다. 단어 카운트, 중복 제거, 줄 정렬 등 일상적인 텍스트 처리를 안전하고 빠르게 수행할 수 있습니다.',
    'footer_copyright': '© 2026 Textools · 모든 도구는 클라이언트에서 실행 · 데이터 업로드 없음',
    'footer_links': {'Home': '/', '개인정보': '/privacy.html', '블로그': '/articles/'},
    'cat_seo_titles': {
        'text-analysis': ['단어 카운터', '문자 카운터', 'Markdown 미리보기'],
        'text-processing': ['중복 줄 제거', '줄 정렬', '대소문자 변환', '찾기 및 바꾸기', '텍스트 뒤집기', '텍스트 분할', '텍스트 차이 비교', '공백 문자 제거', '줄 번호 매기기', '템플릿 도구', '포르투나 미리보기'],
        'encoding-conversion': ['Base64 인코더/디코더', 'URL 인코더/디코더', 'URL 슬러그 생성기', '타임스탬프 변환기', 'JSON 포맷터'],
        'utilities': ['비밀번호 생성기', '정규식 테스터', '랜덤 선택'],
    },
}

def gen_index(lang_data):
    ld = lang_data
    l = ld['lang']
    
    categories = {
        'text-analysis': [],
        'text-processing': [],
        'encoding-conversion': [],
        'utilities': [],
    }
    
    for cat, slugs in TOOL_CATEGORIES.items():
        for slug in slugs:
            if slug in ld['tools']:
                categories[cat].append(slug)
        # Also add any extra tools that exist but aren't in default categories
    # Add any tools not in default categories to text-processing
    all_defined = set()
    for slugs in TOOL_CATEGORIES.values():
        all_defined.update(slugs)
    extras = set(ld['tools'].keys()) - all_defined - {'fortuna-preview'}
    for slug in sorted(extras):
        categories['text-processing'].append(slug)
    # fortuna-preview goes to utilities if it exists
    if 'fortuna-preview' in ld['tools']:
        categories['utilities'].append('fortuna-preview')
    
    lang_links = {
        'ja': '<a href="/">English</a>\n    <a href="/ko/">한국어</a>\n    <a href="/zh-hk/">繁體中文</a>',
        'ko': '<a href="/">English</a>\n    <a href="/ja/">日本語</a>\n    <a href="/zh-hk/">繁體中文</a>',
    }
    
    lines = []
    lines.append('<!DOCTYPE html>')
    lines.append(f'<html lang="{l}">')
    lines.append('<head>')
    lines.append('<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-5545263418745440" crossorigin="anonymous"></script>')
    lines.append('<meta charset="UTF-8">')
    lines.append('<meta name="viewport" content="width=device-width, initial-scale=1.0">')
    lines.append('<link rel="icon" type="image/svg+xml" href="/favicon.svg">')
    lines.append('<link rel="alternate icon" href="/favicon.ico" sizes="any">')
    lines.append(f'<title>{ld["title"]}</title>')
    lines.append(f'<meta name="description" content="{ld["desc"]}">')
    lines.append(f'<link rel="canonical" href="https://textools.site/{l}/">')
    lines.append(f'<link rel="alternate" hreflang="{l}" href="https://textools.site/{l}/">')
    lines.append('<link rel="alternate" hreflang="en" href="https://textools.site/">')
    lines.append('<link rel="alternate" hreflang="ja" href="https://textools.site/ja/">')
    lines.append('<link rel="alternate" hreflang="ko" href="https://textools.site/ko/">')
    lines.append('<link rel="alternate" hreflang="zh-HK" href="https://textools.site/zh-hk/">')
    lines.append('<link rel="alternate" hreflang="x-default" href="https://textools.site/">')
    lines.append(f'<meta property="og:title" content="{ld["h1"]}">')
    lines.append(f'<meta property="og:description" content="{ld["desc"]}">')
    lines.append(f'<meta property="og:url" content="https://textools.site/{l}/">')
    lines.append('<meta property="og:type" content="website">')
    lines.append('<meta property="og:image" content="https://textools.site/og-tools.svg">')
    lines.append('<meta name="twitter:card" content="summary_large_image">')
    lines.append(f'<meta name="twitter:title" content="{ld["h1"]}">')
    lines.append(f'<meta name="twitter:description" content="{ld["desc"]}">')
    lines.append('<meta name="twitter:image" content="https://textools.site/og-tools.svg">')
    lines.append('<meta name="robots" content="index, follow">')
    lines.append('''<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI','Noto Sans SC','Noto Sans TC','Noto Sans JP','Noto Sans KR',Roboto,sans-serif;background:#1e1e2e;color:#cdd6f4;min-height:100vh;line-height:1.6}
.container{max-width:960px;margin:0 auto;padding:24px 20px}
h1{font-size:28px;font-weight:900;background:linear-gradient(135deg,#89b4fa,#a6e3a1);-webkit-background-clip:text;-webkit-text-fill-color:transparent;letter-spacing:1px;margin-bottom:6px;text-align:center}
.sub{color:#7f849c;font-size:13px;text-align:center;margin-bottom:8px;letter-spacing:.5px}
.trust-banner{text-align:center;background:rgba(166,227,161,.06);border:1px solid rgba(166,227,161,.12);border-radius:10px;padding:10px 16px;margin:10px auto 24px;max-width:520px;font-size:13px;color:#a6e3a1}
.trust-banner strong{color:#b8eab4}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:12px;margin-top:20px}
.card{background:linear-gradient(135deg,rgba(24,24,37,.95),rgba(17,17,27,.95));border:1px solid rgba(137,180,250,.12);border-radius:12px;padding:16px;transition:all .25s;text-decoration:none;display:block;position:relative}
.card:hover{border-color:#89b4fa;transform:translateY(-2px);box-shadow:0 8px 24px rgba(137,180,250,.12)}
.card .icon{font-size:26px;margin-bottom:4px}
.card h3{color:#cdd6f4;font-size:14px;font-weight:600;margin-bottom:2px}
.card p{color:#a6adc8;font-size:11px;line-height:1.5}
.sec-title{font-size:14px;color:#585b70;text-align:center;margin:28px 0 6px;letter-spacing:1px}
.footer{text-align:center;padding:30px 0 10px;color:#45475a;font-size:11px;margin-top:20px;border-top:1px solid rgba(137,180,250,.06)}
.footer a{color:#585b70;text-decoration:none;margin:0 6px}
.footer a:hover{color:#89b4fa}
.lang-links{text-align:center;margin:16px 0;font-size:11px}
.lang-links a{color:#585b70;text-decoration:none;margin:0 4px;padding:2px 8px;border-radius:4px;border:1px solid rgba(137,180,250,.1)}
.lang-links a:hover{color:#89b4fa;border-color:#89b4fa}
.seo-section{margin-top:30px;padding-top:20px;border-top:1px solid rgba(137,180,250,.06)}
.seo-section h2{font-size:15px;color:#cdd6f4;margin-bottom:10px;font-weight:600}
.seo-section p{font-size:12px;color:#7f849c;line-height:1.7;margin-bottom:8px}
.seo-section ul{list-style:none;padding:0;display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:4px 16px}
.seo-section ul li{font-size:11px;color:#585b70;line-height:1.8}
.seo-section ul li a{color:#585b70;text-decoration:none;border-bottom:1px solid transparent}
.seo-section ul li a:hover{color:#89b4fa;border-color:#89b4fa}
@media(max-width:600px){h1{font-size:24px}.grid{grid-template-columns:1fr 1fr}}
</style>''')
    lines.append('</head>')
    lines.append('<body>')
    lines.append('<div class="container">')
    lines.append(f'  <h1>{ld["h1"]}</h1>')
    lines.append(f'  <p class="sub">{ld["sub"]}</p>')
    lines.append(f'  <div class="trust-banner">{ld["trust"]}</div>')
    
    cat_labels = ['text-analysis', 'text-processing', 'encoding-conversion', 'utilities']
    cat_labels_en = ['text-analysis', 'text-processing', 'encoding-conversion', 'utilities']
    
    for cat in cat_labels:
        tools = categories[cat]
        if not tools:
            continue
        lines.append(f'  <div class="sec-title">{ld["cat"][cat]}</div>')
        lines.append(f'  <div class="grid">')
        for slug in tools:
            icon, name, desc = ld['tools'][slug]
            lines.append(f'    <a href="/{l}/{slug}.html" class="card">')
            lines.append(f'      <div class="icon">{icon}</div>')
            lines.append(f'      <h3>{name}</h3>')
            lines.append(f'      <p>{desc}</p>')
            lines.append(f'    </a>')
        lines.append(f'  </div>')
    
    lines.append(f'  <div class="lang-links">')
    lines.append(f'    {lang_links[l]}')
    lines.append(f'  </div>')
    
    lines.append(f'  <div class="seo-section">')
    lines.append(f'    <h2>{ld["seo_h2"]}</h2>')
    lines.append(f'    <p>{ld["seo_p"]}</p>')
    lines.append(f'    <h3>すべてのツール</h3>' if l == 'ja' else f'    <h3>모든 도구</h3>')
    lines.append(f'    <ul>')
    for cat in cat_labels:
        for slug in categories[cat]:
            _, name, _ = ld['tools'][slug]
            lines.append(f'      <li><a href="/{l}/{slug}.html">{name}</a></li>')
    lines.append(f'    </ul>')
    lines.append(f'  </div>')
    
    lines.append(f'  <div class="footer">')
    fl = []
    for label, url in ld['footer_links'].items():
        fl.append(f'<a href="{url}">{label}</a>')
    lines.append(f'    {" · ".join(fl)}')
    lines.append(f'    <br><br>')
    lines.append(f'    <span>{ld["footer_copyright"]}</span>')
    lines.append(f'  </div>')
    lines.append('</div>')
    lines.append('</body>')
    lines.append('</html>')
    
    return '\n'.join(lines)

# Generate and write
ja_html = gen_index(JA)
with open(f'{ROOT}/ja/index.html', 'w', encoding='utf-8') as f:
    f.write(ja_html)
print(f'JA: written ({len(ja_html)} chars)')

ko_html = gen_index(KO)
with open(f'{ROOT}/ko/index.html', 'w', encoding='utf-8') as f:
    f.write(ko_html)
print(f'KO: written ({len(ko_html)} chars)')
