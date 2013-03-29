# coding: utf-8
import tornado.web


class AdminMenu(tornado.web.RequestHandler):
    def head(self, text, level=2):
        return '<h%s>%s</h%s>' % (level, text, level)

    def link(self, href):
        # http://www.tornadoweb.org/documentation/escape.html
        # tornado.escape.linkify
        return '<a href="%s">%s</a><br/>' % (href, href)

    def form(self, action, properties={}):
        r = '<form action="%s" method="post">' % (action,)
        r += '<input type="submit" value="%s"/>' % (action,)
        for prop, value in properties.iteritems():
            r += '<label for="%s">%s</label>' % (prop, prop)
            r += '<input type="text" name="%s" value="%s"/>' % (prop, value)
        r += '</form>'
        return r

    def get(self):
        self.write('<html><body>')
        self.write(self.head('Development', level=1))
        self.write(self.head('Example', level=2))
        self.write(self.link('/admin'))
        self.write(self.form('/form', dict(attr='')))
        self.write('</body></html>')
