import requests

from flask import Flask, render_template, request, redirect

app = Flask(__name__)

url = "https://jobs.github.com/positions.json?description=python&location=new+york"

req = requests.get(url)
json_form = req.json()


class Job:
    def __init__(self, job_id, job_type, job_url, created_at, company, company_url, location, title, description, how_to_apply,
                 company_logo):
        self.id = job_id
        self.type = job_type
        self.url = job_url
        self.created_at = created_at
        self.company = company
        self.company_url = company_url
        self.location = location
        self.title = title
        self.description = description
        self.how_to_apply = how_to_apply
        self.company_logo = company_logo


def create_data_list(json_list):
    """
    create a list of Job classes
    :param json_list:
    :return: list of Jobs
    """
    job_list = []
    if json_list:
        for line in json_list:
            job = Job(line["id"], line["type"], line["url"], line["created_at"], line["company"],
                      line["company_url"], line["location"],
                      line["title"], line["description"], None, line["company_logo"])
            job_list.append(job)
    return job_list


def create_data(line):
    if line:
        return Job(line["id"], line["type"], line["url"], line["created_at"], line["company"],
                      line["company_url"], line["location"],
                      line["title"], line["description"], line["how_to_apply"], line["company_logo"])


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        search = request.form["search"]
        url = "https://jobs.github.com/positions.json?description=" + search
        req = requests.get(url)
        json = req.json()
        data = create_data_list(json)
    else:
        data = ''

    context = {
        'data': data,
        'num_results': len(data),
    }

    return render_template('index.html', context=context)


@app.route('/details/<string:id>')
def details(id):
    url = "https://jobs.github.com/positions/"+id+".json"
    req = requests.get(url)
    json = req.json()
    data = create_data(json)
    return render_template('details.html', data=data)