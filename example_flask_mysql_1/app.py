from flask import Flask, render_template, request, json, redirect, url_for
from flask.ext.mysql import MySQL
from werkzeug import generate_password_hash, check_password_hash


app = Flask(__name__)
mysql = MySQL()

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_DB'] = 'BucketList'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

conn = mysql.connect()

@app.route("/")
def home():
    return render_template("index.html")


@app.route('/signup', methods=["GET", "POST"])
def signup():

    if request.method == "GET":
        return render_template('signup.html')

    if request.method == "POST":
        name = request.form['inputName']
        email = request.form['inputEmail']
        password = request.form['inputPassword']
        hashed_password = generate_password_hash(password)
        cursor = conn.cursor()
        cursor.callproc('sp_createUser',(name,email,hashed_password))
        data = cursor.fetchall()

        if len(data) is 0:
            conn.commit()
            print json.dumps({'message':'User created successfully !'})
        else:
            print json.dumps({'error':str(data[0])})

        return redirect(url_for('home'))




if __name__=="__main__":
    app.run()
