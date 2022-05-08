from flask import Flask, request, render_template, redirect, session, choice, flash
from surveys import Question, Survey, survey
from flask_debugtoolbar import DebugToolbarExtension

RESPONSES_KEY = "responses"

app = Flask(__name__)
app.config['SECRET_KEY'] = "secret"
app.debug = True
debug = DebugToolbarExtension(app)

@app.route("/")
def show_survey():
    return render_template("start_survey.html", survey=survey)

@app.route("/start", methods=["POST"])
def start_survey():
    session[RESPONSES_KEY] = []
    return redirect("/questions/0")

@app.route("/answer", methods=["POSTS"])
def answered_question():
    choice = request.form['answer']

    responses = session[RESPONSES_KEY]
    responses.append(choice)
    if(len(responses) == len(survey.questions)):
        return redirect("/complete")

@app.route("/questions/<int:qnum>")
def show_questions(qnum):
    responses = session.get(RESPONSES_KEY)
    
    if (responses is None):
        return redirect("/")

    if (len(responses) == len(survey.questions)):
        flash("Thank you for answering the question!")
        return redirect("/complete")

    if (len(responses) != qnum):
        flash(f"Not the correct question order, please try again!")
        return redirect(f"/questions/")

    question = survey.questions[qnum]
    return render_template("questions.html", question_num=qnum, question=question)


@app.route("/complete")
def completed():
    return render_template("completed.html")


if __name__ == "__main__":
  app.run(debug=True)