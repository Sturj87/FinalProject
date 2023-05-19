from flask import Flask, render_template, request, redirect
import sqlite3
import datetime

app = Flask(__name__)
DATABASE = 'my_blog.db'

def create_tables():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS posts (id INTEGER PRIMARY KEY AUTOINCREMENT, author_id INT NOT NULL, title TEXT, published_date TEXT, content TEXT)"
    )
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, user_name TEXT NOT NULL, full_name TEXT NOT NULL, password TEXT NOT NULL)"
    )
    conn.commit()
    conn.close()


@app.route('/')
def index():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM posts ORDER BY published_date DESC")
    posts = cursor.fetchall()
    conn.close()
    return render_template('index.html', posts=posts)


@app.route('/dashboard')
def dashboard():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM posts ORDER BY published_date DESC")
    posts = cursor.fetchall()
    conn.close()
    return render_template('dashboard.html', posts=posts)


@app.route('/add_post', methods=['GET', 'POST'])
def add_post():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        published_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        author_id = 1

        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO posts (author_id, title, published_date, content) VALUES (?, ?, ?, ?)",
                       (author_id, title, published_date, content))
        conn.commit()
        conn.close()

        return redirect('/dashboard')
    else:
        return render_template('add_post.html')


@app.route('/edit_post/<int:post_id>', methods=['GET', 'POST'])
def edit_post(post_id):
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute("UPDATE posts SET title = ?, content = ? WHERE id = ?", (title, content, post_id))
        conn.commit()
        conn.close()

        return redirect('/dashboard')
    else:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM posts WHERE id = ?", (post_id,))
        post = cursor.fetchone()
        conn.close()
        return render_template('edit_post.html', post=post)


@app.route('/delete_post/<int:post_id>')
def delete_post(post_id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM posts WHERE id = ?", (post_id,))
    conn.commit()
    conn.close()
    return redirect('/dashboard')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username == 'admin' and password == 'admin':
            return redirect('/dashboard')
        else:
            error = 'Invalid username or password'
            return render_template('login.html', error=error)

    return render_template('login.html')


if __name__ == '__main__':
    create_tables()
    app.run()
