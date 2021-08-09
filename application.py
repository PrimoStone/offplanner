import os
import locale
locale.getlocale()


from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
import datetime
import calendar
from flask_session import Session
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

# Configure application
app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure database
db = SQL("sqlite:///shifts.db")
global vector
global today
global c_year
global c_month
global today
today =datetime.datetime.now()
c_year = today.year
c_month = today.month

c_day = today.day

@app.route("/switch", methods=["POST"])
def switch():

    session["shift"] = request.form["shift"]
    # rows = db.execute("SELECT * FROM 'Shift' WHERE  Id = :id ",id = session["id"])
    rows = db.execute("SELECT * FROM 'Shift' WHERE Company = :company AND Patternname = :pattern AND Shift == :shift",pattern=session["pattern"],shift=session["shift"],company=session["company"])
    shifts = db.execute("SELECT * FROM 'Shift' GROUP BY Company,Patternname")
    shifts_l = list(session["pattern"])
    session['vector'] = 0
    session["cyear"] = 0

    # get current date
    today = datetime.datetime.now()

    # explode results
    c_year = today.year
    c_month = today.month
    c_day = today.day

    # numer of rows for shortest month
    cal_rows = 4
    # first day of month
    first = datetime.datetime(c_year,c_month,1)
    # getting previos month
    prev = datetime.datetime(c_year,c_month-1,1)
    # getting next month
    next_m = datetime.datetime(c_year,c_month+1,1)
    # number of days
    num_d = (next_m-first).days
     # calculate last day of previous month
    previous = (first-prev).days
    # number of day of the week for 1st day of month
    first_day = datetime.datetime(c_year,c_month,1).weekday()
    #shift pattern start

    for row in rows :
        f = '%Y-%m-%d'
        pat_s = datetime.datetime.strptime(row["Shiftstartdate"], f)
        pattern_s = (( first - (pat_s) ).days)%row["Shiftpattern"]-first_day
        shift_p = row["Shiftpattern"]
        session["id"] = row["Id"]
        session["shift"] = row["Shift"]
        session["company"] = row["Company"]
        session["pattern"] = row["Patternname"]



    if (first_day != 0 ) :
        first_day = 0-first_day
        cal_rows = cal_rows +1
    if num_d> 29 :
        cal_rows = cal_rows +1



    day_name = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    calendar.setfirstweekday(calendar.MONDAY)
    weekdays= calendar.Calendar()
    c_month = datetime.date(c_year,c_month,1).strftime("%B %Y")
    # if logged get friends
    if session.get("user_id") :
        user_data = db.execute("SELECT * FROM 'uzers' WHERE Id = :userid",userid=session["user_id"])

        for row in user_data:
            user = row['Username']
        friends = db.execute("SELECT * FROM :user",user=user)
    else:
        friends=""

    return render_template("index.html" ,today = today, weekdays=weekdays,day_name=day_name,
    first_day=first_day,previous=previous,cal_rows=cal_rows, num_d=num_d, rows=rows,c_day=c_day,friends=friends,
    pattern_s=pattern_s,shift_p=shift_p,c_month=c_month,vector = session['vector'],shifts=shifts,shifts_l=shifts_l,company=session["company"],shift=session["shift"],pattern=session["pattern"])

