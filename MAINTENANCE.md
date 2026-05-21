# 工具站 (textools.site) 维护文档

## 基本信息
- 纯静态站点（无后端服务）
- 根目录：`/home/ubuntu/textools/`
- 域名配置在 Nginx（`/etc/nginx/sites-enabled/textools`）

## 站点结构
```
textools/
├── index.html              # 首页（工具网格 + SEO内容区）
├── case-converter.html      # 大小写转换
├── find-replace.html        # 查找替换
├── password-generator.html  # 密码生成器
├── remove-duplicates.html   # 去重工具
├── sort-lines.html          # 行排序
├── template-tool.html       # 模板工具
├── word-counter.html        # 字数统计
├── _pool/                   # 自动生成系统的数据
│   ├── tool-ideas.json      # 长青词工具池（34个候选词）
│   └── template-reference.md # 工具页面模板参考
├── articles/                # SEO软文
│   └── *.html               # 工具介绍文章
├── sitemap.xml
├── ja/                      # 日语版
├── ko/                      # 韩语版
└── zh-hk/                   # 粤语版
```

## 自动系统（核心）

系统每周二四 04:00 自动运行，实现"活的"可持续运转：

1. **检查词池** → 读取 `_pool/tool-ideas.json`，找下一个未用的词
2. **有未用词** → 生成新工具页面 + SEO软文 + 更新首页 + 更新 sitemap
3. **词池用完** → 切换到仅生成软文模式

### 决策逻辑
- `done=false` 的词条存在 → 新工具生成流水线
- 全部 `done=true` → 仅软文模式（挑选已有工具写介绍文章）

### 新工具生成流水线
1. 从 `_pool/tool-ideas.json` 选词
2. AI 生成工具 HTML（参照 `_pool/template-reference.md`）
3. `node` 语法验证 → 失败则修复重试
4. 标记词条已用（`"done": true`）
5. 生成 SEO 软文（`articles/{slug}.html`）
6. 更新 `index.html`（工具网格 + 链接列表 + 页脚）
7. 更新 `sitemap.xml`

## 手动操作

### 1. 手动触发工具生成
```bash
hermes cron run 149746d67895
```

### 2. 添加新工具池词条
编辑 `_pool/tool-ideas.json`，追加一条：
```json
{"slug":"tool-name","keyword":"Tool Name","emoji":"🔧","desc":"One-line description","how_to":"How to use","difficulty":"easy","done":false}
```
系统下次运行会自动生成。

### 3. 手动编辑工具页面
直接修改对应的 HTML 文件。注意保持：
- Dark 主题（#0a0a14 背景）
- 隐私优先（所有处理在浏览器本地）
- AdSense 脚本保留
- OG tags、canonical 正确

### 4. 修改首页布局
编辑 `index.html`：
- `.grid` 里的工具卡片
- `.seo-section` 里的工具链接列表
- 页脚链接

### 5. 重启服务
textools 是纯静态站，修改 HTML 后立即生效（nginx 服务无需重启）
如有 nginx 配置改：`sudo nginx -t && sudo systemctl reload nginx`

## Cron
- **工具站自动流水线**：每周二四 04:00（cron ID: 149746d67895）
- 技能依赖：`seo:seo-content-pipeline`

## ⚠️ 切记
- 站点定位：隐私优先（所有处理在浏览器本地完成，不上传数据）
- 主题风格：Dark 主题，移动端友好
- **不要** 做 Text Diff、简历、翻译/AI检测 类工具
- 广告要精准嵌入（位置已有预留），不要破坏用户体验
- 如果手动修改 `index.html`，注意保留工具网格结构的一致性
- 如果手动添加工具，记得也更新 `sitemap.xml`
