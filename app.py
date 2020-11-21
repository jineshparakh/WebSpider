from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, IntegerField, DecimalField
import validators
from wtforms.validators import (DataRequired, Regexp, NumberRange, URL)
import scrapping

app = Flask(__name__)
app.config['SECRET_KEY'] = 'be951dcde0aa8ef79d522fe7f3e9e396'


class URLForm(FlaskForm):
    url = StringField('Enter URL to start crawling: ', validators=[DataRequired('URL is required'), URL(
        message='Please enter a valid Base URL')], default='https://www.ubs.com/in/en.html')
    levels = IntegerField('Enter Number of levels:', validators=[NumberRange(
        min=1, max=2, message='Please enter a value between 1 and 2'), DataRequired()], default=1)
    submit = SubmitField('Start Crawling')


@app.route('/', methods=['GET', 'POST'])
def main():
    form = URLForm()
    if form.validate_on_submit():
        # print(form.url.data)
        # print(form.levels.data)
        wordCloud, wordsInEachLevel, AvarageLengthOfWordsInEachLevel, bigramCloud = (
            scrapping.startScraping(form.url.data, form.levels.data-1))
        return render_template('plots.html', wordCloud=wordCloud, wordsInEachLevel=wordsInEachLevel, AvarageLengthOfWordsInEachLevel=AvarageLengthOfWordsInEachLevel, bigramCloud=bigramCloud)
    return render_template('index.html', form=form)


@app.route('/plots')
def plots():
    return render_template('plots.html')


if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)