@app.route("/pattern", methods=["POST"])
def pattern():

    # session["pattern"] = request.form["pattern"]
    session["id"] = request.form["Id"]
    # session["shift"] = (session["pattern"])[0]
    rows = db.execute("SELECT * FROM 'Shift' WHERE Id = :id",id=session["id"])
    shifts = db.execute("SELECT * FROM 'Shift' GROUP BY Company,Patternname")
    shifts_l = list(session["pattern"])
    session['vector'] = 0
    session["cyear"] = 0
    # get current date
    today = datetime.datetime.now()

    # explode results
    c_year = today.year
    c_month = today.month
    c_day = today.day

    # numer of rows for shortest month
    cal_rows = 4
    # first day of month
    first = datetime.datetime(c_year,c_month,1)
    # getting previos month
    prev = datetime.datetime(c_year,c_month-1,1)
    # getting next month
    next_m = datetime.datetime(c_year,c_month+1,1)
    # number of days
    num_d = (next_m-first).days
     # calculate last day of previous month
    previous = (first-prev).days
    # number of day of the week for 1st day of month
    first_day = datetime.datetime(c_year,c_month,1).weekday()
    #shift pattern start

    for row in rows :
        f = '%Y-%m-%d'
        pat_s = datetime.datetime.strptime(row["Shiftstartdate"], f)
        pattern_s = (( first - (pat_s) ).days)%row["Shiftpattern"]-first_day
        shift_p = row["Shiftpattern"]
        session["company"] = row["Company"]
        session["pattern"] = row["Patternname"]
        session["shift"] = row["Shift"]
    shifts_l = list(session["pattern"])

    if (first_day != 0 ) :
        first_day = 0-first_day
        cal_rows = cal_rows +1
    if num_d> 29 :
        cal_rows = cal_rows +1
    # week dys names for calenaderdar he
    day_name = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    calendar.setfirstweekday(calendar.MONDAY)
    weekdays= calendar.Calendar()
    c_month = datetime.date(c_year,c_month,1).strftime("%B %Y")

    # get friends for logged user
    if session.get("user_id") :
        user_data = db.execute("SELECT * FROM 'uzers' WHERE Id = :userid",userid=session["user_id"])

        for row in user_data:
            user = row['Username']
        friends = db.execute("SELECT * FROM :user",user=user)
    else:
        friends=""

    return render_template("index.html" ,today = today, weekdays=weekdays,day_name=day_name,
    first_day=first_day,previous=previous,cal_rows=cal_rows, num_d=num_d, rows=rows,c_day=c_day,friends=friends,

    pattern_s=pattern_s,shift_p=shift_p,c_month=c_month,vector = session['vector'],shifts=shifts,shifts_l=shifts_l,company=session["company"],shift=session["shift"],pattern=session["pattern"])



