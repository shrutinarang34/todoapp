from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime

app = Flask(__name__)
conn = sqlite3.connect("TODO.db")

@app.route('/todo', methods=['POST', 'GET'])
def todo():
    if request.method == 'POST':
        try:
            # SNO=request.form['SNO']
            Title = request.form['Title']
            Description = request.form['Description']
            Date_created = datetime.now()
            with sqlite3.connect("TODO.db") as conn:
              cur = conn.cursor()
              cur.execute('CREATE TABLE IF NOT EXISTS TODO_LIST (SNO INTEGER PRIMARY KEY AUTOINCREMENT, Title TEXT, Description TEXT, Date_created TIMESTAMP)')
              cur.execute("INSERT INTO TODO_LIST ( Title, Description, Date_created) VALUES ( ?, ?, ?)", ( Title, Description, Date_created))
              conn.commit()
            # msg = "Record successfully added"
        except:
            conn.rollback()
            # msg = "Error in insert operation"
        finally:
            conn.close()
            # return f'<html><body>{msg} <h2> <a href="/">Go back to home page</a></h2></body></html>'
            return redirect(url_for('index'))
    else:
        return "Invalid request method."

@app.route('/delete/<int:SNO>', methods=['GET'])
def delete(SNO):
    conn = sqlite3.connect("TODO.db")
    cur = conn.cursor()
    cur.execute("DELETE FROM TODO_LIST WHERE SNO=?", (SNO,))
    conn.commit()
    return redirect(url_for('index'))

@app.route('/update/<int:SNO>', methods=['POST','GET'])
def update(SNO):
    if request.method=="POST":
        title = request.form.get('Title')
        description = request.form.get('Description')
        conn = sqlite3.connect("TODO.db")
        cur = conn.cursor()
        cur.execute("UPDATE TODO_List SET Title=?, Description=? WHERE SNO=?", (title, description, SNO))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    
    conn = sqlite3.connect("TODO.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM TODO_List WHERE SNO=?", (SNO,))
    todo = cur.fetchone()
    conn.close()

    if todo:
        todo = {"title": todo[1], "description": todo[2]}
    else:
        todo = {"title": "", "description": ""}
    return render_template('update.html', SNO=SNO,todo=todo)


@app.route('/About-App')
def AboutApp():
   return render_template('AboutApp.html')


@app.route('/')
def index():
    conn = sqlite3.connect("TODO.db")
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT * FROM TODO_LIST")
    rows = cur.fetchall()
    return render_template("index.html", data=rows)



if __name__ == '__main__':
    app.run()


