---
layout: post
title:  "Running an Example Node.js Kubernetes Application with the Developer Sandbox for Red Hat OpenShift"
date:   2021-04-01
categories: [open hybrid cloud, kubernetes, openshift, nodejs]
---
I'm a Product Designer at Red Hat. Every day I must consider "How can we improve the experience for our users?". Let me share my experience with the [new Developer Sandbox for Red Hat OpenShift](https://developers.redhat.com/developer-sandbox). In my opinion it's an excellent step towards improving our Developer's Experience of using OpenShift.

You might be wondering "who is this Developer persona?" that we are serving with this Sandbox environment. A lot of the features of the OpenShift Developer Console target a DevOps Engineer. This person may be exploring what it would mean for their team to transition to a containerized deployment. It could be argued that an IT Decision Maker like an IT Manager or Director, an Architect, or a trailblazing Application Developer are personas that are also targeted with this Sandbox.

Let's walk through the process of launching your Developer Sandbox for Red Hat OpenShift. Then I'll take you through the process of deploying an example Node.js application.<br><br>

#### First: Request your Developer Sandbox for Red Hat OpenShift.
What does it mean to have a Developer Sandbox? You'll get Developer access to an OpenShift cluster at zero charge for 30 days.  If you'd like to follow along, you can [request a Sandbox of your own](https://developers.redhat.com/developer-sandbox).
![Developer Sandbox](https://github.com/lizsurette/lizsurette.github.io/raw/main/static/img/_posts/developer-sandbox.png)

In order to launch a Sandbox, you will need to create a Red Hat account or if you already have one, log in to your existing account. Once you have requested a Sandbox, logging in is a breeze since you make use of your Red Hat account. Make sure you select to log in as the "DevSandbox" user. The "OpenShift_SRE" user is the login that the team ensuring your cluster remains running and functional uses to administer things :)<br><br>

#### Second: Enjoy a guided tour of the Developer Console.
Now that you are logged in, you can walk through a quick guided tour of the Developer perspective of the Console. (Of course if you wish, you can skip this!) In this tour you will get a better grounding around where you might go for Monitoring, how to Search for resources, and how to get Help if you need further assistance. You'll also learn about the Perspective switcher that will allow you to switch from the Developer perspective to the Administrator perspective. While you do have access to this Administrator area of the console, you won't be able to see and manage EVERYTHING a user with Admin privileges would be able to.
![Developer Perspective Welcome](https://github.com/lizsurette/lizsurette.github.io/raw/main/static/img/_posts/welcome-dev-perspective.png)
<img src="https://github.com/lizsurette/lizsurette.github.io/raw/main/static/img/_posts/guided-tour.png" alt="Guided Tour" width="500"/><br><br>

#### Third: Get a sample application up and running.
Now let's get an application running. I recommend starting with creating a sample application to get a feel for what you can do ultimately with your own application. Within the "Topology" section, there is a card that lists out a few "Quick Starts". The first link allows you to work through a tutorial on creating a sample application. Click that link to find that a side panel slides out with a few steps to follow.
![Select Quickstart](https://github.com/lizsurette/lizsurette.github.io/raw/main/static/img/_posts/select-quickstart.png)
<br><br>

Following the instructions in the quick start, you'll notice a number of choice you'd be able to make if you wanted to get started using a code sample. In this case we will follow the quick start's lead and select Node.js.
![Select Node.js](https://github.com/lizsurette/lizsurette.github.io/raw/main/static/img/_posts/select-nodejs.png)
<br><br>

Since we are making use of the sample, we can go ahead and accept the defaults that have been filled in on the form. This is where if you are deploying your own Node.js application you could point to your own Git Repo.
![Create Application](https://github.com/lizsurette/lizsurette.github.io/raw/main/static/img/_posts/create-application.png)
<br><br>

It's as simple as that! The application will take just a few seconds to spin up and the donut chart around the Node.js logo will turn from a light blue to a darker blue signifying there is a pod running.
![Application Created](https://github.com/lizsurette/lizsurette.github.io/raw/main/static/img/_posts/application-created.png)
<br><br><br>

#### Fourth: Dig in a bit deeper to get to know the details of your application.
If you are following the quick start, you can continue on to get an understanding of a few extra pieces around your application running. There are a few icons surrounding the Node.js logo that we should explore.

In the bottom left, there is an icon that represents the build status. Hovering over it will give you a quick textual status and clicking it will drill into the log for the build that has run. Typically, you'd really only need to navigate in this far if something seems like it's gone wrong with the build.<br>
<img src="https://github.com/lizsurette/lizsurette.github.io/raw/main/static/img/_posts/build-status.png" alt="Build Status" width="250"/>
<br><br>
![Build Logs](/static/img/_posts/build-logs.png)
<br><br>

In the bottom right, there is an icon that represents the source code location. Hovering over it will give you a quick textual hint that you can access the code and clicking it will drill into the source code for editing. In the case of this sample running on the OpenShift Developer Sandbox, it opens up [Red Hat CodeReady Workspaces](https://developers.redhat.com/products/codeready-workspaces/overview) which is an OpenShift-native developer workspace server and IDE.<br>
<img src="https://github.com/lizsurette/lizsurette.github.io/raw/main/static/img/_posts/source-code.png" alt="Source Code" width="250"/>
<br><br>
![CodeReady Workspaces](/static/img/_posts/crw.png)
<br><br>

Finally, in the top right, there is an icon that represents the URL to your running application. Hovering over it will guide you towards opening the URL and clicking it will open the application in a new tab. In this case we get to see the sample application output running which gives even more guidance around developing with OpenShift.<br>
<img src="https://github.com/lizsurette/lizsurette.github.io/raw/main/static/img/_posts/open-url.png" alt="Open URL" width="250"/>
<br><br>
![Application](/static/img/_posts/application.png)
<br><br><br>

That's it for the quick tour of creating an example application making use of the OpenShift Developer Sandbox. If you fall into the category of any type of Developer, I'd encourage you to give it a shot and I'd love to hear any feedback you have. Feel free to [send me an email](https://lizsurette.github.io/about/)! It's always great to hear how we might be able to make improvements on user experience.
