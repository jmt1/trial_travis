from __future__ import print_function
import requests
from jenkinsapi.jenkins import Jenkins
import os
from jenkinsapi.utils.crumb_requester import CrumbRequester
host="https://jenkins.embention.net/"
jenkins = Jenkins(host, ssl_verify=False)#,   requester=CrumbRequester(baseurl=host))
commit = "f6a6f13f025d81baa098bfc03beb4eff64418232"#os.environ["TRAVIS_COMMIT"]
params = {'VERSION': '1.2.3', 'hola': commit}
job='exampletravis'

# This will start the job in non-blocking manner
#jenkins.build_job(job)


# This will start the job and will return a QueueItem object which
# can be used to get bu
# ild results
job = jenkins[job]
qi = job.invoke(build_params=params)

# Block this script until build is finished
if qi.is_queued() or qi.is_running():
    qi.block_until_complete()

build = qi.get_build()
data=int(str(build).split("#")[1])
last_failed = job.get_last_failed_buildnumber()
r = requests.get(job.url+"/"+str(data)+"/logText/progressiveHtml?start=0", verify=False)
if data==last_failed:
    print("Ha falladooo esta build: "+str(build))
    print(r.text)
    exit(1)
print("Todo Correcto")
print(build)
print(r.text)
