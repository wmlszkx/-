
import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/movie')
def movie():
    datalist=[]
    con=sqlite3.connect("movie.db")
    cur=con.cursor()
    sql="select * from movie250"
    data=cur.execute(sql)
    for item in data:
        datalist.append(item)
    cur.close()
    con.close()



   
    return render_template("movie.html",movies=datalist)
@app.route('/score')
def score():
    score=[]#评分
    number=[]#评分对应电影数
    con=sqlite3.connect("movie.db")
    cur=con.cursor()
    sql="select score,count(score) from movie250 group by score"#按照评分分组
    data=cur.execute(sql)
    for item in data:
        score.append(item[0])
        number.append(item[1])

        
    cur.close()
    con.close()
    return render_template("score.html",score=score,number=number)

@app.route('/word')
def word():
    return render_template("word.html")

@app.route('/team')
def team():
    return render_template("team.html")

if __name__=='__main__':
    app.run()