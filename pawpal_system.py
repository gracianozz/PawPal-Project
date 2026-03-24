"""Core class skeletons for the PawPal system."""

from dataclasses import dataclass, field


class Owner:
	def __init__(self, owner_id, name, phone_number, email):
		self.owner_id = owner_id
		self.name = name
		self.phone_number = phone_number
		self.email = email
		self.pets = []

	def add_pet(self, pet):
		pass

	def remove_pet(self, pet):
		pass

	def edit_pet(self, pet):
		pass


@dataclass
class Pet:
	name: str
	breed: str
	animal_type: str
	tasks_for_pet: list["Task"] = field(default_factory=list)


@dataclass
class Task:
	task_id: str
	task_name: str
	task_length: int
	task_priority: str

	def edit_task(self):
		pass

	def mark_task_complete(self):
		pass


class Scheduler:
	def __init__(self, date, pet_name, daily_plan, task, status):
		self.date = date
		self.pet_name = pet_name
		self.daily_plan = daily_plan
		self.task = task
		self.status = status
