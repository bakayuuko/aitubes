from flask import Flask, render_template, request
from wtforms import Form, FloatField, validators
from compute import compute

app = Flask(__name__)

# Model
class InputForm(Form):
    p = FloatField(validators=[validators.InputRequired()])
    q = FloatField(validators=[validators.InputRequired()])
    r = FloatField(validators=[validators.InputRequired()])

# View
@app.route('/', methods=['GET', 'POST'])
def index():
    form = InputForm(request.form)
    if request.method == 'POST' and form.validate():
        p = form.p.data
        q = form.q.data
        r = form.r.data
        s = compute(p, q, r)
        return render_template("view_output.html", form=form, s=s)
    else:
        return render_template("view_input.html", form=form)

if __name__ == '__main__':
    app.run(debug=True)
