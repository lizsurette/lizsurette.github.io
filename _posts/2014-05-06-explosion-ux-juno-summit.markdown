---
layout: post
title:  "The OpenStack Years: An explosion of User Experience discussions at the OpenStack Juno Summit"
date:   2014-05-06
categories: [openstack]
---

> <em>This was originally written and shared on May 6, 2014 when I was working daily with the OpenStack Community.</em>

---

Next week OpenStackers will be getting together in person for the Juno Summit in Atlanta to plan out what exactly we think is important to deliver in the Juno release of OpenStack. I’m extremely happy to say that there are a number of sessions that are focused on talking through use cases, users, and User Experience efforts within OpenStack. I wanted to take some time to introduce the sessions that I plan to participate in with respect to UX and I hope to see any of you who are interested join me!

__Sessions 1 & 2 - [User Experience Designers Gathering](http://junodesignsummit.sched.org/event/e13c8775849567fe8576c16875d5c547#.U2ewpuZdXC4)__ on the Cross-Project track
<em>Tuesday May 13, 2:50pm-4:20pm</em>

The last time I was at summit, it seemed like there were a lot of “Cross-project” topics that needed to be discussed in the design summit sessions. This year, the coordinators of these sessions made sure that there was a track set up for this type of discussion. Although they don’t specify one specific component of OpenStack, these talks are just as important as the core track sessions since they could actually contain one or more of the components. The User Experience group was lucky enough to get two of these session times back-to-back where we will have time to discuss moving ourselves forward as a group.

In this session we will try to get through as much as we can around the following topics:
1. Introduction of everyone in the session.
  - What role do you have today?
  - How does UX affect you?
  - How will you (if you plan to) contribute to OpenStack UX?
  - How active do you plan to be for the Juno development cycle?
2. Discussion of where are are currently in UX.
  - What components have we worked on so far?
  - What does our current process look like?
  - What tools do we use?
  - What has worked well?
  - What could be improved?
3. Discussion on where we want to go for Juno.
  - How should we improve our process and tooling during the Juno release? How do we track this and who will take certain action items?
  - What tools should we remove/add?
  - What are our goals for UX during the Juno release? (More research/requirements work? More designing? More user testing?...) Which components will we focus on? (Horizon? Tuskar? Heat? Ceilometer?….) Which features will we focus on?
4. UX as a program.
  - What does it mean to be a program?
  - Would UX make sense to be a program? If so, how should we work together to make this something we could propose as a team?

The design summit sessions are separate from the main conference sessions. They happen in parallel, so you might need to make some hard decisions as a designer, developer, or operator on which talks vs. design sessions you attend. The great news is that mostly all of the talks given in the main conference are recorded and shared on the [OpenStack Foundation youtube channel](https://www.youtube.com/user/OpenStackFoundation) a few weeks after summit. Also, all of the design summit session notes will be tracked in [respective etherpads](https://wiki.openstack.org/wiki/Summit/Juno/Etherpads). You can find the etherpad for this specific session [here](https://etherpad.openstack.org/p/juno-summit-cross-project-user-experience).

__Session 3 - [User Experience in the OpenStack Community](http://openstacksummitmay2014atlanta.sched.org/event/e19260fd989bb307e94b5a25558612f4#.U2eNceZdWG_)__ as part of the main conference <em>Wednesday May 14, 3:30pm-4:10pm</em>

This is the one talk during the main conference that I will be delivering with 3 other UX professionals. It was exciting to me that this was accepted in the main conference since it showed that there is interest from the attendees in where we’ve been with User Experience so far in OpenStack and where we plan to go.

In this talk we will be sharing our progress in the following areas:
- Understanding the OpenStack users
- Requirements gathering
- Interaction design
- Design support during development
- Usability testing and feeding results back into new requirements

We will also discuss the recent efforts, which build on Dave Neary’s previous work, to develop a set of personas to help the development community align with their users' needs and tasks. We'll review the methodology used to develop the personas, insights from the user interviews, and the personas created from the effort. Finally, we will provide recommendations and examples for how the community can effectively use the personas during their own planning, design, development, and testing efforts to improve the overall user experience.

__Session 4 - [Review Horizon Usability Test feedback, proposals](http://junodesignsummit.sched.org/event/db0c611f2dce2bf80df2287039c68d76#.U2ew2uZdWG8)__ on the Horizon track <em>Friday May 16, 9:00am-9:40am</em>

Back in March we conducted a set of baseline usability tests on the Horizon UI. My last blog post explained the process we took and reported out our findings. In this design session, we will quickly review these findings and then start discussing the design directions we’ve started to take on fixing these usability issues that were identified. The main proposals we will go through cover the following topics:
1. Fix Launch Instance workflow for end user and power user.
2. Improve error messages and error message catalog.
3. Improve informational help information about form fields.

A [discussion](http://lists.openstack.org/pipermail/openstack-dev/2014-April/033625.html) has been started on the development mailing list, so if you plan to attend this session, take a quick look at the history to familiarize yourself with the topics and designs we will be discussing.

__Session 5 - [Dashboard Accessibility / Improving Overview Pages in Horizon](http://junodesignsummit.sched.org/event/5114c75a9b7567d6bca752fcd0c28302#.U2ew3eZdWG8)__ on the Horizon track <em>Friday May 16, 9:50am - 10:30am</em>

There were so many great design summit proposals this time around, that our PTL suggested we try to combine a few so that each can have time during Summit for discussion. This session combines a talk around the current state and next steps of making sure the Horizon UI is accessible with an effort around improving the Overview pages in Horizon. Both topics encompass bringing a new level of maturity to the Horizon dashboard and focusing on needs of the end-user.

The Accessibility talk will go through a [wiki page](https://wiki.openstack.org/wiki/Horizon/WebAccessibility) of ideas around both improving accessibility as well as continuing to test for issues.

The Overview page discussion time will be used to present some design options for using data from Ceilometer that would be shown to End Users or Administrators depending on their role. A few early concepts have been created and can be seen in the [session schedule details](http://junodesignsummit.sched.org/event/5114c75a9b7567d6bca752fcd0c28302#.U2ew3eZdWG8).

__Session 6 - [Horizon Dev/Ops Session](http://junodesignsummit.sched.org/event/056d1eccc8485910e62bed8c65f7a8e5#.U2ew3-ZdWG8)__ on the Horizon track <em>Friday May 16, 10:50am-11:30am</em>

There has been feedback from operators who attended past summits that they didn’t feel welcome to attend any of the design summit sessions. The goal of these sessions is to allow for uninterrupted planning discussions for deciding what will be accomplished in the next release of OpenStack, but I know that the intention was not to shut operators out! Coordinators heard this feedback and are making sure that all operators feel welcome to come give their real-world feedback to developers as we work through planning the Juno release.

On top of this, Tom Fifield had the brilliant idea of setting aside some time for each track to have a specific discussion between operators and developers to be sure that developers understand the needs of their end-users. What are developers working on today that they need feedback on from operators? Where are there gaps in Horizon for operators today that developers need to put some focus on? I’m mostly looking forward to observing this discussion, but would love to make some contacts with operators for future usability testing and persona research efforts.

If you have any interest in User Experience in OpenStack, I highly recommend that you try to attend at least one of these sessions and get to know other designers and developers who are working in this space. Even if you are an end user or administrator of a cloud environment today and have some feedback for us, make sure you track us down!

Best,
Liz
