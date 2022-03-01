from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify, abort, make_response
from flask_mysqldb import MySQL,MySQLdb
import bcrypt
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['SESSION_TYPE'] = 'filesystem'
app.config['MYSQL_HOST'] = 'sql6.freemysqlhosting.net'
app.config['MYSQL_USER'] = 'sql6476219'
app.config['MYSQL_PASSWORD'] = 'ebjfEmemns'
app.config['MYSQL_DB'] = 'sql6476219'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)

@app.route('/')
def home():
    if session:
        cur = mysql.connection.cursor()
        cur.execute("SELECT COUNT(id_user) AS usercount FROM users")
        usercount = cur.fetchall()
        cur.execute("SELECT COUNT(id_hardware) AS hardwarecount FROM hardware")
        hardwarecount = cur.fetchall()
        cur.execute("SELECT hardware.name AS hardwarename, hardware_log.ph_level, hardware_log.temperature, hardware_log.humidity, hardware_log.water_level, hardware_log.image, hardware_log.time FROM hardware_log INNER JOIN hardware ON hardware_log.id_hardware = hardware.id_hardware")
        hardware_log = cur.fetchall()
        cur.execute("SELECT * FROM hardware")
        hardware = cur.fetchall()
        cur.close()
        return render_template("index.html", usercount=usercount, hardwarecount=hardwarecount, hardware_log=hardware_log, hardware=hardware)
    else:
        return redirect(url_for('login'))

@app.route('/login',methods=["GET","POST"])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password'].encode('utf-8')

        curl = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        curl.execute("SELECT * FROM users WHERE email=%s",(email,))
        user = curl.fetchone()
        curl.close()

        if user:
            if bcrypt.hashpw(password, user["password"].encode('utf-8')) == user["password"].encode('utf-8'):
                session['firstname'] = user['first_name']
                session['lastname'] = user['last_name']
                session['email'] = user['email']
                return redirect(url_for('home'))
            else:
                flash('User and password not match!')
                return render_template("login.html")
        else:
            flash('User not found!')
            return render_template("login.html")
    else:
        return render_template("login.html")

@app.route('/logout', methods=["GET", "POST"])
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == 'GET':
        return render_template("register.html")
    else:
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        password = request.form['password'].encode('utf-8')
        hash_password = bcrypt.hashpw(password, bcrypt.gensalt())

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users (first_name, last_name, email, password) VALUES (%s,%s,%s,%s)",(firstname,lastname,email,hash_password,))
        mysql.connection.commit()
        session['firstname'] = request.form['firstname']
        session['lastname'] = request.form['lastname']
        session['email'] = request.form['email']
        return redirect(url_for('home'))

@app.route('/forgot-password', methods=["GET", "POST"])
def forgotpassword():
    return render_template("forgot-password.html")

@app.route('/edit-profile', methods=["GET", "POST"])
def editprofile():
    return render_template("editprofile.html")

@app.route('/updateprofile', methods=["POST"])
def updateprofile():
    email = request.form['email']
    firstname = request.form['firstname']
    lastname = request.form['lastname']
    cur = mysql.connection.cursor()
    cur.execute("UPDATE users SET first_name=%s, last_name=%s WHERE email=%s", (firstname,lastname,email,))
    mysql.connection.commit()
    session['firstname'] = firstname
    session['lastname'] = lastname
    return redirect(url_for('editprofile'))

@app.route('/list-users', methods=["GET", "POST"])
def listusers():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users")
    rv = cur.fetchall()
    cur.close()
    return render_template("list-users.html", users=rv)

@app.route('/adduser',methods=["POST"])
def adduser():
    firstname = request.form['firstname']
    lastname = request.form['lastname']
    email = request.form['email']
    password = request.form['password'].encode('utf-8')
    hash_password = bcrypt.hashpw(password, bcrypt.gensalt())
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO users (first_name, last_name, email, password) VALUES (%s,%s,%s,%s)",(firstname,lastname,email,hash_password,))
    mysql.connection.commit()
    return redirect(url_for('listusers'))

@app.route('/updateuser', methods=["POST"])
def updateuser():
    id_user = request.form['id_user']
    firstname = request.form['firstname']
    lastname = request.form['lastname']
    cur = mysql.connection.cursor()
    cur.execute("UPDATE users SET first_name=%s, last_name=%s WHERE id_user=%s", (firstname,lastname,id_user,))
    mysql.connection.commit()
    return redirect(url_for('listusers'))

