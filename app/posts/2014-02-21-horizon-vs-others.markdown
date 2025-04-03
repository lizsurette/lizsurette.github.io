---
layout: post
title:  "The OpenStack Years: How does Horizon Stack up versus other Cloud Computing UIs?"
date:   2014-02-21
categories: [openstack]
---

> <em>This was originally written and shared on February 21, 2014 when I was working daily with the OpenStack Community.</em>

---

One big part of designing a solution is understanding how the design compares to the other things out there that are similar. What has been done already? What are other users and designers doing in this space? In some cases, the design might be one of a kind, but in the case of Horizon, there are a fair amount of other players in the space. I took some time recently to look into some of the other UIs that exist. It gave me a good idea of how Horizon stacked up compared to these other UIs:
> 1. Netflix Asgard
2. Windows Azure
3. PayPal Aurora
4. CloudStack
5. Google Compute Engine
6. Amazon Web Services

This exercise gave me some great inspiration for improvements that could be made to Horizon. What are others doing out there to solve the needs that Horizon can’t solve for users? How can we improve Horizon to meet these needs? Here are some of the things that I noticed from a design perspective.

#### Netflix Asgard
If you’ve used OpenStack enough, you know that certain tables begin to grow to be extremely large. Currently, there is a filter function on the Instances table within Horizon, but it’s not quite as slick as the one that is available in Asgard. A simple, yet powerful search which gives instant feedback to the user will be crucial to be available on all of the tables that continue to grow as OpenStack users continue to gain more and more historical data. Here is a look at a section of a table with 564 items in it. The user does have the option to sort by any of the columns available in the table, but more powerfully, they can start typing in the filter text box to start weeding down the table items:
![Asgard Search 1](https://github.com/lizsurette/lizsurette.github.io/raw/main/static/img/_posts/asgard-search-1.png)

As the user starts typing, the table below is filtered automatically, and quickly:
![Asgard Search 2](https://github.com/lizsurette/lizsurette.github.io/raw/main/static/img/_posts/asgard-search-2.png)

#### Windows Azure
Azure is overall a very polished UI. One thing that stuck out to me as great inspiration is the simplicity of the wizards in this UI for creating items in your cloud. Although this slickness can be done in many different ways, the Azure designers chose to use vertical blades to show the number of steps and the progress that the user has made through the wizard.

Another very nice design decision that the Azure team made was to build responsive forms. As a user navigates through all of the fields for which they need to provide data, the forms are constantly checking for errors inline. The user will notice right away if a field that requires a unique name needs to be changed before they continue filling out the form. It’s a nice time saver for later on when they click the “Create” button and don’t have to go back to the form to figure out which errors may need to be fixed. Take a look at this design in action:
![Azure Wizard and Form](https://github.com/lizsurette/lizsurette.github.io/raw/main/static/img/_posts/azure-wizard-and-form.png)

#### PayPal Aurora
The PayPal designers have done a great job taking the information available via OpenStack and reworking the Information Architecture in their Aurora UI. Take a look at a snapshot of their current navigation structure:
![Aurora IA](https://github.com/lizsurette/lizsurette.github.io/raw/main/static/img/_posts/aurora-ia.png)

Not only have they grouped things logically in buckets that the user might be looking to act on, but they've included breadcrumbs above the working area on the left for users to be able to ground themselves on where they are at any time in the application. This is especially useful if the user has drilled down into a low level details page. Overall, I think this Information Architecture is a huge improvement over the one in Horizon.

#### CloudStack
I personally haven't had the chance to use CloudStack, but any time I catch a glimpse of the dashboards that are in their UI, I know the designers are doing it right. The information is organized in a clear and concise way without too much clutter. It looks as though the folks working on this UI have done research to figure out what is the most important data to surface to users at a glance, and they've left the rest to further drill down detail pages. The visuals are soft are inviting which makes it easy for users to have up on one of their screens throughout the day if needed for monitoring a cloud environment. Here are some of the examples I've seen out there:
![CloudStack Dashboard 1](https://github.com/lizsurette/lizsurette.github.io/raw/main/static/img/_posts/cloudstack-dashboard-1.jpg)

![CloudStack Dashboard 2](https://github.com/lizsurette/lizsurette.github.io/raw/main/static/img/_posts/cloudstack-dashboard-2.png)


#### Google Compute Engine
I hadn't tried out Google Compute Engine before, so when I gave it a go I was pleasantly surprised at the first time user experience. Rather than dropping the user into an Overview with statistics that are empty considering they haven't spun up any instances, Google decided to try and push the user in the right direction. They give a few options right off the bat:
![Google First Time User 1](https://github.com/lizsurette/lizsurette.github.io/raw/main/static/img/_posts/google-first-time-user-1.png)

![Google First Time User 2](https://github.com/lizsurette/lizsurette.github.io/raw/main/static/img/_posts/google-first-time-user-2.png)

Another important decision that Google made was to be sure to give users plenty of information before they decide to take certain actions. For example, when a user tries to delete a project (a pretty huge action), they are given a description of what will happen next if they confirm the action. I think this is a great view into designers thinking about how certain actions will impact users long term:
![Google Delete Project](https://github.com/lizsurette/lizsurette.github.io/raw/main/static/img/_posts/google-delete-project.png)

#### Amazon Web Services
Amazon Web Services includes a ton of different applications that a user can take advantage of. They've done a great job organizing their information architecture to handle all of these selections. One key design feature they added was to take into consideration the importance of horizontal screen space and to allow the user to hide/show the left hand navigation as needed.
![AWS Dashboard](https://github.com/lizsurette/lizsurette.github.io/raw/main/static/img/_posts/aws-dashboard.png)

The dashboard in this view is also something to note. The designers have included a mixture of statistics along with common actions that they know a user will want to take when they jump into this UI.

Are there any features that you’ve seen out there that inspire you to have something better in Horizon? These are definitely some of the things that have caught my eye. Let me know if you have seen any others, I’m happy to log blueprints and put together designs!

Best,
Liz
