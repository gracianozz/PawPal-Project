from datetime import datetime, date

from pawpal_system import Owner, Pet, Task, Scheduler


def print_todays_schedule(scheduler: Scheduler) -> None:
	today = date.today()
	tasks_by_pet = scheduler.get_tasks_by_pet()
	pet_name_by_task_id = {}
	schedule_items = []

	for pet_name, tasks in tasks_by_pet.items():
		for task in tasks:
			pet_name_by_task_id[id(task)] = pet_name

	for task in scheduler.sort_tasks_by_time():
		if task.scheduled_time.date() == today:
			pet_name = pet_name_by_task_id.get(id(task), "Unknown Pet")
			schedule_items.append((pet_name, task))


	print(f"Today's schedule ({today.isoformat()}):")
	if not schedule_items:
		print("No tasks scheduled for today.")
		return

	for pet_name, task in schedule_items:
		status = "Complete" if task.is_complete else "Pending"
		formatted_time = task.get_display_time()
		print(f"- {formatted_time} | {pet_name} | {task.description} ({task.frequency}) [{status}]")


def print_schedule_conflict_warnings(scheduler: Scheduler) -> None:
	warnings = scheduler.detect_task_conflicts()
	if not warnings:
		return

	print("Schedule warnings:")
	for warning in warnings:
		print(f"- {warning}")


def print_tasks_by_completion_status(scheduler: Scheduler) -> None:
	print("Tasks by completion status:")
	for task in scheduler.sort_by_completion_status():
		status = "Complete" if task.is_complete else "Pending"
		print(f"- {task.get_display_time()} | {task.description} [{status}]")


def main() -> None:
	owner = Owner("OWN-001", "Jamie Carter", "555-0101", "jamie@example.com")

	bella = Pet("Bella", "Golden Retriever", "Dog")
	milo = Pet("Milo", "Tabby", "Cat")

	owner.add_pet(bella)
	owner.add_pet(milo)

	scheduler = Scheduler(owner)

	task_1 = Task(
		description="Morning walk",
		scheduled_time=datetime.now().replace(hour=10, minute=0, second=0, microsecond=0),
		frequency="Daily",
	)
	task_2 = Task(
		description="Feed breakfast",
		scheduled_time=datetime.now().replace(hour=10, minute=0, second=0, microsecond=0),
		frequency="Daily",
	)
	task_3 = Task(
		description="Evening playtime",
		scheduled_time=datetime.now().replace(hour=18, minute=15, second=0, microsecond=0),
		frequency="Daily",
	)

	scheduler.add_task_to_pet(bella, task_1)
	scheduler.add_task_to_pet(milo, task_2)
	scheduler.add_task_to_pet(bella, task_3)

	scheduler.mark_task_complete(task_2)

	print_schedule_conflict_warnings(scheduler)

	print_todays_schedule(scheduler)
	print_tasks_by_completion_status(scheduler)

 
if __name__ == "__main__":
	main()
