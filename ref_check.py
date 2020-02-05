from datetime import datetime, timedelta

from werkzeug.routing import ValidationError


def main():
    try:
        ref_date = datetime.strptime('2000-10-19', '%Y-%m-%d')
        now = datetime.now()
        if not (now - timedelta(days=90) <= ref_date <= now):
            print('Not within 90 days')
            raise ValidationError('Not within 90 days')

    except ValueError as ve:
        print("Date value passed should be in YYYY-mm-dd format and within "
              "the past 90 days:::", ve)

    # use the parse() function to load and parse an XML file
    # tree = ET.parse("data/eurofxref-hist-90d.xml");
    # try:
    #     tree = ET.parse("data/eurofxref-hist-90da.xml");
    # except FileNotFoundError:
    #     return ("XML file not found to fetch rates to sue for convention. "
    #             "Either place conversion file locally or check if URL for "
    #             "fetching latest XML is valid")
    # root = tree.getroot()
    #
    # # print out the document node and the name of the first child tag
    # date = root[2][0].attrib['time']
    #
    # for child in root[2][0].findall(".//*[@currency='USD']"):
    #     print(child.attrib)
    #     print(child.tag)
    #     print(child.attrib['rate'])
    # #
    # cubes = ET.getElementsByTagName("Cube")
    # counter = 0
    # for cube in cubes:
    #     date = cube.getAttribute("time")
    #     # nickname = staff.getElementsByTagName("nickname")[0]
    #     # salary = staff.getElementsByTagName("salary")[0]
    #     # print("id:%s, nickname:%s, salary:%s" %
    #     #       (date, nickname.firstChild.data, salary.firstChild.data))
    #     if date != '':
    #         print("Date:",date)
    #         break
    #     counter += 1
    # latest_conversion_rates = cubes[counter]
    # latest_conversion_date = cubes[counter].getAttribute("time")
    # print(latest_conversion_rates.getElementsByTagName("Cube"))
    # print (latest_conversion_date)
    # # get a list of XML tags from the document and print each one
    # expertise = doc.getElementsByTagName("expertise")
    # print
    # "%d expertise:" % expertise.length
    # for skill in expertise:
    #     print
    #     skill.getAttribute("name")
    #
    # # create a new XML tag and add it into the document
    # newexpertise = doc.createElement("expertise")
    # newexpertise.setAttribute("name", "BigData")
    # doc.firstChild.appendChild(newexpertise)
    # print
    # " "
    #
    # expertise = doc.getElementsByTagName("expertise")
    # print
    # "%d expertise:" % expertise.length
    # for skill in expertise:
    #     print
    #     skill.getAttribute("name")
    #


if __name__ == '__main__':
    main()
