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
    """Renders start survey page"""
    return render_template('survey_start.html', title=survey.title, instructions=survey.instructions)  # Send Whole Surevy


@app.post('/begin')
def redirect_to_first_question():
    """Sends redirect to the first question page"""
    return redirect('/questions/0')


@app.get('/questions/<int:question_num>')
def render_question(question_num):
    """Renders page for a specific question"""
    if question_num > len(responses):
        return redirect(f'/questions/{len(responses)}')
    return render_template('question.html', question=survey.questions[question_num])


@app.post('/answer')
def redirect_to_next_question():
    """Sends redirect to the next unanswered question"""
    # dot notation to access property form and bracket notation to access the key
    answer = request.form['answer']
    responses.append(answer)
    print(f"**********************************{responses}")

    if len(survey.questions) <= len(responses):
        return redirect('/completion')

    return redirect(
        f'/questions/{len(responses)}')


@app.get('/completion')
def show_completion():
    """Renders Completion page"""
    if len(responses) != len(survey.questions):
        return redirect(f'/questions/{len(responses)}')
    return render_template('completion.html', responses=responses, questions=survey.questions)
