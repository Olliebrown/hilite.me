# -*- coding: utf-8 -*-
#
# Copyright © 2009-2011 Alexander Kojevnikov <alexander@kojevnikov.com>
#
# hilite.me is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# hilite.me is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with hilite.me.  If not, see <http://www.gnu.org/licenses/>.

import re

from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter

def hilite_me(code, lexer, options, style, linenos, divstyles):
    # Fallback to defaults when a variable is empty
    lexer = lexer or 'python'
    style = style or 'colorful'

    # Default styles we always want included
    defstyles = 'overflow:auto;width:auto;'

    # Create Pygments HtmlFormatter
    formatter = HtmlFormatter(style=style,
                              linenos=False,
                              noclasses=True,
                              cssclass='',
                              cssstyles=defstyles + divstyles,
                              prestyles='margin: 0')

    # Generate HTML and optionally insert line numbers
    html = highlight(code, get_lexer_by_name(lexer, **options), formatter)
    if linenos:
        html = insert_line_numbers(html)

    # Add comment about hilite.me and return
    html = "<!-- HTML generated using hilite.me -->" + html
    return html

def get_default_style():
    return 'border:solid gray;border-width:.1em .1em .1em .8em;padding:.2em .6em;'

def insert_line_numbers(html):
    # Use regex to extract specific parts from the HTML
    match = re.search('(<pre[^>]*>)(.*)(</pre>)', html, re.DOTALL)
    if not match: return html

    # Extract match groups to variables
    pre_open = match.group(1)
    pre = match.group(2)
    pre_close = match.group(3)

    # Generate the line numbers with proper padding and formatting
    numbers = range(1, pre.count('\n') + 1)
    format = '%' + str(len(str(numbers[-1]))) + 'i'
    lines = '\n'.join(format % i for i in numbers)

    # Rewrite each part of the HTML with the line numbers embedded
    html = html.replace(pre_close, '</pre></td></tr></table>')
    html = html.replace(pre_open, '<table><tr><td>' + pre_open + lines + '</pre></td><td>' + pre_open)

    # Return the html with the injected line numbers
    return html
