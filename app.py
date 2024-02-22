from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

responses = []

debug = DebugToolbarExtension(app)


@app.get('/')
def start_survey():
    return render_template('survey_start.html', title=survey.title, instructions=survey.instructions)


@app.post('/begin')
def redirect_to_first_question():
    return redirect('/questions/0')


@app.get('/questions/<int:question_num>')
def render_question(question_num):
    return render_template('question.html', question=survey.questions[question_num])

@app.post('/answer')
def redirect_to_next_question():
    # dot notation to access property form and bracket notation to access the key
    answer = request.form['answer']
    responses.append(answer)

    return redirect(
        f'/questions/{len(responses)}')