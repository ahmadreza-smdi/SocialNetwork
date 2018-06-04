import tornado.ioloop
import tornado.web
import os
import random
import string
import sqlite3



def generateRandomString(length):
    s = string.ascii_lowercase + string.digits + string.ascii_uppercase
    return str(''.join(random.sample(s, length)))

class SignUpHandler(tornado.web.RequestHandler):
    def post(self):
        name = self.get_argument('name')
        username = self.get_argument('username')
        password = self.get_argument('password')
        location = self.get_argument('location')
        phone_number =self.get_argument('phone_number')
        email = self.get_argument('email')
        bio = self.get_argument('bio')
        birthdate = self.get_argument('birthdate')
        profile_picture = self.get_argument('profile_picture')
        agreement = self.get_argument('agreement')

        self.application.db.execute(
            "INSERT INTO member VALUES(?,?,?,?,?,?,?,?,?,?);",
            [name,username,password,location,birthdate,phone_number,email,bio,profile_picture,agreement]
        )
        self.application.db.commit()
        self.write('Done Successfully')

def make_app():

    settings = {
        "template_path": os.path.join(os.path.dirname(__file__), "templates"),
        "cookie_secret": generateRandomString(50),
    }

    return tornado.web.Application([
        (r"/signup", SignUpHandler),
    ], **settings)


if __name__ == "__main__":
    app = make_app()
    app.db = sqlite3.connect("db.sqlite")
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
