import concurrent.futures
import multiprocessing
from multiprocessing import Pipe
import time

def algoritm(i, numbers, result, q):
    for j in range(i+1, len(numbers)-i):
        q.put(result[i+j])
        if numbers[i+j] % numbers[i] == 0:
            result[i+j] = 1
    return result

def progress(q, i, numbers):
        print(f'Вычисление для числа {numbers[i]}: {q.get()} из {len(numbers)}')


if __name__ == '__main__':
    print("До какого числа искать?")
    quantity = int(input())

    numbers = [i for i in range(2, quantity)]
    flags = [0 for i in range(2, quantity)]

    simple = []

    i = 0
    while i < len(numbers):
        if flags[i] == 0:
            simple.append(numbers[i])
            with open("simple.txt", "w", encoding='utf-8') as file:
                for number in simple:
                    file.writelines(f"{number}\n")
            j = i + 1
            while j < len(numbers):
                if flags[j] == 0:
                    simple.append(numbers[j])
                    with open("simple.txt", "w", encoding='utf-8') as file:
                        for number in simple:
                            file.writelines(f"{number}\n")
                    resultProcesses = []
                    resultProcess1 = [0 for i in range(2, quantity)]
                    resultProcess2 = [0 for i in range(2, quantity)]
                    with concurrent.futures.ProcessPoolExecutor() as executor:
                        progress1 = multiprocessing.Queue()
                        progress2 = multiprocessing.Queue()

                        resultProcesses.append(executor.submit(algoritm, i, numbers, resultProcess1, progress1))  #процессы с рассчетами
                        resultProcesses.append(executor.submit(algoritm, j, numbers, resultProcess2, progress2))

                        executor.submit(progress, progress1, i, numbers)   # процессы для мониторинга прогресса
                        executor.submit(progress, progress2, j, numbers)

                        concurrent.futures.as_completed(resultProcesses)

                        for f in range(len(resultProcesses[0].result())):
                            if resultProcesses[0].result()[f] == 1 or resultProcesses[1].result()[f] == 1:
                                flags[f] = 1
                    i += j - i
                    break
                j += 1
        i += 1

    



