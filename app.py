import os
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from cs50 import SQL
from datetime import datetime, date
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)

uri = os.getenv("DATABASE_URL")
if uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://")
db = SQL(uri)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

app.config["TEMPLATES_AUTO_RELOAD"] = True


@app.route("/")
def index():
    if session.get("user_id")  != None:
        return redirect("/home")
    return render_template("index.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "GET":
        if session.get("user_id")  != None:
            return redirect("/home")
        return render_template("signup.html")
    else:
        firstname = request.form.get("first-name")
        lastname = request.form.get("last-name")
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        password_conf = request.form.get("password-conf")
        phone = request.form.get("phone")
        country = request.form.get("country")
        city = request.form.get("city")
        gender = request.form.get("gender")
        time = date.today().strftime("%d %B %Y")


        if not password == password_conf:
            flash("passwords don't match")
            return redirect("/signup")

        if len(password) < 8:
            flash("password must be 8 characters or more")
            return redirect("/signup")

        upper = lower = False
        for x in password:
            if x.isupper():
                upper = True
            if x.islower():
                lower = True

        if not upper or not lower:
            flash("password must contain lowercase and uppercase letters")
            return redirect("/signup")

        if " " in username:
            flash("username must not contain any spaces")
            return redirect("/signup")

        users_username = db.execute(
            "SELECT * FROM users WHERE username = ?", username)
        if not len(users_username) == 0:
            flash("username is taken")
            return redirect("/signup")
        
        users_email = db.execute(
            "SELECT * FROM users WHERE email = ?", email)
        if not len(users_email) == 0:
            flash("this email is already associated with another account")
            return redirect("/signup")
        
        users_phone = db.execute(
            "SELECT * FROM users WHERE phone = ?", phone)
        if not len(users_phone) == 0:
            flash("this phone number is alreay associated with another account")
            return redirect("/signup")

        hashed = generate_password_hash(password)
        db.execute("INSERT INTO users (firstname,lastname,hash,username,phone,email,time,country,city,gender,state) VALUES(?,?,?,?,?,?,?,?,?,?,?)",
                    firstname, lastname, hashed, username, phone, email, time,country,city,gender,"active")
        row = db.execute(
            "SELECT id FROM users WHERE username = ?", username)
        db.execute("INSERT INTO bios (user_id) VALUES(?)", row[0]["id"])
        session["user_id"] = row[0]["id"]
        return redirect("/home")


@app.route("/signin", methods=["GET", "POST"])
def signin():
    if request.method == "GET":
        if session.get("user_id")  != None:
            return redirect("/home")
        return render_template("signin.html")
    else:
        user_input = request.form.get("username-email")
        rows = db.execute("SELECT * FROM users WHERE username = ? OR email = ?",
                          user_input, user_input)

        password = request.form.get("password")

        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], password):
            flash("username and/or password aren't correct")
            return render_template("signin.html")
        
        if rows[0]["state"] == "active":
            flash("you are already signed in on another device")
            return render_template("signin.html")

        session["user_id"] = rows[0]["id"]
        db.execute("UPDATE users SET state = ? WHERE id = ?", "active",rows[0]["id"])
        return redirect("/home")


@app.route("/logout")
def logout():
    if session.get("user_id")  == None:
            return redirect("/")
    
    db.execute("UPDATE users SET state = ? WHERE id = ?", "not active",session["user_id"])
    
    session.clear()

    return redirect("/")

@app.route("/home")
def home():
        if session.get("user_id") == None:
            return redirect("/")

        now = datetime.now()
        user_id = session["user_id"]
        today_date = now.strftime("%B, %Y")
        
        
        notes_count = db.execute("SELECT COUNT(*) FROM notes WHERE user_id = ?",user_id)[0]["count"]
        notes_m_count = db.execute("SELECT COUNT(*) FROM notes WHERE date LIKE ? AND user_id = ?", '%'+today_date,user_id)[0]["count"]
        diary_count = db.execute("SELECT COUNT(*) FROM diary WHERE user_id = ?",user_id)[0]["count"]
        diary_m_count = db.execute("SELECT COUNT(*) FROM diary WHERE date LIKE ? AND user_id = ?", '%'+today_date,user_id)[0]["count"]
        
        arr = [notes_count,notes_m_count,diary_count,diary_m_count]
        
        

        return render_template("home.html",arr=arr)


@app.route("/notes", methods=["GET", "POST"])
def notes():
    if request.method == "GET":
        if session.get("user_id")  == None:
            return redirect("/")
        user_id = session["user_id"]
        user_notes = db.execute(
            "SELECT * FROM notes WHERE user_id = ?", user_id)
        return render_template("notes.html", user_notes=user_notes)
    else:
        user_id = session["user_id"]
        now = datetime.now()
        form_type = request.form.get("submit")
        if form_type == "make":
            title = request.form.get("new-title")
            note = request.form.get("new-note")
            date = now.strftime("%d %B, %Y")
            time = now.strftime("%H:%M")
            db.execute("INSERT INTO notes (user_id,title,note,date,time) VALUES(?,?,?,?,?)",
                       user_id, title, note, date, time)
            return redirect("/notes")
        elif form_type == "edit":
            title = request.form.get("edited-title")
            note = request.form.get("edited-note")
            note_id = request.form.get("id")
            db.execute(
                "UPDATE notes SET title = ?, note = ? WHERE note_id = ?", title, note, note_id)
            return redirect("/notes")
        elif form_type == "yes":
            note_id = request.form.get("id")
            db.execute("DELETE FROM notes WHERE note_id = ?", note_id)
            return redirect("/notes")


