#!/usr/bin/env python3
"""
Convert LaTeX book to EPUB format for Kindle/Apple Books
"""

import re
from ebooklib import epub
import html

def clean_latex(text):
    """Remove LaTeX commands and convert to plain text"""
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
    text = re.sub(r'\\vspace\{[^}]+\}', '', text)
    text = re.sub(r'\\hspace\{[^}]+\}', '', text)
    text = re.sub(r'\\clearpage', '', text)
    text = re.sub(r'\\newpage', '', text)
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

    title = "The Lighthouse Within"
    author = "The Lighthouse Within"

    if title_match:
        title = clean_latex(title_match.group(1))
        title = re.sub(r'<[^>]+>', '', title)  # Remove HTML tags for title
    if author_match:
        author = clean_latex(author_match.group(1))

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
        start_pos = match.end()
        end_pos = chapter_matches[i + 1].start() if i + 1 < len(chapter_matches) else len(body)

        # Get chapter content
        chapter_content = body[start_pos:end_pos]

        # Determine which part this chapter belongs to
        part_title = None
        for part in reversed(parts):
            if part['pos'] < match.start():
                part_title = part['title']
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
        'chapters': chapters
    }

def process_chapter_content(content):
    """Process chapter content and convert to HTML"""
    html_parts = []

    # Split by environments and sections
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

def create_epub(book_data, output_file):
    """Create EPUB file from book data"""

    book = epub.EpubBook()

    # Set metadata
    book.set_identifier('lighthouse-within-001')
    book.set_title(book_data['title'])
    book.set_language('en')
    book.add_author(book_data['author'])

    # Create CSS
    css = '''
        body {
            font-family: Georgia, serif;
            line-height: 1.6;
            margin: 1em;
        }
        h1 {
            color: #283C5A;
            font-size: 2em;
            margin-top: 2em;
            margin-bottom: 1em;
        }
        h2 {
            color: #283C5A;
            font-size: 1.5em;
            margin-top: 1.5em;
        }
        h3 {
            color: #283C5A;
            font-size: 1.2em;
            margin-top: 1em;
        }
        h4 {
            color: #283C5A;
            font-weight: bold;
        }
        p {
            margin: 1em 0;
            text-align: justify;
        }
        .reflection-box {
            background-color: #F5F7FA;
            border-left: 4px solid #283C5A;
            padding: 1em;
            margin: 1.5em 0;
        }
        .center {
            text-align: center;
            font-style: italic;
            margin: 1.5em 0;
        }
        em { font-style: italic; }
        strong { font-weight: bold; }
        ul, ol {
            margin: 1em 0;
            padding-left: 2em;
        }
        li { margin: 0.5em 0; }
    '''

    nav_css = epub.EpubItem(
        uid="style_nav",
        file_name="style/nav.css",
        media_type="text/css",
        content=css
    )
    book.add_item(nav_css)

    # Create chapters
    epub_chapters = []
    toc = []
    spine = ['nav']

    current_part = None
    part_chapters = []

    for i, chapter in enumerate(book_data['chapters']):
        # Check if we're starting a new part
        if chapter['part'] and chapter['part'] != current_part:
            if current_part and part_chapters:
                toc.append((epub.Section(current_part), part_chapters))
                part_chapters = []
            current_part = chapter['part']

        # Create chapter
        c = epub.EpubHtml(
            title=chapter['title'],
            file_name=f'chap_{i:02d}.xhtml',
            lang='en'
        )

        c.content = f'''
            <html>
            <head>
                <title>{chapter['title']}</title>
                <link rel="stylesheet" href="style/nav.css" type="text/css"/>
            </head>
            <body>
                <h1>{chapter['title']}</h1>
                {chapter['content']}
            </body>
            </html>
        '''

        c.add_item(nav_css)
        book.add_item(c)
        epub_chapters.append(c)
        spine.append(c)

        if current_part:
            part_chapters.append(c)
        else:
            toc.append(c)

    # Add last part
    if current_part and part_chapters:
        toc.append((epub.Section(current_part), part_chapters))

    # Configure spine and toc
    book.toc = toc
    book.spine = spine

    # Add navigation files
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())

    # Write EPUB file
    epub.write_epub(output_file, book)
    print(f"EPUB created successfully: {output_file}")

def main():
    # Read LaTeX file
    with open('lighthouse_within.tex', 'r', encoding='utf-8') as f:
        latex_content = f.read()

    print("Parsing LaTeX content...")
    book_data = extract_content(latex_content)

    print(f"Found {len(book_data['chapters'])} chapters")

    print("Creating EPUB file...")
    create_epub(book_data, 'lighthouse_within.epub')

    print("\n✓ Conversion complete!")
    print("Output: lighthouse_within.epub")
    print("\nThis file is ready to be uploaded to:")
    print("  • Amazon Kindle Direct Publishing (KDP)")
    print("  • Apple Books")
    print("  • Other ebook retailers")

if __name__ == '__main__':
    main()
