---
title: Team
nav:
  order: 3
  tooltip: About our team
---

# {% include icon.html icon="fa-solid fa-users" %}Team

Our team ranges from undergraduate and higher degree research students to postdoctoral and senior researchers. We have a range of student projects in the pipeline for numerate graduates. If you are interested in colaborating or joining our team, please get in contact. 

{% include section.html %}

{% include list.html data="members" component="portrait" filters="role: pi" %}
{% include list.html data="members" component="portrait" filters="role: ^(?!pi$)" %}

{% include section.html background="images/background.jpg" dark=true %}

We work within the School of Mathematics and Statistcis and the Climate Change Research Centre at at the University of New South Wales and are also linked to a range of national projects. See the links below.

{% include section.html %}

{% capture content %}

{% include figure.html image="images/unsw_logo.png" link="https://www.unsw.edu.au/science/our-schools/maths"%}
{% include figure.html image="images/ACEAS_logo.png" link="https://antarctic.org.au/" %}

{% include figure.html image="images/Udash-logo-revised-04-2.png" link="https://www.unsw.edu.au/research/udash" %}

{% endcapture %}

{% include grid.html style="square" content=content %}
