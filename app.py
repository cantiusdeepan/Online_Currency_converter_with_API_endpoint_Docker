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
            return ('The reference date should be provided and be in the past '
                    '90 days'), 400
    except ValueError as ve:
        return "Reference date value must be passed in YYYY-mm-dd format", 400
    # To make sure missing zeros don't cause issues with date format matching
    # in XML, we are converting the date back from date format to string
    # with zero fill as required
    input_date = str(ref_date.date())

    # Check amount passed is a positive value
    if (input_amount <= 0.0):
        return 'Input amount should be provided and be a positive integer or ' \
               '' \
               '' \
               'float value', 400

    # Check to make sure, source and destination currencies are provided
    if input_src_curr == 'EU' or input_dest_curr == 'EU' or input_src_curr \
            == input_dest_curr:
        return "Source and destination currencies need to be provided in " \
               "three letter format e.g., USD", 400
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
        return "HTTP error raised while fetching XML:" + str(httpErr), 500
    except requests.exceptions.RequestException as reqErr:
        return "Exception raised while fetching XML:" + str(reqErr), 500
    except IOError:
        return "Could not access local XML file check -> " \
               "data/eurofxref-hist-90d.xml", 500

    # use the parse() function to load and parse an XML file
    try:
        tree = ET.parse("data/eurofxref-hist-90d.xml")
    except FileNotFoundError:
        return "XML file not found to fetch rates to use for convention. " \
               "Either place conversion file locally or check if URL for " \
               "fetching latest XML is valid", 503

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
                    return "Conversion rate not available for the source " \
                           "currency", 501

            if input_dest_curr != 'EUR':
                dest_curr_child = date_child[0].findall(".//*["
                                                        "@currency='" +
                                                        input_dest_curr +
                                                        "']")
                if len(dest_curr_child) > 0:
                    dest_rate_with_EUR = float(
                            dest_curr_child[0].attrib['rate'])
                else:
                    return "Conversion rate not available for the " \
                           "destination currency", 501
        else:
            return "Conversion rates not available for the specified " \
                   "reference date", 501

    except ParseError as parErr:
        return "Exception raised while parsing XML to fetch conversion " \
               "rates- " \
               "check XML content or input parameter values-  reference date " \
               "" \
               "or " \
               "Source or destination currencies" + str(parErr), 500

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
    app.run()
