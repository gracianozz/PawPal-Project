import pytest
from datetime import datetime
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
