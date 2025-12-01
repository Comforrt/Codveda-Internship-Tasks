#for the program to read and write json files
import json
# my_task.json is used to persist tasks between runs


# writes the todoList in a json file named my_task
def store_json():
    with open("my_task.json", "w") as file:
        json.dump(todo_list, file, indent=2) #converts this list into Json and then writes it and also the indent is to make it appear more readable


#loads all the saved task from the json file that's my_task to the program when it starts
def load_json():
    global todo_list
    try:
        with open("my_task.json", "r") as file:
            todo_list = json.load(file)
    except FileNotFoundError: #prevents the program from crashing when list is empty
        todo_list = []
        print("File not available!!")



todo_list = [] # Global in-memory list of tasks
try:
    # defining the def functions


    def add_task():
        task = str(input("Input a task : "))
        if task == "": #checks if user didn't input a task and if the user does not it returns early
            print("The task field can't be empty!!")
            return
        todo_list.append({"Task": task, "Status": "Pending"}) #adds the user's task and its status to the todoList
        print("Task added successfully!!\n")
        store_json()


    def list_task():
        print("------My Todo list-----")
        if len(todo_list) == 0:
            print("There is no task!!")
        else:
            for index, task in enumerate(todo_list, 1): #enumerates task by starting from 1 not 0
                print(f"{index} : {task['Task']} - {task['Status']}")
        print("\n")


    def delete_task():
        if len(todo_list) == 0: #checking for empty list
            print("List is empty already!!")
        else:
            try:
                search_list = int(input("Input the number you would like to remove from MyTodoList : ")) - 1
                if 0 <= search_list < len(todo_list): # validate index range before popping
                    delete = todo_list.pop(search_list) #deletes the preferred number of the user from todoList
                    print(f'Task deleted : {delete['Task']}')
                    store_json()
                else:
                    print("Task number is not available!!")
            except ValueError:
                print("Invalid input")


    def complete_task():
        if todo_list == 0:
            print("List is empty already!!")
        else:
            try:
                complete_list = int(input("Input the number you would like to mark as complete : ")) - 1
                if 0 <= complete_list < len(todo_list):
                    todo_list[complete_list]['Status'] = 'Complete'
                    print(f"Task : {todo_list[complete_list]['Task']}, has been marked as done!!")
                    store_json()
                else:
                    print("Task number is not available!!")
            except ValueError:
                print("Invalid input")


    def menu():
        while True:
            print("")
            print("1--Add a task ")
            print("2--List tasks ")
            print("3--Remove a task ")
            print("4--Mark task as done ")
            print("5--Exit ")

            option = int(input("Input the action you want to perform (1-5) : "))

            if option == 1:
                add_task()

            elif option == 2:
                list_task()

            elif option == 3:
                delete_task()

            elif option == 4:
                complete_task()

            elif option == 5:
                print("Exiting list....")
                print("Exited")
                exit()

            else:
                print("Invalid input!!!")


    # Load saved tasks and start the menu
    load_json()
    menu()


except ValueError:
    print("Invalid input")

