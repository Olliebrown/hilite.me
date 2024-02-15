# hilite.me

hilite.me is a small webapp that converts your code snippets into pretty-printed HTML
format, easily embeddable into blog posts and websites.  The webapp is split into a
backend api and a simple frontend example that uses the api.

Note that the original hilite.me (and the corresponding website) are out of date. They
were build with earlier versions of both Python and Pygments. This fork amends the code
to run with Python 3 and the latest version of Pygments.

## Backend API

The API provides a single endpoint at `./api` that accepts a GET or POST request. The
endpoint accepts the following query-parameter encoded properties:
- `code` (required): The code to be highlighted.
- `lexer`: The [pygments lexer](http://pygments.org/docs/lexers/) to use for highlighting
    corresponding to the language of the code. The default is `python`.
- `style`: The [pygments style](http://pygments.org/docs/styles/) to use for highlighting
    the code. The default is `colorful`.
- `linenos`: Whether to include line numbers in the output. Leave empty to disable. The
    default is no line numbers.
- `divstyles`: The CSS styles to apply to the outer wrapping div. `overflow:auto;width:auto;`
    is always included. The default will add `border:solid gray;border-width:.1em .1em .1em .8em;padding:.2em .6em;`
- `options`: Comma-separated list of lexer specific options in the form `key=value`

The endpoint returns the highlighted code as HTML but with a content type of `text/plain` so
that it can be more easily embedded into other context instead of being rendered by a browser.

If the `code` parameter is not provided, the API will return a plain text description of how
to use the endpoint.

## Development

To set up a development environment, it is recommended to use virtualenv:

- `virtualenv env`
- `source env/bin/activate`
- `pip3 install -r requirements.txt` or `python3 -m pip install -r requirements.txt`

Type `make run` (or simply run 'main.py') and then visit http://localhost:5001 to use
the app. This employs the Flask development server, which is not suitable for production
use.  A WSGI server is recommended for production use (see run-uwsgi for an example).
