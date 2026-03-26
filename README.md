# Sample Photos of Functionality 
-   Choose Problems --> Review Problem--> Bundle --> Create Assignment --> GitLab Project Created
-   Detailed information below.

Home Page
<img width="1512" height="866" alt="Screenshot 2026-03-25 at 9 00 35 PM" src="https://github.com/user-attachments/assets/0159a447-e7ea-4672-8545-c1a5c6dac73c" />
View Problems
<img width="1512" height="869" alt="Screenshot 2026-03-25 at 9 07 45 PM" src="https://github.com/user-attachments/assets/0eee1b38-d70d-4670-99cd-f7416088a42e" />
Review Problem Content
<img width="1512" height="865" alt="Screenshot 2026-03-25 at 9 08 05 PM" src="https://github.com/user-attachments/assets/106b6246-ebc3-4cf1-b88c-4b69b161c655" />
Add to assignment
<img width="1512" height="862" alt="Screenshot 2026-03-25 at 9 09 13 PM" src="https://github.com/user-attachments/assets/3970c23c-4620-40fd-a540-bf7f80f099c8" />
ALTERNATIVE - AI Chat BOT (Prompt)
<img width="1512" height="863" alt="Screenshot 2026-03-25 at 9 09 43 PM" src="https://github.com/user-attachments/assets/7bf28346-9d59-443c-92d1-3c5e51be3ebd" />
Problems Added
<img width="1512" height="866" alt="Screenshot 2026-03-25 at 9 09 59 PM" src="https://github.com/user-attachments/assets/e0e8fbfd-0646-4e37-b0f7-f9f6a244caca" />
Create assignment prompt
<img width="1512" height="867" alt="Screenshot 2026-03-25 at 9 10 22 PM" src="https://github.com/user-attachments/assets/e84fdefe-e102-4a1b-b859-c62b1d5a7bdd" />
Review or Publish
<img width="1512" height="871" alt="Screenshot 2026-03-25 at 9 12 12 PM" src="https://github.com/user-attachments/assets/0781a20f-4594-43ec-8dc7-1be123f75ef4" />
Built
<img width="1512" height="868" alt="Screenshot 2026-03-25 at 9 16 09 PM" src="https://github.com/user-attachments/assets/81b0335e-7543-4cdb-82fa-66c716a694e9" />
Assignment in GitLab
<img width="1512" height="866" alt="Screenshot 2026-03-25 at 9 16 40 PM" src="https://github.com/user-attachments/assets/64899442-f176-42ec-8504-bfbb779b72cb" />




# Current Progress
Added Claude AI by calling its API into my program, manager now has AI builder as well. The fundamentals are the user picks and matchs problems to bundle into an assignment. Upon user choice, the assignments are sent to gitlab in their own project with repositories. These are then available and ready for students to clone to complete and commit back to GitLab.

-    Claude API Called
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

Update this section to describe your project for milestone 2 and complete the following sections. If your project is
using assets, be sure to keep the citations, sources, and resources section updated.

### Current Progress

Update this section to describe the current progress of your project.

### Challenges

Update this section to describe the challenges for your project at this stage.

### Future Directions

What are your plans for the final submission?



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
