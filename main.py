
import json
import os

JsonData = {}
JsonStr = ""


def view():
    global JsonData
    if "list" not in JsonData:
        JsonData["list"] = []
        print("The list is empty! ")
        return
    print("The list: ")
    cnt = 1
    if len(JsonData["list"]) == 0:
        print("is empty! ")
    else:
        for i in JsonData["list"]:
            if cnt >= 10000:
                print("Task is too much!")
                return
            print("{:>4d}".format(cnt), end="")
            cnt += 1
            if i["done"] == True:
                print("{:>4s}".format("▣ "), end="")
            else:
                print("{:>4s}".format("▢ "), end="")
            print(i["name"])
    print()


def add(name, done):
    global JsonData
    obj = {}
    if name:
        obj["name"] = name
    else:
        print("Input the task:")
        obj["name"] = input()
    if done == None:
        print("It has been done(y/n):")
        done = input()
        if done == "y":
            obj["done"] = True
        elif done == "n":
            obj["done"] = False
        else:
            print("Input error! ")
            return
    else:
        obj["done"] = done
    JsonData["list"].append(obj)
    return


def read():
    file = open("data.json", encoding="UTF-8")
    global JsonStr
    JsonStr = file.read()
    file.close()
    global JsonData
    JsonData = json.loads(JsonStr)


def write():
    global JsonStr
    global JsonData
    JsonStr = json.dumps(JsonData, ensure_ascii=False)
    if "list" in JsonData:
        file = open("data.json", mode="w", encoding="UTF-8")
        file.write(JsonStr)
        file.close()
    else:
        print("The data has error! ")


def delete(ser):
    global JsonData
    if ser == None:
        print(
            "Input the number you want to delete:(Input \"esc\" to cancel the opporation)")
        num = input()
    else:
        num = ser
    if num == "esc":
        return
    else:
        try:
            if num <= 0:
                raise
            del JsonData["list"][int(num)-1]
        except:
            print("The serier is not exist! ")


def finish(num):
    global JsonData
    if num == None:
        print(
            "Input the number you want to finish:(Input \"esc\" to cancel the opporation)")
        num = input()
    if num == "esc":
        return
    else:
        try:
            if num <= 0:
                raise
            JsonData["list"][int(num)-1]["done"] = True
            JsonData["list"].append(JsonData["list"].pop(int(num)-1))
        except:
            print("The serier is not exist! ")


def focus():
    global JsonData
    print("Input the number you want to delete:(Input \"esc\" to cancel the opporation)")
    num = input()
    if num == "esc":
        return
    else:
        try:
            temp = JsonData["list"][int(num)-1]
            del JsonData["list"][int(num)-1]
            JsonData["list"].insert(0, temp)
        except:
            print("The input is incorrect! ")


def manage():
    global JsonData
    cnt = 0
    for i in JsonData["list"]:
        if i["done"] == True:
            JsonData["list"].append(JsonData["list"].pop(cnt))
        cnt += 1


def clear(undo):
    global JsonData
    if undo:
        JsonData["list"].clear()
        return
    cnt = 0
    for i in range(len(JsonData["list"])):
        if JsonData["list"][cnt]["done"] == True:
            JsonData["list"].pop(cnt)
        else:
            cnt += 1


def fun_import():
    file = open("tasks.json", encoding="UTF-8")
    TaskStr = file.read()
    file.close()
    TaskData = json.loads(TaskStr)
    ListTemp = []

    for TaskGroup in TaskData["Tasks"]:
        for Task in TaskData["Tasks"][TaskGroup]:
            for Project in Task["proj"]:
                name = Task["name"] + '-' + Project["task"]
                ddl = Project["ddl"]
                if ddl == ["Every Day"]:
                    ddl = 0
                else:
                    ddl = ddl[0]*31 + ddl[1]
                ListTemp.append({"name": name, "ddl": ddl})
    ListTemp = sorted(ListTemp, key=lambda task: task["ddl"])
    for task in ListTemp:
        add(task["name"], False)


def help():
    print("there are many order you can use:")
    print("\"ls\": Show the list. ")
    print("\"add\": Add a task to your list. ")
    print("\"del\": Delete a task from your list. ")
    print("\"fin\": Sign a task in your list to 'finished'. ")
    print("\"foc\": Focus on a task. ")
    print("\"man\": Put all finished tasks back. ")
    print("\"clear\": Clear the finished tasks. ")
    print("\"cls\": Clear the consle. ")
    print("\"exit\": Exit the program. ")
    print("\"ipt\": import tasks in \"tasks.json\". ")


op = None
addition = []
read()
view()
while True:
    print(">>>", end="")
    order = input().split()
    if len(order) == 0:
        continue
    op = order[0]
    addition = []
    if len(order) > 1:
        addition = order[1:]

    if op == "ls":
        if addition:
            print("The addition order is invalid! ")
            continue
        view()

    elif op == "add":
        odn = len(addition)
        name = None
        done = None
        if odn >= 1 and addition[0] == "-d":
            done = False
            del addition[0]
            odn -= 1
        if odn >= 1:
            name = addition[0]
            del addition[0]
            odn -= 1
        if odn:
            print("The addition order is invalid! ")
            continue
        add(name, done)

    elif op == "del":
        ser = None
        if len(addition) == 1:
            if not addition[0].isnumeric():
                print("The addition order is invalid! ")
                continue
            ser = int(addition[0])
            del addition[0]
        if addition:
            print("The addition order is invalid! ")
            continue
        delete(ser)

    elif op == "fin":
        odn = len(addition)
        doclear = False
        num = None
        if odn >= 1 and addition[0] == "-c":
            doclear = True
            del addition[0]
            odn -= 1
        if odn == 1:
            if not addition[0].isnumeric():
                print("The addition order is invalid! ")
                continue
            num = int(addition[0])
            del addition[0]
            odn -= 1
        if odn:
            print("The addition order is invalid! ")
            continue
        finish(num)
        if doclear:
            clear(False)

    elif op == "foc":
        if addition:
            print("The addition order is invalid! ")
            continue
        focus()

    elif op == "man":
        if addition:
            print("The addition order is invalid! ")
            continue
        manage()

    elif op == "clear":
        undo = False
        if addition and addition[0] == "-a":
            undo = True
            del addition[0]
        if addition:
            print("The addition order is invalid! ")
            continue
        clear(undo)

    elif op == "ipt":
        if addition:
            print("The addition order is invalid!")
            continue
        fun_import()

    elif op == "cls":
        if addition:
            print("The addition order is invalid! ")
            continue
        os.system("cls")

    elif op == "help":
        if addition:
            print("The addition order is invalid! ")
            continue
        print("help page")
        help()

    elif op == "exit":
        if addition:
            print("The addition order is invalid! ")
            continue
        break

    else:
        print("The order is worng!(input \"help\" to look up valid orders)")

    write()
    print()

print("program has been closed. ")
