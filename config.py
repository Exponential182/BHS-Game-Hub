ALLOWED_TAGS = {
    "p", "h1", "h2", "h3", "h4", "h5", "h6",
    "li", "ul", "ol", "span", "br", "pre",
    "strong", "em", "b", "u", "s",
    "img", "a",
}

ALLOWED_ATTRIBUTES = {
    "a": {"target", "href"},
    "img": {"src", "alt", "width", "height"},
    "*": {"class"},
}

URL_HEADERS = {
    "http", "https", "mailto"
}
