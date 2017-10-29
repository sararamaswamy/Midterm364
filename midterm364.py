import requests
from flask import Flask, request, render_template, json, make_response, url_for, flash, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import Required, Email
import json

app = Flask(__name__)
app.debug = True 

app.config['SECRET_KEY'] = 'bsistudent324'

@app.route('/movieform')
def movieForm():
    return render_template('movieform.html')


@app.route('/movieinfo', methods = ['GET', 'POST'])
def movie_result():
	if request.method == 'GET':
		result = request.args
		params = {}
		params['term'] = result.get('movie')
		resp = requests.get('https://itunes.apple.com/search?', params = params)
		data_return = json.loads(resp.text)
		r = json.dumps(data_return, indent = 2)
		print(r)
		return render_template('movie_info.html', movies = data_return["results"])

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(505)
def internal_server_error(e):
    return render_template('505.html'), 505

@app.route('/albumlinks')
def movieLinks():
    return render_template('albumlinks.html')

@app.route('/specific/album/<artistname>', methods = ['GET', 'POST'])
def specific_album(artistname):
	if request.method == 'GET':
		result = request.args
		params = {}
		params['term'] = artistname
		resp = requests.get('https://itunes.apple.com/search?', params = params)
		data_return = json.loads(resp.text)
		r = json.dumps(data_return, indent = 2)
		print(r)
		return render_template('specificalbums.html', artistdata = data_return["results"])

class ArtistForm(FlaskForm):
    name = StringField('What is your favorite music artist?', validators=[Required()])
    submit = SubmitField('Submit')

@app.route('/wtfform')
def wtf():
    userForm = ArtistForm()
    return render_template('wtfform.html', form=userForm)

@app.route('/wtfresult', methods = ['GET', 'POST'])
def result():
	form = ArtistForm(request.form)
	if request.method=='POST' and form.validate_on_submit():
		return redirect(url_for(result))
		## redirect(url_for(wttf)) --do I want to redirect to original form or the result?
	name = form.name.data
	r = make_response(render_template('wtfresult.html', name= name))
	r.set_cookie('name', name)
	flash('Enter your artist of choice!')
	return r

## testing wtfforms and cookie
## do something
    # if form.validate_on_submit():
    #     name = request.form['name']
    #     response = make_response(render_template('wtfresult.html', form=form, name = name))
    #     response.set_cookie('name', name) ## sets cookie to certain response
    #     print(name)
        # return response
    # flash('Enter your artist of choice!')
    # return redirect(url_for('wtfform'))
    # name = request.cookies.get('name')
    # # print(name)
    # return render_template('wtfresult.html', form=form, name = name)
    	


if __name__ == '__main__':
    app.run()
