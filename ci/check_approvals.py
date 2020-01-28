import os
import argparse
import subprocess
import json
import requests

def task(cmd,cwd = None, pr = True):
    p = ""
    task = subprocess.Popen(cmd, cwd=cwd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    for line in iter(task.stdout.readline, b''):
        line_d = line.decode("latin-1",  errors="ignore")
        if pr == True:
            print(line_d.replace("\r\n", ""))
        p = p + str(line_d)
    task.stdout.close()
    task.wait()

    return p, task.returncode

github_token=os.environ["GITHUB_TOKEN"]
github_repository=os.environ["GITHUB_REPOSITORY"]
github_event_path=os.environ["GITHUB_EVENT_PATH"]

URI="https://api.github.com"
API_HEADER="Accept: application/vnd.github.v3+json"
AUTH_HEADER="Authorization: token "+github_token

action=task("jq --raw-output .action "+github_event_path, pr=False)[0]
state=task("jq --raw-output .review.state "+github_event_path, pr=False)[0]
number=task("jq --raw-output .pull_request.number "+github_event_path, pr=False)[0]
labels=json.loads(task("jq --raw-output .pull_request.labels "+github_event_path, pr=False)[0])
print("number: "+str(number))
print("labels: "+str(labels))



def check_aprovals(approvals_required):

    # https://developer.github.com/v3/pulls/reviews/#list-reviews-on-a-pull-request
    headers = {'Authorization': 'token %s' % github_token}
    reviews = requests.get("https://api.github.com/repos/" + github_repository + "/pulls/" + str(number) + "/reviews",
                        headers=headers).json()

    approvals = 0

    for review in reviews:
        rState=review["state"]
        if rState == "APPROVED":
            approvals=approvals+1

        print(str(approvals)+"/"+str(approvals_required)+" approvals")

    if approvals >= approvals_required:
        print("Approved")
    else:
        exit(-1)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Check approvals in pull request')

    parser.add_argument('--min_approvals', type=int,
                        help='Minimun of approvals required', required=True)

    args = parser.parse_args()
    for label in labels:
        id =label["name"]
        if id == "Code":
            check_aprovals(args.min_approvals)



