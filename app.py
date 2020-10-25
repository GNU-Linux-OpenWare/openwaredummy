from flask import Flask, render_template, url_for, request
from flask_mail import Mail, Message
#import sqlalchemy
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

#set the env to 'PROD' before merge in the main for CI
ENV = 'DEV'

if ENV == 'DEV':
    app.debug = True
    #configure the database localy for testing
    app.config['SQLALCHEMY_DATABASE_URI'] =  'mysql://root:yourpassword@localhost/database_name'
else:
    #run the online db (uncomment it first)
    app.debug = False
   # app.config['SQLALCHEMY_DATABASE_URI'] =  #paste the url for the database from your heroku account after creating it

# diable mofication tracking
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# initialize the database
db = SQLAlchemy(app)


class Emails(db.Model):
    __table_name__ = 'emails'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(200), unique= True)

    def __init__(self,email):
        self.email = email


app.config['DEBUG'] = True
app.config['TESTING'] = False
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
# app.config['MAIL_DEBUG'] = True
app.config['MAIL_USERNAME'] = 'gnulinuxopenware@gmail.com'
app.config['MAIL_PASSWORD'] = 'club09@.com'
app.config['MAIL_DEFAULT_SENDER'] = ('GNU | Linux OpenWare', 'gnulinuxopenware@gmail.com')
app.config['MAIL_MAX_EMAILS'] = None
app.config['MAIL_SUPPRESS_SEND'] = False
app.config['MAIL_ASCII_ATTACHMENTS'] = False

mail = Mail(app)


@app.route("/")
def index():
    return render_template("index.html")

#create a submit route
@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        email = request.form['email']
        print(email)
        if email == '':
            return render_template('index.html', message = 'This field cannot be empty!')

            #ensure no duplicate emails to avoid db errors
        if db.session.query(Emails).filter(Emails.email==email).count() == 0:
            data = Emails(email)
            db.session.add(data)
            db.session.commit()
            print("yes")
            return render_template('index.html', message2='You have successfully subscribed to our mailing list!')
        return render_template('index.html')


@app.route("/mail")
def send_mail():
    msg = Message(subject="Testing",
                  body ="This is just a bloody test",
                  recipients=['jimmywilliamotieno@gmail.com', 'otienosamwel135@gmail.com', 'jamie.william.284@outlook.com'])
    mail.send(msg)
    return "Sent to recipients"


if __name__ == "__main__":
    app.run(debug=True)
