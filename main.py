import concurrent.futures
from multiprocessing import Process, Queue
import multiprocessing as mp
import time

sentinel = -1

def algoritm(i, numbers, result, q):
    for j in range(i+1, len(numbers)-i):
        q.put([numbers[i], numbers[i+j], len(numbers)])
        if numbers[i+j] % numbers[i] == 0:
            result[i+j] = 1

    while q.empty() != True:
        q.get()
    return result

def progress(q):
    while True:
        time.sleep(1)
        data = q.get()
        print(f'Вычисление для числа {data[0]}: {data[1]} из {data[2]}')

        if data is sentinel:
            break

def gui():
    last = 0
    simple = []

    print("1 - продолжить вычисления; 2 - новые вычисления")

    choice = input()
    try:
        int(choice)
    except:
        print("Ошибка ввода данных")
        gui()

    choice = int(choice)
    if choice != 1 and choice != 2:
        print("Нет такого выбора")
        gui()

    print("До какого числа искать?")
    quantity = int(input())

    numbers = [i for i in range(2, quantity)]
    flags = [0 for i in range(2, quantity)]

    if choice == 1:
        with open("simple.txt", "r", encoding='utf-8') as file:
            contents = file.readlines()
            for line in contents:
                simple.append(int(line))
        with open("flags.txt", "r", encoding='utf-8') as file:
            contents = file.readlines()
            for flag in range(len(contents)):
                flags[flag] = int(contents[flag])
        last = simple[-1]-1

    elif choice == 2:
        with open("simple.txt", "w", encoding='utf-8') as file:
            file.writelines("")
        with open("flags.txt", "w", encoding='utf-8') as file:
            file.writelines("")

    m = mp.Manager()

    q1 = m.Queue()
    q2 = m.Queue()

    monitor1 = Process(target=progress, args=(q1,))
    monitor2 = Process(target=progress, args=(q2,))
    monitor1.start()
    monitor2.start()

    print(last, flags)

    i = last
    while i < len(numbers):
        if flags[i] == 0:
            simple.append(numbers[i])
            with open("simple.txt", "a", encoding='utf-8') as file:
                    file.writelines(f"{simple[-1]}\n")
            j = i + 1
            while j < len(numbers):
                if flags[j] == 0:
                    simple.append(numbers[j])
                    with open("simple.txt", "a", encoding='utf-8') as file:
                            file.writelines(f"{simple[-1]}\n")
                    resultProcesses = []
                    resultProcess1 = [0 for i in range(2, quantity)]
                    resultProcess2 = [0 for i in range(2, quantity)]
                    with concurrent.futures.ProcessPoolExecutor() as executor:

                        resultProcesses.append(executor.submit(algoritm, i, numbers, resultProcess1, q1))  # процессы с рассчетами
                        resultProcesses.append(executor.submit(algoritm, j, numbers, resultProcess2, q2))

                        concurrent.futures.as_completed(resultProcesses)

                        for f in range(len(resultProcesses[0].result())):
                            if resultProcesses[0].result()[f] == 1 or resultProcesses[1].result()[f] == 1:
                                flags[f] = 1
                    i += j - i
                    break
                j += 1
        with open("flags.txt", "w", encoding='utf-8') as flagsFile:
            for flag in flags:
                flagsFile.writelines(f"{flag}\n")
        i += 1

    monitor1.kill()
    monitor2.kill()

    print("Готово")

if __name__ == '__main__':
    gui()