from datetime import datetime, date

from pawpal_system import Owner, Pet, Task, Scheduler


def print_todays_schedule(scheduler: Scheduler) -> None:
	today = date.today()
	tasks_by_pet = scheduler.get_tasks_by_pet()
	schedule_items = []

	for pet_name, tasks in tasks_by_pet.items():
		for task in tasks:
			if task.scheduled_time.date() == today:
				schedule_items.append((task.scheduled_time, pet_name, task))

	schedule_items.sort(key=lambda item: item[0])

	print(f"Today's schedule ({today.isoformat()}):")
	if not schedule_items:
		print("No tasks scheduled for today.")
		return

	for scheduled_time, pet_name, task in schedule_items:
		status = "Complete" if task.is_complete else "Pending"
		formatted_time = scheduled_time.strftime("%I:%M %p")
		print(f"- {formatted_time} | {pet_name} | {task.description} ({task.frequency}) [{status}]")


def main() -> None:
	owner = Owner("OWN-001", "Jamie Carter", "555-0101", "jamie@example.com")

	bella = Pet("Bella", "Golden Retriever", "Dog")
	milo = Pet("Milo", "Tabby", "Cat")

	owner.add_pet(bella)
	owner.add_pet(milo)

	scheduler = Scheduler(owner)

	task_1 = Task(
		description="Morning walk",
		scheduled_time=datetime.now().replace(hour=8, minute=0, second=0, microsecond=0),
		frequency="Daily",
	)
	task_2 = Task(
		description="Feed breakfast",
		scheduled_time=datetime.now().replace(hour=9, minute=30, second=0, microsecond=0),
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

	print_todays_schedule(scheduler)


if __name__ == "__main__":
	main()
