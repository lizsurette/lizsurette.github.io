---
layout: post
title:  "Findings from Reviewing the oVirt Overall Dashboard Concept at Red Hat Summit"
date:   2015-08-05
categories: [virtualization]
---

> <em>This was originally written and shared on August 5, 2015 when I was working with the oVirt Community.</em>

---

At [Red Hat Summit](http://www.redhat.com/summit/) this past year, we presented a few concepts that we hope to include as features in oVirt.NEXT. One of those concepts was a design for an overall dashboard. This dashboard would aggregate all of the data from within an environment (all data centers) and present the user with visualizations of this information. The following is the initial design concept for the overall dashboard that we showed:
![Overall Dashboard](https://github.com/lizsurette/lizsurette.github.io/raw/main/static/img/_posts/overall-dashboard.png)

We talked to about a dozen people at Summit as they visited our locations in Customer Central as well as Community Central and asked them to give their initial reactions to the design. The questions that we focused on were:
1. What do you like with this design?
2. What could be improved with this design?
3. Is there anything missing in this design?
4. Is there anything that could be taken away to simplify this design?

A list of the top findings that we came away with are:
1. This dashboard needs to be broken down to focus on each Data Center to be really useful. An example that I talked to one user about is how currently we show that there is 300GB of free storage. If the user wants to create a storage domain and allocate 150GB to it they need to know which Data Center to create that Storage Domain in. If Data Center 1 has 200GB free and Data Center 2 has 100GB free, there is currently no way to know that the user should create this Storage Domain in Data Center 1. If they try to create it in Data Center 2 they will be unsuccessful.
2. The "Most Utilized" lists will be EXTREMELY useful. They are a must-keep.
3. Perhaps the data that makes up the Health statistics could be filtered for just within last day. This way the user could see these and know that if a change occurs it is something they should take a look at right away.
4. The differences between the Storage in Utilization and the Storage Capacity area could be explained better. More research and design is needed to work these details out to make it clear to the user.
5. Users really liked seeing trends. The radial graphs with trends for history will be very helpful while monitoring oVirt environments.

Based on this feedback that we got from our users, we have a clear path on the updates that we’d like to make to this design. Stay tuned for the next version! If you have any feedback of your own, please feel free to leave a comment below.

Thanks,
Liz
