import tornado.ioloop
import tornado.web
import os
import random
import string
import sqlite3

class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("user")

def generateRandomString(length):
    s = string.ascii_lowercase + string.digits + string.ascii_uppercase
    return str(''.join(random.sample(s, length)))


class MainHandler(BaseHandler):
    def get(self):
        self.render("index.html")


class SignInHandler(BaseHandler):
    def get(self):
        self.render("Signin.html",greeting='false',wrong='false')

    def post(self):
        username = self.get_argument("username")
        password = self.get_argument("password")
        query = 'SELECT * FROM "member" WHERE "m_username" = ? AND "m_password"=?'
        cur = self.application.db.execute(query,[username,password])
        res = cur.fetchone()
        if not res:
            self.render("Signin.html",greeting='false',wrong='true')

        else:
            self.set_secure_cookie("user",res[0])
            self.write("welcom"+res[0])

class ForgetPassHandler(BaseHandler):
    def get(self):
        self.render("forgetpass.html")



class LogOut(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.clear_cookie("user")
        self.redirect("/signin")

class SignUpHandler(BaseHandler):

    def get(self):
        self.render("Signup.html")
   
   
    def post(self):
        name = self.get_argument('name')
        username = self.get_argument('username')
        password = self.get_argument('password')
        location = self.get_argument('location')
        phone_number =self.get_argument('phone_number')
        email = self.get_argument('email')
        bio = self.get_argument('bio')
        birthdate = self.get_argument('birthdate')
        agreement = self.get_argument('agreement')

        self.application.db.execute(
            "INSERT INTO member VALUES(?,?,?,?,?,?,?,?,?,?,?);",
            [name,username,password,location,birthdate,phone_number,email,bio,agreement,0,0]
        )
        self.application.db.commit()
        self.render("Signin.html",greeting='true')

def make_app():

    settings = {
        "static_path": os.path.join(os.path.dirname(__file__), "static"),
        "template_path": os.path.join(os.path.dirname(__file__), "templates"),
        "cookie_secret": generateRandomString(50),
        "login_url": "/signin",

    }

    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/signup", SignUpHandler),
        (r"/signin",SignInHandler),
        (r"/forgetpass",ForgetPassHandler)
    ], **settings)


if __name__ == "__main__":
    app = make_app()
    app.db = sqlite3.connect("db.sqlite")
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
