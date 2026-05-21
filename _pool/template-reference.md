# Tool Page Template Reference

Use this when generating a new tool page for textools.site.

## Required HTML Structure

```html
<!DOCTYPE html>
<html lang="en">
<head>
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-5545263418745440" crossorigin="anonymous"></script>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>TOOL_NAME — Free Online Text Tool | Textools</title>
<meta name="description" content="DESCRIPTION with keyword, mention free and 100% private browser processing.">
<meta name="robots" content="index, follow">
<link rel="canonical" href="https://textools.site/TOOL_SLUG.html">
<meta property="og:title" content="TOOL_NAME — Free Online Tool">
<meta property="og:description" content="Brief OG description.">
<meta property="og:url" content="https://textools.site/TOOL_SLUG.html">
<meta property="og:image" content="https://textools.site/og-tools.png">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="https://textools.site/og-tools.png">
```

## CSS Style Rules

- Background: `#0a0a14`, text: `#d0c8e0`
- Accent purple: `#7b68ee`, light purple: `#e0c8ff`
- Container max-width: 800px, padding: 24px 20px
- h1: 26px, gradient `linear-gradient(135deg,#e0c8ff,#7b68ee,#4a3aa0)`, `-webkit-background-clip:text`
- Trust badge: green rgba(100,220,150), text `100% Private — All processing in your browser`
- Textarea: `#0e0e1a` bg, `#1e1e3a` border, monospace font
- Buttons: purple gradient `#7b68ee→#5a4acd`, border-radius 8px
- Stat cards: dark gradient with purple border
- Toast notification: fixed bottom center, purple border
- Rec-bar: related tools navigation bar
- Mobile: h1 22px, grid 3 columns
- SEO content section at bottom
- Footer: centered, dim gray

## Structured Data (JSON-LD)

Include TWO schema blocks:

### 1. BreadcrumbList:
```json
{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
  {"@type":"ListItem","position":1,"name":"Home","item":"https://textools.site/"},
  {"@type":"ListItem","position":2,"name":"Tools","item":"https://textools.site/tools/"},
  {"@type":"ListItem","position":3,"name":"TOOL_NAME"}
]}
```

### 2. FAQPage: 3-4 Q&A pairs about the tool

Example questions:
- "Is TOOL free?"
- "Does it work offline?"
- "Can I use it for [use case]?"
- "How accurate is it?"

## Tool UI Pattern

```
[Title]
[Subtitle: brief description]
[Trust Badge]
[Textarea / Input]
[Action Buttons: Process, Clear, Copy]
[Results Area: stats cards or output box]
[Related Tools Bar (rec-bar)]
[SEO Content Section]
[Footer]
```

## SEO Content Section

Must include:
- h2: "What is [Tool Name]?"
- Paragraph explaining the tool
- h3: "How to Use [Tool Name]" — numbered steps
- h3: "Common Use Cases" — bullet list with practical scenarios
- h3: "Why Choose Textools?" — emphasize privacy, speed, no signup

## JavaScript Pattern

- Main function: `processText()` called on button click
- Real-time update: `textarea.addEventListener('input', processText)`
- Copy button: `navigator.clipboard.writeText()`
- Clear button: clear textarea and reset results
- Toast notification: class `.toast.show` toggle with setTimeout(2000)
- ALL processing must be client-side only (no API calls, no fetch)

## Validation After Generation

Run: `node -e "YOUR_JS_CODE"` to check for syntax errors.
If errors, fix and regenerate.
