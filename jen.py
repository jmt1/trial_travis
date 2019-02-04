"""
This example shows how to create job from XML file and how to delete job
"""
from __future__ import print_function
from pkg_resources import resource_string
from jenkinsapi.jenkins import Jenkins

jenkins = Jenkins('http://jenkins.embention.net:1136/')
print(jenkins.version)