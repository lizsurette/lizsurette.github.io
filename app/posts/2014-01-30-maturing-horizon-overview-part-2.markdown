---
layout: post
title:  "The OpenStack Years: Maturing the Horizon Overview Page Part 2 - Interaction Design"
date:   2014-01-30
categories: [openstack]
---

> <em>This was originally written and shared on January 30, 2014 when I was working daily with the OpenStack Community.</em>

---

After going through an activity to [understand the user and gather a list of requirements](https://lizsurette.github.io/openstack/2014/01/27/maturing-horizon-overview-part-1.html), Ju and I were in great shape to begin designing an Overview page that we could be sure would meet our Horizon users needs. As mentioned in my previous post, Ju played a big role in defining both the users and their requirements, but she continued to participate as I was designing to give feedback along the way as a use case expert.

The first step in almost all of my designs includes some sort of sketching and/or whiteboarding. Depending on where I am and if I’m collaboratively designing, I’ll either sketch in my [Moleskine](http://www.moleskine.com/en/) or jump into a room with a whiteboard and start drawing. I normally just let my mind go over the requirements and try to capture things on paper/whiteboard as fast as I can, trying to avoid overthinking things. The best thing about drawing on paper or on a whiteboard is that you don’t get too attached to your designs. It’s easy to scrap ideas if you haven’t put a ton of effort into them. Here is a look into the very first ideas that Ju and I came up with for the updated Overview page:
![Overview Sketches](https://github.com/lizsurette/lizsurette.github.io/raw/main/static/img/_posts/overview-sketches.png)

Pretty ugly at this point, right? Yes, I know I don’t have a future as a sketch artist. Well, the ideas are just starting to form at this point and organization and legibility isn’t a huge factor. At this point I’m talking and thinking much faster than my hand can capture. Let me try to translate a bit about the thought process here… We’d like to break down the information that a user would want to see on the Overview page into 3 main sections: Compute, Storage, and Network & Security. It would be great to give the user some visualizations that they can glance at quickly to get an idea of how their environment is performing. Perhaps a mixture of a sparkline to show the trend over time and a bar graph to give the user a picture of the current utilization would be the best way to represent this mix of data. Since this is an Overview page, the user will likely jump off and perform certain actions from this page. It would be nice to have a section of quick links to common actions to support this. There will be additional links and details for certain categories of information that also need to be represented on the screen.

After a good hour of sketching and further discussion with Ju, I took a stab at translating these ideas into wireframes. Wireframes are more solid than sketching, but that doesn’t mean they are a final product. The goal behind wireframes is to get them into a legible format that can be distributed. Wireframes can still be changed very easily. They are not set in stone by any means, but they serve as a great way to get feedback on what certain pieces of the UI could start to look like. For these wireframes, I used Adobe InDesign, although I’ve used a lot of other tools in the past eight years of my design career. A quick side bar on a few of the tools I’ve used and why I'd use them in the future:
> #### Axure
Great for working on a shared prototype with a group. Can check in /out files to prevent from stepping on each others toes. The output is a clickable HTML prototype which is great for getting a sense of the small interaction details of a design.
> #### Photoshop
Super steep learning curve, but a very powerful tool once you get the basics down. Great for prototyping high-fidelity mockups or even cutting up and editing an existing mockup quickly.
> #### Illustrator
Similar to Photoshop with respect to learning curve. Certain basics like selecting objects isn\'t consistent with Photoshop which can be frustrating, but a great tool in the end for creating vector designs that may need to scale. I\'ve also used this for print designs with success.
> #### Balsamiq
Awesome for really quick WISIWIG wireframing/prototyping. Very nice “Sketch” skin that makes it clear these wireframes can be changed easily. There is also a way to change the skin to look a bit more polished if needed. This tool also allows assigning of clickable elements which produces a PDF that acts like a clickable prototype.
> #### InDesign
The use of masters makes larger sets of designs where elements are reused throughout pages easy to wrangle. Similar to Photoshop and Illustrator with respect to features, but again the slight difference in interactions gives the user yet another learning curve. There is also a way to make elements clickable in an outputted PDF, so this can simulate a prototype.

A big factor in the tool I use is which other designers I'm working with and what tools they are using. I try really hard to sync up with the majority of other designers that I’m working collaboratively and use what they are using. It makes it that much easier to bounce ideas off of each other, share, and reuse designs.

After half of a day of translating sketches to wireframes and adding in a few extra details, here is how the first cut panned out:
![Overview Wireframes](https://github.com/lizsurette/lizsurette.github.io/raw/main/static/img/_posts/overview-wireframes.png)

If you are familiar with Horizon, you will probably first notice that the navigation structure looks a bit different from the current Havana release. We have been experimenting with updating the navigation design and the idea of horizontal navigation just happened to make this set of wireframes, so if you can, ignore the navigation changes for now and focus on the content of this Overview page. As in the early sketches, the wireframe is broken down into 3 sections. The first focuses on Compute information. Users are presented a graph of information showing details for Instances, vCores, vCPUs, and Memory. They can quickly view how many of each of these are currently in use compared to the quota that is allowed. Users can also quickly jump via links to public or private images that are being used by instances. Similarly, the user can view a section for Storage information: specifically Ephemeral, Object, Block, and Snapshot usage and quotas. I decided to break down the larger "Quick Links" area into a list of links specific to each section of data. This breakdown, for example, will make it easier to jump to Storage actions if the user is currently focused on a Storage task. With respect to Network and Security, the user can quickly see the number of Floating IPs both mapped and unmapped as well as the number of Security Groups.

After getting to a solid point with the wireframes, the next step was to reach out to a few different groups for feedback. I [reached out](http://ask-openstackux.rhcloud.com/question/59/improvements-to-horizon-overview/) to the UX community for some thoughts. This community is fairly new. I didn’t get much feedback here considering two of the main contributors to the site are Ju and me. Another team that I reached out to for feedback was the Horizon development team. During the weekly meeting I shared my progress and they were excited about the direction of this design. I figured using the weekly meeting would be a more targeted way of getting feedback rather than blasting the entire openstack-dev mailing list, but using the mailing list in the future might be a good way to get more eyes on designs.  Currently, I'm seeking out feedback from end users to validate that these wireframes would meet their needs. I've [posted](http://lists.openstack.org/pipermail/openstack-operators/2014-January/003956.html) to the openstack-operators mailing list in hopes that some potential users will be able to give some thoughts on these designs.

I've linked to these designs in the Horizon [blueprint](https://blueprints.launchpad.net/horizon/+spec/project-overview-page-ceilometer) for this feature. My next steps are to give any design support that is needed (answering questions, updating the design) during the development of this blueprint. After the implementation is done, I want to do some usability testing with end users to be sure it works for them in their work environment. Stay tuned for posts on both of these topics.

What do you think about this design? Is there anything missing at an overview level that you would expect to be here for an end user? How about the design process? I’d love to hear if you have any suggestions on improving this as well.

Best,
Liz
