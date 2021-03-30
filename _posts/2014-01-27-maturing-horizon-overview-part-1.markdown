---
layout: post
title:  "Maturing the Horizon Overview Page Part 1 - Understanding the User and Gathering"
date:   2014-01-27
categories: [openstack]
---

> This was originally written and shared on January 27, 2014 when I was working daily with the OpenStack Community.

---

Let's take a quick look at the current (Havana) Horizon Overview page:
![Havana Horizon Overview!](/static/img/_posts/current-horizon-overview-page.png)

Upon login, non-administrator users are taken to the Project Overview page within [Horizon](http://docs.openstack.org/developer/horizon/). Here the user can see a basic set of information about the number of instances, VCPUs, RAM, Floating IPs, and Security Groups that are currently in use in their environment along with the quota that they are allowed. There is also a table that lets the user view the running instances along with a usage summary for the instances shown. The user has the opportunity to filter this table by date range when needed. While this information might cover certain use cases, my colleague [Ju Lim](https://plus.google.com/105626042354015503324/posts) and I wanted to take a step back from the current Overview page and think through the type of information that this user of Horizon would want to see when they first log in.

Now before I go on, this is when [Personas](http://en.wikipedia.org/wiki/Persona_(user_experience)) could have <em>REALLY</em>  helped us. Unfortunately, we hadn't gotten far enough along with our Persona work within OpenStack to use them, so we had to rely on what we knew from past projects we've worked on as well as the data we had from the set of users we had talked to about how they currently use OpenStack. In the coming months, I'll share the work that we are starting to do in the Persona space, but for now I'd like to note that we plan to revisit these requirements once we have some great Persona data so that we are sure that these completely meet end users needs.

After reviewing the current state of the Horizon Project Overview page, Ju and I started to brainstorm on how we might improve this page for end users. The goal of this effort was to take this page to the next level of maturity. The big questions that we needed to answer were:
1. Who is the main end user of this page?
2. What does this user want and need to see at an Overview level?

Without Personas, we started off by defining the main responsibilities and objectives of the Consumer, the end user of the Overview page:

> As a Consumer, I need to understand the usage of the resources I consume within each project. Due to this, I am concerned with getting a bird’s eye view to the resources within my project. I want to monitor usage data over time so that I can optimize the utilization of my resources.
>
> My responsibilities/objectives:
1. I'm interested in monitoring usage for the projects that I manage:
  - I want to be able to see usage vs. quota limit.
  - I'd like to be able to drill-down in order to view more details.
  - I need to be able to troubleshoot an alert to identify root cause.
  - I want to analyze usage levels and trends to see if the resource is running out of capacity
2. I'm responsible for managing resources within my project:
  - I can have access to one or more projects but currently have no ability to see an overview page with multiple projects.  I can only switch between projects.
  - I interact with project images (create, rename, delete).
  - I launch and terminate instances.
  - I attach and detach network interfaces.
  - I associate and unassociate Floating IP addresses.
  - I manage key pairs (as needed for object storage).

After gathering a better understanding of what the primary user looking at the Overview page wants to do, it was important for us to stay focused on the word Overview. As we talked about all of the information that we could <i>potentially</i> show, we kept a list. Of course, we needed to make sure we kept ourselves honest and took a look through the metrics that are [available in Ceilometer today](http://docs.openstack.org/developer/ceilometer/measurements.html). Here is the list of important metrics that we came up with:
> - Instances
- Public Images
- Private Images
- vCores
- vCPUs
- Memory usage
- Ephemeral storage capacity
- Duration of the ephemeral storage
- Object storage capacity
-  Objects
- Average object size
- Containers
- Key Pairs
- Block volume capacity
- Block volumes
- Snapshot capacity
- Snapshots
- Backup capacity
- Backups
- Floating IPs Mapped / Allocated
- Floating IPs Unmapped / Unallocated
- Load Balancers
- Security Groups
- Services’ Status -- globally and across region (and domain)
- Alerts

We took this rough list of metrics and started to discuss each one.
1. What specifically about each would the user be interested in seeing?
2. What would the units be?
3. Is this really a piece of information that's helpful to see at an overview level?
4. Would it make more sense for the user to drill in further for this information?
5. Is this a future concept?

We wanted to be sure that our current requirements are attainable. We also started to think about not only the metrics that a user would want to monitor, but what actions would a user want to be able to quickly perform from this view? After a few revisions, we ended up with a more detailed requirement list, organized by metric type:
> 1. Summary (Count) of resources
  - Instances and Images
    - Instances (used / running and available out my quota limit)
    - Images (aka instance snapshots)
    - Public Images
    - Private Images
    - vCores (used and available)
    - vCPUs (used and available)
    - Memory (used and available)
    - Quick Links: Launch a new instance, Launch a new stack
2. Storage
    - Ephemeral
      - Ephemeral capacity (used and available)
      - Duration of the ephemeral storage
    - Object
      - Object capacity (used and available)
      - Number of Objects
      - Average object size
      - Number of Containers
      - Number of Key Pairs
      - Quick Links: Create a container, Create a key pair
    - Block / Persistent
      - Block volume capacity (used / active and available)
      - Number of Block volumes (used and available)
      - Snapshot capacity (used and available)
      - Number of Snapshots
      - Backup capacity (used and available)
      - Number of Backups
      - Quick Links: Create a volume
3.  Network
  - Number of Floating IPs
  - Number of Mapped / Number of Allocated<
  - Number of Unmapped / Number of Unallocated<
  - Number of Load Balancers (currently available on experimental basis)
4. Security
  - Number of Security Groups
5. Health
  - Services’ Status -- globally and across region (and domain)
6. Alerts
  - Number of Alerts

There. A nice organized list of metrics that we want to design towards. Do you have any feedback on this list of requirements as it exists so far? I'm always looking to improve requirements and designs based on user feedback.

Also, keep an eye out for my next post in the "Maturing the Overview page in Horizon\" series where I walk through the design phase of this effort.

Best,
Liz
