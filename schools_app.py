# -*- coding: utf-8 -*-
from flask import Flask
from flask import render_template
from flask import request
from flask import session
from forms import ContactForm
from gevent.wsgi import WSGIServer
from db_methods import get_districts, get_schools, get_results
from db_methods import get_scores_results


app = Flask(__name__)
app.secret_key = 'temporary development key'


@app.route('/')
def cover_page():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/district', methods=['GET', 'POST'])
def district():
    districts = get_districts()
    return render_template('district.html', district_list=districts)


@app.route('/schools/')
def choose_school():
    district = request.args.get('district')
    session['district'] = district
    schools = get_schools(district)
    return render_template(
        'choose_school.html', school_list=schools,
        district=session['district'])


@app.route('/results/')
def results_page():
    school_name = request.args.get('school')
    number_to_return = request.args.get('numschools')
    grade = request.args.get('grade')
    ret_list = []
    for item in request.args:
        if item in ('school', 'numschools', 'grade'):
            pass
        else:
            ret_list.append(str(request.args.get(item)))
    table_headings = [
        'School', 'District', 'Enrollment', '% Free/Reduced',
        '% American Indian', '% Asian', '% Pacific Islander',
        '% Asian Pacific Islander', '% Black', '% Hispanic',
        '% Migrant', '% Bilingual', '% SPED']
    results, chosen_school = get_results(school_name,
                                         session['district'],
                                         number_to_return,
                                         grade,
                                         tuple(ret_list))
    # workaround to get scores for display - currently am not necessarily
    # getting all scores for a given school.
    scores = []
    score_hdg = []
    for subject in ['reading', 'writing', 'math', 'science']:
        if subject in chosen_school[0]:
            scores.append(subject)
            score_hdg.append(subject.capitalize())
    return render_template('results.html',
                           results=results,
                           target_school=chosen_school,
                           scores=scores,
                           score_hdg=score_hdg,
                           headings=table_headings)


@app.route('/demographics')
def demographics():
    return render_template('demographics.html')


@app.route('/clusters')
def cluster_scores():
    grade = request.args.get('grade')
    test = request.args.get('test')
    ret_list = []
    for item in request.args:
        if item in ('grade', 'test'):
            pass
        else:
            ret_list.append(str(request.args.get(item)))
    table_headings = [
        'Enrollment', '% Free/Reduced',
        '% American Indian', '% Asian', '% Pacific Islander',
        '% Asian Pacific Islander', '% Black', '% Hispanic',
        '% Migrant', '% Bilingual', '% SPED']
    demo_results, scores = get_scores_results(grade,
                                              test,
                                              tuple(ret_list))
    test = test.capitalize()
    cluster0_scores = scores[0]
    cluster1_scores = scores[1]
    cluster2_scores = scores[2]
    cluster3_scores = scores[3]
    return render_template('cluster_scores.html',
                           grade=grade,
                           test=test,
                           table_headings=table_headings,
                           demo_results=demo_results,
                           cluster0_scores=cluster0_scores,
                           cluster1_scores=cluster1_scores,
                           cluster2_scores=cluster2_scores,
                           cluster3_scores=cluster3_scores,
                           )


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if request.method == 'POST':
        return 'Form posted.'
    elif request.method == 'GET':
        return render_template('contact.html', form=form)


if __name__ == '__main__':
    http_server = WSGIServer(('', 5000), app)
    http_server.serve_forever()
    # app.run(debug=True)
