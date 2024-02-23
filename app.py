from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

# need to replace with session['responses']
# responses = []

debug = DebugToolbarExtension(app)


@app.get('/')
def start_survey():
    """Renders start survey page"""
    # not supposed to change data here in a get, better in redirect_to_first_question
    session['responses'] = []
    return render_template(
        'survey_start.html',
        title=survey.title,
        instructions=survey.instructions)  # Send Whole Surevy


@app.post('/begin')
def redirect_to_first_question():
    """Sends redirect to the first question page"""
    return redirect('/questions/0')


@app.get('/questions/<int:question_num>')
def render_question(question_num):
    """Renders page for a specific question. Redirects to current question if user
    tries to jump ahead or complete survey"""
    # handle edge case of not using a number in URL for queestion

    # make session response a variable
    if len(survey.questions) == len(session['responses']):
        flash('You\'ve already finsihed the survey')
        return redirect('/completion')

    if question_num != len(session['responses']):
        flash(f"Trying to access questions without answering question {len(session['responses'])} first!")
        return redirect(f'/questions/{len(session["responses"])}')
    # make the inputs below into variables question=survey.questions[question_num]
    return render_template('question.html', question=survey.questions[question_num])


@app.post('/answer')
def redirect_to_next_question():
    """Sends redirect to the next unanswered question unless survey has been completed
    , then redirects to completion page"""
    # dot notation to access property form and bracket notation to access the key
    answer = request.form['answer']
    responses = session['responses']

    responses.append(answer)
    session['responses'] = responses

    print(f"**********************************{session['responses']}")

    if len(survey.questions) <= len(session['responses']):
        return redirect('/completion')

    return redirect(f'/questions/{len(session["responses"])}')


@app.get('/completion')
def show_completion():
    """Renders Completion page unless survey hasn't been completed, then redirects
    to current question"""
    if len(session['responses']) != len(survey.questions):
        flash("Trying to access completion! You haven't finished the survey!")
        return redirect(f'/questions/{len(session["responses"])}')

    return render_template(
        'completion.html',
        responses=session['responses'],
        questions=survey.questions)