@app.route('/deleteuser/<string:id_user>', methods=["GET"])
def hapususer(id_user):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM users WHERE id_user=%s", (id_user,))
    mysql.connection.commit()
    return redirect(url_for('listusers'))

@app.route('/list-hardware', methods=["GET", "POST"])
def listhardware():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM hardware")
    rv = cur.fetchall()
    cur.close()
    return render_template("list-hardware.html", hardware=rv)

@app.route('/addhardware',methods=["POST"])
def addhardware():
    name = request.form['name']
    security_code = request.form['security_code']
    status = request.form['status']
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO hardware (name, security_code, status) VALUES (%s,%s,%s)",(name,security_code,status,))
    mysql.connection.commit()
    return redirect(url_for('listhardware'))

@app.route('/updatehardware', methods=["POST"])
def updatehardware():
    id_hardware = request.form['id_hardware']
    name = request.form['name']
    security_code = request.form['security_code']
    status = request.form['status']
    cur = mysql.connection.cursor()
    cur.execute("UPDATE hardware SET name=%s, security_code=%s, status=%s WHERE id_hardware=%s", (name,security_code,status,id_hardware,))
    mysql.connection.commit()
    return redirect(url_for('listhardware'))

@app.route('/deletehardware/<string:id_hardware>', methods=["GET"])
def hapushardware(id_hardware):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM hardware WHERE id_hardware=%s", (id_hardware,))
    mysql.connection.commit()
    return redirect(url_for('listhardware'))

@app.route('/hardware-details', methods=["GET", "POST"])
def hardwaredetails():
    name = request.args.get('name')
    id_hardware = request.args.get('id_hardware')
    cur = mysql.connection.cursor()
    cur.execute("SELECT hardware.name AS hardwarename, hardware_log.ph_level, hardware_log.temperature, hardware_log.humidity, hardware_log.water_level, hardware_log.image, hardware_log.time FROM hardware_log INNER JOIN hardware ON hardware_log.id_hardware = hardware.id_hardware WHERE hardware_log.id_hardware=%s", (id_hardware,))
    rv = cur.fetchall()
    cur.execute("SELECT * FROM hardware_log WHERE id_hardware=%s ORDER BY time desc LIMIT 10", (id_hardware,))
    rvchart = cur.fetchall()
    cur.close()
    return render_template("detail-hardware.html", hardware_log=rv, hardware_chart=rvchart, hardwarename=name)

@app.route('/addhardwarelog',methods=["POST"])
def addhardwarelog():
    req = request.get_json()
    if req == None:
        abort(make_response({'message': 'No key value detected', 'code':'FORBIDDEN'}, 403))
    id_hardware = req["id_hardware"]
    security_code = req["security_code"]
    curl = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    curl.execute("SELECT * FROM hardware WHERE id_hardware=%s",(id_hardware,))
    hardware = curl.fetchone()
    curl.close()
    if hardware:
        if security_code == hardware["security_code"]:
            id_hardware = req["id_hardware"]
            ph_level = req["ph_level"]
            temperature = req["temperature"]
            humidity = req["humidity"]
            water_level = req["water_level"]
            image = req["image"]
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO hardware_log (id_hardware, ph_level, temperature, humidity, water_level, image) VALUES (%s,%s,%s,%s,%s,%s)",(id_hardware, ph_level, temperature, humidity, water_level, image,))
            mysql.connection.commit()
            return make_response({'message': 'New log successfully added', 'code':'SUCCESS'},201)
        else:
            return make_response({'message': 'Hardware security code not match!', 'code':'FAILED'},201)
    else:
        return make_response({'message': 'Hardware not found!', 'code':'FAILED'},201)

@app.route('/checkhardwarestatus/<string:id_hardware>', methods=["GET"])
def checkhardwarestatus(id_hardware):
    cur = mysql.connection.cursor()
    cur.execute("SELECT name, status FROM hardware WHERE id_hardware=%s LIMIT 1", (id_hardware,))
    rv = cur.fetchall()
    cur.close()
    return make_response(
    {
        'message':'Status hardware successfully fetched', 'code':'SUCCESS',
        'data':rv[0]
    }
        ,201)

@app.errorhandler(404)
def not_found(e):
  return render_template("404.html")

if __name__ == '__main__':
    app.run(debug=True)