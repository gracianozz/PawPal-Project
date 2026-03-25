import pytest
from datetime import datetime, timedelta
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from pawpal_system import Owner, Pet, Task, Scheduler


class TestTaskCompletion:
    """Test suite for task completion functionality."""

    def test_mark_task_complete_changes_status(self):
        """Verify that calling mark_task_complete() changes the task's is_complete status to True."""
        task = Task(
            description="Feed the dog",
            scheduled_time=datetime.now(),
            frequency="Daily"
        )
        
        assert task.is_complete is False, "Task should start as incomplete"
        assert task.completed_at is None, "Task should have no completion timestamp initially"
        
        task.mark_task_complete()
        
        assert task.is_complete is True, "Task should be marked as complete"
        assert task.completed_at is not None, "Task should have a completion timestamp"
        assert isinstance(task.completed_at, datetime), "Completion timestamp should be a datetime object"

    def test_mark_task_incomplete_reverts_status(self):
        """Verify that marking a task incomplete reverts the completion state."""
        task = Task(
            description="Morning exercise",
            scheduled_time=datetime.now(),
            frequency="Daily"
        )
        
        task.mark_task_complete()
        assert task.is_complete is True
        
        task.mark_task_incomplete()
        assert task.is_complete is False, "Task should be marked as incomplete"
        assert task.completed_at is None, "Completion timestamp should be cleared"


class TestPetTaskManagement:
    """Test suite for pet task management."""

    def test_add_task_to_pet_increases_count(self):
        """Verify that adding a task to a pet increases that pet's task count."""
        pet = Pet(
            name="Buddy",
            breed="Golden Retriever",
            animal_type="Dog"
        )
        
        initial_count = len(pet.tasks)
        assert initial_count == 0, "Pet should start with no tasks"
        
        task1 = Task(
            description="Walking",
            scheduled_time=datetime.now(),
            frequency="Twice Daily"
        )
        pet.add_task(task1)
        
        assert len(pet.tasks) == initial_count + 1, "Pet task count should increase by 1"
        assert task1 in pet.tasks, "Task should be in pet's task list"

    def test_add_multiple_tasks_to_pet(self):
        """Verify that adding multiple tasks to a pet increases count correctly."""
        pet = Pet(
            name="Whiskers",
            breed="Siamese",
            animal_type="Cat"
        )
        
        tasks = [
            Task("Feed", datetime.now(), "Daily"),
            Task("Play", datetime.now(), "Daily"),
            Task("Groom", datetime.now(), "Weekly")
        ]
        
        for task in tasks:
            pet.add_task(task)
        
        assert len(pet.tasks) == 3, "Pet should have 3 tasks"
        for task in tasks:
            assert task in pet.tasks, f"Task '{task.description}' should be in pet's task list"

    def test_add_duplicate_task_does_not_increase_count(self):
        """Verify that adding the same task twice only increases count by 1."""
        pet = Pet(
            name="Max",
            breed="Labrador",
            animal_type="Dog"
        )
        
        task = Task(
            description="Exercise",
            scheduled_time=datetime.now(),
            frequency="Daily"
        )
        
        pet.add_task(task)
        initial_count = len(pet.tasks)
        
        pet.add_task(task)
        
        assert len(pet.tasks) == initial_count, "Adding duplicate task should not increase count"

    def test_remove_task_from_pet_decreases_count(self):
        """Verify that removing a task from a pet decreases task count."""
        pet = Pet(
            name="Luna",
            breed="Husky",
            animal_type="Dog"
        )
        
        task = Task(
            description="Training",
            scheduled_time=datetime.now(),
            frequency="Daily"
        )
        
        pet.add_task(task)
        assert len(pet.tasks) == 1
        
        pet.remove_task(task)
        
        assert len(pet.tasks) == 0, "Task count should decrease after removal"
        assert task not in pet.tasks, "Task should no longer be in pet's task list"


class TestOwnerPetTaskIntegration:
    """Test suite for owner-pet task integration."""

    def test_owner_get_all_pet_tasks(self):
        """Verify that owner can retrieve all tasks from all their pets."""
        owner = Owner("OWN-001", "Alice", "555-1234", "alice@example.com")
        
        bella = Pet("Bella", "Golden Retriever", "Dog")
        milo = Pet("Milo", "Tabby", "Cat")
        
        owner.add_pet(bella)
        owner.add_pet(milo)
        
        task1 = Task("Walk", datetime.now(), "Daily")
        task2 = Task("Feed", datetime.now(), "Daily")
        task3 = Task("Play", datetime.now(), "Daily")
        
        bella.add_task(task1)
        bella.add_task(task2)
        milo.add_task(task3)
        
        all_tasks = owner.get_all_pet_tasks()
        
        assert len(all_tasks) == 3, "Owner should have access to all 3 tasks"
        assert task1 in all_tasks
        assert task2 in all_tasks
        assert task3 in all_tasks

    def test_scheduler_retrieves_tasks_by_pet(self):
        """Verify that scheduler correctly organizes tasks by pet."""
        owner = Owner("OWN-002", "Bob", "555-5678", "bob@example.com")
        
        max_dog = Pet("Max", "German Shepherd", "Dog")
        luna_cat = Pet("Luna", "Persian", "Cat")
        
        owner.add_pet(max_dog)
        owner.add_pet(luna_cat)
        
        max_task1 = Task("Running", datetime.now(), "Daily")
        max_task2 = Task("Training", datetime.now(), "Weekly")
        luna_task1 = Task("Brushing", datetime.now(), "Weekly")
        
        max_dog.add_task(max_task1)
        max_dog.add_task(max_task2)
        luna_cat.add_task(luna_task1)
        
        scheduler = Scheduler(owner)
        tasks_by_pet = scheduler.get_tasks_by_pet()
        
        assert "Max" in tasks_by_pet
        assert "Luna" in tasks_by_pet
        assert len(tasks_by_pet["Max"]) == 2
        assert len(tasks_by_pet["Luna"]) == 1


