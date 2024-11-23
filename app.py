from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

mysql = MySQL(app)

@app.route('/')
def index():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM employees")
    employees = cur.fetchall()
    cur.close()
    return render_template('index.html', employees=employees)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        position = request.form['position']
        
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO employees (name, email, position) VALUES (%s, %s, %s)",
                   (name, email, position))
        mysql.connection.commit()
        cur.close()
        
        flash('员工添加成功！')
        return redirect(url_for('index'))
    
    return render_template('add.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    cur = mysql.connection.cursor()
    
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        position = request.form['position']
        
        cur.execute("UPDATE employees SET name=%s, email=%s, position=%s WHERE id=%s",
                   (name, email, position, id))
        mysql.connection.commit()
        flash('员工信息更新成功！')
        return redirect(url_for('index'))
    
    cur.execute("SELECT * FROM employees WHERE id = %s", (id,))
    employee = cur.fetchone()
    cur.close()
    return render_template('edit.html', employee=employee)

@app.route('/delete/<int:id>')
def delete(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM employees WHERE id = %s", (id,))
    mysql.connection.commit()
    cur.close()
    flash('员工删除成功！')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True) 