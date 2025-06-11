
from flask import Flask, render_template, request,session,redirect,url_for,jsonify
import mysql.connector
import pandas as pd
import numpy as np
from datetime import datetime
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
 
app = Flask(__name__)
app.secret_key="login"


@app.route('/')
def renderhome():
    # Render the 'index.html' template
    return render_template('home.html')



@app.route('/adhome')
def renadhome():
    # Render the 'index.html' template
    return render_template('adminhome.html')

@app.route("/test")
def redir():
    return render_template('index.html')



@app.route("/ureg",methods=["POST"])
def userregister():
    
    if request.method== "POST":
        name=request.form["name"]
        email=request.form["email"]
        passw=request.form["password"]
        gender=request.form["gender"]
        contact=request.form["contact"]
        address=request.form["address"]

        merged_string = f"{name} {email} {passw} {gender} {contact} {address}"
        input_list = [merged_string]
        print(input_list)
        model=joblib.load('sql_injection_model.joblib')
        vectorizer = joblib.load('vectorizer.joblib')
        input_vector = vectorizer.transform(input_list)
        y=model.predict(input_vector)
        print(y)
        if y==1:
            mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="nids")
            mycursor = mydb.cursor()
            mes="The REQUEST BLOCKED DUE TO MALICIOUS ACTIVITY DETECTED"
            current_date = datetime.now().date()  # Extracts only the date
            current_time = datetime.now().time() 
            sql = "INSERT INTO sql_injection_logs (date, time, sql_pattern) VALUES (%s, %s, %s)"
            values = (current_date, current_time, name)
            mycursor.execute(sql, values)
            
            mydb.commit()  # Commit the transaction
            mycursor.close()
            mydb.close()




            return render_template('response.html',message=mes)



        mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="nids")
        mycursor = mydb.cursor()
        """insert_query = 
        INSERT INTO users (name, email, password, contact, gender, address) 
        VALUES (%s, %s, %s, %s, %s, %s)
        
        data = (name, email, passw, gender, contact, address)
        mycursor.execute(insert_query, data)"""

        insert_query = f"""
        INSERT INTO users (name, email, password, contact, gender, address) 
        VALUES ('{name}', '{email}', '{passw}', '{gender}', '{contact}', '{address}')"""
        mycursor.execute(insert_query)
        mydb.commit()  # Commit the transaction
        mycursor.close()
        mydb.close()

        mes="User REGISTERED Sucessfully"

        return render_template('resultreg.html',message=mes)

    return





@app.route("/vadlogin",methods=["POST"])
def validateadlogin():
    
    if request.method== "POST":
        userna=request.form["email"]
        userpass=request.form["password"]

        merged_string = f"{userpass}"
        input_list = [merged_string]
        model=joblib.load('sql_injection_model.joblib')
        vectorizer = joblib.load('vectorizer.joblib')
        input_vector = vectorizer.transform(input_list)
        print(input_list)
        y=model.predict(input_vector)
        print(y)
        if y==1:
            mes="The REQUEST BLOCKED DUE TO MALICIOUS ACTIVITY DETECTED"
            mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="nids")
            mycursor = mydb.cursor()
            mes="The REQUEST BLOCKED DUE TO MALICIOUS ACTIVITY DETECTED"
            current_date = datetime.now().date()  # Extracts only the date
            current_time = datetime.now().time() 
            sql = "INSERT INTO sql_injection_logs (date, time, sql_pattern) VALUES (%s, %s, %s)"
            values = (current_date, current_time, userpass)
            mycursor.execute(sql, values)

            mydb.commit()  # Commit the transaction
            mycursor.close()
            mydb.close()


            return render_template('response.html',message=mes)
            
        


        mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="nids")
        mycursor = mydb.cursor()
        sql = f"SELECT email,password FROM users WHERE email='{userna}'"
        mycursor.execute(sql)
        row = mycursor.fetchone()
        mydb.commit()
        mycursor.close()
        mydb.close()
                
        if row:
            db_username, db_password = row

            if userna==db_username and userpass==db_password:
                mes="User Sucessfully Logged"
                return render_template('resultlog.html',message=mes)
            
            else:
                mes="INCORRECT UserName Or PASSWORD"
                return render_template('response.html',message=mes)
                
        else:
             mes="NO USERFOUND!!"
             return render_template('response.html',message=mes)
            
             
        
    return



@app.route("/logs")
def sql_logs():
    mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="nids")
    mycursor = mydb.cursor()
    mycursor.execute("SELECT date,time,sql_pattern FROM sql_injection_logs ORDER BY date ASC")
    logs = mycursor.fetchall()
    mydb.commit()
    mycursor.close()
    mydb.close()
    return render_template("logs.html", logs=logs)


    

    return



if __name__ == '__main__':
    app.run(debug=True)


