import datetime
import xml.etree.ElementTree as ET

import requests


def return_dest_curr_value(input_amount, input_date, input_src_curr,
                           input_dest_curr):
    r = requests.get(
            'https://www.ecb.europa.eu/stats/eurofxref/eurofxref-hist-90d.xml')

    with open('data/eurofxref-hist-90d.xml', 'w') as f:
        f.write(r.text)
    # use the parse() function to load and parse an XML file
    tree = ET.parse("data/eurofxref-hist-90d.xml");
    root = tree.getroot()

    date_xpath = ".//*[@time='" + input_date + "']"
    print("date_xpath:", date_xpath)
    # root[2] is the parent element of the dates, which in turn is the
    # parent for the exchange rates
    for date_child in root[2].findall(date_xpath):

        ref_date = datetime.datetime.strptime(date_child.attrib['time'],
                                              '%Y-%m-%d')
        print("Date:", ref_date.date())
        for src_curr_child in date_child.findall(".//*["
                                                 "@currency='" +
                                                 input_src_curr + "']"):
            src_rate_with_EUR = float(src_curr_child.attrib['rate'])
            break
        for dest_curr_child in date_child.findall(".//*["
                                                  "@currency='" +
                                                  input_dest_curr + "']"):
            dest_rate_with_EUR = float(dest_curr_child.attrib['rate'])
            break

        dest_curr_value = (
                                  input_amount / src_rate_with_EUR) * \
                          dest_rate_with_EUR

        print("dest_curr_value:", dest_curr_value)


if __name__ == '__main__':
    return_dest_curr_value(20, '2020-01-29', 'USD', 'INR')
