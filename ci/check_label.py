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

labels=json.loads(task("jq --raw-output .pull_request.labels "+github_event_path, pr=False)[0])
print("labels: "+str(labels))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Check approvals in pull request')

    parser.add_argument('--label', type=str,
                        help='Label to check in pull requests', required=True)

    args = parser.parse_args()

    for label in labels:
        if label["name"] == args.label:
            exit(0)

    exit(-1)