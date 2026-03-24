"""Core class skeletons for the PawPal system."""

from datetime import datetime
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

	def mark_task_complete(self, task): #Mark a task as complete using the Task's method
		task.mark_task_complete()
"""Core class skeletons for the PawPal system."""


class Owner:
	def __init__(self, owner_id, name, phone_number, email):
		self.owner_id = owner_id
		self.name = name
		self.phone_number = phone_number
		self.email = email
		self.pets = []

	def add_pet(self, pet):  #Add a pet to the owner's list and set the pet's owner reference
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

	def add_task(self, pet_name, task): #   Add a task to a pet by name and refresh the scheduler's task list
		pet = self.owner.get_pet_by_name(pet_name)
		if pet is None:
			return False
		pet.add_task(task)
		self.refresh_tasks()
		return True

	def remove_task_from_pet(self, pet, task): #Remove a task from a pet and refresh the scheduler's task list
		pet.remove_task(task)
		self.refresh_tasks()

	def mark_task_complete(self, task): #Mark a task as complete using the Task's method
		task.mark_task_complete()
		



	

