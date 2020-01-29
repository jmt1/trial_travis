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



def check_aprovals(code_approvals, rest_approvals):

    # https://developer.github.com/v3/pulls/reviews/#list-reviews-on-a-pull-request
    headers = {'Authorization': 'token %s' % github_token}
    reviews = requests.get("https://api.github.com/repos/" + github_repository + "/pulls/" + str(number) + "/reviews",
                        headers=headers).json()

    approvals = 0
    for label in labels:
        id =label["name"]
        if id == "Code":
            approvals_required=code_approvals
            break
        else:
            approvals_required=rest_approvals

    for review in reviews:
        rState=review["state"]
        if rState == "APPROVED":
            approvals=approvals+1

        print(str(approvals)+"/"+str(approvals_required)+" approvals")

    if approvals >= approvals_required:
        print("Approved")
        requests.post("https://api.github.com/repos/" + github_repository + "/statuses/" + str(number) + "",
                      json.dumps({
                          "state": "success",
                          "description": "You can merge",
                          "context": "Required_3_approvals_to_merge"
                      }), headers=headers)

    else:
        requests.post("https://api.github.com/repos/" + github_repository + "/statuses/" + str(number) + "",
                      json.dumps({
                          "state": "pending",
                          "description": "You need 3 approvals to merge",
                          "context": "Required_3_approvals_to_merge"
                      }), headers=headers)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Check approvals in pull request')

    parser.add_argument('--code_approvals', type=int,
                        help='Minimun of approvals required for label Code', required=True)
    parser.add_argument('--rest_approvals', type=int,
                        help='Minimun of approvals required for rest of labels', required=True)

    args = parser.parse_args()
    check_aprovals(args.code_approvals, args.rest_approvals)



