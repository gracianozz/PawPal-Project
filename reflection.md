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

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
