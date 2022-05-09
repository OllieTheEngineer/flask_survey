from flask import Flask, request, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

RESPONSES_KEY = "responses"

app = Flask(__name__)
app.config['SECRET_KEY'] = "secret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.debug = True
debug = DebugToolbarExtension(app)

@app.route("/")
def show_survey():
    return render_template("start_survey.html", survey=survey)

@app.route("/start", methods=["POST"])
def start_survey():
    session[RESPONSES_KEY] = []
    return redirect("/questions/0")

@app.route("/response", methods=["POSTS"])
def answered_question():
    choice = request.form['response']

    responses = session[RESPONSES_KEY]
    responses.append(choice)
    session[RESPONSES_KEY] = responses
    
    if(len(responses) == len(survey.questions)):
        return redirect("/complete")
    
    else:
        return redirect(f"/questions/{len(responses)}")

@app.route("/questions/<int:qnum>")
def display_question(qnum):
    responses = session.get(RESPONSES_KEY)
    
    if (responses is None):
        return redirect("/")

    if (len(responses) == len(survey.questions)):
        flash("Thank you for answering the question!")
        return redirect("/complete")

    if (len(responses) != qnum):
        flash(f"Not the correct question order: {qnum}, please try again!")
        return redirect(f"/questions/{len(responses)}")

    question = survey.questions[qnum]
    return render_template("questions.html", question_num=qnum, question=question)


@app.route("/complete")
def completed():
    return render_template("completed.html")


if __name__ == "__main__":
  app.run(debug=True)