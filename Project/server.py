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
        self.render("index.html")



class setting(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        current_user = str(self.current_user, encoding='utf-8')
        query = 'SELECT * FROM "member" WHERE "m_username"=?;'
        cursor = self.application.db.execute(query,[current_user])
        res = cursor.fetchone()
        self.render("settings.html",val=res,change='false')
   
    @tornado.web.authenticated
    def post(self):
        current_user = str(self.current_user, encoding='utf-8')
        name = self.get_argument('name')
        username = self.get_argument('username')
        password = self.get_argument('password')
        location = self.get_argument('location')
        phone_number =self.get_argument('phone_number')
        email = self.get_argument('email')
        bio = self.get_argument('bio')
        birthdate = self.get_argument('birthdate')
        agreement = self.get_argument('agreement')

        query = 'SELECT * FROM "member" WHERE "m_username"=?;'
        cursor = self.application.db.execute(query,[current_user])
        res = cursor.fetchone()
        call_signin = False
        if res[1]!=username or res[2]!=password :
            call_signin = True

        query="UPDATE 'member' SET 'm_name'=?,'m_password'=?,'m_username'=? ,'m_location'=? ,'birthdate'=?,'phone_number'=?,'email'=?,'bio'=?,'agreement'=? WHERE m_username=? ; "
        self.application.db.execute(query,[name, password,username, location, birthdate, phone_number, email, bio, agreement,username])
        self.application.db.commit()

        if call_signin==True:
            self.redirect("/logout")

        query = 'SELECT * FROM "member" WHERE "m_username"=?;'
        cursor = self.application.db.execute(query,[current_user])
        res = cursor.fetchone()
        self.render("settings.html",val=res,change='true')

class postHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.render("post.html")

    @tornado.web.authenticated
    def post(self):
        current_user = str(self.current_user,encoding='utf-8')
        postt = self.get_argument('posttt')
        qu="SELECT m_name from 'member' WHERE m_username = ?"
        namee = self.application.db.execute(qu,[current_user])
        name = namee.fetchone()
        print(name)
        query = "INSERT INTO posts VALUES (?,?,?,?,?);"
        self.application.db.execute(query,[name[0],current_user,postt,date,0])
        self.application.db.commit()
        self.write("successfully")


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
            self.redirect('/firstpage')
class ForgetPassHandler(BaseHandler):
    def get(self):
        self.render("forgetpass.html")
        #we have not have any server but in here we email the guy his password


class profile(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        current_user = str(self.current_user,encoding='utf-8')
        query = 'SELECT * FROM "member" WHERE "m_username"=?;'
        cursor = self.application.db.execute(query,[current_user])
        res = cursor.fetchone()

        queryy='SELECT * FROM "posts" WHERE m_username=?'
        cursorr = self.application.db.execute(queryy,[current_user])
        post = cursorr.fetchall()
        length = len(post)
        self.render("Profile.html",post=post,val=res,length=length)

class firstpage(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        query = " select * from posts"
        cursor = self.application.db.execute(query)
        post = cursor.fetchall()
        length = len(post)
        self.render("firstpage.html",post=post,length=length)

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
            "INSERT INTO member VALUES(?,?,?,?,?,?,?,?,?);",
            [name,username,password,location,birthdate,phone_number,email,bio,agreement]
        )
        self.application.db.commit()
        self.render("Signin.html",greeting='true',wrong='false')

if __name__ == "__main__":

    settings = {
        "static_path": os.path.join(os.path.dirname(__file__), "static"),
        "template_path": os.path.join(os.path.dirname(__file__), "templates"),
        "cookie_secret": generateRandomString(50),
        "login_url": "/signin",
    }

    app = tornado.web.Application([
        (r"/", MainHandler),
        (r"/signup", SignUpHandler),
        (r"/signin",SignInHandler),
        (r"/forgetpass",ForgetPassHandler),
        (r"/logout",LogOut),
        (r"/firstpage",firstpage),
        (r"/about",about),
        (r"/settings",setting),
        (r"/profile",profile),
        (r"/post",postHandler),
        (r"/likes",like)
    ], **settings)

    app.db = sqlite3.connect("db.sqlite")
    app.listen(8989)
    tornado.ioloop.IOLoop.current().start()
