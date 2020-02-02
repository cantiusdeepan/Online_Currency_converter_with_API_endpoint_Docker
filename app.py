
app = Flask(__name__)
#app.config['MONGO_URI'] ='mongodb://AdminUser_IDP:MNYC_2018#19@localhost
# :27017/tripLogs'

#mongo = PyMongo(app)

@app.route("/")
def about_page():
    return render_template('about.html', title='About')

@app.route("/trips")
def trips():
    detected_trips= mongo.db.detected_Trips.find({})
    response = [result for
    result in detected_trips]
    json_response = json.dumps(response, default=json_util.default,
                            sort_keys=True,
               indent=4, separators=(',', ':'))
    return render_template("trips.html",
        response=json_response)

@app.route("/users")
def users():
        user_cursor = mongo.db.Users.find({},{"Password":0,"_id":0})
        response = [result for
                    result in user_cursor]
        json_response = json.dumps(response, default=json_util.default,
                                   sort_keys=True,
                                   indent=4, separators=(',', ':'))
        return render_template("users.html",
                               response=response)


import xml.dom.minidom


def main():
    # use the parse() function to load and parse an XML file
    doc = xml.dom.minidom.parse("data/eurofxref-hist-90d.xml");

    # print out the document node and the name of the first child tag
    print
    doc.nodeName
    print
    doc.firstChild.tagName

    # get a list of XML tags from the document and print each one
    expertise = doc.getElementsByTagName("expertise")
    print
    "%d expertise:" % expertise.length
    for skill in expertise:
        print
        skill.getAttribute("name")

    # create a new XML tag and add it into the document
    newexpertise = doc.createElement("expertise")
    newexpertise.setAttribute("name", "BigData")
    doc.firstChild.appendChild(newexpertise)
    print
    " "

    expertise = doc.getElementsByTagName("expertise")
    print
    "%d expertise:" % expertise.length
    for skill in expertise:
        print
        skill.getAttribute("name")



if __name__ == '__main__':
    app.run(host= '0.0.0.0',port=8080)