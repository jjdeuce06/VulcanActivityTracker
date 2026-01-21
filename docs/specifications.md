Vulcan Activity Tracker

*The Athletic Activity Tracker for PennWest California Students.*

Specifications Document

Team Members:

Margo Bonal

John Gerega

Luke Ruffing

Professor:

Dr. Weifeng Chen

Course: Software Engineering Project I

School: Pennsylvania Western University

**[Instructor Comments/Evaluation]{.underline}**

# **[Table of Contents]{.underline}** {#table-of-contents .TOC-Heading}

[**Abstract** [3](#abstract)](#abstract)

[**Description of the Document**
[5](#description-of-the-document)](#description-of-the-document)

[**Purpose and Use** [5](#purpose-and-use)](#purpose-and-use)

[**Intended Audience** [5](#intended-audience)](#intended-audience)

[**System Description** [5](#system-description)](#system-description)

[**Overview** [5](#overview)](#overview)

[**Environment and Constraints:**
[6](#environment-and-constraints)](#environment-and-constraints)

[**End User Profile** [6](#end-user-profile)](#end-user-profile)

[**User Interaction** [6](#user-interaction)](#user-interaction)

[**Hardware Constraints**
[6](#hardware-constraints)](#hardware-constraints)

[**Software Constraints**
[7](#software-constraints)](#software-constraints)

[**Time Constraints** [7](#time-constraints)](#time-constraints)

[**Cost Constraints** [8](#cost-constraints)](#cost-constraints)

[**Other Concerns** [8](#other-concerns)](#other-concerns)

[**Acceptance Test Criteria**
[9](#acceptance-test-criteria)](#acceptance-test-criteria)

[**Testers** [9](#testers)](#testers)

[**Criteria for User Acceptance**
[10](#criteria-for-user-acceptance)](#criteria-for-user-acceptance)

[**System Modeling** [11](#system-modeling)](#system-modeling)

[**Functional: Use Cases & Scenarios**
[11](#functional-use-cases-scenarios)](#functional-use-cases-scenarios)

[**Entity: Class Diagrams**
[13](#entity-class-diagrams)](#entity-class-diagrams)

[**Dynamic: Statechart** [16](#dynamic-statechart)](#dynamic-statechart)

[**States** [17](#states)](#states)

[**Events** [18](#events)](#events)

[**Transitions** [18](#transitions)](#transitions)

[**Dataflow Diagrams Components**
[19](#dataflow-diagrams-components)](#dataflow-diagrams-components)

[**Tools Needed** [20](#tools-needed)](#tools-needed)

[**List of Resources** [21](#list-of-resources)](#list-of-resources)

[**Appendix I: Glossary of Terms**
[22](#appendix-i-glossary-of-terms)](#appendix-i-glossary-of-terms)

[**Appendix III: Workflow Authentication**
[25](#appendix-iii-workflow-authentication)](#appendix-iii-workflow-authentication)

[**Appendix IV: Writing Center report**
[27](#appendix-iv-writing-center-report)](#appendix-iv-writing-center-report)

# 

# **[Abstract]{.underline}**

This project, the Vulcan Activity Tracker, is an activity tracker that
can be accessed by students attending Pennsylvania Western University's
California branch. The activity tracker will allow students to track any
physical activity they participate in, which may include running,
sports, walking, lifting, and many more. *Strava (2025),* running and
fitness app, is the initial inspiration for this project, however,
campus life will be modeled as the environment. This project will use a
Docker container, a database, and a Python backend, built alongside a
CSS/Vanilla HTML frontend. All these components will be used to track
user data, such as login information and the activities the user has
completed. The Docker container will be used to keep the frontend,
backend, and database in one place. This will also ensure that the app
runs consistently across multiple platforms. The database will store all
the users and their data. Functions to retrieve, create, and delete data
will be written in the Python programming language. The user will be
able to add activities manually and view other users' activities. This
document will cover all necessary details for the user and the
development team regarding the functionality of the final product.

# **[Description of the Document]{.underline}**

## **[Purpose and Use]{.underline}**

The purpose of this document is to define the scope and specific
requirements for the project. These requirements include the product's
functionality and system requirements. The developers and clients will
use this document to state the terms of their arrangement. The client
has the right to dispute the contents of this document, so the product
properly reflects their desired requirements. After acceptance of the
terms stated in this document, it shall be known that this document
becomes a binding contract.

## **[Intended Audience]{.underline}**

This document's intended audience includes the clients and product
developers. The product developers have created this document to make an
outline of their finished product. By doing so, it helps the client to
know exactly what product, functionality, and the cost that will be
associated with this project. It also assists the development team to
know which direction they are headed in and states their priorities for
the project. Any uncertainty in this document needs to be addressed as
this serves as a binding contract.

# **[System Description]{.underline}**

## **[Overview]{.underline}**

The Vulcan Activity Tracker is a software application, accessed via a
web application. The main function of the activity tracker is to
manually track exercise activities. A user can track exercise activities
ranging from multiple sports. These could include running, lifting,
biking, swimming, any organized sport, and many other activities. A user
will also be able to join their sports team, recreational club team, or
create a group with friends. With recreational clubs and teams there
will be a person to admit users into the organization. Users can view
activities from everyone on campus. A leaderboard for each activity will
also be accessible to all users in order to inspire some friendly
competition.

# **[Environment and Constraints:]{.underline}**

## **[End User Profile]{.underline}**

The most common end users of the Vulcan Activity Tracker are PennWest
students, most likely ones involved in sports or recreational clubs.
Users should be familiar with using web applications to interact with
the website. With a basic understanding of navigating web applications,
any student will be able to add an activity, view their statistics, view
other students' activities, and view the leaderboards.

## **[User Interaction]{.underline}**

The user interaction will be through the software application that runs
the web application. Once the user logs in or creates a new account with
Pennsylvania Western credentials, they will be redirected to the home
page with all recent student activities. The user can then find the
buttons to redirect them to the leaderboard section, group section, and
the section to actually add an activity. In the leaderboard section,
users will be able to filter based on activity type and by group,
meaning they can see the leaderboard of only their group or
organization.

##  **[Hardware Constraints]{.underline}**

The following are hardware constraints of the Vulcan Activity Tracker. A
user will need the following:

- A desktop computer system (with mouse & keyboard), laptop computer, or
  mobile device with internet access and WIFI capabilities.

- Internet network components of router, modem, ethernet.

- Mobile device data plan from ISP.

- Current Windows version 11

- External fitness tracker i.e. smart watch for collecting activity
  tracking data.

## **[Software Constraints]{.underline}**

Software constraints for the Vulcan Activity Tracker will include
components that directly impact both development and useability. A
current updated operating system is important for proper functioning.
Mobile devices must also be updated for optimal use. To ensure multiple
users can interact with the site at one without system throttling,
internet speed will need to be tested. Antivirus software applications
will need to be tested and monitored to see if they slow operations by
any means.

## **[Time Constraints]{.underline}**

The time constraints for this project are designed for Senior Project
course requirements. Fall 2025 semester is allocated for documentation
of team chosen project. This will make up fifteen-week timeline. The
following fifteen-week term will be dedicated to development and design.
Several hours per week will be allotted to team meetings, development,
testing, and advisory check-in meetings. A goal will be set to have the
project adequately finished in sufficient time before due date and end
presentation to ensure testing time. All declared and documented
features will be anticipated to be completed and functioning at the end
of proposed timeline.

## **[Cost Constraints]{.underline}**

Cost constraints will be related to software toolsets and subscriptions.
Development tools will need to be evaluated and considered with cost
analysis. Since most toolsets and libraries will be open-sourced, the
primary cost constraint for the Vulcan Activity Tracker will be web
application hosting service. Most services only allot certain time
periods for free hosting, or certain qualities of service. The best
hosting application will be decided through team decisions.

## **[Other Concerns]{.underline}**

The end-user will need to have access to Wi-Fi or a Data Plan to utilize
the website. If a student is out of range of cellular service, for
example, hiking, access to the Vulcan Activity Tracker will be impacted.
Users must also have valid Pennsylvania Western University credentials.
Limitations need to prevent non-PennWest students from using the
application. The sharing of student credentials is unintended and
improper use case. A final but significant concern is the uploading of
malicious content to data entry fields. Since the Vulcan Activity
tracker is primarily a web-based application, cybersecurity attacks such
as internet virus infection, data injection, and DDoS are of concern.
The developers of the Vulcan Activity Tracker are held non-responsible
for user data corruption and cybersecurity attacks; however, software
precautions will be implemented to protect the CIA Cybersecurity Triad:
Confidentiality, Integrity, and Accessibility. The *Fortinet (2025)*
article, CIA Triad, provided helpful information for team security
modeling. *"Applying the CIA triad can help strengthen an organization's
overall security strategy. It protects sensitive data from exposure,
ensures information isn't tampered with, and keeps systems available
when users need them. Together, these three pillars reduce risk, support
compliance, and build a robust IT environment. (Fortinet, 2025)"*

# **[Acceptance Test Criteria]{.underline}**

## **[Testers]{.underline}**

The Vulcan Activity Tracker will be thoroughly tested to ensure proper
functionality and quality assurance. Primary testing will be carried out
by Senior Project development team. All members will perform individual
testing along with team testing on hardware/software accessibility,
application use, feature operations, and mobile device access. Each
member will exhaust their testing abilities and resources. Testing will
be performed throughout the project's development. Additional testers
will be brought in to explore application use and provide external
opinions to ensure that useability is of primary importance for campus
students.

The following people will serve as testers for the Vulcan Activity
tracker:

Developers:

- Margo Bonal

- John Gerega

- Luke Ruffing

Professor:

- Dr. W. Chen

External Testers (PennWest Student outside of CS Major):

- Oumer Abdulkadir

- Bilal Ghasfan

## **[Criteria for User Acceptance]{.underline}**

Proper criteria for successful user acceptance of the Vulcan Activity
Tracker will be reached when a user can access the platform and perform
all features with no errors. A user should be able to log into the user
portal to access fitness data, leaderboards, activity routes, and group
activities. The following criteria are represented in the following
points established by the Senior Project development team as application
success.

- PennWest secure Student Log In

- Access platform

- Navigate pages: User Profile, Activity Page, Leaderboard Page

- Students can log athletic activities, with input of workout statistics
  and data

- Students can choose or add custom activity environments

- Past activity history can be viewed and sorted.

- Students can make activity groups for friends or clubs

- Students can view leaderboard features to see highest participation
  and stats

- Friendly social interaction between users will be achieved

> **[Integration of Separate Parts and Installation]{.underline}**

The Vulcan Activity Tracker is designed for easy accessibility. Since it
will be a web-based application, the user is not required to install or
download software. This encourages more users to participate since
laptop storage constraints can discourage use, especially students
storing many homework assignments. For access to the Vulcan Activity
Tracker, a PennWest student user will need to access the application
through the web browser on either a computer or mobile device and enter
their student email address credentials for valid entry.

# **[System Modeling]{.underline}**

# **[Functional: Use Cases & Scenarios]{.underline}**

Upon entering the correct PennWest credentials, the user can choose
between 7 options shown in the diagram below.

![](media/image1.png){width="6.5in" height="4.325694444444444in"}

Figure 1 displays a simple Use Case Diagram of what the user would see
once they have successfully logged in. They will be redirected to the
activity page once logged in, but will have a menu bar with multiple
options that they can click on and redirect to. The activity feed will
display all users\' recent activities around campus. The View
Leaderboard section will take the user to the leaderboard, which the
user can then filter by activity, club/team, or by group if they want a
more specified leaderboard. The Add Activity page will let the user
manually enter an activity they have recently completed. The user will
need to enter the activity type, duration, mileage (if applicable), date
completed, route completed on, and detailed specifications based on the
activity type. An example of detailed specifications would be an average
mile time if a user completed a run. The detailed section will be
optional, as not every student will have access to that kind of
information. The Club/Organization page will allow the user to see more
details about their group, club, organization, or team activity which
they are a part of. Clubs, Organizations, and Teams will have an Admin
who will oversee who is allowed into their group on the application.
Groups can be made between friends and will be open to anybody. The User
Profile page will display the user's activities only, as well as an
overview of their statistics based on their logged activities. The Log
Out button will redirect the user to the original login page.

[Run Scenario]{.underline}

1.  User logs in with correct PennWest credentials

2.  User is redirected to Activity Feed, but clicks on the Add Activity
    button to track their most recent run

3.  User enters required details for a run, which includes the distance,
    time, and whether it was an indoor or outdoor run

    a.  Outdoor runs will have routes that can be taken around campus
        available to choose from

4.  The User then names the run and hits submit in order to upload it
    into the database

5.  The User goes to view their own profile to make sure the run was
    uploaded and is visible on their profile.

6.  The User clicks on the Leaderboard Section of the app and is
    redirected to a general leaderboard.

7.  The User then filters the leaderboard to running to see if their
    most recent activity affected their standings

8.  User clicks Log Out

##  ******[Entity: Class Diagrams]{.underline}**

![A screenshot of a computer AI-generated content may be
incorrect.](media/image2.png){width="6.094612860892388in"
height="2.3336636045494314in"}

Figure 2: Class Diagrams

**[Class name / description / type]{.underline}**

**User Class:** The User Class holds the data needed for each user. It
will hold the first name, last name, email and password that the user
used to sign up, after sign up each user will be given a User ID which
is an integer used to link the user to their activities and groups.

**Activity Class:** The Activity Class holds the data needed for each
activity. As soon as the create activity button is pushed an activity
object will be created giving the object a unique activity ID and
storing the ID of the user creating the activity. Once created, the
activity will ask for the input of activity type, distance, duration,
date, route name (Optional), and Pace (Optional). Once all the needed
data is added to the activity it will be stored in the database.

**Group Class:** The Group Class holds the data needed to create and
manage each group. Once a group is created by a user the group object
will receive a unique group ID. The user will then input an appropriate
group name and become the group's administrator. Each group object will
also hold the Admin ID (ID of user that created the group), a list of
the members, and a group leaderboard that tracks group performance.

**[Attributes]{.underline}**

User Class Attributes:

  ---------------------------------------------------------------------------
  **Attribute**            **Type**        **Description**
  ------------------------ --------------- ----------------------------------
  FirstName                string          The user's first name.

  LastName                 string          The user's last name.

  UserID                   int             A unique number that is used to
                                           identify each user.

  Email                    string          The email address the user used to
                                           register.

  Password                 string          The password the user used to
                                           register.

  Groups                   list\<Group\>   A list of groups the user is a
                                           member of.

                                           
  ---------------------------------------------------------------------------

Activity Class Attributes:

  -----------------------------------------------------------------------
  **Attribute**            **Type**    **Description**
  ------------------------ ----------- ----------------------------------
  ActivityID               int         A unique number that is used to
                                       identify each activity.

  UserID                   int         The ID of the user who created the
                                       activity.

  ActivityType             string      The type of activity that was
                                       performed.

  Distance                 float       The total distance covered during
                                       the activity.

  Duration                 float       The total time spent completing
                                       the activity.

  Date                     date        The date on which the activity
                                       occurred.

  RouteName                string      An optional field that hold the
                                       name of the route taken.

  Pace                     float       An optional field for recording
                                       the user's pace.

                                       
  -----------------------------------------------------------------------

Group Class Attributes:

  --------------------------------------------------------------------------
  **Attribute**            **Type**       **Description**
  ------------------------ -------------- ----------------------------------
  GroupID                  int            A unique number that is used to
                                          identify the group.

  GroupName                string         The name of the group.

  AdminID                  int            The ID of the user who created and
                                          manages the group.

  Member                   list\<User\>   A list of all users who are
                                          members of the group.

  GroupLeaderboard         leaderboard    A leaderboard that displays the
                                          performance of all users in the
                                          group.

                                          
  --------------------------------------------------------------------------

#  **[]{.underline}****[Dynamic: Statechart]{.underline}**

**[\]{.underline}**
![A diagram of a computer AI-generated content may be
incorrect.](media/image3.png){width="6.5in"
height="3.423996062992126in"}

Figure 3: User State Diagram

Figure 3 shows the User State Diagram, which models how a user can
navigate the Vulcan Activity Tracker. The user starts in the logged-out
state, after the user enters valid credentials, they are put into the
activity page. From the activity page the user can navigate between
adding activities, viewing leaderboards, viewing activity feed, and
viewing/joining clubs, users are also able to manage a club if they are
an admin of the club.

![A screenshot of a computer AI-generated content may be
incorrect.](media/image4.png){width="7.178884514435696in"
height="2.4182720909886264in"}

Figure 4: Add Activity State Diagram

#  **[States]{.underline}**

- The user logs in with PennWest Credentials and is redirected to the
  Activity Page

- Once logged in, the user has 5 options

  - State 1: Add an Activity by adding all required information

  - State 2: View Leaderboard, filtering as desired

  - State 3: View Activity Feed, seeing all recent activities completed
    by students on campus

  - State 4: Club Page, if part of a club, organization, team, or group,
    this page will show the data for everyone part of the organization.
    If user is an admin they can go in and edit club details.

  - State 5: Log Out, which will take user back to the log in page

##  **[Events]{.underline}**

> There are many user-driven events that trigger the transition between
> states in the Vulcan Activity Tracker:

1.  Click "Log In"

2.  Click "Add Activity"

3.  Click "View Leaderboard"

4.  Click "View Activity Feed"

5.  Click "Club Page"

6.  Click "Join/View Clubs"

7.  Click "Manage Clubs"

8.  Click "Back"

9.  Click "Log Out"

##  **[Transitions]{.underline}**

- Once the user is logged in, they have a series of options they may
  choose. The initial state is the activity feed page, which will be
  considered the home page. The user can loop through as many times as
  they want through Activity feed, Add Activity, View Leaderboard, and
  Club Page. The only way the user may exit the program is by logging
  out.**\**

# **[Dataflow Diagrams Components]{.underline}**

![A screenshot of a computer AI-generated content may be
incorrect.](media/image5.png){width="6.5in"
height="2.384027777777778in"}

Figure 5: Add Activity Sequence Diagram

The sequence diagram above illustrates the process flow of adding a new
activity in the Vulcan Activity Tracker. The sequence starts with the
user requesting the addition of a new activity, this happens when the
user clicks "Add Activity" in the activity page. The activity page UI
collects the activity details from the user and then sends them to the
controller, which is responsible for validating the details provided by
the user. After the data has been validated by the controller it is sent
to the database to store the new activity record. After the database has
successfully stored the record, confirmation is sent back to the
controller, the controller then sends a confirmation message to the
activity page UI. Finally, the activity page UI displays a success
message to the user, and the user's activity feed is updated with the
new activity.

# **[Tools Needed]{.underline}**

Tools for the development of The Vulcan Activity Tracker will include
both software and hardware components. For software development, Visual
Studio Code, GitHub, Git, Docker, SQL Database, Python libraries, Flask
Server logic, a hosting service, frontend programming language, and
schema framework will be used. These software components are crucial to
the building of The Vulcan Activity Tracker's web-application. A QR-code
generator will be needed to package mobile access link and display onto
site. However, since the Vulcan Activity Tracker is designed with the
user in mind, in Production Phase, there are no required hardware
components needed to build. The user needs UpToDate operating system and
a device (mobile or computer) to access.

# **[List of Resources]{.underline}**

Docker. (2025) ***What is Docker?***

<https://docs.docker.com/get-started/docker-overview/>

Fortinet. (2025) ***CIA Triad.***

<https://www.fortinet.com/resources/cyberglossary/cia-triad>

Jeremiah, O. (2024, Aug 18^th^). ***Python Backend Development: A
Complete Guide for Beginners.***

<https://www.datacamp.com/tutorial/python-backend-development>

SolarWinds. (2025). What is a Database Query?

<https://www.solarwinds.com/resources/it-glossary/database-query>

Strava, Inc. (2025, Sept 11). ***Strava* (Version 428.0.1)** *\[Website
and Mobile App\].*

<https://www.strava.com>

Yasae, K. (2024, Nov 25^th^). ***What is web application (web apps) and
its benefits?***

<https://www.techtarget.com/searchsoftwarequality/definition/Web-application-Web-app>

# **[Appendix I: Glossary of Terms]{.underline}**

**Activity Feed --** component that show past and current activities
participated in. Allow the sorting by date, or data statistic.

**Admin --** a user with full access privileges to an application with
no limitation. Privileges may be view, read, write, execute for data
modification.

**API (Application Programming Interface) -** Short for Application
Programming Interface, a connection between computers or computer
programs that offer services to other pieces of software.

**Database --** a structured set of data held in a computer, especially
one that is accessible in various ways.

**Database Query --** A database query is the logic that is used to
access, retrieve, delete, manipulate information from the database
container. It is a specific format that allows for table injections.

**Docker Container --** Docker is an application that aids in
developing, shipping, and running applications. It consolidated database
logic into one place, allowing you to run your database and application
together instead of building separate. Allows for easy and fast
management*. "Docker provides the ability to package and run an
application in a loosely isolated environment called a container (2025,
Docker)."*

**Entity Class Diagram --** shows the structure of data classes in a
system. Represents the relationship between data, the actions performed,
and methods used. This diagram is mainly mor systematic modeling for
object-oriented software projects.

**Frontend (CSS/HTML) --** the frontend of an application is the part
that users interact with. This is what is loaded when the application is
opened. Frontends are usually written in Vanilla HTML and CSS
programming languages. This allows for formatting, styling, and coloring
of the site.

**Git --** A distributed version control software system that can manage
versions of source code or data. It is often used to control source code
by programmers who are developing software collaboratively.

**GitHub --** A proprietary developer platform that allows developers to
create, store, manage, and share their code. It uses Git to provide
distributed version control and GitHub itself provides access control,
bug tracking, software feature requests, task management, continuous
integration, and wikis for every project.

**Leaderboard --** a social interactive feature that stores overall
highest activity data.

**Python Backend --** refers to the server side or behind the scenes
logic that drives/powers a web application. It is built in the python
programming language. The python server handles logic, data processing,
and database communication. This communication is done through series of
API calls.

**Server --** A computer that provides information to other computers
called "clients" on a computer network. Servers can provide various
functionalities, often called "services," such as sharing data or
resources among multiple clients of performing computations for a
client.

**State Chart Diagram --** shows the relation of how objects and systems
change over time while responding to certain events. This diagram
represents behavior, phases, and event driven systems.

**Use Case Diagram --** the use case diagram is used to illustrate how
users interact with a system or application.

**Web Application -- "***A program that is stored on a remote server and
delivered over the internet through a browser interface (2025,
TechTarget)"*. This differs from a website because websites are
primarily static web pages connected for reading information, whereas
web applications are powered by servers and databases to provide user
functionality.

**[\
Appendix II: Team Details]{.underline}**

This specifications document was developed through the collaboration of
all team members. The document was made with the combined efforts of the
entire team over the course of the project timeline. While each member
contributed across various parts of the document, the primary
contributors for each section are listed below:

- Margo Bonal:

  - Title Page, table of contents, Hardware/software/time /cost/other
    constraints, acceptance test criteria, tester, user acceptance,
    integration and installation, appendix II, III, IV, glossary,
    reference list

- John Gerega:

  - Title Page, Abstract, Description of document- purpose, intended
    audience, system description, end user, user interaction

- Luke Ruffing:

  - System modeling, functional use case scenario, entity class diagram,
    class descriptions, dataflow diagrams

The rest of the major sections of the document were completed
collaboratively with all members participating equally in discussions,
decision making, and writing. This collaborative approach taken to
completing the document allowed the group to refine ideas and reach a
consensus before making any big decisions.

In addition to the writing of each section, all team members took part
in proof reading and formatting ensuring the creation of a clear,
concise and well-organized document. Together the team worked to check
for proper grammar, proper citation, and adherence to all formatting
guidelines.

# **[Appendix III: Workflow Authentication]{.underline}**

I, Margo Bonal, confirm that all work I have contributed to this
document has been to the best of my knowledge, completed with integrity
and in accordance with the objectives and collaborative standards
established by the team. I attest that I will maintain these standards
in all future contributions to this project.

Signature: ![A close-up of a black text AI-generated content may be
incorrect.](media/image6.png){width="1.7395833333333333in"
height="0.4326388888888889in"} Date: 11/14/25

I, John Gerega confirm that all work I have contributed to this document
has been to the best of my knowledge completed with integrity and in
accordance with the objectives and collaborative standards established
by the team. I attest that I will maintain these standards in all future
contributions to this project.

Signature: ![A black text on a white background AI-generated content may
be incorrect.](media/image7.png){width="1.7243055555555555in"
height="0.5680555555555555in"} Date: 11/14/25

I, Luke Ruffing, confirm that all work I have contributed to this
document has been to the best of my knowledge completed with integrity
and in accordance with the objectives and collaborative standards
established by the team. I attest that I will maintain these standards
in all future contributions to this project.

Signature:![A close-up of a signature AI-generated content may be
incorrect.](media/image8.png){width="1.8493055555555555in"
height="0.6354166666666666in"} Date: 11/14/25

# **[Appendix IV: Writing Center report]{.underline}** 

The following notes related to your 11/12/2025 2:00 PM EST appointment
with Chayse Lizon have been shared with you:

Your and your group came in for a review of your paper overall and in
comparison to the rubric and the example papers provided. Content wise I
think that you did good in making sure that every single one of the
sections was hit and I didn\'t notice anything content or grammar wise
that particularly stood out. While most of the paper follows the
formatting rules, for the figure numbers it should be altered into being
times new roman and 12 point. Also, I suggest that you make the figure
title closer to the figures present. Another thing that was observed was
that some sections should be indented (there is one that says Figure 3
that probably should be). You should read through the paper aloud on
your own to verify if there is anything that sounds incorrect or should
be further explained. Make sure for your resources page that the
citations are in the proper format and have all the details necessary,
and as we discussed you will need to put them in alphabetical order.
When you refer to these sources in the paper and you do in-text
citations make sure that they are before the periods and not inside of
quotation marks. Delete any extra spacing above titles and make sure all
your titles are centered, consistency is key. Another thing that stood
out was the bullet points seemed to be over a significant amount so you
should try and move those over if possible. I meant to point it out, but
if your quote wasn\'t italicized then do not italicize it in the paper.
If you have any following questions, please feel free to email me at
liz58193@pennwest.edu 