class TestTaskRecurrence:
    """Test suite for automatic recurrence generation."""

    def test_mark_daily_task_complete_creates_next_occurrence(self):
        owner = Owner("OWN-003", "Cara", "555-9999", "cara@example.com")
        pet = Pet("Nova", "Beagle", "Dog")
        owner.add_pet(pet)

        scheduled_time = datetime(2026, 3, 24, 8, 0)
        daily_task = Task("Morning walk", scheduled_time, "Daily")
        pet.add_task(daily_task)

        scheduler = Scheduler(owner)
        scheduler.mark_task_complete(daily_task)

        assert daily_task.is_complete is True
        assert len(pet.tasks) == 2

        next_task = [task for task in pet.tasks if task is not daily_task][0]
        assert next_task.description == daily_task.description
        assert next_task.frequency == daily_task.frequency
        expected_next_date = (datetime.now() + timedelta(days=1)).date()
        assert next_task.scheduled_time.date() == expected_next_date
        assert next_task.scheduled_time.time() == scheduled_time.time()
        assert next_task.is_complete is False

    def test_mark_weekly_task_complete_creates_next_occurrence(self):
        owner = Owner("OWN-004", "Drew", "555-1111", "drew@example.com")
        pet = Pet("Pip", "Maine Coon", "Cat")
        owner.add_pet(pet)

        scheduled_time = datetime(2026, 3, 24, 18, 30)
        weekly_task = Task("Litter deep clean", scheduled_time, "Weekly")
        pet.add_task(weekly_task)

        scheduler = Scheduler(owner)
        scheduler.mark_task_complete(weekly_task)

        assert len(pet.tasks) == 2
        next_task = [task for task in pet.tasks if task is not weekly_task][0]
        expected_next_date = (datetime.now() + timedelta(days=7)).date()
        assert next_task.scheduled_time.date() == expected_next_date
        assert next_task.scheduled_time.time() == scheduled_time.time()

    def test_mark_non_recurring_task_complete_does_not_create_new_task(self):
        owner = Owner("OWN-005", "Evan", "555-2222", "evan@example.com")
        pet = Pet("Skye", "Mix", "Dog")
        owner.add_pet(pet)

        one_time_task = Task("Vet appointment", datetime(2026, 3, 24, 14, 0), "Once")
        pet.add_task(one_time_task)

        scheduler = Scheduler(owner)
        scheduler.mark_task_complete(one_time_task)

        assert one_time_task.is_complete is True
        assert len(pet.tasks) == 1

    def test_mark_already_completed_task_does_not_duplicate_next_occurrence(self):
        owner = Owner("OWN-006", "Fran", "555-3333", "fran@example.com")
        pet = Pet("Echo", "Spaniel", "Dog")
        owner.add_pet(pet)

        daily_task = Task("Evening walk", datetime(2026, 3, 24, 19, 0), "Daily")
        pet.add_task(daily_task)

        scheduler = Scheduler(owner)
        scheduler.mark_task_complete(daily_task)
        scheduler.mark_task_complete(daily_task)

        assert len(pet.tasks) == 2


class TestTaskConflictDetection:
    """Test suite for lightweight schedule conflict detection."""

    def test_detects_overlapping_tasks_for_same_pet(self):
        owner = Owner("OWN-007", "Gina", "555-4444", "gina@example.com")
        pet = Pet("Blue", "Poodle", "Dog")
        owner.add_pet(pet)

        conflict_time = datetime(2026, 3, 24, 9, 0)
        pet.add_task(Task("Feed", conflict_time, "Daily"))
        pet.add_task(Task("Walk", conflict_time, "Daily"))

        scheduler = Scheduler(owner)
        warnings = scheduler.detect_task_conflicts()

        assert len(warnings) == 1
        assert "Blue has overlapping tasks" in warnings[0]
        assert "Feed" in warnings[0]
        assert "Walk" in warnings[0]

    def test_detects_overlapping_tasks_for_different_pets(self):
        owner = Owner("OWN-008", "Hank", "555-5555", "hank@example.com")
        pet_one = Pet("Nala", "Shiba", "Dog")
        pet_two = Pet("Mochi", "Bengal", "Cat")
        owner.add_pet(pet_one)
        owner.add_pet(pet_two)

        conflict_time = datetime(2026, 3, 24, 10, 30)
        pet_one.add_task(Task("Nala breakfast", conflict_time, "Daily"))
        pet_two.add_task(Task("Mochi breakfast", conflict_time, "Daily"))

        scheduler = Scheduler(owner)
        warnings = scheduler.detect_task_conflicts()

        assert len(warnings) == 1
        assert "Multiple pets have tasks" in warnings[0]
        assert "Mochi" in warnings[0]
        assert "Nala" in warnings[0]

    def test_returns_no_warnings_when_no_overlap_exists(self):
        owner = Owner("OWN-009", "Ivy", "555-6666", "ivy@example.com")
        pet = Pet("Rex", "Mixed", "Dog")
        owner.add_pet(pet)

        pet.add_task(Task("Morning feed", datetime(2026, 3, 24, 8, 0), "Daily"))
        pet.add_task(Task("Evening walk", datetime(2026, 3, 24, 18, 0), "Daily"))

        scheduler = Scheduler(owner)
        warnings = scheduler.detect_task_conflicts()

        assert warnings == []
