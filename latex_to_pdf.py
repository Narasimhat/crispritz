#!/usr/bin/env python3
"""
Convert LaTeX book to PDF format
"""

import re
from weasyprint import HTML, CSS

def clean_latex(text):
    """Remove LaTeX commands and convert to HTML"""
    # Remove comments
    text = re.sub(r'%.*?\n', '\n', text)

    # Convert LaTeX formatting to HTML
    text = re.sub(r'\\textbf\{([^}]+)\}', r'<strong>\1</strong>', text)
    text = re.sub(r'\\textit\{([^}]+)\}', r'<em>\1</em>', text)
    text = re.sub(r'\\emph\{([^}]+)\}', r'<em>\1</em>', text)

    # Convert quotes
    text = text.replace('``', '"').replace("''", '"')

    # Remove common LaTeX commands but keep content
    text = re.sub(r'\\(large|Large|LARGE|huge|Huge|normalfont|bfseries|itshape|sffamily)', '', text)
    text = re.sub(r'\\vspace\*?\{[^}]+\}', '', text)
    text = re.sub(r'\\hspace\{[^}]+\}', '', text)
    text = re.sub(r'\\clearpage', '<div class="page-break"></div>', text)
    text = re.sub(r'\\newpage', '<div class="page-break"></div>', text)
    text = re.sub(r'\\thispagestyle\{[^}]+\}', '', text)
    text = re.sub(r'\\addcontentsline\{[^}]+\}\{[^}]+\}\{[^}]+\}', '', text)

    # Remove LaTeX backslashes before newlines
    text = text.replace('\\\\', '<br/>')

    # Clean up extra whitespace
    text = re.sub(r'\n\n+', '\n\n', text)

    return text.strip()

def extract_content(latex_content):
    """Extract chapters and content from LaTeX"""

    # Extract metadata
    title_match = re.search(r'\\title\{(.+?)\}', latex_content, re.DOTALL)
    author_match = re.search(r'\\author\{(.+?)\}', latex_content)
    date_match = re.search(r'\\date\{(.+?)\}', latex_content)

    title = "The Lighthouse Within"
    author = "The Lighthouse Within"
    date = "January 2026"

    if title_match:
        title = clean_latex(title_match.group(1))
        title = re.sub(r'<[^>]+>', ' ', title)  # Remove HTML tags for title
        title = re.sub(r'\s+', ' ', title).strip()
    if author_match:
        author = clean_latex(author_match.group(1))
    if date_match:
        date = clean_latex(date_match.group(1))

    # Extract document body
    doc_match = re.search(r'\\begin\{document\}(.+)\\end\{document\}', latex_content, re.DOTALL)
    if not doc_match:
        raise ValueError("Could not find document environment")

    body = doc_match.group(1)

    # Parse structure
    chapters = []
    parts = []

    # Extract parts
    part_pattern = r'\\part\{([^}]+)\}'
    for match in re.finditer(part_pattern, body):
        parts.append({
            'title': clean_latex(match.group(1)),
            'pos': match.start()
        })

    # Extract chapters (including chapter*)
    chapter_pattern = r'\\chapter\*?\{([^}]+)\}'
    chapter_matches = list(re.finditer(chapter_pattern, body))

    for i, match in enumerate(chapter_matches):
        chapter_title = clean_latex(match.group(1))
        chapter_title = re.sub(r'<[^>]+>', '', chapter_title)
        start_pos = match.end()
        end_pos = chapter_matches[i + 1].start() if i + 1 < len(chapter_matches) else len(body)

        # Get chapter content
        chapter_content = body[start_pos:end_pos]

        # Determine which part this chapter belongs to
        part_title = None
        for part in reversed(parts):
            if part['pos'] < match.start():
                part_title = part['title']
                part_title = re.sub(r'<[^>]+>', '', part_title)
                break

        # Extract sections and reflection boxes
        content_html = process_chapter_content(chapter_content)

        chapters.append({
            'title': chapter_title,
            'content': content_html,
            'part': part_title
        })

    return {
        'title': title,
        'author': author,
        'date': date,
        'chapters': chapters
    }

def process_chapter_content(content):
    """Process chapter content and convert to HTML"""
    html_parts = []

    # Handle reflection boxes
    reflection_pattern = r'\\begin\{reflectionbox\}(.+?)\\end\{reflectionbox\}'

    last_end = 0
    for match in re.finditer(reflection_pattern, content, re.DOTALL):
        # Add content before reflection box
        before = content[last_end:match.start()]
        if before.strip():
            html_parts.append(process_text(before))

        # Add reflection box
        box_content = clean_latex(match.group(1))
        html_parts.append(f'<div class="reflection-box"><h4>REFLECTION</h4>{process_text(box_content)}</div>')

        last_end = match.end()

    # Add remaining content
    remaining = content[last_end:]
    if remaining.strip():
        html_parts.append(process_text(remaining))

    return '\n'.join(html_parts)

def process_text(text):
    """Convert LaTeX text content to HTML"""
    text = clean_latex(text)

    # Handle sections
    text = re.sub(r'\\section\*?\{([^}]+)\}', r'<h3>\1</h3>', text)

    # Handle itemize
    itemize_pattern = r'\\begin\{itemize\}(.+?)\\end\{itemize\}'
    text = re.sub(itemize_pattern, lambda m: convert_itemize(m.group(1)), text, flags=re.DOTALL)

    # Handle enumerate
    enumerate_pattern = r'\\begin\{enumerate\}(.+?)\\end\{enumerate\}'
    text = re.sub(enumerate_pattern, lambda m: convert_enumerate(m.group(1)), text, flags=re.DOTALL)

    # Handle center environment
    center_pattern = r'\\begin\{center\}(.+?)\\end\{center\}'
    text = re.sub(center_pattern, r'<div class="center">\1</div>', text, flags=re.DOTALL)

    # Remove remaining LaTeX commands
    text = re.sub(r'\\[a-zA-Z]+', '', text)
    text = re.sub(r'[{}]', '', text)

    # Convert paragraphs
    paragraphs = text.split('\n\n')
    html_paragraphs = []
    for para in paragraphs:
        para = para.strip()
        if para and not para.startswith('<'):
            para = f'<p>{para}</p>'
        if para:
            html_paragraphs.append(para)

    return '\n'.join(html_paragraphs)

