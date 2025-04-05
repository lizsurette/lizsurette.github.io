---
layout: post
title:  "The OpenStack Years: Streamlining the Install of OpenStack with the RDO Manager UI"
date:   2015-06-10
categories: [openstack]
---

> <em>This was originally written and shared on June 10, 2015 when I was working with the OpenStack Community.</em>

> <em>This post was [featured on GreenStack](http://greenstack.die.upm.es/2015/06/10/streamlining-the-install-of-openstack-with-the-rdo-manager-ui/).</em>

***

Before being able to use everything that OpenStack has to offer, you need to be able to install it. The installation step of OpenStack has been a heavily talked about topic over the last few years. Whether you are a developer or tester trying to get your environment up and running or an end user trying to use OpenStack to spin up VMs, you've most likely put a fair amount of time into the install and configuration step. Since it's the first thing every user experiences with OpenStack we really need to make it as effortless as possible. OpenStack is an interesting beast because there are so many pieces to the project (some being optional) which make configuration very tricky. We've set out to reduce the frustration from a user's point of view as we designed [RDO Manager](https://www.rdoproject.org/RDO-Manager).

Since OpenStack is so complex, it's difficult to design an installation and configuration UI that steps the user through every single setting. One of the main goals we had in designing the RDO Manager UI is to surface the common configuration parameters to the user and tuck away the rest. This way, the novice user could install and configure their cloud without having to dig. The advanced user could dig a little deeper and get into additional settings that they might want to control. Designing the UI this way requires talking with as many people as possible who will use this application to install OpenStack so that we are sure we surface the most important configuration options. We are still learning more as new people use RDO Manager and give us feedback. The following is a walkthrough of the current design of the Overview page of the RDO Manager UI.

For all users, when they log into the RDO Manager UI they will first see the Overview page. From this view, the user should be able to do everything they need to for a simple OpenStack install. On the right, they will see a checklist to follow as they complete the necessary steps to plan their cloud deployment. Once they have fulfilled each step, they will be ready to deploy their cloud.
![Checklist](https://github.com/lizsurette/lizsurette.github.io/raw/main/static/img/_posts/checklist.png)

The first thing a user will do to begin the planning process is register nodes. This is the hardware that will run the cloud. Clicking on "Register Nodes" will bring up a modal dialog for the user to either register nodes manually, or upload a set of nodes from a file such as a CSV.
![Register Nodes](https://github.com/lizsurette/lizsurette.github.io/raw/main/static/img/_posts/register-nodes.png)

We've designed this modal to allow for registering multiple nodes at once so that the user doesn't have to continue to come back into this modal for each additional node they'd like to register. Uploading a CSV file will populate the nodes from that file in a list on the left of the modal. The user can edit any parameters they wish before clicking "Register Nodes".
![Register Nodes Modal](https://github.com/lizsurette/lizsurette.github.io/raw/main/static/img/_posts/register-nodes-modal.png)

As nodes are registered, they will drop into groups (or Node Profiles) based on the their hardware specifications. This will make it easier to identify which nodes should be assigned to perform Compute, Controller, or Storage functions.

Once the nodes have been registered, the user will want to define their network configuration. In the first version of RDO Manager, there will be templates provided to create the networks, generate IP addresses for each node, and configure the services to run on the appropriate networks. Users will be able to edit this configuration file within a modal in the UI.

Before assigning deployment roles to nodes, the user may need to provide configuration details for some of the roles. This configuration includes things such as the provisioning image and service configuration for each role.
![Edit Role](https://github.com/lizsurette/lizsurette.github.io/raw/main/static/img/_posts/edit-role.png)

Editing the service configuration will apply these parameters to the underlying services running on a node with this deployment role. This is where the most work has been needed to be sure we surface the most important configuration and hide away the advanced parameters so that we can keep it as simple as possible for the user.
![Edit Role Modal](https://github.com/lizsurette/lizsurette.github.io/raw/main/static/img/_posts/edit-role-modal.png)

Assigning deployment roles to nodes is the last step in the checklist before the user can Verify and Deploy their environment. Users can either drag and drop roles onto node profiles or they can click the "+" to assign a role to a number of nodes. After assigning a role, the user can choose how many nodes they would like from the node profile to take on that deployment role.
![Assign Roles](https://github.com/lizsurette/lizsurette.github.io/raw/main/static/img/_posts/assign-roles.png)

Once the user has met all of the requirements in the checklist, they can click the Verify and Deploy button to kick off the deployment of their cloud.
![Verify and Deploy](https://github.com/lizsurette/lizsurette.github.io/raw/main/static/img/_posts/verify-and-deploy.png)

What do you think about this design so far? Feel free to leave your thoughts in a comment below :) In a following post, I will cover the initial design thinking around monitoring the environment during and after deployment.

Will you be at [Red Hat Summit](http://www.redhat.com/summit/) this year and want to try RDO Manager out? Come to the RDO Booth in the Community Central area and I will have a system running for you to poke at and give comments on. I'd love to get your feedback in person!

Thanks!
Liz
