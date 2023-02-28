# Disaster recovery PoC

Use a number of views counter flask app and then when a disaster occurs don't lose the number of views when recovering - good case study

<!-- TODO: Create a terra for a non-critical app -->
<!-- TODO: Look into terra reservation affinity -->
<!-- TODO: Look at creating vm from snapshot not image - clarify this with the team (where is the state stored? On the hard drive bundled with the whole OS or is it a seperate bucket for the state?) -->
<!-- TODO: Create mechanism/python script to remove non-critical workload (look at tag) with the same machine type from one region and replace it with the workload critical workload of another region  -->

<!-- Theres two things to look into here: what happens with the state? How to ensure that we can maintain a similar state e.g. similar view count without loosing too much? -> turboreplication every n hours? Other question is the automation of moving critical from one region, and replacing non-critical in the other region -->

Don't need to have a database of machine types for critical and non-critical workloads as the data is all in the terraform in any case