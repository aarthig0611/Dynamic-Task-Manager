import pandas as pd
from datetime import datetime
from skip_list import SkipList
from fibonacci_heap import FibonacciHeap
import timeit
import random

class Task:
    def __init__(self, name, priority, due_date, status='Incomplete'):
        """
        Initialize a task with a name, priority, due date, and status.
        :param name: The name of the task.
        :param priority: The priority of the task.
        :param due_date: The due date of the task.
        :param status: The status of the task (default is 'Incomplete').
        """
        self.name = name
        self.priority = priority
        self.due_date = due_date
        self.status = status

    def __lt__(self, other):
        """
        Compare tasks based on priority for sorting purposes.
        :param other: The other task to compare with.
        :return: True if this task's priority is less than the other task's priority.
        """
        return self.priority < other.priority

class TaskManager:
    def __init__(self, excel_file='tasks.xlsx'):
        """
        Initialize the Task Manager with a Skip List and Fibonacci Heap.
        :param excel_file: Path to the Excel file to load/save tasks.
        """
        self.skip_list = SkipList(max_level=16)
        self.fib_heap = FibonacciHeap()
        self.excel_file = excel_file
        self._load_tasks_from_excel()

    def _load_tasks_from_excel(self):
        """
        Load tasks from the Excel file into the Skip List and Fibonacci Heap.
        """
        try:
            df = pd.read_excel(self.excel_file)
            for _, row in df.iterrows():
                task = Task(row['name'], row['priority'], row['due_date'], row['status'])
                self.add_task(task, save=False)
        except FileNotFoundError:
            pass

    def _save_tasks_to_excel(self):
        """
        Save all tasks from the Skip List to the Excel file.
        """
        tasks = []
        current = self.skip_list.header.forward[0]
        while current:
            task = current.value
            tasks.append({
                'name': task.name,
                'priority': task.priority,
                'due_date': task.due_date,
                'status': task.status
            })
            current = current.forward[0]
        df = pd.DataFrame(tasks)
        df.to_excel(self.excel_file, index=False)

    def add_task(self, task, save=True):
        """
        Add a new task to the Skip List and Fibonacci Heap.
        :param task: The task to add.
        :param save: Whether to save the tasks to the Excel file (default is True).
        """
        existing_task = self.skip_list.search(task.name)
        if existing_task:
            print(f"Task with name '{task.name}' already exists.")
            if existing_task.due_date == task.due_date:
                response = input("A task with the same details already exists. Do you want to add this task anyway? (yes/no): ")
                if response.lower() != 'yes':
                    print("Task not added.")
                    return

        self.skip_list.insert(task.name, task)
        self.fib_heap.insert(task.priority, task)
        if save:
            self._save_tasks_to_excel()

    def remove_task(self, task_name):
        """
        Remove a task by name from the Skip List and rebuild the Fibonacci Heap.
        :param task_name: The name of the task to remove.
        """
        task = self.skip_list.search(task_name)
        if task:
            self.skip_list.delete(task_name)
            self._rebuild_heap()
            self._save_tasks_to_excel()

    def _rebuild_heap(self):
        """
        Rebuild the Fibonacci Heap from the tasks in the Skip List.
        """
        tasks = []
        current = self.skip_list.header.forward[0]
        while current:
            tasks.append(current.value)
            current = current.forward[0]
        self.fib_heap = FibonacciHeap()
        for task in tasks:
            self.fib_heap.insert(task.priority, task)

    def get_next_task(self):
        """
        Get the next incomplete task with the highest priority.
        :return: The next incomplete task with the highest priority.
        """
        incomplete_tasks = [node.value for node in self._iterate_list(self.fib_heap.min_node) if node.value.status == 'Incomplete']
        if incomplete_tasks:
            return min(incomplete_tasks, key=lambda t: t.priority)
        return None

    def complete_next_task(self):
        """
        Complete the next task by extracting it from the Fibonacci Heap and removing it from the Skip List.
        :return: The completed task.
        """
        min_node = self.fib_heap.extract_min()
        if min_node:
            self.skip_list.delete(min_node.value.name)
            self._save_tasks_to_excel()
            return min_node.value
        return None

    def sort_tasks_by_due_date(self):
        """
        Get all incomplete tasks sorted by due date.
        :return: List of incomplete tasks sorted by due date.
        """
        tasks = self._get_incomplete_tasks()
        tasks.sort(key=lambda x: datetime.strptime(x.due_date, '%Y-%m-%d'))
        return tasks

    def sort_tasks_by_priority(self):
        """
        Get all incomplete tasks sorted by priority.
        :return: List of incomplete tasks sorted by priority.
        """
        tasks = self._get_incomplete_tasks()
        tasks.sort(key=lambda x: x.priority)
        return tasks

    def update_task(self, task_name, **updates):
        """
        Update the details of an existing task.
        :param task_name: The name of the task to update.
        :param updates: Dictionary of fields to update.
        """
        task = self.skip_list.search(task_name)
        if task:
            if 'priority' in updates:
                task.priority = updates['priority']
            if 'due_date' in updates:
                task.due_date = updates['due_date']
            if 'status' in updates:
                task.status = updates['status']
            self._rebuild_heap()
            self._save_tasks_to_excel()
        else:
            print(f"Task {task_name} not found.")

    def _get_incomplete_tasks(self):
        """
        Get a list of all incomplete tasks.
        :return: List of incomplete tasks.
        """
        tasks = []
        current = self.skip_list.header.forward[0]
        while current:
            task = current.value
            if task.status != 'Complete':
                tasks.append(task)
            current = current.forward[0]
        return tasks

    def _iterate_list(self, head):
        """
        Iterate through a circular list starting from the head node.
        :param head: The head node of the list.
        :yield: Each node in the list.
        """
        node = head
        while node:
            yield node
            node = node.right
            if node == head:
                break

    def display_menu(self):
        print("\nTask Manager")
        print("1. Add Task")
        print("2. Update Task")
        print("3. Remove Task")
        print("4. View Next Task")
        print("5. View Tasks Sorted by Due Date")
        print("6. View Tasks Sorted by Priority")
        print("7. Exit")
        return input("Select an option: ")
    
    def user_interface(self):
        """
        Main user interface for interacting with the Task Manager.
        """
        while True:
            choice = self.display_menu()
            
            if choice == '1':
                name = input("Enter task name: ")
                priority = int(input("Enter task priority (lower number = higher priority): "))
                due_date = input("Enter task due date (YYYY-MM-DD): ")
                task = Task(name, priority, due_date)
                self.add_task(task)
                print(f"Task '{name}' added successfully.")
            
            elif choice == '2':
                name = input("Enter the name of the task to update: ")
                print("Leave blank to skip an update for that field.")
                priority = input("Enter new priority (press Enter to skip): ")
                due_date = input("Enter new due date (YYYY-MM-DD) (press Enter to skip): ")
                status = input("Enter new status (Complete/Incomplete) (press Enter to skip): ")
                updates = {}
                if priority:
                    updates['priority'] = int(priority)
                if due_date:
                    updates['due_date'] = due_date
                if status:
                    updates['status'] = status
                self.update_task(name, **updates)
                print(f"Task '{name}' updated successfully.")
            
            elif choice == '3':
                name = input("Enter the name of the task to remove: ")
                self.remove_task(name)
                print(f"Task '{name}' removed successfully.")
            
            elif choice == '4':
                next_task = self.get_next_task()
                if next_task:
                    print(f"Next task to do: {next_task.name}")
                else:
                    print("No incomplete tasks available.")
            
            elif choice == '5':
                print("Tasks sorted by due date:")
                for task in self.sort_tasks_by_due_date():
                    print(f"{task.name} - {task.due_date}")
            
            elif choice == '6':
                print("Tasks sorted by priority:")
                for task in self.sort_tasks_by_priority():
                    print(f"{task.name} - {task.priority}")
            
            elif choice == '7':
                print("Exiting Task Manager.")
                break
            else:
                print("Invalid option. Please try again.")

    def performance_test(self):
        """
        Conduct performance tests for the Dynamic Task Manager.
        """
        # Performance testing for adding tasks
        num_tasks=1000

        start_time = timeit.default_timer()
        for i in range(num_tasks):
            task = Task(f"Task {i}", random.randint(1, 5), f"2024-12-{random.randint(1, 31)}")
            # self.add_task(task, save=False)
            self.add_task(task)
        elapsed_time = timeit.default_timer() - start_time
        print(f"Time taken to add {num_tasks} tasks: {elapsed_time:.4f} seconds")

        # Performance testing for retrieving the next task
        start_time = timeit.default_timer()
        self.get_next_task()
        elapsed_time = timeit.default_timer() - start_time
        print(f"Time taken to retrieve the next task: {elapsed_time:.6f} seconds")

        # Performance testing for sorting tasks by due date
        start_time = timeit.default_timer()
        self.sort_tasks_by_due_date()
        elapsed_time = timeit.default_timer() - start_time
        print(f"Time taken to sort tasks by due date: {elapsed_time:.4f} seconds")

        # Performance testing for sorting tasks by priority
        start_time = timeit.default_timer()
        self.sort_tasks_by_priority()
        elapsed_time = timeit.default_timer() - start_time
        print(f"Time taken to sort tasks by priority: {elapsed_time:.4f} seconds")

        # Performance testing for deleting tasks
        start_time = timeit.default_timer()
        for i in range(num_tasks):
            self.remove_task(f"Task {i}")
        elapsed_time = timeit.default_timer() - start_time
        print(f"Time taken to delete {num_tasks} tasks: {elapsed_time:.4f} seconds")

if __name__ == "__main__":
    task_manager = TaskManager()
    task_manager.user_interface()
    task_manager.performance_test()