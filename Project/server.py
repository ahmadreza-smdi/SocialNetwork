import tornado.ioloop
import tornado.web
import os
import random
import string
import sqlite3

class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("username")

def generateRandomString(length):
    s = string.ascii_lowercase + string.digits + string.ascii_uppercase
    return str(''.join(random.sample(s, length)))


class MainHandler(BaseHandler):
    def get(self):
        self.render("index.html")



class setting(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        current_user = str(self.current_user, encoding='utf-8')
        query = 'SELECT * FROM "member" WHERE "m_username"=?;'
        cursor = self.application.db.execute(query,[current_user])
        res = cursor.fetchone()
        self.render("settings.html",val=res)
   
    @tornado.web.authenticated
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
        query="UPDATE 'member' SET 'm_name'=?,'m_password'=?,'m_username'=? ,'m_location'=? ,'birthdate'=?,'phone_number'=?,'email'=?,'bio'=?,'agreement'=? WHERE m_username=? ; "
        self.application.db.execute(query,[name, password,username, location, birthdate, phone_number, email, bio, agreement,username])
        self.application.db.commit()
        self.render("firstpage.html")




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
            self.set_secure_cookie("username",res[1])
            self.render("firstpage.html")
class ForgetPassHandler(BaseHandler):
    def get(self):
        self.render("forgetpass.html")

class firstpage(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.render("firstpage.html")

class LogOut(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.clear_cookie("username")
        self.redirect("/signin")

class about(BaseHandler):   
    def get(self):
        self.render("about.html")
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
        self.render("Signin.html",greeting='true',wrong='false')

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
        (r"/forgetpass",ForgetPassHandler),
        (r"/logout",LogOut),
        (r"/firstpage",firstpage),
        (r"/about",about),
        (r"/settings",setting)
    ], **settings)


if __name__ == "__main__":
    app = make_app()
    app.db = sqlite3.connect("db.sqlite")
    app.listen(8989)
    tornado.ioloop.IOLoop.current().start()
