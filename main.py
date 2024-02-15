#!/usr/bin/env python3
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

import datetime
import markdown

from urllib.parse import quote, unquote

from flask import Flask, make_response, render_template, request

from pygments.lexers import get_all_lexers
from pygments.styles import get_all_styles

from tools import *

# Create a new flask app
app = Flask(__name__)

# Main HTML route for the flask app (the 'index.html')
@app.route("/", methods=['GET', 'POST'])
def index():
    # Read all request variables with fallbacks to cookies or default values
    code = request.form.get('code', "print 'hello world!'")
    lexer = (
        request.form.get('lexer', '') or
        unquote(request.cookies.get('lexer', 'python')))
    style = (
        request.form.get('style', '') or
        unquote(request.cookies.get('style', 'colorful')))
    linenos = (
        request.form.get('linenos', '') or
        request.method == 'GET' and
        unquote(request.cookies.get('linenos', ''))) or ''
    divstyles = request.form.get(
        'divstyles', unquote(request.cookies.get('divstyles', '')))
    divstyles = divstyles or get_default_style()

    # Generate list of available lexers (skipping ones with blank aliases) 
    lexers = []
    for l in get_all_lexers():
        if len(l) > 1 and len(l[1]) > 0:
            lexers.append((l[1][0], l[0]))
    lexers.sort(key=lambda a: a[1].lower())

    # Generate HTML for highlighted code to insert in template
    html = hilite_me(code, lexer, {}, style, linenos, divstyles)

    # Local list of styles used in HTML template
    styles = sorted(get_all_styles(), key=str.lower)

    # Create the page to use as response from template
    response = make_response(render_template('index.html', **locals()))

    # Cache the variables in cookies
    next_year = datetime.datetime.now() + datetime.timedelta(days=365)
    response.set_cookie('lexer', quote(lexer), expires=next_year)
    response.set_cookie('style', quote(style), expires=next_year)
    response.set_cookie('linenos', quote(linenos), expires=next_year)
    response.set_cookie('divstyles', quote(divstyles), expires=next_year)

    # Return the response
    return response

# The backend api route
@app.route("/api", methods=['GET', 'POST'])
def api():
    # Was the 'code' variable provided?
    code = request.values.get('code', '')
    if not code:
        mdContent = render_template('api.md')
        response = make_response(markdown.markdown(mdContent))
        response.headers["Content-Type"] = "text/html"
        return response

    # Read the other variables (with fallbacks to defaults)
    lexer = request.values.get('lexer', '')
    options = request.values.get('options', '')
    style = request.values.get('style', '')
    linenos = request.values.get('linenos', '')
    divstyles = request.form.get('divstyles', get_default_style())

    # Function to split all options into key-value pairs
    def convert(item):
        key, value = item
        if value == 'False':
            return key, False
        elif value == 'True':
            return key, True
        else:
            return key, value

    # Split options into key-value dictionary pairs
    options = dict(convert(option.split('=')) for option in options.split(',') if option)

    # Convert the provided code to HTML
    html = hilite_me(code, lexer, options, style, linenos, divstyles)

    # Return the HTML as plain text for easy copy-pasting
    response = make_response(html)
    response.headers["Content-Type"] = "text/plain"
    return response

# When run from command line, serve on localhost:5001
if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5001)
