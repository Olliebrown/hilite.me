# hilite.me API documentation

GET or POST to http://hilite.me/api with these parameters (query-string encoded):

* __`code`__: source code to format
* __`lexer`__: [lexer](http://pygments.org/docs/lexers/) to use, default is `python`
* __`options`__: optional comma-separated list of lexer options
* __`style`__: [style](http://pygments.org/docs/styles/) to use, default is `colorful`
* __`linenos`__: if not empty, the HTML will include line numbers
* __`divstyles`__: CSS style to use in the wrapping &lt;div&gt; element, can be empty

The request will return the HTML code in UTF-8 encoding (with a text/plain content type).
