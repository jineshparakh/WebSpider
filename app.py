'''
Importing the necessary imports for the flask app
'''
from flask import Flask, render_template, url_for
from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, IntegerField, DecimalField
import validators
from wtforms.validators import (DataRequired, Regexp, NumberRange, URL)
import scrapping #importing the scrapping module created

app = Flask(__name__)
#configuring the secret key
app.config['SECRET_KEY'] = 'be951dcde0aa8ef79d522fe7f3e9e396'

'''
The flask form for taking baseURL and maximum number of levels as input
The maxLevels are purposefully kept small because the timeout is 30s for the request to load on herkoku after deployment
'''
class URLForm(FlaskForm):
    url = StringField('Enter URL to start crawling: ', validators=[DataRequired('URL is required'), URL(
        message='Please enter a valid Base URL')], default='https://www.ubs.com/in/en.html')
    levels = IntegerField('Enter Number of levels:', validators=[NumberRange(
        min=1, max=2, message='Please enter a value between 1 and 2'), DataRequired()], default=1)
    submit = SubmitField('Start Crawling')


'''
The main and only route
'''
@app.route('/', methods=['GET', 'POST'])
def main():
    form = URLForm() #creating the URLForm instance
    if form.validate_on_submit(): #if form is validated then proceed with the crawling and the analysis
        wordCloud, wordsInEachLevel, AvarageLengthOfWordsInEachLevel, bigramCloud = (scrapping.startScraping(form.url.data, form.levels.data-1))
        #rendering the plots template
        return render_template('plots.html', wordCloud=wordCloud, wordsInEachLevel=wordsInEachLevel, AvarageLengthOfWordsInEachLevel=AvarageLengthOfWordsInEachLevel, bigramCloud=bigramCloud)
    #rendering the base template
    return render_template('index.html', form=form)

if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)