@app.route("/diary", methods=["GET", "POST"])
def diary():
    now = datetime.now()
    date = now.strftime("%d %B, %Y")
    time = now.strftime("%H:%M")
    if request.method == "GET":
        if session.get("user_id")  == None:
            return redirect("/")
        user_id = session["user_id"]
        user_diary = db.execute(
            "SELECT * FROM diary WHERE user_id = ?", user_id)
        today_diary = db.execute(
            "SELECT * FROM diary WHERE date = ? and user_id = ?", date,user_id)
        return render_template("diary.html", user_diary=user_diary,today_diary=today_diary)
    else:
        user_id = session["user_id"]
        form_type = request.form.get("submit")
        if form_type == "make":
            title = request.form.get("new-title")
            diary = request.form.get("new-diary")
            db.execute("INSERT INTO diary (user_id,title,diary,date,time) VALUES(?,?,?,?,?)",
                       user_id, title, diary, date, time)
            return redirect("/diary")
        elif form_type == "edit":
            title = request.form.get("edited-title")
            diary = request.form.get("edited-diary")
            diary_id = request.form.get("id")
            db.execute(
                "UPDATE diary SET title = ?, diary = ? WHERE diary_id = ?", title, diary, diary_id)
            return redirect("/diary")
        elif form_type == "yes":
            diary_id = request.form.get("id")
            db.execute("DELETE FROM diary WHERE diary_id = ?", diary_id)
            return redirect("/diary")


@app.route("/settings", methods=["GET", "POST"])
def settings():
    if request.method == "GET":
        if session.get("user_id")  == None:
            return redirect("/")
        user_id = session["user_id"]
        user_data = db.execute("SELECT * FROM users WHERE id = ?",user_id)[0]
        user_bio = db.execute("SELECT * FROM bios WHERE user_id = ?",user_id)[0]
        for x in user_data:
            if not user_data[x]:
                user_data[x] = "was not set"
        return render_template("settings.html",user_data=user_data, user_bio=user_bio)
    else:
        user_id = session["user_id"]
        user_data = db.execute("SELECT * FROM users WHERE id = ?",user_id)[0]
        password = request.form.get("password")

        if len(password) < 8:
            flash("password must be 8 characters or more")
            return redirect("/settings")

        user_password = user_data["hash"]
        form_type = request.form.get("submit")
        if not check_password_hash(user_password,password):
            flash("wrong password")
            return redirect("/settings")
        else:
            if form_type == "delete":
                db.execute("DELETE FROM users WHERE id = ?",user_id)
                db.execute("DELETE FROM notes WHERE user_id = ?",user_id)
                db.execute("DELETE FROM diary WHERE user_id = ?",user_id)
                db.execute("DELETE FROM bios WHERE user_id = ?",user_id)
                session.clear()
                return redirect("/")
            else:
                field_name = request.form.get("type")
                if field_name == "name":
                    firstname = request.form.get("firstname")
                    lastname = request.form.get("lastname")
                    db.execute("UPDATE users SET firstname = ? , lastname = ? WHERE id = ?", firstname,lastname,user_id)
                    return redirect("/settings")
                elif field_name == "username":
                    username = request.form.get("username")
                    users_username = db.execute("SELECT * FROM users WHERE username = ?",username)
                    if len(users_username) != 0:
                        flash("username is taken")
                        return redirect("/settings")
                    db.execute("UPDATE users SET username = ? WHERE id = ?", username,user_id)
                    return redirect("/settings")
                elif field_name == "email":
                    email = request.form.get("email")
                    users_email = db.execute("SELECT * FROM users WHERE email = ?",email)
                    if len(users_email) != 0:
                        flash("email is already associated with another account")
                        return redirect("/settings")
                    db.execute("UPDATE users SET email = ? WHERE id = ?", email,user_id)
                    return redirect("/settings")
                elif field_name == "phone":
                    phone = request.form.get("phone")
                    users_phone = db.execute("SELECT * FROM users WHERE phone = ?",phone)
                    if len(users_phone) != 0:
                        flash("phone number is already associated with another account")
                        return redirect("/settings")
                    db.execute("UPDATE users SET phone = ? WHERE id = ?", phone,user_id)
                    return redirect("/settings")
                elif field_name == "password":
                    if request.form.get("new-password") == request.form.get("new-password-conf"):
                        hash = generate_password_hash(request.form.get("new-password"))
                        db.execute("UPDATE users SET hash = ? WHERE id = ?", hash,user_id)
                        return redirect("/settings")
                    else:
                        flash("passwords don't match")
                        return redirect("/settings")
                elif field_name == "country":
                    country = request.form.get("country")
                    db.execute("UPDATE users SET country = ? WHERE id = ?", country,user_id)
                    return redirect("/settings#info")
                elif field_name == "city":
                    city = request.form.get("city")
                    db.execute("UPDATE users SET city = ? WHERE id = ?", city,user_id)
                    return redirect("/settings#info")
                elif field_name == "gender":
                    gender = request.form.get("gender")
                    db.execute("UPDATE users SET gender = ? WHERE id = ?", gender,user_id)
                    return redirect("/settings#info")
                elif field_name == "status":
                    status = request.form.get("status")
                    db.execute("UPDATE users SET 'marital-status' = ? WHERE id = ?", status,user_id)
                    return redirect("/settings#info")
                elif field_name == "bio":
                    bio = request.form.get("bio")
                    db.execute("UPDATE bios SET bio = ?  WHERE user_id = ?", bio,user_id)
                    return redirect("/settings#info")
