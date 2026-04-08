# Sample Photos of Functionality 
-   Choose Problems --> Review Problem--> Bundle --> Create Assignment --> GitLab Project Created
-   Detailed information below.

<img width="968" height="624" alt="Screenshot 2026-03-10 at 10 45 26 PM" src="https://github.com/user-attachments/assets/bea6c9f8-d83b-4b0f-bb57-7af1e7a18467" />
<img width="962" height="619" alt="Screenshot 2026-03-10 at 10 45 53 PM" src="https://github.com/user-attachments/assets/9501736f-9679-4221-90a1-e3e9cdc53632" />
<img width="967" height="624" alt="Screenshot 2026-03-10 at 10 46 59 PM" src="https://github.com/user-attachments/assets/39780d37-3353-4568-887b-b65e7d304e0d" />
<img width="1512" height="869" alt="Screenshot 2026-03-10 at 10 51 25 PM" src="https://github.com/user-attachments/assets/b137dd89-36fc-4f3f-8e8e-71920aa947c8" />



# Current Progress
Assignment manager lets user pick and match problems to bundle into assignment. Upon user choice, the assignments are sent to gitlab in their own project with repositories. These are then available and ready for students to clone to complete and commit back to GitLab.

-    Code organized using SOLID principles

# Project Estimated Completion Date
- May 2026

# Project - Assignment Manager

This repository is for the semester project. For each milestone, you should update the corresponding
section with information about your project status. Do not complete README sections for future milestones or
the final submission when we still have not gotten to an earlier milestone. This is likely to cause
confusion for peer code reviewers. Doing so may result in the loss of points, up to and including
an award of 0 points as determined by the instructor.

## Milestone 1

My project for milestone one is the framework for an assignment manager for computer science professors at Georgia 
Highlands College. This project will communicate with GitLab to receive repository's, build assignments, then send them
out to students to complete through PyCharm. This goal for this project is to increase the efficiency at which problem sets 
are created as well as group together topics that will be useful to learn. I will be creating the assignment database, 
generator, and GUI that will result in easy accessibility for the user to carry out the tasks they want.

### Current Progress

The current progress of my project is the framework. I am using SQLite 3 to create the database at which files
like build_assignment and insert_problems will communicate with. When I receive the repository for the problems I will be 
implementing, the database will be more complete with what the professor will be able to choose from. I have also started
working on the GUI that will be used by the user themselves. After doing some research I have created a local web app using
html, however I am considering moving this to a live website but not entirely sure.

### Challenges

The challenges I have faced so far have been learning the different things needed for this project like, SQLite 3 and Html.
Another issue I have faced is making sure everything is connected, when creating the database, sometimes different parts of it 
were not connecting therefore it created an empty database. Once I figured this out, the sample problems started populating. 

### Future Directions

My plans for the next milestone is to start playing around with incorporating the repository problems with my program and doing 
research on how to do so. I also want to look into maybe moving my web application into a live website. Along with 
that, I will be designing and improving the look and functionality of the GUI as well. Need to connect problem set labs into database
and GUI.



## Milestone 2

From Milestone 1, my project the development of my project has drastically changed. I have completed many features that are going to be useful
in using my application. Milestone 2 was about getting my project functioning to the best of its ability and being able to present to others.
The goal I set for this application is coming alive as the creation of assignments is happening in just a few clicks of a button. The database is
created, GUI, as well as the creation of repositories in GitLab. I am ready to continue polishing my project until it is ready for deployment but
have made immense progress since milestone 1.

### Current Progress

I have set up the GUI in Textual (Rapid Development Framework) to bypass any government restrictions and also allowing
my project to be viewed in the terminal or on web app. The database is up to date with source code, README files, and test files. The user can pick the 
assignment they want, package in into an assignment, and then it is automatically created in GitLab to be cloned for other students to work on. I have also
sorted my code through SOLID principles, which states each directory or file supports a modular component. For example, my tui folder supports the textual
interface I am working with. I have also created scripts that automatically populate information into the database by syncing problems from GitLab and inputing
them into the table. 

### Challenges

The challenges I have had during Milestone 2 were reorganizing my project and building from there. After receiving some guidance that working directly in a 
web app was not going to work because of accessibility issues, I had to pivot. I switched to Textual, which works in the terminal but also has an option to work
on a web app as well. I have not worked in the terminal before this project and I learned a lot when it comes to developing the framework, buttons, and how to 
access the terminal from my program. This challenge was ultimately a positive for me because I ended up learning some HTML as well as working with Textual. After
making this switch and reorganizing my files, I then built out to what it is now.

### Future Directions

My plans for the final submission is to clean up the assignment generation in GitLab. Currently, when the user creates an assignment, its own project is created
and repository. I need some clarification on if that is the way it should be done or another way. Once I get this, I believe everything will come together. Something
else I am looking in to is having generated feedback for students, kind of like a chatbot to speak on what the students did right vs wrong. Lastly, I would like to 
add a feature where the professor can create new problems instead of the ones that are in the database currently. However, I am not 100% sure how to do so yet. Overall,
I am happy with where I am at and looking forward to continue my work!



## Final Submission

### Overview

The overview should be at least a paragraph and describe what your project is about.

### Tutorial

The tutorial should at least be 2 paragraphs long and describe how to get started using the program. For example, if it
is a game then you might want to introduce how to start playing and what the basic controls are. If it is a web
application, you might want to indicate how to navigate the application and interact with different components.

### Installation Instructions

Write instructions here for running your program and any files required to do so as appropriate for your programming
language**. For Python projects, this typically means having a `requirements.txt` file that you create using
`pip freeze > requirements.txt`.

### Citation, Sources, and References

Complete this section to include citations for assets and resources that you used for your project. For example, you could
write this section like in the following example:


[UI-Pack Sci-FI from kenney.nl](https://kenney.nl/assets/ui-pack-sci-fi)

[Digital Audio Pack from kenny.nl](https://kenney.nl/assets/digital-audio)

I created by own ASCII art using the [asciiflow web application](https://asciiflow.com/#/ ) and generative AI.


> [!note]
> Any assets and resources you use need to be verifiable that they are licenced for you to use. If you made your
own assets or used generative AI, you must indicate that you did so. Include a link to any assets that you
downloaded and used. 

> [!important]
> Leaving the "Citation, Sources, and References" section unedited will count as not having completed it.