def convert_itemize(content):
    """Convert LaTeX itemize to HTML list"""
    items = re.findall(r'\\item\s+(.+?)(?=\\item|$)', content, re.DOTALL)
    html_items = [f'<li>{clean_latex(item.strip())}</li>' for item in items]
    return f'<ul>{"".join(html_items)}</ul>'

def convert_enumerate(content):
    """Convert LaTeX enumerate to HTML ordered list"""
    items = re.findall(r'\\item\s+(.+?)(?=\\item|$)', content, re.DOTALL)
    html_items = [f'<li>{clean_latex(item.strip())}</li>' for item in items]
    return f'<ol>{"".join(html_items)}</ol>'

def create_html(book_data):
    """Create HTML from book data"""

    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{book_data['title']}</title>
    <style>
        @page {{
            size: A5;
            margin: 2cm;
            @bottom-center {{
                content: counter(page);
            }}
        }}

        body {{
            font-family: 'Georgia', 'Times New Roman', serif;
            font-size: 11pt;
            line-height: 1.6;
            color: #000;
        }}

        .title-page {{
            page-break-after: always;
            text-align: center;
            padding-top: 40%;
        }}

        .title {{
            font-size: 28pt;
            font-weight: bold;
            color: #283C5A;
            margin-bottom: 0.5em;
        }}

        .subtitle {{
            font-size: 14pt;
            margin-bottom: 2em;
        }}

        .author {{
            font-size: 12pt;
            margin-top: 3em;
        }}

        .copyright-page {{
            page-break-after: always;
            text-align: center;
            padding-top: 80%;
            font-size: 10pt;
        }}

        .part {{
            page-break-before: always;
            page-break-after: always;
            text-align: center;
            padding-top: 40%;
        }}

        .part-title {{
            font-size: 24pt;
            font-weight: bold;
            color: #283C5A;
        }}

        .chapter {{
            page-break-before: always;
        }}

        h1 {{
            color: #283C5A;
            font-size: 20pt;
            margin-top: 1em;
            margin-bottom: 1em;
            page-break-after: avoid;
        }}

        h2 {{
            color: #283C5A;
            font-size: 16pt;
            margin-top: 1.5em;
            page-break-after: avoid;
        }}

        h3 {{
            color: #283C5A;
            font-size: 14pt;
            margin-top: 1em;
            page-break-after: avoid;
        }}

        h4 {{
            color: #283C5A;
            font-weight: bold;
            font-size: 11pt;
        }}

        p {{
            margin: 1em 0;
            text-align: justify;
            orphans: 3;
            widows: 3;
        }}

        .reflection-box {{
            background-color: #F5F7FA;
            border-left: 4px solid #283C5A;
            padding: 1em;
            margin: 1.5em 0;
            page-break-inside: avoid;
        }}

        .center {{
            text-align: center;
            font-style: italic;
            margin: 1.5em 0;
        }}

        em {{ font-style: italic; }}
        strong {{ font-weight: bold; }}

        ul, ol {{
            margin: 1em 0;
            padding-left: 2em;
        }}

        li {{
            margin: 0.5em 0;
        }}

        .page-break {{
            page-break-after: always;
        }}
    </style>
</head>
<body>
    <div class="title-page">
        <div class="title">{book_data['title']}</div>
        <div class="subtitle">A New Year Gift for Dreamers</div>
        <div class="author">{book_data['author']}</div>
    </div>

    <div class="copyright-page">
        <strong>The Lighthouse Within</strong><br/>
        Copyright © 2025<br/>
        <br/>
        All rights reserved.<br/>
        This book is a gift.<br/>
        Share it freely with those who need light.<br/>
        <br/>
        {book_data['date']}
    </div>
'''

    current_part = None
    for chapter in book_data['chapters']:
        # Add part divider if new part
        if chapter['part'] and chapter['part'] != current_part:
            current_part = chapter['part']
            html += f'''
    <div class="part">
        <div class="part-title">{current_part}</div>
    </div>
'''

        # Add chapter
        html += f'''
    <div class="chapter">
        <h1>{chapter['title']}</h1>
        {chapter['content']}
    </div>
'''

    html += '''
</body>
</html>
'''

    return html

def main():
    # Read LaTeX file
    with open('lighthouse_within.tex', 'r', encoding='utf-8') as f:
        latex_content = f.read()

    print("Parsing LaTeX content...")
    book_data = extract_content(latex_content)

    print(f"Found {len(book_data['chapters'])} chapters")

    print("Creating HTML...")
    html_content = create_html(book_data)

    # Save HTML for debugging
    with open('lighthouse_within.html', 'w', encoding='utf-8') as f:
        f.write(html_content)

    print("Generating PDF...")
    HTML(string=html_content).write_pdf('lighthouse_within.pdf')

    print("\n✓ PDF created successfully!")
    print("Output: lighthouse_within.pdf")
    print("\nThis PDF is formatted for:")
    print("  • A5 paper size (standard book size)")
    print("  • Professional print-ready quality")
    print("  • Reading on tablets/computers")

if __name__ == '__main__':
    main()