@app.route("/", methods=["GET", "POST"])
def index():

    if request.method == "POST":

        #date

        today =datetime.datetime.now()

        # Navigation
        if request.form["direction"]:
            direction = request.form["direction"]


            if direction == "Prev":
                session["vector"]=session["vector"]+1
                c_month = (today.month-(session["vector"]))%12

                if c_month == 0:
                    c_month=12
                    session["cyear"] = session["cyear"] +1
                    c_year = today.year - (session["cyear"])
                else:
                    c_year = today.year - (session["cyear"])

            if direction == "Next":
                session["vector"]=session["vector"]-1
                c_month = (today.month-(session["vector"]))%12

                if  c_month > 12 :
                    c_month = 1

                    c_year = today.year - (session["cyear"])+1
                #if new month is january add year
                elif c_month == 0:
                    c_month = 12
                    c_year = today.year - (session["cyear"])
                elif c_month ==1:
                    session["cyear"] -=1
                    c_year = today.year - (session["cyear"])
                else:

                    c_year = today.year - (session["cyear"])


        shifts_l = list(session["pattern"])
        rows = db.execute("SELECT * FROM 'Shift' WHERE  Id = :id ",id=session["id"])
        shifts = db.execute("SELECT * FROM 'Shift' GROUP BY Company,Patternname")

        # explode results

        c_day = today.day

        today = datetime.date(c_year,c_month,1)

        # numer of rows for shortest month
        cal_rows = 4
        # first day of monthzy
        first = datetime.datetime(c_year,c_month,1)
        # getting previous month
        if c_month>1:
            prev = datetime.datetime(c_year,(c_month-1),1)
            first_day = datetime.datetime(c_year,c_month,1).weekday()
        elif c_month==1:
            prev = datetime.datetime(c_year-1,12,1)
            first_day = datetime.datetime(c_year,1,1).weekday()

        # getting next month
        if c_month<12:
            next_m = datetime.datetime(c_year,c_month+1,1)
            first_day = datetime.datetime(c_year,c_month,1).weekday()
        elif c_month==12:
            next_m = datetime.datetime(c_year+1,1,1)
            first_day = datetime.datetime(c_year,12,1).weekday()

        # number of days
        num_d = (next_m-first).days
         # calculate last day of previous month
        if num_d<1:
            num_d=31
        previous = (first-prev).days
        # number of day of the week for 1st day of month
        if previous>33:
            previous= 31

        #shift pattern start
        for row in rows :
            # format date
            f = '%Y-%m-%d'
            pat_s = datetime.datetime.strptime(row["Shiftstartdate"], f)
            pattern_s = (( first - (pat_s) ).days)%row["Shiftpattern"]-first_day
            shift_p = row["Shiftpattern"]


        if (first_day >4 ) :
            cal_rows = cal_rows +1
        if (first_day >4 and num_d>29) :
            cal_rows = cal_rows +1
        if (first_day < 5 ) :
            cal_rows = cal_rows +1
        if num_d> 28 :
            cal_rows = cal_rows +1

        first_day = 0-first_day


        day_name = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        calendar.setfirstweekday(calendar.MONDAY)
        weekdays= calendar.Calendar()

        c_month = datetime.date(c_year,c_month,1).strftime("%B %Y")
        # list o f friends
        if session.get("user_id") :
            user_data = db.execute("SELECT * FROM 'uzers' WHERE Id = :userid",userid=session["user_id"])
            for row in user_data:
                user = row['Username']
            friends = db.execute("SELECT * FROM :user",user=user)
        else:
            friends=""

        return render_template("index.html" ,today = today, weekdays=weekdays,day_name=day_name,first_day=first_day,previous=previous,c_day=c_day,vector=session["vector"],
        cal_rows=cal_rows, num_d=num_d, rows=rows, pattern_s=pattern_s,shift_p=shift_p,c_month=c_month,shifts=shifts,shifts_l=shifts_l,company=session["company"],shift=session["shift"],pattern=session["pattern"]
        ,friends=friends)

        # return redirect("/")

    else:

        #Default values for shift to show
        session["id"] = 4


        if  session.get("user_id") == True:
            user_id = session["user_id"]
        else:
            user_id =""

        rows = db.execute("SELECT * FROM 'Shift' WHERE Id = :id",id=session["id"])

        shifts = db.execute("SELECT * FROM 'Shift' GROUP BY Company,Patternname")
        # shifts_l = list(session["pattern"])
        session['vector'] = 0
        session["cyear"] = 0
        # get current date
        today = datetime.datetime.now()

        # explode results
        c_year = today.year
        c_month = today.month
        c_day = today.day

        # numer of rows for shortest month
        cal_rows = 4
        # first day of month
        first = datetime.datetime(c_year,c_month,1)
        # getting previos month
        prev = datetime.datetime(c_year,c_month-1,1)
        # getting next month
        next_m = datetime.datetime(c_year,c_month+1,1)
        # number of days
        num_d = (next_m-first).days
         # calculate last day of previous month
        previous = (first-prev).days
        # number of day of the week for 1st day of month
        first_day = datetime.datetime(c_year,c_month,1).weekday()
        #shift pattern start
        for row in rows :
            # format date
            f = '%Y-%m-%d'
            pat_s = datetime.datetime.strptime(row["Shiftstartdate"], f)
            pattern_s = (( first - (pat_s) ).days)%row["Shiftpattern"]-first_day
            shift_p = row["Shiftpattern"]
            session["company"] = row["Company"]
            session["pattern"] = row["Patternname"]
            session["shift"] = row["Shift"]
            shifts_l = list(session["pattern"])
            # session["id"] = 4

        if (first_day != 0 ) :
            first_day = 0-first_day
            cal_rows = cal_rows +1
        if num_d> 29 :
            cal_rows = cal_rows +1


        day_name = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        calendar.setfirstweekday(calendar.MONDAY)
        weekdays= calendar.Calendar()
        c_month = datetime.date(c_year,c_month,1).strftime("%B %Y")
        # list o f friends
        if session.get("user_id") :
            user_data = db.execute("SELECT * FROM 'uzers' WHERE Id = :userid",userid=session["user_id"])

            for row in user_data:
                user = row['Username']
            friends = db.execute("SELECT * FROM :user",user=user)
        else:
            friends=""

        return render_template("index.html" ,today = today, weekdays=weekdays,day_name=day_name,
        first_day=first_day,previous=previous,cal_rows=cal_rows, num_d=num_d, rows=rows,c_day=c_day,friends=friends,
        pattern_s=pattern_s,shift_p=shift_p,c_month=c_month,vector = session['vector'],shifts=shifts,shifts_l=shifts_l,company=session["company"],shift=session["shift"],pattern=session["pattern"])



