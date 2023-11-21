from flask import render_template, send_file, session, Blueprint
from werkzeug.utils import secure_filename
from app.models.latex_file_form import LaTeXFileForm

translation = Blueprint('translation', __name__)

@translation.route('/')
def home():
    form_translator = LaTeXFileForm()
    session['translate'] = False
    return render_template("application.html", form_translator=form_translator)

@translation.route('/translation/', methods=['GET', 'POST'])
def translate():
    form_translator = LaTeXFileForm()
    if form_translator.validate_on_submit():
        translated = form_translator.translate_file()
        if form_translator.error != None:
            session['translate'] = True
            return render_template('application.html', form_translator=form_translator, message_error=form_translator.error)
        else:
            return send_file(translated, as_attachment=True)
    else:
        session['translate'] = True
        return render_template('application.html', form_translator=form_translator, message_error=form_translator.errors['LaTeXFile'][0])
