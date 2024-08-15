import pandas as pd
from datetime import datetime
from skip_list import SkipList
from fibonacci_heap import FibonacciHeap

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
            return max(incomplete_tasks, key=lambda t: t.priority)
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

# Example usage
if __name__ == "__main__":
    task_manager = TaskManager()
    task_manager.add_task(Task("Task 1", 5, "2024-08-10"))
    task_manager.add_task(Task("Task 2", 3, "2024-08-12"))
    task_manager.add_task(Task("Task 3", 4, "2024-08-11"))
    task_manager.add_task(Task("Task 4", 2, "2024-08-15"))
    task_manager.add_task(Task("Task 5", 3, "2024-08-18"))
    task_manager.add_task(Task("Task 3", 4, "2024-08-11")) #Task 3 duplicate

    next_task = task_manager.get_next_task()
    if next_task:
        print("Next task to do:", next_task.name)

    print("---> Delete the Task 4.")
    task_manager.remove_task("Task 4")
    task = task_manager.skip_list.search("Task 4")
    if task:
        print("Task 4 not deleted")
    else:
        print("Task 4 has been deleted successfully")

    print("Tasks sorted by due date:")
    for task in task_manager.sort_tasks_by_due_date():
        print(f"{task.name} - {task.due_date}")

    print("Tasks sorted by priority:")
    for task in task_manager.sort_tasks_by_priority():
        print(f"{task.name} - {task.priority}")

    print("---> Update the Task 2.")
    task_manager.update_task("Task 2", priority=1, status="Complete")
    print("Updated Task 2 details:")
    task = task_manager.skip_list.search("Task 2")
    if task:
        print(f"{task.name} {task.priority} {task.due_date} {task.status}")
    else:
        print("Task 2 not found.")
