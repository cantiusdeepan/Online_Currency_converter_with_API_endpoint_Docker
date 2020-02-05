import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
from xml.etree.ElementTree import ParseError

import requests
from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route("/convert", methods=['GET'])
def return_dest_curr_value():
    """
    This method is called when using the 'convert' endpoint of the API for
    converting amounts from a source currency to destination currency using
    the rates for the past 90 days fetched from "europa.eu". The
    method is called using a http GET request with the following four
    parameters.

    Sample URL: http://localhost:8080/convert?amount=25&reference_date=2020
    -02-04&src_currency=USD&dest_currency=INR

    amount - The amount in source currency that needs to be converted
    reference_date - The reference date to be used for fetching conversion
    rates
    src_currency - The source currency for which the amount is provided
    dest_currency - The destination currency to which the amount will be
    coverted

    :return: The destination currency and amount in JSON format
    """

    # The  parameters from the URL are fetched and saved as local variables

    input_amount = request.args.get('amount', default=-1.0, type=float)
    input_src_curr = request.args.get('src_currency', default='EU', type=str)
    input_dest_curr = request.args.get('dest_currency', default='EU',
                                       type=str)
    input_date = request.args.get('reference_date', default='2000-01-01',
                                  type=str)

    # Some input validations are performed
    try:
        # Check date format and if the date is within the past 90 days
        ref_date = datetime.strptime(input_date, '%Y-%m-%d')
        now = datetime.now()
        if not (now - timedelta(days=90) <= ref_date <= now):
            return ('The reference date should be in the past '
                    '90 days')
    except ValueError as ve:
        return ("Date value passed should be in YYYY-mm-dd format:", ve)

    if (input_amount <= 0.0):
        return ('Input amount should be a positive integer or float value')

    if input_src_curr == 'EU' or input_dest_curr == 'EU':
        return ("Source and destination currencies need to be provided in "
                "three letter format e.g., USD")
    # Fetching the latest xml file for conversion rates and saving it locally
    # If unable to fetch latest xml, locally available file will be used
    try:
        r = requests.get(
                'https://www.ecb.europa.eu/stats/eurofxref/eurofxref-hist'
                '-90d.xml')

        # Raise error if response for request is an Http error
        r.raise_for_status()

        with open('data/eurofxref-hist-90d.xml', 'w') as f:
            f.write(r.text)
    except requests.exceptions.HTTPError as httpErr:
        print("HTTP error raised while fetching XML:", httpErr)
    except requests.exceptions.RequestException as reqErr:
        # catastrophic error. bail.
        print("Exception raised while fetching XML:", reqErr)
    except IOError:
        print(
                "Could not read local XML file check -> "
                "data/eurofxref-hist-90d.xml")

    # use the parse() function to load and parse an XML file
    try:
        tree = ET.parse("data/eurofxref-hist-90d.xml")
    except FileNotFoundError:
        raise ("XML file not found to fetch rates to use for convention. "
               "Either place conversion file locally or check if URL for "
               "fetching latest XML is valid")

    # Initializing rates with reference to the EUR
    src_rate_with_EUR = 1
    dest_rate_with_EUR = 1
    try:
        root = tree.getroot()
        # Fetch the part of the element tree that matches the input reference
        # date provided. Here, root[2] is the parent element of the dates,
        # which in turn is the parent for the exchange rates
        date_child = root[2].findall(".//*[@time='" + input_date + "']")
        if len(date_child) > 0:
            # Find the source and destination rates with reference to EUR on
            # the provided reference date
            # No rates for EUR in XML as EUR is the reference value,
            # so handling conversions to and from EUR using initialization
            if input_src_curr != 'EUR':
                src_curr_child = date_child[0].findall(".//*["
                                                       "@currency='" +
                                                       input_src_curr +
                                                       "']")
                if len(src_curr_child) > 0:
                    src_rate_with_EUR = float(src_curr_child[0].attrib['rate'])
                else:
                    return (
                        "Conversion rate not available for the source "
                        "currency")

            if dest_rate_with_EUR != 'EUR':
                dest_curr_child = date_child[0].findall(".//*["
                                                        "@currency='" +
                                                        input_dest_curr +
                                                        "']")
                if len(dest_curr_child) > 0:
                    dest_rate_with_EUR = float(
                            dest_curr_child[0].attrib['rate'])
                else:
                    return (
                        "Conversion rate not available for the destination "
                        "currency")
        else:
            return ("Conversion rates not available for the specified "
                    "reference date")

    except ParseError as parErr:
        return (
            "Exception raised while parsing XML to fetch conversion rates- "
            "check XML content or input parameter values-  reference date or "
            "Source or destination currencies",
            parErr)

    # Calculate the destination currency value using fetched rates
    try:
        dest_curr_value = round(
                ((input_amount / src_rate_with_EUR) * dest_rate_with_EUR), 2)
    except ZeroDivisionError as zd:
        return ("Zero Division Error, check source currency rate:::", zd)
    # Return the calculated value and currency in json format
    return jsonify({"amount"  : dest_curr_value,
                    "currency": input_dest_curr})


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080)
