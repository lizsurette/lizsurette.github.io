---
layout: post
title:  "The OpenStack Years: Running a Baseline Usability Test on Horizon"
date:   2014-03-25
categories: [openstack]
---

> <em>This was originally written and shared on March 25, 2014 when I was working daily with the OpenStack Community.</em>

---

Over the last few months, I’ve been working with a group of folks from multiple companies on doing research around [building a set of Personas](https://wiki.openstack.org/wiki/Personas#The_OpenStack_Personas_Working_Group) to present at the Atlanta Summit. In one of our first meetings, we talked about the need to do some [usability testing](http://en.wikipedia.org/wiki/Usability_testing) as a separate effort from the Persona research. Earlier this month, a few of the folks from HP mentioned that they were hoping to run a usability test on the most recent (Icehouse) version of Horizon. This would be the first usability test within the community that I’m aware of and I was super excited that they were willing to let those of us interested to be a part of this testing effort.

The decision was made to focus this first round of testing on self-service end users of Horizon and write tasks for our participants to perform based on typical tasks these types of users often perform. NOTE: We would like to do more and more usability testing and continue to include other types of users and tasks.

We started out by putting together a [screener](https://www.surveymonkey.com/s/R8QZ2RB) to be sure that we got the correct people to test. Here's a quick look at the questions that we asked:
> 1. What company do your work for?
2. How many people work for your organization worldwide? Please take into account all branches and locations.
3. What is the primary business or industry of your company?
4. What is your job title?
5. What is your primary job role?
6. How many years have you performed system administration and/or network management/administration?
7. Do your PRIMARY job responsibilities include any of the following?
8. Do you manage or use cloud services?
9. Please select the cloud service providers and technologies that you have good working knowledge of.
10. Which of the following administration tasks do you perform at least once a month?
11. In your daily software use as an IT professional, what percent of your time do you use?
12. Does your IT department currently offer cloud computing services at you company?
13. How many virtual servers are there in your server environment?
14. Who owns the servers in your company?
15. Please provide your email so we can potentially contact you for a study.
16. Please provide your first and last name.
17. Would you like us to consider you for other OpenStack community studies?

This is one of the most important pieces to doing a usability test. It’s really important to be sure to test the users on tasks that they would actually perform in their daily work so that you get the best results possible. We kept the screener nice and short so that folks didn’t feel overwhelmed and could respond to the survey in just a few minutes. We actually ended up getting a really great response from the community mailing lists and LinkedIn on the screener. It was very encouraging as responses of people interested in participating in the testing started to flow in.

As we sifted through the screener results, we took some time to write up the scenarios and tasks that each participant would go through. We made sure to list these in priority order since depending on time, we might not be able to get to each task with all of our users. Here’s a list of what the users would be doing during the testing:

> __Scenario 1: Launching an instance__
- Individual Tasks:
  - Create a security key pair.
  - Create a network.
  - Boot from cirros image.
  - Confirm that instance was launched successfully.

> __Scenario 2: Understand how many vCPUs are currently in use vs. how much quota is left.__
- Individual Tasks:
  - Check out Overview Page to review current quota use/limit details.

> __Scenario 3: Take a snapshot of an Instance to save for later use.__
- Individual Tasks:
  - Either Launch an instance successfully, or identify a running instance in the instance view.
  - Choose to take a snapshot of that instance.
  - Confirm that the snapshot was successful.

> __Scenario 4: Launch an instance from a snapshot.__
- Individual Tasks:
  - Choose to either create an instance and boot from a snapshot, or identify a snapshot to create an instance from.
  - Confirm that the instance was started successfully.

> __Scenario 5: Launch an instance that boots from a specific volume.__
- Individual Tasks:
  - Create a volume.
  - Launch an instance using Volume X as a boot source.

At this point, we were pretty much ready to run the tests. HP had a system running the latest and greatest version of Horizon that our users could access, it was just a matter of scheduling some time with a few of the people who responded to the screener. Scheduling can sometimes take a fair amount of time, but these users were extremely quick to respond. I wondered if that’s just the way it is with testing passionate open source software users.

We didn’t record the testing, since we wanted to be sure that the identity of the participants was protected, but we did take a ton of notes during each of the tests to be sure we captured everything that went on both good and bad. Since there were a few of us who wanted to observe the testing and one person running the test, we used online meeting software in order to share the screen and audio during the test. We had a few hiccups with audio quality and definitely have areas that we could improve on for the next round of testing, but for a first test we got some awesome results.

Throughout the testing, we found that the majority of the hour that we had with participants was taken up by the first task. This isn’t necessarily a bad thing, especially for a first time test within the community. There were a lot of findings that came out of “Launching your first Instance" since it is fairly broad and hit a lot of pieces of the UI. We did get to go through a few of the other scenarios with a few users as well for additional findings, but here's where we ended up with the list of improvements that we can make:

> __High Priority__
* Improve error messages and error message catalog.
* Fix Launch Instance workflow for end user and power user.
* Improve informational help information about form fields.
* Fix terminology. (e.g. launch instance, boot, shutoff, shutdown, etc.)
* Show details for key pair and network in Launch Instance workflow.
* Recommend a new Information Architecture.

> __Medium Priority__
* Create UI guidelines (of best practices) for Developers to use.
* Improve Online Help.
* Provide clearer indication the application is working after clicking a button and the application doesn’t respond immediately.
* Ensure consistency of network selection. (Drag and drop of networks very inconsistent from the other pieces of the launch instance modal)
* Create consistency of visualizations and section of action button recommendations on Instance table.
* Suggest defaults for the forms entry fields.
* Provide Image information details during image selection.

> __Low Priority__
* Allow users to edit the network an instance after launching instance.
* Resolve confusion around the split inline actions button.
* Explain what the Instance Boot Source field in Create Instance modal.
* Provide description/high level information about flavors for flavor selection.
* Make sorting clearer visually.
* Provide solution for subnet checkbox to improve usability.

> __Nice to Have__
* Provide "Save as Draft" option in the wizard.
* Change security group default name to "Default security group".

Now that we’ve gathered a lot of great data, we will be focusing on how to make improvements to Horizon based initially on the high priority findings. This includes logging bugs and registering blueprints within Launchpad (both in the [Horizon](https://launchpad.net/horizon) and [User Experience](https://launchpad.net/openstack-ux) spaces). The current plan is to come up with some proposal designs and have a [design session](http://summit.openstack.org/cfp/details/32) at the Atlanta Summit to create a plan for next steps on making sure Juno releases with features and improved functionality in Horizon that is important to our OpenStack users.