@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Fget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):

            flash("ENTER USERNAME")
            return render_template("login.html")

        # Ensure password was submitted
        elif not request.form.get("password"):
            flash("ENTER PASSWORD")
            return render_template("login.html")

        # Query database for username
        username=request.form.get("username")
        rows = db.execute("SELECT * FROM uzers WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["Hash"], request.form.get("password")):
            flash("Ivalid")
            render_template("login.html")

        # Remember which user has logged in
        for row in rows:

            session["user_id"] = row["Id"]
            session["pattern"] = row["Pattern"]
            session["company"] = row["Company"]
            session["shift"] = row["Shift"]
        # User default shift
        shift_id = db.execute("SELECT * FROM  :user ", user = username)
        for row in shift_id:
            session["id"] = row["Shift_Id"]

        # Redirect user to home page

            return redirect("/")

    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/registerr", methods=["GET", "POST"])
def registerr():

    if request.method == "GET":
        # Data for form
        db = SQL("sqlite:///shifts.db")
        companies =  db.execute("SELECT * FROM 'Shift' GROUP BY Company")
        patterns = db.execute("SELECT * FROM 'Shift' GROUP BY Patternname")
        shifts = db.execute("SELECT * FROM 'Shift' GROUP BY Shift")
        return render_template("registerr.html",companies=companies,patterns=patterns,shifts=shifts)
    else:
        # data for forms
        db = SQL("sqlite:///shifts.db")
        companies =  db.execute("SELECT * FROM 'Shift' GROUP BY Company")
        patterns = db.execute("SELECT * FROM 'Shift' GROUP BY Patternname")
        shifts = db.execute("SELECT * FROM 'Shift' GROUP BY Shift")
        name = request.form.get('username')
        passwd = request.form.get('password')
        cpasswd = request.form.get('confirmation')
        company = request.form.get('company')
        pattern = request.form.get('pattern')
        shift = request.form.get('shift')
        if name == '':
            flash("ENTER USERNAME")
            return render_template("registerr.html",companies=companies,patterns=patterns,shifts=shifts)
        elif passwd == '':
            flash("Enter Password")
            return render_template("registerr.html",companies=companies,patterns=patterns,shifts=shifts)
        elif passwd != cpasswd:
            flash("PASSWORDS DOESN'T MATCH")
            return render_template("registerr.html",companies=companies,patterns=patterns,shifts=shifts)
        else:
            db = SQL("sqlite:///shifts.db")
            try:
                register = db.execute("INSERT INTO uzers (Username, Hash, Company, Pattern, Shift) VALUES (:name, :hash, :company, :pattern, :shift)",
                                      name=name, hash=generate_password_hash(passwd),company=company,pattern=pattern,shift=shift)

            except:
                flash("Username already taken")

        db.execute("CREATE TABLE :name ('Name' text,'Surname' text,'Nick' text, 'Company' text, 'Shift' text, 'Department' text, 'Shift_Id' smallint)", name=name)

        return redirect("/")

@app.route("/addperson", methods=["GET", "POST"])
def addperson():

    if request.method == "GET":
        # Data for form
        db = SQL("sqlite:///shifts.db")
        companies =  db.execute("SELECT * FROM 'Shift' GROUP BY Company")
        patterns = db.execute("SELECT * FROM 'Shift' GROUP BY Patternname")
        shifts = db.execute("SELECT * FROM 'Shift' GROUP BY Shift")
        return render_template("addperson.html",companies=companies,patterns=patterns,shifts=shifts)
    else:
        # data for forms
        db = SQL("sqlite:///shifts.db")
        companies =  db.execute("SELECT * FROM 'Shift' GROUP BY Company")
        patterns = db.execute("SELECT * FROM 'Shift' GROUP BY Patternname")
        shifts = db.execute("SELECT * FROM 'Shift' GROUP BY Shift")
        name = request.form.get('name')
        surname = request.form.get('surname')
        nick = request.form.get('nick')
        company = request.form.get('company')
        pattern = request.form.get('pattern')
        shift = request.form.get('shift')
        shift_ID = db.execute("SELECT * FROM 'Shift' WHERE Company=:company AND Patternname=:pattern AND Shift=:shift",company=company,pattern=pattern,shift=shift)
        for row in shift_ID:
            shift_id=row["Id"]
        user_data = db.execute("SELECT * FROM 'uzers' WHERE Id = :userid",userid=session["user_id"])
        for row in user_data:
            user = row['Username']
        if name == '':
            flash("ENTER USERNAME")
            return render_template("addperson.html",companies=companies,patterns=patterns,shifts=shifts)
        elif nick == '':
            flash("ENTER NICK NAME")
            return render_template("addperson.html",companies=companies,patterns=patterns,shifts=shifts)
        elif company == '':
            flash("SELECT COMPANY")
            return render_template("addperson.html",companies=companies,patterns=patterns,shifts=shifts)
        elif pattern == '':
            flash("SELECT PATTERN")
            return render_template("addperson.html",companies=companies,patterns=patterns,shifts=shifts)
        elif shift == '':
            flash("SELECT SHIFT")
            return render_template("addperson.html",companies=companies,patterns=patterns,shifts=shifts)
        else:
            db = SQL("sqlite:///shifts.db")
            try:
                db.execute("INSERT INTO :user (Name, Surname,Nick, Company, Shift, Shift_Id) VALUES (:name, :surname, :nick, :company,  :shift, :shift_id)",user=user,
                                      name=name, surname=surname,nick=nick,company=company,shift=shift,shift_id=shift_id)

            except:
                flash("somethine went wrong")



        return redirect("/")



@app.route("/friends", methods=["GET", "POST"])
def friends():
    rows= db.execute("SELECT * FROM 'Shift' WHERE Id=:id",id=request.form.get('friends'))
    for row in rows:
        session["company"] = row["Company"]
        session["pattern"] = row["Patternname"]
        session["shift"] = row["Shift"]
        session["id"] = row["Id"]

    rows = db.execute("SELECT * FROM 'Shift' WHERE Company= :company AND Patternname = :pattern AND Shift == :shift",company=session["company"],pattern=session["pattern"],shift=session["shift"])
    shifts = db.execute("SELECT * FROM 'Shift' GROUP BY Company,Patternname")
    shifts_l = list(session["pattern"])
    session['vector'] = 0
    session["cyear"] = 0
    # get current date
    today = datetime.datetime.now()

    # explode results
    c_year = today.year
    c_month = today.month

    c_day = today.day


    # numer of rows for shortest month
    cal_rows = 4
    # first day of month
    first = datetime.datetime(c_year,c_month,1)
    # getting previos month
    prev = datetime.datetime(c_year,c_month-1,1)
    # getting next month
    next_m = datetime.datetime(c_year,c_month+1,1)
    # number of days
    num_d = (next_m-first).days
     # calculate last day of previous month
    previous = (first-prev).days
    # number of day of the week for 1st day of month
    first_day = datetime.datetime(c_year,c_month,1).weekday()
    #shift pattern start

    for row in rows :
        f = '%Y-%m-%d'
        pat_s = datetime.datetime.strptime(row["Shiftstartdate"], f)
        pattern_s = (( first - (pat_s) ).days)%row["Shiftpattern"]-first_day
        shift_p = row["Shiftpattern"]



    if (first_day != 0 ) :
        first_day = 0-first_day
        cal_rows = cal_rows +1
    if num_d> 29 :
        cal_rows = cal_rows +1



    day_name = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    calendar.setfirstweekday(calendar.MONDAY)
    weekdays= calendar.Calendar()
    c_month = datetime.date(c_year,c_month,1).strftime("%B %Y")
    # list o f friends
    if session.get("user_id") :
        user_data = db.execute("SELECT * FROM 'uzers' WHERE Id = :userid",userid=session["user_id"])

        for row in user_data:
            user = row['Username']
        friends = db.execute("SELECT * FROM :user",user=user)
    else:
        friends=""

    return render_template("index.html" ,today = today, weekdays=weekdays,day_name=day_name,
    first_day=first_day,previous=previous,cal_rows=cal_rows, num_d=num_d, rows=rows,c_day=c_day,friends=friends,
    pattern_s=pattern_s,shift_p=shift_p,c_month=c_month,vector = session['vector'],shifts=shifts,shifts_l=shifts_l,company=session["company"],shift=session["shift"],pattern=session["pattern"])

