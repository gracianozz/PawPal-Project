import streamlit as st
from datetime import datetime
from pawpal_system import Owner, Pet, Task 


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
st.caption("Add a few tasks. In your final version, these should feed into your scheduler.")

col1, col2, col3, col4 = st.columns(4)
with col1:
    task_title = st.text_input("Task title", value="Morning walk")
with col2:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
with col3:
    priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)
with col4:
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
            selected_pet.add_task(
                Task(
                    description=task_description,
                    scheduled_time=datetime.now(),
                    frequency=priority,
                )
            )
            st.success(f"Task added to {selected_pet.name}.")

if st.session_state.owner is not None:
    all_tasks = st.session_state.owner.get_all_pet_tasks()
else:
    all_tasks = []

if all_tasks:
    st.write("Current tasks:")
    task_rows = []
    for pet in st.session_state.owner.pets:
        for task in pet.tasks:
            task_rows.append(
                {
                    "pet": pet.name,
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
st.caption("This button should call your scheduling logic once you implement it.")

if st.button("Generate schedule"):
    st.warning(
        "Not implemented yet. Next step: create your scheduling logic (classes/functions) and call it here."
    )
    st.markdown(
        """
Suggested approach:
1. Design your UML (draft).
2. Create class stubs (no logic).
3. Implement scheduling behavior.
4. Connect your scheduler here and display results.
"""
    )
