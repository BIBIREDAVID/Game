from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

from models import User, Quiz, Question, Result

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = bcrypt.generate_password_hash(request.form['password']).decode('utf-8')
        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        flash('Account created!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            flash('Logged in successfully!', 'success')
            return redirect(url_for('quiz'))
        else:
            flash('Login failed. Check your credentials.', 'danger')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have logged out.', 'info')
    return redirect(url_for('index'))

@app.route('/quiz', methods=['GET', 'POST'])
@login_required
def quiz():
    quiz = Quiz.query.first()  # Fetch the first quiz for simplicity
    if request.method == 'POST':
        score = 0
        for question in quiz.questions:
            answer = request.form.get(str(question.id))
            if answer == question.correct_answer:
                score += 1
        result = Result(user_id=current_user.id, score=score)
        db.session.add(result)
        db.session.commit()
        return redirect(url_for('result', score=score))
    return render_template('quiz.html', quiz=quiz)

@app.route('/result/<int:score>')
@login_required
def result(score):
    return render_template('result.html', score=score)

# API Endpoint to fetch quiz questions
@app.route('/api/quizzes/<int:quiz_id>')
def get_quiz(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    questions = [{"id": q.id, "text": q.text, "choices": q.choices.split(",")} for q in quiz.questions]
    return jsonify({"quiz_id": quiz.id, "title": quiz.title, "questions": questions})

if __name__ == '__main__':
    app.run(debug=True)
