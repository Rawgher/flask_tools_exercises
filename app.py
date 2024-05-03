from surveys import satisfaction_survey as survey
from flask import Flask, render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)

# the toolbar is only enabled in debug mode:
app.debug = True

# set a 'SECRET_KEY' to enable the Flask session cookies
app.config['SECRET_KEY'] = 'itsasecret'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

toolbar = DebugToolbarExtension(app)

RESPONSES = 'responses'

@app.route('/')
def home():
    title = survey.title
    instructions = survey.instructions
    return render_template('home.html', title=title, instructions=instructions)

@app.route('/start', methods=['POST'])
def start():
    session[RESPONSES] = []
    return redirect('/questions/0')

@app.route('/questions/<int:id>')
def questions(id):
    responses = session.get(RESPONSES)
    
    if (responses is None):
        return redirect('/')
    
    if len(responses) == len(survey.questions):
        return redirect('/thank-you')
    
    if len(responses) != id:
        flash(f'Please answer the questions in order! You should be answering question {len(responses) + 1}')
        return redirect(f"/questions/{len(responses)}")
    
    question = survey.questions[id].question
    choices = survey.questions[id].choices

    return render_template('question.html', question=question, choices=choices, id=id)


@app.route('/answer', methods=['POST'])
def post_answer():
    answer = request.form['answer']
    responses = session[RESPONSES]
    responses.append(answer)
    session[RESPONSES] = responses

    if len(responses) == len(survey.questions):
        return redirect('/thank-you')
    else:
        return redirect(f'/questions/{len(responses)}')


@app.route('/thank-you')
def thanks():
    return render_template('thanks.html')