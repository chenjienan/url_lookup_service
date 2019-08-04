# Microservices with Docker, Flask

[![Build Status](https://travis-ci.org/chenjienan/testdriven-app.svg?branch=master)](https://travis-ci.org/chenjienan/url_lookup_service)

# URL lookup service
-------------------------------

We have an HTTP proxy that is scanning traffic looking for malware URL's. Before allowing HTTP connections to be made, this proxy asks a service that maintains several databases of malware URL's if the resource being requested is known to contain malware.

Write a small web service, in the language/framework your choice, that responds to GET requests where the caller passes in a URL and the service responds with some information about that URL. The GET requests look like this:

       GET /urlinfo/1/{hostname_and_port}/{original_path_and_query_string}

The caller wants to know if it is safe to access that URL or not. As the implementer you get to choose the response format and structure. These lookups are blocking users from accessing the URL until the caller receives a response from your service.

### Your finished product should include:

* Necessary documentation for us to set up the service ourselves on EC2/Vagrant/Docker or similar system of your choosing. Please do not utilize services such as AppEngine or Heroku. Bonus if you do this using Ansible/Salt/Chef or other configuration management.
* Documentation on your solution’s result format/structure
* Ability to handle an expected load of thousands of requests per second
* Unit tests. Integration tests would be great as well, but not required.

### Give some thought to the following:

* The size of the URL list could grow infinitely, how might you scale this beyond the memory capacity of this VM?
* The number of requests may exceed the capacity of this VM, how might you solve that?
* What are some strategies you might use to update the service with new URLs? Updates may be as much as 5 thousand URLs a day with updates arriving every 10 minutes. These updates will include insertions and deletions.
* How would you design the system to tolerate component failure such that you can achieve 100% uptime.
