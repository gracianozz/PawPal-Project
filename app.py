import streamlit as st
from datetime import datetime
from pawpal_system import Owner, Pet, Task, Scheduler


st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")


if "owner" not in st.session_state:
    st.session_state.owner = None
if "owner_name" not in st.session_state:
    st.session_state.owner_name = ""

with st.form("owner_form"):
    typed_name = st.text_input("Owner name", value=st.session_state.owner_name)
    save_clicked = st.form_submit_button("Save owner")

if save_clicked:
    clean_name = typed_name.strip()
    if clean_name:
        st.session_state.owner_name = clean_name
        if st.session_state.owner is None:
            st.session_state.owner = Owner("OWN-001", clean_name, "", "")
        else:
            st.session_state.owner.name = clean_name
        st.success("Owner saved in session.")
    else:
        st.warning("Please enter a name.")

if st.session_state.owner is not None:
    st.write(f"Current owner: {st.session_state.owner.name}")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

st.subheader("Quick Demo Inputs (UI only)")

st.markdown("Adding a Pet")
col_pet_1, col_pet_2, col_pet_3 = st.columns(3)
with col_pet_1:
    pet_name = st.text_input("Pet name", value="Mochi")
with col_pet_2:
    breed = st.text_input("Breed", value="Mixed")
with col_pet_3:
    species = st.selectbox("Species", ["dog", "cat", "other"])

if st.button("Add pet"):
    if st.session_state.owner is None:
        st.warning("Save an owner first.")
    else:
        clean_pet_name = pet_name.strip()
        if not clean_pet_name:
            st.warning("Please enter a pet name.")
        else:
            existing_pet = st.session_state.owner.get_pet_by_name(clean_pet_name)
            if existing_pet is not None:
                st.info("That pet already exists for this owner.")
            else:
                st.session_state.owner.add_pet(
                    Pet(name=clean_pet_name, breed=breed.strip() or "Unknown", animal_type=species)
                )
                st.success("Pet added and stored in session.")

if st.session_state.owner is not None and st.session_state.owner.pets:
    st.write("Current pets:")
    st.table(
        [
            {"name": p.name, "breed": p.breed, "species": p.animal_type}
            for p in st.session_state.owner.pets
        ]
    )
elif st.session_state.owner is not None:
    st.info("No pets yet. Add one above.")

st.markdown("### Tasks")
st.caption("Add a few tasks with a selected time. In your final version, these should feed into your scheduler.")

col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    task_title = st.text_input("Task title", value="Morning walk")
with col2:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
with col3:
    priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)
with col4:
    task_time = st.time_input("Task time", value=datetime.now().replace(second=0, microsecond=0).time())
with col5:
    pet_options = [pet.name for pet in st.session_state.owner.pets] if st.session_state.owner else []
    selected_pet_name = st.selectbox("Pet", pet_options, disabled=not pet_options)

if st.button("Add task"):
    if st.session_state.owner is None:
        st.warning("Save an owner first.")
    elif not pet_options:
        st.warning("Add a pet first.")
    else:
        selected_pet = st.session_state.owner.get_pet_by_name(selected_pet_name)
        clean_task_title = task_title.strip()
        if selected_pet is None:
            st.warning("Select a valid pet.")
        elif not clean_task_title:
            st.warning("Please enter a task title.")
        else:
            task_description = f"{clean_task_title} ({int(duration)} min, {priority})"
            scheduled_datetime = datetime.combine(datetime.now().date(), task_time)
            selected_pet.add_task(
                Task(
                    description=task_description,
                    scheduled_time=scheduled_datetime,
                    frequency=priority,
                )
            )
            st.success(f"Task added to {selected_pet.name}.")

if st.session_state.owner is not None:
    all_tasks = st.session_state.owner.get_all_pet_tasks()
    scheduler = Scheduler(st.session_state.owner)
else:
    all_tasks = []
    scheduler = None

if all_tasks:
    conflict_warnings = scheduler.detect_task_conflicts() if scheduler is not None else []
    if conflict_warnings:
        st.warning("Schedule conflict warnings:")
        for warning in conflict_warnings:
            st.write(f"- {warning}")

    tasks_by_pet = scheduler.get_tasks_by_pet() if scheduler is not None else {}
    pet_name_by_task_id = {}
    for pet_name, pet_tasks in tasks_by_pet.items():
        for task in pet_tasks:
            pet_name_by_task_id[id(task)] = pet_name

    st.write("Current tasks:")
    task_rows = []
    for task in scheduler.sort_tasks_by_time():
        task_rows.append(
            {
                "pet": pet_name_by_task_id.get(id(task), "Unknown Pet"),
                "scheduled_time": task.get_display_time(),
                "description": task.description,
                "frequency": task.frequency,
                "complete": task.is_complete,
            }
        )
    st.table(task_rows)
else:
    st.info("No tasks yet. Add one above.")

st.divider()

st.subheader("Build Schedule")
st.caption("Generate a sorted schedule and view any conflict warnings.")

if st.button("Generate schedule"):
    if scheduler is None:
        st.warning("Save an owner first.")
    elif not scheduler.tasks:
        st.info("No tasks available to schedule.")
    else:
        st.success("Schedule generated.")

        schedule_rows = []
        tasks_by_pet = scheduler.get_tasks_by_pet()
        pet_name_by_task_id = {}
        for pet_name, pet_tasks in tasks_by_pet.items():
            for task in pet_tasks:
                pet_name_by_task_id[id(task)] = pet_name

        for task in scheduler.sort_tasks_by_time():
            schedule_rows.append(
                {
                    "time": task.get_display_time(),
                    "pet": pet_name_by_task_id.get(id(task), "Unknown Pet"),
                    "task": task.description,
                    "status": "Complete" if task.is_complete else "Pending",
                }
            )
        st.table(schedule_rows)

        conflict_warnings = scheduler.detect_task_conflicts()
        if conflict_warnings:
            st.warning("Conflict warnings:")
            for warning in conflict_warnings:
                st.write(f"- {warning}")
        else:
            st.info("No schedule conflicts detected.")
