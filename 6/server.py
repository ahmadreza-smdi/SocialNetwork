import tornado.ioloop
import tornado.web
import os
import random
import string
import sqlite3
import time


date = str(time.asctime( time.localtime(time.time()) ))
class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("username")

def generateRandomString(length):
    s = string.ascii_lowercase + string.digits + string.ascii_uppercase
    return str(''.join(random.sample(s, length)))


class MainHandler(BaseHandler):
    def get(self):
        self.render("login.html")

class todo(BaseHandler):
    @tornado.web.authenticated
    def get (self):
        self.render("todo.html")

    


class SignInHandler(BaseHandler):
    def get(self):
        self.render("login.html")

    def post(self):
        username = self.get_argument("username")
        password = self.get_argument("password")
        query = 'SELECT * FROM "member" WHERE "m_username" = ? AND "m_password"=?'
        cur = self.application.db.execute(query,[username,password])
        res = cur.fetchone()
        if not res:
            self.render("login.html")

        else:
            self.set_secure_cookie("username",res[0])
            self.redirect('/todo')


class LogOut(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.clear_cookie("username")
        self.redirect("/signin")

class SignUpHandler(BaseHandler):

    def get(self):
        self.render("signup.html")
   
   
    def post(self):
        username = self.get_argument('username')
        password = self.get_argument('password')
        self.application.db.execute("INSERT INTO member VALUES(?,?);",[username,password])
        self.application.db.commit()
        self.render("login.html")

if __name__ == "__main__":

    settings = {
        "static_path": os.path.join(os.path.dirname(__file__), "static"),
        "template_path": os.path.join(os.path.dirname(__file__), "templates"),
        "cookie_secret": generateRandomString(50),
        "login_url": "/login",
    }

    app = tornado.web.Application([
        (r"/", MainHandler),
        (r"/signup", SignUpHandler),
        (r"/login",SignInHandler),
        (r"/todo",todo),
        (r"/logout",LogOut)
    ], **settings)

    app.db = sqlite3.connect("db.sqlite")
    app.listen(9090)
    tornado.ioloop.IOLoop.current().start()
