from flask_wtf.file import FileField, FileAllowed, FileRequired
from flask_wtf import FlaskForm
from wtforms import SubmitField
from werkzeug.utils import secure_filename
import latextranslator, os, logging

current_folder = os.path.dirname(os.path.abspath(__file__))

class LaTeXFileForm(FlaskForm):
	LaTeXFile = FileField('', validators=[FileRequired(), FileAllowed(['tex'], 'Extensión no permitida')])
	translator_submit = SubmitField('Traducir')

	def validate_data(self):
		try:
			f = self.LaTeXFile.data
			filename = secure_filename(f.filename)
			# Direction of folder where archive will be saved
			f.save(os.path.join('storage', filename))
			logging.info(f"File saved successfully: {filename}")
			return filename
		except Exception as e:
			logging.error(f"An error has occurred while saving the file: {e}")
			self.error = str(e)

	def translate_file(self):
		try:
			self.error = None
			filename = self.validate_data()
			translated_file = latextranslator.translate(os.path.join(current_folder, '..', '..', 'storage', filename))
			logging.info("File translated successfully")
			return translated_file
		except Exception as e:
			logging.error(f"An error has occurred while translating the file: {e}")
			self.error = str(e)
