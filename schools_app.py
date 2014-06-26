# -*- coding: utf-8 -*-
from flask import Flask
from flask import g
from flask import render_template
from flask import abort
from flask import request
from flask import url_for
from flask import redirect
from flask import session
from forms import ContactForm
from gevent.wsgi import WSGIServer
from db_methods import get_districts, get_schools, get_similar_schools
from db_methods import get_id_for_selected_school
import json

app = Flask(__name__)
app.secret_key = 'temporary development key'


@app.route('/')
def cover_page():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/main')
def main_page():
    districts = get_districts()
    return render_template('main.html', district_list=districts)


@app.route('/schools/')
def choose_school():
    district = request.args.get('district')
    schools = get_schools(district)
    return render_template('choose_school.html', school_list=schools)


@app.route('/results/')
def results_page():
    school_name = request.args.get('school')
    number_to_return = request.args.get('numschools')
    results = not_implemented_db_get_results(school, numschools)
    return render_template('results.html', results)


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if request.method == 'POST':
        return 'Form posted.'
    elif request.method == 'GET':
        return render_template('contact.html', form=form)


def get_results(school_id, school_type, num2return):
    # not needed
    return get_similar_schools(school_id, school_type, num2return)

if __name__ == '__main__':
    http_server = WSGIServer(('', 5000), app)
    http_server.serve_forever()
