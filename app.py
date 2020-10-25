from flask import Flask, render_template, url_for, request
from flask_mail import Mail, Message
#import sqlalchemy
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

#set the env to 'PROD' before merge in the main for CI
ENV = 'PROD'

if ENV == 'DEV':
    app.debug = True
    #configure the database localy for testing
    app.config['SQLALCHEMY_DATABASE_URI'] =  'mysql://root:password@localhost/database_name'
else:
    #run the online db (uncomment it first)
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://rugtrpplqvipsm:e7a4c3f4b6cc5da33a85e60bbd73b6f955c4a224567d369268b5db11ea544d77@ec2-18-210-180-94.compute-1.amazonaws.com:5432/d90q5sm991bmr2'

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
            msg = Message(subject="WELCOME TO THE GUILD",
                body ="Hello and welcome. You will receive further communications from our team",
                recipients=[email])
            mail.send(msg)
            return render_template('index.html', message2='You have successfully subscribed to our mailing list!')
        return render_template('index.html')



if __name__ == "__main__":
    app.run(debug=True)
