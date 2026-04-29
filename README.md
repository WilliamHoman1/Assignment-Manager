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

My project is a program that automates the creation of assignments. The audience of the project is for CS professors at
Georgia Highlands College. The project accomplishes the goals of saving time and improving the overall process of assignment
creation. It works by using a database of problems that are then available for the teacher to select from which will be populated
in GitLab for students to then clone. Multiple scripts, functions, methods, and files are spread across the entire program, 
each performing a task to make everything run correctly. As a bonus, I have also added an AI chatbot using Claude's API so that
if the user decides to, the same tasks can be carried out using prompts. The progression of this project has gone from a manual
creation of assignments by the professor, to a few clicks of a button, and now a few prompts. This project has taught me a lot
and I have thoroughly enjoyed creating software that will have an impact.

### Tutorial

To run my program the user needs to be able to install all dependencies and packages. Once this is accomplished, the user will follow 
the instructions below to run the program either on a web app or in the terminal. Once this process is complete, the user then can 
navigate through the program and explore the options that are available to them.

After exploring, the steps to make an assignment are first to click 'view problems' from there, the user is able to browse and click on
which coding problems they would like to include in their assignment. These problems include the source code, test files, and instructions.
Next, if the user likes that problem, they can then click 'add to assignment', this will then add it to the assignment que for review.
The user can repeat the this process until all problems they desire are included in the assignment. Once the assignment is loaded with 
the problems they want, they must add a number to the problem set (assignment). Once this action is completed, they can click build assignment
and this will generate the assignment in their GitLab, ready to send out to students for completion. This process can then be repeated for
different assignments as the semester progress's. 

BONUS: If the user wishes to use the AI chatbot, with Claude. They must enter their own Anthropic API key and once they do this, they will be
able to build assignments and add problems using prompts. Instead of navigating the application, they will be able to do the same process with
a few sentences.

### Installation Instructions

#### Prerequisites
- Python 3.8 or higher (download from https://www.python.org if needed)
- A terminal (Terminal on Mac, Command Prompt or PowerShell on Windows)

---

#### Step 1 - Clone the Repository
Clone the project from GitLab or download it as a zip file and unzip it.

---

#### Step 2 - Navigate to the Project Folder
Open your terminal and navigate to wherever you cloned or downloaded the project.
For example:

   cd ~/Downloads/Project_wazevedo

The folder name may vary depending on where you saved it.

---

#### Step 3 - Install Dependencies
Run the following command to install all required packages:

   pip install -r requirements.txt

    DEPENDECIES INCLUDE:

    anthropic==0.97.0
    python-dotenv==1.2.2
    python_gitlab==8.1.0
    textual==8.2.4
    textual-serve==1.1.3
---

#### Step 4 - Set Up Environment Variables

If you wish to use your own credentials instead, rename .env.example
to .env and fill in your own values:

   - GITLAB_TOKEN: GitLab → Settings → Access Tokens
   - GITLAB_PROJECT_ID: GitLab → Your Project → Settings → General 
   - ANTHROPIC_API_KEY: https://console.anthropic.com

---

#### Step 5 - Run the App

**Option 1 - Terminal**

   python3 main.py

**Option 2 - Web Browser**

   python3 -c "from textual_serve.server import Server; Server('python3 main.py').serve()"

   Then open your browser and go to: http://localhost:8000

`pip freeze > requirements.txt`.

### Citation, Sources, and References

Complete this section to include citations for assets and resources that you used for your project. For example, you could
write this section like in the following example:

- Anthropic. (2026). Claude API Documentation. https://docs.anthropic.com

- GitLab. (2026). GitLab API Documentation. https://docs.gitlab.com/ee/api/

- Textualize. (2026). Textual Documentation. https://textual.textualize.io
