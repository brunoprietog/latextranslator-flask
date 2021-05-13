import os
import subprocess
from flask import Flask, render_template, redirect, url_for, send_file, session
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import SubmitField
from werkzeug.utils import secure_filename
import lt as lt

app = Flask(__name__)
app.config['SECRET_KEY'] = '7110c8ae51a4b5af97be6534caef90e4bb9bdcb3380af008f90b23a5d1616bf319bc298105da20fe' 

class LaTeXFileForm(FlaskForm):
	LaTeXFile = FileField('CARGAR UN ARCHIVO', validators=[FileRequired(), FileAllowed(['tex'], 'Solo están permitidos archivos LaTeX')])
	translator_submit = SubmitField('TRADUCIR')

class DownloadFileForm(FlaskForm):
	download_submit = SubmitField('DESCARGAR ARCHIVO FINAL')

@app.route('/')
def inicio():
	form_translator = LaTeXFileForm()
	session['translate']=False
	return render_template("traduccion.html", form_translator=form_translator)

@app.route('/traduccion/', methods=['GET', 'POST'])
def traduccion():
	form_translator = LaTeXFileForm()
	if form_translator.validate_on_submit():
		f = form_translator.LaTeXFile.data
		filename = secure_filename(f.filename)
		session['filename'] = filename
		f.save(os.path.join('archivos', filename))
		session['translate'] =True
		return redirect(url_for('traduccion'))
	form_download = DownloadFileForm()
	if form_download.validate_on_submit():
		session['translate']=False
		lt.translate("archivos/"+session['filename'])
		cont=0
		final=""
		for i in session['filename']:
			if cont < len(session['filename'])-4: final+=i
			cont+=1
		return send_file('archivos/'+final+' traducido.txt', as_attachment=True)
	if session['translate']==True: return render_template('traduccion.html', form_translator=form_translator, form_download=form_download, translate=session['translate'])
	else: return render_template('traduccion.html', form_translator=form_translator)

@app.route('/instrucciones/')
def instrucciones():
	return render_template("instrucciones.html")

@app.route('/quienes-somos/')
def quienes_somos():
	return render_template("quienes_somos.html")

@app.route('/mas/')
def mas():
	return render_template("mas.html")

if __name__ == "__main__":
	app.run(host='0.0.0.0', port=5000)