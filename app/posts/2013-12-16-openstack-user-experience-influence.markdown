---
layout: post
title:  "The OpenStack Years: Which groups in OpenStack do User Experience designers influence today?"
date:   2013-12-16
categories: [openstack]
---

> <em>This was originally written and shared on December 16, 2013 when I was working daily with the OpenStack Community.</em>

---

Before I jump into blog posts about OpenStack user experience requirements, designs, and user testing, I wanted to start with some level setting and explain some of the groups that have been a focus in the user experience space.

#### User Experience
To start, let me give a quick introduction to the way user experience design currently works within OpenStack. How do we as user experience professionals work within the OpenStack community? Today, we work very closely with the Horizon and TripleO/Tuskar teams. We attend the weekly IRC meetings, participate in feature requirement discussions, register blueprints, report bugs, design wireframes for new features, and test existing features with users.

User experience isn't an official program in OpenStack, but a few of us have started to form a team around the efforts in the UX space. We now have an [Ask OpenStack UX](http://ask-openstackux.rhcloud.com/questions/) site where we house design discussions. Weekly, we send out an update to the mailing list on the [current topics](http://lists.openstack.org/pipermail/openstack-dev/2013-December/020935.html\) that are being discussed. As a group we are continuously improving our processes. We are discussing the option of moving to and using the [StoryBoard](https://github.com/openstack-infra/storyboard\) tool that Thierry Carrez proposed at the Hong Kong summit.

How could you contribute to the user experience effort in OpenStack? Join us in discussions on Ask OpenStack UX, share your wireframes, give your feedback as an OpenStack user, or simply give your thoughts on how we could improve our way of working. You can find us in #openstack-ux on Freenode if you'd like to chat.

#### Horizon
As I mentioned in [my first blog post](https://lizsurette.github.io/openstack/2013/12/12/openstack-an-introduction.html), Horizon is where I jumped into the OpenStack world. This is the only user interface that is currently shipped with the core OpenStack product and it seems obvious to me that others will have the same experience. The Horizon Dashboard gives the user a visual way to perform basic OpenStack tasks like spinning up an Instance and assigning that instance a floating IP. Of course, the user can do these things from the command line interface (CLI), but the UI is where most of the user experience work that has been done so far has been focused.

The Horizon development team is a great bunch to work with and are extremely supportive of making sure this component has great user experience design. Currently, Horizon only supports the other core components, but developers are welcomed to add plugins to Horizon for components they are working on outside of the core.

There are a few options that I know about for quickly getting access to a running version of Horizon if you'd like to poke around and test things out.
1. http://trystack.org/ - You can get a free account by joining their Facebook group. Once you've been added to the group, simply use your Facebook credentials for authentication and you'll be able to view the Horizon UI.
2. http://www.stacklab.org/ - This is another quick way to get access to Horizon to poke around.
3. If you are feeling brave and would like to get your own environment up and running -- Spin up a RHEL-based Linux distro in a VM and run through the [Quick Start guide](http://openstack.redhat.com/Quickstart).
4. Another way to get a development environment up and running would be to use http://devstack.org/

If you are interested in jumping into the development or review side of Horizon, feel free to come to one of our [weekly meetings on IRC](https://wiki.openstack.org/wiki/Meetings#Horizon_team_meeting) to get a feel for what we are working on today. Also, getting started with Horizon can be done by following the [quick start instructions](http://docs.openstack.org/developer/horizon/quickstart.html).

#### TripleO
In my introductory [Why a blog? Who is the intended audience of this blog?](https://lizsurette.github.io/openstack/2013/12/12/openstack-an-introduction.html), I mentioned that I quickly realized that installation and deployment are big areas in which the usability of OpenStack could be improved. [TripleO](https://wiki.openstack.org/wiki/TripleO) and Tuskar work together to tackle just this.

> TripleO is a program aimed at installing, upgrading and operating OpenStack clouds using OpenStack's own cloud facilities as the foundations - building on nova, neutron and heat to automate fleet management at data center scale. (https://wiki.openstack.org/wiki/TripleO)

It's a bit of a mind bending concept, but I highly recommend watching Robert Collins' [talk from the Portland OpenStack Summit](https://www.youtube.com/watch?v=RjUvpfzejtU&ab_channel=OpenInfrastructureFoundation). Although TripleO continues to evolve with each release, I found this talk to be a great introduction.

#### Tuskar
We haven't worked on any user experience designs specifically for TripleO, but this is where [Tuskar](https://wiki.openstack.org/wiki/TripleO/Tuskar) comes into play.

> Tuskar gives administrators the ability to control how and where OpenStack services are deployed across the data center. Using Tuskar, administrators divide hardware into "resource classes" that allow predictable elastic scaling as cloud demands grow. This resource orchestration allows Tuskar users to ensure SLAs, improve performance, and maximize utilization across the data center. (https://wiki.openstack.org/wiki/TripleO/Tuskar)

Tuskar has recently combined efforts with the TripleO program and is bringing a user interface into the mix. Although there are [huge discussions](http://lists.openstack.org/pipermail/openstack-dev/2013-December/021388.html) currently taking place about the requirements for the Icehouse release of Tuskar working with TripleO, a demo of the initial concepts shown at the Hong Kong Summit can be seen [here](https://www.youtube.com/watch?v=VEY035-Lyzo).

Ultimately, TripleO and Tuskar will work together to provide a community solution for installing and deploying an OpenStack environment solving a huge need for the end users of OpenStack!

Thoughts?
