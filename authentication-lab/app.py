from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase

firebaseConfig = {
  "apiKey": "AIzaSyAoi8zChw_x1RQIzhdy-UHZz8DuwcAjF5g",
  "authDomain": "cs-project-1-c8c59.firebaseapp.com",
  "projectId": "cs-project-1-c8c59",
  "storageBucket": "cs-project-1-c8c59.appspot.com",
  "messagingSenderId": "1075130569298",
  "appId": "1:1075130569298:web:7a3f2ccc522962ac00458b",
  "measurementId": "G-BG9FSH5P21", 
  "databaseURL" : "https://cs-project-1-c8c59-default-rtdb.europe-west1.firebasedatabase.app/"
};

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()
db = firebase.database()

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'


@app.route('/', methods=['GET', 'POST'])
def signin():
    error = ""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            login_session['user'] = auth.sign_in_with_email_and_password(email, password)
            return redirect(url_for('add_tweet'))
        except:
            error = "Authentication failed"
    return render_template("signin.html")



@app.route('/signup', methods=['GET', 'POST'])
def signup():
    error = ""
    if request.method == 'POST':
       email = request.form['email']
       password = request.form['password']
       username = request.form['username']
       full_name = request.form['full_name']
       bio = request.form['bio']
       try:
            login_session['user'] = auth.create_user_with_email_and_password(email, password)
            UID = login_session['user']['localId']
            user = {"email" : email,
                    "password" : password,
                    "username" : username,
                    "full_name" : full_name,
                    "bio" : bio
            }
            db.child("Users").child(UID).set(user)
            return redirect(url_for('add_tweet'))
       except:
           error = "Authentication failed"
    return render_template("signup.html")






@app.route('/add_tweet', methods=['GET', 'POST'])
def add_tweet():
    if request.method == 'POST':
       title = request.form['Title']
       text = request.form['Text']
       try:
            UID = login_session['user']['localId']
            tweet = {"Title" : title,
                    "text" : text,
                    "uid" : UID
            }
            db.child("Tweets").push(tweet)
            return redirect(url_for('tweets'))

       except:
           error = "Authentication failed"
    return render_template("add_tweet.html")


@app.route('/tweets', methods=['GET', 'POST'])
def tweets():
    tweetsDic = db.child("Tweets").get().val()
    print(tweetsDic)
    return render_template("tweets.html", tweets = tweetsDic)



if __name__ == '__main__':
    app.run(debug=True)