from flask import Flask, render_template
from datetime import datetime

import requests, time

app = Flask(__name__)

filterFrom = {
    "CS": {
        "5060",
        "6040",
        "6020",
        "6980",
        "5120",
        "5160",
        "5180",
        "5440",
        "5620",
        "5750",
        "5800",
        "6050",
        "6060",
        "6120",
        "6150",
        "6250",
        "6410",
        "6420",
        "6440",
        "6571",
        "6572",
        "6573",
        "6800",
        "6820",
        "6830",
        "6840",
        "6850",
        "6860",
        "6890",
    },
    "EE": {"6981", "6153", "6633", "6663", "6673", "6743"},
}

# other column settings -> http://bootstrap-table.wenzhixin.net.cn/documentation/#column-options
columns = [
    {
        "field": "classNumber",
        "title": "Class No.",
    },
    {
        "field": "title",  # which is the field's name of data key
        "title": "Course Name",  # display as the table header's name
        "sortable": True,
    },
    {
        "field": "subject",
        "title": "Sub",
        "sortable": True,
    },
    {
        "field": "catalogNumber",
        "title": "Code",
        "sortable": True,
    },
    {
        "field": "status",
        "title": "Status",
        "sortable": True,
    },
    {
        "field": "primaryInstructor.displayName",
        "title": "Instructor",
        "sortable": True,
    },
    {
        "field": "capacity",
        "title": "Cap",
        "formatter": "capFormatter",
    },
]


def sendAlert():
    pass


@app.route("/")
def main():
    url = "https://ais.kube.ohio.edu/api/course-offerings/search/query?selectedTab=ATHN&page=1&pageSize=50"
    body = {
        # "terms": ["2231::FALL", "2235::SPRING"],
        "terms": ["2231::FALL"],
        "campuses": ["ATHN"],
        "subjects": ["CS", "EE"],
        "catalogNumber": "",
        "name": "",
        "topic": "",
        "level": "GRAD",
        "status": ["OPEN", "WAITLIST", "FULL", "MAJORS", "PERMISSION"],
        "generalEducationTier1": [],
        "generalEducationTier2": [],
        "generalEducationTier3": [],
        "bricks": [],
        "isSync": True,
        "isAsync": True,
        "instructors": [],
        "description": "",
        "offeredInPerson": True,
        "offeredOnline": True,
        "days": [],
        "eligibleGrades": "",
        "building": [],
    }

    # while True:
    #     time.sleep(10 * 1000)
    response = requests.post(
        url,
        headers={
            "accept": "application/json, text/plain, */*",
            "accept-language": "en-US,en;q=0.9",
            "content-type": "application/json",
            "sec-ch-ua": '"Chromium";v="104", " Not A;Brand";v="99", "Google Chrome";v="104"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "Referer": "https://webapps.ohio.edu/",
            "Referrer-Policy": "strict-origin-when-cross-origin",
        },
        json=body,
    )

    now = datetime.now()
    # data = response.read()
    # dict = json.loads(response.json)

    result = response.json()["results"]

    data = []
    for c in result:
        app.logger.info(str(filterFrom[c["subject"]]))
        app.logger.info([c["catalogNumber"]])

        if c["catalogNumber"] in filterFrom[c["subject"]]:
            app.logger.info("trueee", c["catalogNumber"])
            data.append(c)

    app.logger.info(len(data))

    return render_template(
        "home.html",
        data=data,
        columns=columns,
        time=now,
    )
