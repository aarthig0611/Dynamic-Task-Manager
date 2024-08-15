## Dynamic Task Manager: Effective Solutions for Task Prioritization and Sorting

Aarthi Ganesan (MSCS), Reema Ramchandra Kadechkar (MSCS), Rosalia Miray (MSDS) 

CS622 Discrete Math and Algorithms for Computing, School of Technology & Computing, City University of Seattle 

### Overview

In today's fast-paced world, staying productive and on schedule is essential. This project introduces a Personal Task Manager designed to streamline task management, prioritization, and sorting. The Task Manager leverages advanced data structures and algorithms to enhance efficiency and user experience.

### Key Features:

* **Skip Lists**: Implemented for fast insertion, deletion, and retrieval of tasks, ensuring quick updates to your task list.
* **Fibonacci Heap**: Used to dynamically track tasks based on their importance, allowing for efficient prioritization.
* **Sorting Algorithms**: Applied to maintain tasks in order by due date or priority, helping users focus on completing the most critical tasks first.

### Benefits

By incorporating these powerful algorithms, the Task Manager significantly improves the handling of complex task lists, making it an invaluable tool for both personal and professional use. Whether you need to manage day-to-day activities or prioritize work tasks, this solution empowers you to boost productivity by keeping your tasks in order of importance.

### Implementation
 
To run the program, ensure you have `pandas` and `openpyxl` installed. You can install these using the following commands:

```pip install pandas```
```pip install openpyxl```

Then, execute the task_manager.py file.
 
Features implemented:
* Adding tasks
* Updating tasks
* Deleting tasks
* Retrieving the next task to complete based on priority (excluding completed tasks)
* Sorting tasks by due date and priority (excluding completed tasks)
* Avoiding duplicate tasks (based on task name and due date and asking user input)