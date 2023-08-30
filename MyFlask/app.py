from flask import Flask, render_template,redirect, request, flash,session
from flask_sqlalchemy import SQLAlchemy
# from flask.ext.session import Session
import sqlite3
import uuid
from flask_mail import *
from email.message import EmailMessage
import ssl
from email.parser import BytesParser, Parser
import smtplib
from random import randint




app = Flask(__name__)
app.app_context().push()
app.config['SQLALCHEMY_DATABASE_URI'] ="sqlite:///pmb.db"
# app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
db = SQLAlchemy(app)
#mail=Mail(app)
otp= randint(0000,9999)

smtp_port = 587
smtp_server = "smtp.gmail.com"


paswrd = 'waubsrqfbjygvwek'

# msg=Message('otp','pmbexamples@gmail.com','hdexamples@gmail.com')





class user_info(db.Model):
    Sno =db.Column(db.String(),primary_key=True)
    username =db.Column(db.String(200),nullable=False  )
    mob =db.Column(db.Integer, nullable=False)
    password =db.Column(db.String(50), nullable=False)


    def __repr__(self) -> str:
        return f"{self.username} - {self.mob}"

class card_info(db.Model):
    cno = db.Column(db.String(), primary_key= True)
    bank =db.Column(db.String(200),nullable=False)
    card_type =db.Column(db.String(200),nullable=False)
    prch_limit =db.Column(db.Integer(),nullable=False)
    Holder_name =db.Column(db.String(200),nullable=False)
    reset_date =db.Column(db.Integer(),nullable=False)
    email = db.Column(db.String(200),nullable=False)
    commi = db.Column(db.Integer(),nullable=False)
    user_id = db.Column(db.String())
        # return f"{self.Holder_name} - {self.card_type}"



@app.route('/')
def home():
   return render_template('index.html')
   return 'Hello, World!'

@app.route('/About')
def About():
    return 'This is all about!!'


@app.route("/login", methods=['GET', 'POST'])
def login():
    logged_in = False
    cur_user = 'LOGIN'
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password'] 
        login = user_info.query.filter_by(username=username, password=password).first()
        if login is not None:
            user = user_info.query.filter_by(username=username).first()
            cur_user = username
            logged_in = True
            return render_template("index.html",cur_user=cur_user,logged_in=logged_in)
        else:
            print("Invalid!!")
    return render_template("login.html",cur_user=cur_user)
   

@app.route("/logout")
def logout():

    return redirect('/')


@app.route("/signup",methods = ["POST","GET"])  
def signup():  
    msg = ""  
    if request.method == "POST": 
        Sno =str(uuid.uuid4()) 
        username = request.form['username']  
        mob = request.form['mob']  
        password = request.form['password']  

        user = user_info(username = username,mob=mob,password=password,Sno=Sno)
        db.session.add(user)
        db.session.commit()
        msg = username
        print("data saved")

        return redirect("/login")
    return render_template("signup.html")  




@app.route("/add_cards", methods=['GET', 'POST'])
def add_cards():
    if request.method == "POST":
        bank= request.form['bank']  
        card_type = request.form['card_type'] 
        Holder_name= request.form['Holder_name'] 
        prch_limit = request.form['prch_limit']
        commi = request.form['commi']
        reset_date= request.form['reset_date'] 
        email = request.form['email']

        cno = str(uuid.uuid4())
        user_id = Holder_name
        # user_info.query.filter_by(username=request.args.get('u_id',None)).first()

        card = card_info(cno=cno,bank = bank,card_type=card_type,prch_limit=prch_limit,Holder_name=Holder_name,reset_date=reset_date,user_id=user_id,email=email,commi=commi)
        db.session.add(card)
        db.session.commit()
        print("Card Added!!")
        return redirect("/")
    return render_template("add_card.html")  


@app.route('/show_card')
def show_card():
    user_data = card_info.query.all()
    return render_template('show_card.html',user_data=user_data)
    
@app.route("/proceed")
def proceed():
   cno = request.args.get('cno')
   card = card_info.query.filter_by(cno=cno).first()

   return render_template("proceed.html",user_data=[card])


@app.route('/send_email')
def send_email( ):

    otp = randint(0000, 9999)
    print(otp)
    email = get_user_email_from_database()

    gmail = request.form.get('email')
    
    sender_email = 'pmbexamples@gmail.com'
    receiver_email =[gmail]

    message=""" hello user!!
            hope u r doing well.

            We are in our developing stage right now.
            our one of user wants to request for your CREDIT card.
            if  you agree then
             HERE IS UR OTP:
        """+ str(otp)+"""<---If not, Ignore kar Ignore !! """
            
    simple_email_context = ssl.create_default_context()
    TIE_server = smtplib.SMTP(smtp_server, smtp_port)
        
    try:
        print("connecting......")

        TIE_server.starttls(context=simple_email_context)
        TIE_server.login(sender_email, paswrd)
        print('Connected to the server')

        TIE_server.sendmail(sender_email, receiver_email, message)

    except Exception as e:
        print(e)
    finally:
        TIE_server.quit() 
        print("email successfully send")
    return render_template("send_email.html",otp=otp,email=email)

def get_user_email_from_database():
    # Replace this with your database logic
    email ='hdexamples@gmail.com'
    return [email]

# @app.route('/verify',methods=["POST"])
# def verify():
#     gmail=request.form[email]
    
#     message=str(otp)
#     print(otp)

#     return redirect('verified')

    
@app.route("/confirm")
def confirm():
 
   return render_template("confirm.html")


@app.route('/Logged')
def Logged():

    return render_template("Logged.html",user_data=user_data)



    



if __name__ == "__main__":
    db.create_all()
    app.run(debug=True, port=8000 )

   