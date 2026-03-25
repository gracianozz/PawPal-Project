"""Core class skeletons for the PawPal system."""

from datetime import datetime, timedelta
from dataclasses import dataclass, field
from typing import Optional


class Owner:
	def __init__(self, owner_id, name, phone_number, email):
		self.owner_id = owner_id
		self.name = name
		self.phone_number = phone_number
		self.email = email
		self.pets = []

	def add_pet(self, pet): #   Add a pet to the owner's list and set the pet's owner reference
		if pet not in self.pets:
			self.pets.append(pet)
		pet.owner = self

	def remove_pet(self, pet): #Remove a pet from the owner's list and clear the pet's owner reference
		if pet in self.pets:
			self.pets.remove(pet)
		if pet.owner is self:
			pet.owner = None

	def edit_pet(self, pet, name=None, breed=None, animal_type=None): #Edit pet details by either pet object or pet name, and return True if successful
		target_pet = pet
		if isinstance(pet, str):
			target_pet = self.get_pet_by_name(pet)

		if target_pet is None or target_pet not in self.pets:
			return False

		if name is not None:
			target_pet.name = name
		if breed is not None:
			target_pet.breed = breed
		if animal_type is not None:
			target_pet.animal_type = animal_type

		return True

	def get_all_pet_tasks(self): #Helper method to gather all tasks from all pets
		all_tasks = []
		for pet in self.pets:
			all_tasks.extend(pet.tasks)
		return all_tasks

	def get_pet_by_name(self, pet_name): #Helper method to find a pet by name
		for pet in self.pets:
			if pet.name == pet_name:
				return pet
		return None

@dataclass
class Pet:
	name: str
	breed: str
	animal_type: str
	tasks: list["Task"] = field(default_factory=list)
	owner: Optional["Owner"] = None

	def add_task(self, task, scheduler=None): #Add a task to the pet and optionally to the scheduler's task list
		if task not in self.tasks:
			self.tasks.append(task)
		if scheduler is not None and task not in scheduler.tasks:
			scheduler.tasks.append(task)

	def remove_task(self, task, scheduler=None): #Remove a task from the pet and optionally from the scheduler's task list
		if task in self.tasks:
			self.tasks.remove(task)
		if scheduler is not None and task in scheduler.tasks:
			scheduler.tasks.remove(task)

@dataclass
class Task:
	description: str
	scheduled_time: datetime
	frequency: str
	is_complete: bool = False
	completed_at: Optional[datetime] = None

	def get_display_time(self): #Return the scheduled time in HH:MM AM/PM format
		return self.scheduled_time.strftime("%I:%M %p")

	def edit_task(self, description=None, scheduled_time=None, frequency=None): #Edit task details
		if description is not None:
			self.description = description
		if scheduled_time is not None:
			self.scheduled_time = scheduled_time
		if frequency is not None:
			self.frequency = frequency

	def mark_task_complete(self): #Mark the task as complete and set the completion timestamp
		self.is_complete = True
		self.completed_at = datetime.now()

	def mark_task_incomplete(self): #Mark the task as incomplete and clear the completion timestamp
		self.is_complete = False
		self.completed_at = None

