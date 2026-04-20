from flask import render_template, request, redirect,Flask
from werkzeug.security import generate_password_hash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column

@app.route("/signup",methods = ["GET","POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]     
        password = request.form["password"]

        if not username or not password:
            return render_template("signup",error = "All field is required")
        
        for user in users: 
            if user["username"] == username: 
                return render_template("signup.html", error="User already exists")
            
        hashed_password = generate_password_hash(password)

        users.append({ "username": username, "password": hashed_password })

        return redirect("/login")
    
    return render_template("signup.html")

if(__name__ == "__main__"):
    app.run(debug=True)