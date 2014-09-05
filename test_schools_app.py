# -*- coding: utf-8 -*-
import pytest
import schools_app


@pytest.fixture(scope='session')
def testapp():
    app = schools_app.app.test_client()
    schools_app.app.config['TESTING'] = True
    return app


def test_root_url_resolves_to_index_page_view(testapp):
    app = testapp
    root_view = app.get('/')
    assert 'School Clustering' in root_view.data


def test_about_url_resolves_to_about_page_view(testapp):
    app = testapp
    about_view = app.get('/about')
    assert 'About' in about_view.data


def test_home_url_resolves_to_home_page_view(testapp):
    app = testapp
    home_view = app.get('/home')
    assert 'Home' in home_view.data


def test_district_url_resolves_to_district_page_view(testapp):
    app = testapp
    district_view = app.get('/district')
    assert 'Select District' in district_view.data


def test_district_submit_invalid_input_returns_to_district(testapp):
    app = testapp
    results = app.post('/district', data=dict(district=None),
                       follow_redirects=True)
    assert 'Select District' in results.data


def test_schools_url_with_valid_input_resolves_to_schools_view_page(testapp):
    app = testapp
    schools_view = app.get('/schools/?district="Enumclaw School District"')
    assert 'Select School' in schools_view.data


def test_schools_url_with_valid_input_contains_correct_data(testapp):
    app = testapp
    schools_view = app.get('/schools/?district="Enumclaw School District"')
    assert 'Enumclaw School District' in schools_view.data


def test_results_url_with_valid_input_resolves_to_results_view_page(testapp):
    app = testapp
    with app.session_transaction() as sess:
        sess['district'] = 'Enumclaw School District'
    results_view = app.get('/results/?school=Enumclaw Middle School'
                           '&numschools=10'
                           '&enrollment=normalized_enrollment&grade=7')
    assert 'Results' in results_view.data


def test_results_url_with_valid_input_contains_correct_data(testapp):
    app = testapp
    with app.session_transaction() as sess:
        sess['district'] = 'Enumclaw School District'
    results_view = app.get('/results/?school=Enumclaw Middle School'
                           '&numschools=10'
                           '&enrollment=normalized_enrollment&grade=7')
    assert 'Enumclaw Middle School' in results_view.data


def test_demographics_url_resolves_to_demographics_view(testapp):
    app = testapp
    demo_view = app.get('/demographics')
    assert 'Select Demographics' in demo_view.data


def test_cluster_scores_url_with_valid_input_resolves_to_cluster_view(testapp):
    app = testapp
    cluster_view = app.get('/clusters?enrollment=normalized_enrollment'
                           '&grade=7&test=reading')
    assert 'Test Score Histograms for Clusters' in cluster_view.data


def test_cluster_scores_url_with_valid_input_contains_correct_data(testapp):
    app = testapp
    cluster_view = app.get('/clusters?enrollment=normalized_enrollment'
                           '&grade=7&test=reading')
    assert 'Grade 7' in cluster_view.data
    assert 'Reading' in cluster_view.data


def test_contact_page_resolves_to_contact_page(testapp):
    app = testapp
    contact_view = app.get('/contact')
    assert 'Contact' in contact_view.data