class Scheduler:
	def __init__(self, owner):  
		self.owner = owner
		self.tasks = self.owner.get_all_pet_tasks()

	def _task_entries(self): #Helper generator to yield (pet, task) pairs for all tasks across all pets, used for conflict detection and other operations that need pet context
		for pet in self.owner.pets:
			for task in pet.tasks:
				yield pet, task

	def _find_pet_for_task(self, task): #Helper method to find which pet a task belongs to by searching through all pets and their tasks
		for pet in self.owner.pets:
			if task in pet.tasks:
				return pet
		return None

	def _get_recurrence_delta(self, frequency): #Convert a frequency string to a timedelta for calculating the next scheduled time
		normalized_frequency = frequency.strip().lower()
		if normalized_frequency == "daily":
			return timedelta(days=1)
		if normalized_frequency == "weekly":
			return timedelta(days=7)
		return None

	def _get_next_scheduled_time(self, task, recurrence_delta):
		next_date = (datetime.now() + recurrence_delta).date()
		return datetime.combine(next_date, task.scheduled_time.time())

	def refresh_tasks(self):  #Refresh the scheduler's task list by gathering all tasks from the owner's pets
		self.tasks = self.owner.get_all_pet_tasks()
		return self.tasks

	def get_tasks_by_pet(self): #Organize tasks by pet name and return a dictionary mapping pet names to their respective task lists
		organized_tasks = {}
		for pet in self.owner.pets:
			organized_tasks[pet.name] = list(pet.tasks)
		return organized_tasks

	def get_pending_tasks(self): #Refresh the task list and return only the pending tasks
		self.refresh_tasks()
		return [task for task in self.tasks if not task.is_complete]

	def get_completed_tasks(self): #Refresh the task list and return only the completed tasks
		self.refresh_tasks()
		return [task for task in self.tasks if task.is_complete]

	def add_task_to_pet(self, pet, task): #Add a task to a pet and refresh the scheduler's task list
		pet.add_task(task)
		self.refresh_tasks()

	def sort_by_completion_status(self): #Return all tasks sorted by completion status, with pending tasks first
		self.refresh_tasks()
		return sorted(self.tasks, key=lambda task: task.is_complete)

	def add_task(self, pet_name, task):  #Add a task to a pet by name and refresh the scheduler's task list
		pet = self.owner.get_pet_by_name(pet_name)
		if pet is None:
			return False
		pet.add_task(task)
		self.refresh_tasks()
		return True

	def remove_task_from_pet(self, pet, task): #Remove a task from a pet and refresh the scheduler's task list
		pet.remove_task(task)
		self.refresh_tasks()

	def sort_tasks_by_time(self): #Return all tasks sorted by their scheduled time
		self.refresh_tasks()
		return sorted(self.tasks, key=lambda task: task.scheduled_time)

	def get_sorted_display_times(self): #Return sorted task times as HH:MM AM/PM strings
		return [task.get_display_time() for task in self.sort_tasks_by_time()]

	def mark_task_complete(self, task): #Mark a task as complete using the Task's method
		if task.is_complete:
			return

		task.mark_task_complete()

		recurrence_delta = self._get_recurrence_delta(task.frequency)
		if recurrence_delta is None:
			return

		pet = self._find_pet_for_task(task)
		if pet is None:
			return

		next_task = Task(
			description=task.description,
			scheduled_time=self._get_next_scheduled_time(task, recurrence_delta),
			frequency=task.frequency,
		)
		pet.add_task(next_task)
		self.refresh_tasks()

	def mark_task_incomplete(self, task): #Mark a task as incomplete using the Task's method
		task.mark_task_incomplete()

	def detect_task_conflicts(self):
		"""Return warning messages for tasks that overlap at the exact same time."""
		time_slots = {}

		for pet, task in self._task_entries():
			time_slots.setdefault(task.scheduled_time, []).append((pet, task))

		warnings = []
		for scheduled_time, entries in sorted(time_slots.items(), key=lambda item: item[0]):
			if len(entries) < 2:
				continue

			pet_names = {pet.name for pet, _ in entries}
			task_descriptions = [task.description for _, task in entries]
			formatted_time = scheduled_time.strftime("%Y-%m-%d %I:%M %p")

			if len(pet_names) == 1:
				pet_name = next(iter(pet_names))
				warnings.append(
					f"Warning: {pet_name} has overlapping tasks at {formatted_time}: {', '.join(task_descriptions)}"
				)
			else:
				warnings.append(
					f"Warning: Multiple pets have tasks at {formatted_time}: {', '.join(sorted(pet_names))}"
				)

		return warnings

