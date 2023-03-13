# Disaster recovery PoC

This Proof of Concept (PoC) repository demonstrates how VM reservations can be used in order to ensure capacity in the event of a disaster. Furthermore, in an effort to use reserved capacity in a more cost-effective way we attempt to demonstrate how idle reserved capacity can be utilized by non-critical workloads (e.g. dev/staging/pre-production environments) and then replaced with critical workloads as part of a Disaster Recovery Plan (DRP).

The `dummy-critical-app` is a Python Flask application which records the amount of page views in a `count.txt` file (gives a sense of persistent state). The Gunicorn server hosting the application is a daemon process registered with `systemd` to manage the process on startup. The whole configuration is recorded in the base `critical-app-python-debian` image.

The `dummy-non-critical-app` is a simple 'Hello world!' Flask application with an open SSH firewall policy for development.



<!-- Use a number of views counter flask app and then when a disaster occurs don't lose the number of views when recovering - good case study -->

<!-- TODO: Create mechanism/python script to remove non-critical workload (look at tag) with the same machine type from one region and replace it with the workload critical workload of another region  -->

<!-- Theres two things to look into here: what happens with the state? How to ensure that we can maintain a similar state e.g. similar view count without loosing too much? -> turboreplication every n hours? Other question is the automation of moving critical from one region, and replacing non-critical in the other region -->

Demo v1 path:
- Intro
    - Show critical application running in region
    - Show non-critical application running in region
    - Show 100% reservation utilization
- Disaster strikes
    - Take down non-critical application running in region designated for disaster recovery
    - Migrate the critical application to the disaster recovery region by enabling the tfvars
    - Show the critical application running
    - Show 100% reservation utilization


Next steps:
- How to identify critical workloads in a region and match them with non-critical workloads in another region (with reserved capacity)


Prevent people from creating VMs in a region when their is a disaster recovery status??

You could simply:
Turn off automatic reservation in the case of a disaster -> hardcode the reservation to take 

<!-- Rule in the centralized VM management system to prevent creation of VMs in the region where DR is occurring with reservation -->