from flask import json

from app import app


# Testing for Happy path - currencies in XML file, with padded zeros
def test_happy_path():
    with app.test_client() as c:
        r = c.get('/convert', query_string={'amount': 20,
                                            'reference_date': '2020-02-03',
                                            'src_currency': 'USD',
                                            'dest_currency': 'INR'})
        data = json.loads(r.get_data(as_text=True))
    assert r.status_code == 200
    assert data == {"amount": 1427.86, "currency": "INR"}


# Testing for Happy path - currencies in XML file with one currency as
# EUR(not in XML file), and without padded zeros, and float amount
def test_happy_path_eur():
    with app.test_client() as c:
        r = c.get('/convert', query_string={'amount': 20.0,
                                            'reference_date': '2020-2-3',
                                            'src_currency': 'USD',
                                            'dest_currency': 'EUR'})
        data = json.loads(r.get_data(as_text=True))
    assert r.status_code == 200
    assert data == {"amount": 18.07, "currency": "EUR"}


# Testing for bad date formats
def test_bad_date_format():
    with app.test_client() as c:
        r = c.get('/convert', query_string={'amount': 20,
                                            'reference_date': '20-2-3',
                                            'src_currency': 'USD',
                                            'dest_currency': 'INR'})
    assert r.status_code == 400


# Testing for date more than 90 days in the past
def test_bad_date_past():
    with app.test_client() as c:
        r = c.get('/convert', query_string={'amount': 20,
                                            'reference_date': '2019-2-3',
                                            'src_currency': 'USD',
                                            'dest_currency': 'INR'})
    assert r.status_code == 400


# Testing for reference date in the future
def test_bad_date_future():
    with app.test_client() as c:
        r = c.get('/convert', query_string={'amount': 20,
                                            'reference_date': '2020-5-3',
                                            'src_currency': 'USD',
                                            'dest_currency': 'INR'})
    assert r.status_code == 400


# Testing for no reference date
def test_no_ref_date():
    with app.test_client() as c:
        r = c.get('/convert', query_string={'amount': 20,
                                            'src_currency': 'USD',
                                            'dest_currency': 'INR'})
    assert r.status_code == 400


# Testing for no input amount
def test_no_amount():
    with app.test_client() as c:
        r = c.get('/convert', query_string={
            'reference_date': '2020-02-03',
            'src_currency': 'USD',
            'dest_currency': 'INR'})
    assert r.status_code == 400


# Testing for negative input amount
def test_neg_amount():
    with app.test_client() as c:
        r = c.get('/convert', query_string={'amount': -20,
                                            'reference_date': '2020-02-03',
                                            'src_currency': 'USD',
                                            'dest_currency': 'INR'})
    assert r.status_code == 400


# Testing for destination currency- same as source currency
def test_same_src_dest_currency():
    with app.test_client() as c:
        r = c.get('/convert', query_string={'amount': 20,
                                            'reference_date': '2020-02-03',
                                            'src_currency': 'USD',
                                            'dest_currency': 'USD'})
    assert r.status_code == 400


# Testing for no source currency
def test_missing_src_currency():
    with app.test_client() as c:
        r = c.get('/convert', query_string={'amount': 20,
                                            'reference_date': '2020-02-03',
                                            'dest_currency': 'INR'})
    assert r.status_code == 400


# Testing for no destination currency
def test_missing_dest_currency():
    with app.test_client() as c:
        r = c.get('/convert', query_string={'amount': 20,
                                            'reference_date': '2020-02-03',
                                            'src_currency': 'USD'})
    assert r.status_code == 400


# Testing for source currency for which conversion rate is not
# available in XML
def test_non_exist_src_currency():
    with app.test_client() as c:
        r = c.get('/convert', query_string={'amount': 20,
                                            'reference_date': '2020-02-03',
                                            'src_currency': 'DWD',
                                            'dest_currency': 'USD'})
    assert r.status_code == 501


# Testing for destination currency for which conversion rate is not
# available in XML
def test_non_exist_dest_currency():
    with app.test_client() as c:
        r = c.get('/convert', query_string={'amount': 20,
                                            'reference_date': '2020-02-03',
                                            'src_currency': 'USD',
                                            'dest_currency': 'DWD'})
    assert r.status_code == 501


# Testing for reference date for which conversion rate is not
# available in XML
def test_non_exist_ref_date():
    with app.test_client() as c:
        r = c.get('/convert', query_string={'amount': 20,
                                            'reference_date': '2020-02-02',
                                            'src_currency': 'INR',
                                            'dest_currency': 'USD'})
    assert r.status_code == 501
