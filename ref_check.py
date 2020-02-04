import xml.etree.ElementTree as ET


def main():
    # use the parse() function to load and parse an XML file
    tree = ET.parse("data/eurofxref-hist-90d.xml");
    root = tree.getroot()

    # print out the document node and the name of the first child tag
    date = root[2][0].attrib['time']

    for child in root[2][0].findall(".//*[@currency='USD']"):
        print(child.attrib)
        print(child.tag)
        print(child.attrib['rate'])
    #
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
