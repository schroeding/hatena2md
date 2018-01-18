"""
hatena2md

A Hatena Notation to Markdown Converter
"""

import re
import urllib.request

class Hatena2MD:

    staticConversionTable = [ # (HATENA, MARKDOWN)
        ('****', '######'), # h6
        ('***', '#####'), # h5
        ('**', '####'), # h4
        ('*', '###'), # h3, Hatena Notation cannot decode h1 & h2, see https://help-en.hatenablog.com/entry/text-hatena-list
        ('++', '\t+'), # lists, just 
        ('+', '+ '),
        ('--', '\t+'),
        ('-', '+ '),
    ]

    text = None

    def __init__(self, text: str):
        if (not isinstance(text, str)):
            raise ValueError('text must be a str')
        self.text = text

    def __getURLMarkdown(self, url: str, title: str) -> str:
        if (isinstance(title, bool) and title):
            try:
                _webpage = urllib.request.urlopen(url).read() # TODO: very doubleplusungood :-D
                _webpageTitel = str(_webpage).split('<title>')[1].split('</title>')[0]
            except (Exception):
                _webpageTitel = url
            return f'[{_webpageTitel}]({url})'
        elif (isinstance(title, str)):
            if (title == ':title'):
                return self.__getURLMarkdown(url, True)
            else:
                return f'[{title[7:]}]({url})'
        else:
            return f'[{url}]({url})'

    def toMarkdown(self):
        convertedText = str()

        isCode = False
        isBlockQuote = False
        footnotes = []
        contents = []
        for line in self.text.splitlines(True):
            match = None

            # Code-Super-Pre
            match = re.search(r'^\|\|<', line)
            if (match != None):
                isCode = False
                line = re.sub(r'^\|\|<', '```', line)
            match = re.search(r'^>\|[a-zA-Z0-9]*\|', line)
            if (match != None):
                isCode = True
                line = re.sub(r'^>\|[a-zA-Z0-9]*\|', f'```{match.group()[2:-1]}', line)
            if (isCode):
                convertedText += line
                continue

            # Block-Quote
            match = re.search(r'^<<', line)
            if (match != None):
                isBlockQuote = False
                line = re.sub(r'^<<', '', line)
            if (isBlockQuote):
                convertedText += '> '
            match = re.search(r'^>>', line)
            if (match != None):
                isBlockQuote = True
                line = re.sub(r'^>>', '', line)      

            # ToC
            match = re.search('^\\*+[^\n]+', line)
            if (match != None):
                contents.append((match.group(0).count('*'), (match.group(0).replace('*', '').strip())))

            # Table
            line = re.sub(r'\| (\*([^\|]*\|)+)', lambda y: f'| {y.group(1).replace("*", " ")}\n|{str().join(["---------|" for n in range(y.group(1).count("|"))])}', line)
            # (very hacky)

            # Google Links
            line = re.sub(r'\[google:images:([^:\]]+)(:title(=[^\]]*)?)?\]', lambda y: f'[https://www.google.com/images?q={y.group(1)}&oe=utf-8{str() if y.group(2) is None else y.group(2)}]', line)
            line = re.sub(r'\[google:news:([^:\]]+)(:title(=[^\]]*)?)?\]', lambda y: f'[https://news.google.com/search?q={y.group(1)}&oe=utf-8{str() if y.group(2) is None else y.group(2)}]', line)
            line = re.sub(r'\[google:([^:\]]+)(:title(=[^\]]*)?)?\]', lambda y: f'[https://www.google.com/search?q={y.group(1)}&oe=utf-8{str() if y.group(2) is None else y.group(2)}]', line)

            # Wikipedia
            line = re.sub(r'\[wikipedia:([a-zA-Z]+:)?([^:\]]+)(:title(=[^\]]*)?)?\]', lambda y: f'[https://{"en." if y.group(1) is None else f"{y.group(1)[:-1]}."}wikipedia.org/wiki/{y.group(2)}{str() if y.group(3) is None else y.group(3)}]', line)

            # ISBN / ASIN
            line = re.sub(r'\[isbn:([^:\]]+)(:title(=[^\]]*)?)?\]', lambda y: f'[https://www.amazon.com/exec/obidos/ASIN/{y.group(1)}/{str() if y.group(3) is None else y.group(3)}]', line)
            line = re.sub(r'\[asin:([^:\]]+)(:title(=[^\]]*)?)?\]', lambda y: f'[https://www.amazon.com/exec/obidos/ASIN/{y.group(1)}/{str() if y.group(3) is None else y.group(3)}]', line)

            # Links
            line = re.sub(r'\[(https?://[^ :\]]+)(:title(=[^\]]*)?)?\]', lambda y: self.__getURLMarkdown(y.group(1), y.group(2)), line)
            line = re.sub(r'(https?://[^ :]+)(:title(=[^ ]*)?)', lambda y: self.__getURLMarkdown(y.group(1), y.group(2)), line)
            line = re.sub(r'\[\](https?://[^\[]*)\[\]', lambda y: f'`{y.group(1)}`', line)

            for entry in self.staticConversionTable:
                line = re.sub(f'^({re.escape(entry[0])})( )?', f'{entry[1]} ', line)

            # Footnote
            line = re.sub(r'\(\(([^\)]+)\)\)', lambda y: f'{str() if footnotes.append(y.group(1)) else str()}[^{len(footnotes)}]', line)

            convertedText += line

        for n in range(len(footnotes)):
            convertedText += f'\n[^{str(n + 1)}] {footnotes[n]}'

        toc = str()
        for count, header in contents:
            if (count > 1):
                toc += '>    + '
            else:
                toc += '> + '
            toc += header
            toc += '\n'
        convertedText = convertedText.replace('[:contents]', toc)

        return convertedText