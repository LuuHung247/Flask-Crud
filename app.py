from flask import Flask, render_template, request, url_for, flash
from werkzeug.utils import redirect
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = 'many random bytes'

app.config['MYSQL_HOST'] = '35.224.201.175'  # Thay thế bằng IP của VM MariaDB
app.config['MYSQL_USER'] = 'myuser'  # Sử dụng người dùng mới
app.config['MYSQL_PASSWORD'] = ''  # KHÔNG CÓ MẬT KHẨU
app.config['MYSQL_DB'] = 'crud'

mysql = MySQL(app)

try:
    cur = mysql.connection.cursor()
    cur.execute("SELECT 1")  # Kiểm tra kết nối
    print("Kết nối MariaDB thành công!")
    cur.close()
except Exception as e:
    print(f"Lỗi kết nối MariaDB: {e}")

@app.route('/')
def Index():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM students")
    data = cur.fetchall()
    cur.close()

    return render_template('index.html', students=data)

@app.route('/insert', methods=['POST'])
def insert():
    if request.method == "POST":
        flash("Data Inserted Successfully")
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO students (name, email, phone) VALUES (%s, %s, %s)", (name, email, phone))
        mysql.connection.commit()
        return redirect(url_for('Index'))

@app.route('/delete/<string:id_data>', methods=['GET'])
def delete(id_data):
    flash("Record Has Been Deleted Successfully")
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM students WHERE id=%s", (id_data,))
    mysql.connection.commit()
    return redirect(url_for('Index'))

@app.route('/update', methods=['POST', 'GET'])
def update():
    if request.method == 'POST':
        id_data = request.form['id']
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']

        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE students SET name=%s, email=%s, phone=%s
            WHERE id=%s
            """, (name, email, phone, id_data))
        flash("Data Updated Successfully")
        return redirect(url_for('Index'))

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)