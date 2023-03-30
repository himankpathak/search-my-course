from flask import Flask, render_template
from datetime import datetime
from zoneinfo import ZoneInfo

import requests, os

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

app = Flask(__name__)

filterFrom = {
    "CS": {
        "5060",
        # "6040", #AA
        "6020",
        "6980",
        "5120",
        "5160",
        "5180",
        "5440",
        "5620",
        # "5750", # IE
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
        # "6890", # DL
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


def getCurrDate():
    now = datetime.now()
    now = now.replace(tzinfo=ZoneInfo("America/New_York"))
    return now


def sendAlert():
    now = getCurrDate()

    message = Mail(
        from_email="a@example.com",
        to_emails=["b@example.com", "c@example.com"],
        subject="!!IMPORTANT!! Course Registration Open!",
        html_content="<strong>Hello, Course registration is open.</strong><br/>Open at:"
        + now.strftime("%m/%d/%Y, %H:%M:%S")
        + "<br/>Link: https://x-y-z.vercel.app/",
    )

    try:
        sg = SendGridAPIClient(os.environ.get("SENDGRID_API_KEY"))
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e)


# "2227::SUMMERFULL", "2227::SUMMER1", "2227::SUMMER2", "2221::FALL", "2225::SPRING"


@app.route("/")
def main():
    return searchCourse(["2241::FALL"])


@app.route("/all")
def all():
    return searchCourse(["2241::FALL"], 0, True)


@app.route("/alert")
def alert():
    return searchCourse(["2241::FALL"], 3)
    # return searchCourse(["2237::SUMMERFULL", "2237::SUMMER1", "2237::SUMMER2","2241::FALL"], True)


# Sends email when alert is more than 0 and
# no of course is greater than or equal to alert
def searchCourse(terms, alert=0, showAll=False):
    try:
        url = "https://ais.kube.ohio.edu/api/course-offerings/search/query?selectedTab=ATHN&page=1&pageSize=50"
        body = {
            # "terms": ["2231::FALL", "2235::SPRING"],
            "terms": terms,
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

        now = getCurrDate()

        # app.logger.info(response.json())
        result = response.json()["results"]

        data = []
        for c in result:
            if showAll or c["catalogNumber"] in filterFrom[c["subject"]]:
                data.append(c)

        if alert and len(data) >= alert:
            sendAlert()

        return render_template(
            "home.html",
            data=data,
            columns=columns,
            time=now,
            noAlert=not alert,
        )
    except Exception as e:
        app.logger.error(e)
        return str(e)
