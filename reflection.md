# PawPal+ Project Reflection

## 1. System Design

- Three core actions a user should be able to perform with this application are:
- Add Pets
- Add tasks for pets
- Display all tasks added

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?


- The classes chosen I chose are the Owner,Pet,Task, and Scheduler classes.
- Each class stores and represents different information:
- The owner class stores basic owner information, such as name, phone number, email, and list of pets owned.
- The pet class stores pet information, like pet name, breed, animal type, and tasks related to the pet.
- The task class stores task information, like the task name, duration, and priority.
- The Scheduler class will create and store a whole schedule with information like date, name, the daily plan, the task for the time, and the status(where the task is marked as complete or not).

- Some responsibilities are that the owner can add, remove, or edit information about a pet. The task class can add, remove, and edit information about a task inputted.

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

- Yes, my design did change during implementation. One change that occured during implementation is ensuring the logic of marking a task complete will ensure to update the status, since copilot noticed that there should be a is_complete bool to ensure. Now, the system will check that a task is correctly marked as complete or not.


---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

- One tradeoff my scheduler makes when sorting tasks on time is ensuring that no tasks with the same timestamp are inserted. The method in scheduler compares and checks the timestamp of the task inserted with the tasks already in the system, and then sends a warning according to time overlapping. This tradeoff is reasonable for this scenerio because since we are building a schedule, it would be unreasonable for two tasks in a schedule to overlap, since it should represent a routine that should smoothly be followed.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?

- I used AI to brainstorm the possible attributes and methods that can be part of my 4 classes. I first made my 4 classes by myself, then asked copilot if my classes with their attributes and methods made sense, and if not to explain and give me possible alternatives to what I was looking for.


- What kinds of prompts or questions were most helpful?
- The questions that were most helpful were on how to implement the algorithms so that they actually interact with the UI. Copilot explained everything well and displayed how the classes and their methods were called to work together to make the whole system functional.


**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.

- One moment where I did not accept an AI suggestion as-is was when it was trying to add more unecessary methods than agreed upon. It was adding methods to display "upcoming" and "overdue" methods, but since those were already covered with the completion status, I rejected them.

- How did you evaluate or verify what the AI suggested?
- I evaluted and verified what the AI suggested by asking it to clarify on what it meant on specific parts of suggestions. This helped me more understand what the AI was really suggesting, and to see If i could implement it myself in any way towards the program.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?
- Some important behaviors that I tested were ensuring no overlapping classes and proper chronological order of tasks. These tasks are important because they bring the idea together on what a schedule should really look like. When someone thinks of a schedule, they would imagine a routine that is followed with times to now which task is next.

**b. Confidence**

- How confident are you that your scheduler works correctly?
- I am somewhat confident that my scheduler works correctly. There were times where I got confused on the requirements, and "spiraled" into adding unecessary attributes or extra information. Working with AI is new to me, so this would be one of my first app projects I have implemented with AI. I followed to the best of my ability. I definitely feel like there are still some minor bugs and tweaks that could be found and fixed to make the app more functional.


- What edge cases would you test next if you had more time?
- An edge case that I would test next If more time was available would be checking to see if proper times fit in the actual schedule. For example: if a task is scheduled at 4:30 and takes 20 minutes, another task cannot be scheduled within that time. The program only checks for scheduling in the SAME time ,but not the actual time it takes a task to be done.

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?
- The part of this project that Im most satisfied with is getting to work with AI and building one of my first apps using AI! It was a very challenging experience, getting familiar with all the setup, and overall understanding what the AI was suggesting, but experience was definitely gained. Overall the project works with functionalities and logic, and i'd say thats a win!

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?
- Something I would redesign would be how the UI towards inputting tasks is. Things like typing out the time would be definitely more convenient when trying to insert a task for a pet. Scrolling through a drop down menu can be more time consuming.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?

- One important thing I learned about desigining systems or working with AI on this project is to always stay in control. I mean this by double checking what AI is adding or suggeting, and see if theres any errors or mistakes behind it, and not just accepting it blatantly. Working more with AI, I personally notices AI also tries to add unecessary attributes or information that you did not ask for, and that would just make your code more complicated, so it is definitely something to watch out for. 