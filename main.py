# -*- coding:utf-8 -*- 

import os
import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.options
import restapi
from tornado.options import define, options

define("port", default=8000, help="run on the given port", type=int)

settings = {
    "static_path": os.path.join(os.path.dirname(__file__), "static"),
    "template_path": os.path.join(os.path.dirname(__file__), "templates")
}


if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = tornado.web.Application(
        handlers=[(r'/add/image', restapi.AddImageHandler),
                  (r'/update/image', restapi.ModifyImageHandler),
                  (r'/delete/image', restapi.DeleteImageHandler),
                  (r'/list', restapi.ListHandler),
                  (r'/add/sketch', restapi.AddSketchHandler),
                  (r'/update/sketch', restapi.ModifySketchHandler),
                  (r'/delete/sketch', restapi.DeleteSketchHandler),
                  (r'/add/link', restapi.AddLinkHandler),
                  (r'/update/link', restapi.ModifyLinkHandler),
                  (r'/delete/link', restapi.DeleteLinkHandler),
                  (r'/image/cover', restapi.CoverImageHandler),
                  (r'/list/link', restapi.ListLinkHandler),
                  (r'/visitcount', restapi.VisitCountHandler),
                  (r'/validate', restapi.UserValidateHandler),
        ], **settings
    )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
