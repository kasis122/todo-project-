from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    priority = db.Column(db.String(50), nullable=False)
    due_date = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(50), default='Pending')

@app.route('/')
def home():
    tasks = Task.query.all()
    return render_template('dashboard.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add():

    title = request.form['title']
    priority = request.form['priority']
    due_date = request.form['due_date']

    new_task = Task(
        title=title,
        priority=priority,
        due_date=due_date
    )

    db.session.add(new_task)
    db.session.commit()

    return redirect('/')

@app.route('/delete/<int:id>')
def delete(id):

    task = Task.query.get(id)

    db.session.delete(task)
    db.session.commit()

    return redirect('/')

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):

    task = Task.query.get(id)

    if request.method == 'POST':

        task.title = request.form['title']
        task.priority = request.form['priority']
        task.due_date = request.form['due_date']
        task.status = request.form['status']

        db.session.commit()

        return redirect('/')

    return render_template('update.html', task=task)

if __name__ == '__main__':

    with app.app_context():
        db.create_all()

    app.run(debug=True)