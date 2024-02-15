# hilite.me API documentation

GET or POST to http://hilite.me/api with these parameters (query-string encoded):

* __code__: source code to format
* __lexer__: [lexer](http://pygments.org/docs/lexers/) to use, default is 'python'
* __options__: optional comma-separated list of lexer options
* __style__: [style](http://pygments.org/docs/styles/) to use, default is 'colorful'
* __linenos__: if not empty, the HTML will include line numbers
* __divstyles__: CSS style to use in the wrapping &lt;div&gt; element, can be empty

The request will return the HTML code in UTF-8 encoding (with a text/plain content type).
