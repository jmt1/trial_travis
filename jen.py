from __future__ import print_function

from jenkinsapi.jenkins import Jenkins

jenkins = Jenkins('http://jenkins.embention.net:1136/')

params = {}
job='exampletravis'

# This will start the job in non-blocking manner
jenkins.build_job(job)


# This will start the job and will return a QueueItem object which
# can be used to get build results
job = jenkins[job]
qi = job.invoke()

# Block this script until build is finished
if qi.is_queued() or qi.is_running():
    qi.block_until_complete()

build = qi.get_build()
print(build)