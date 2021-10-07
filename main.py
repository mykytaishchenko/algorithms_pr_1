from random import shuffle, choice
import time
import pandas as pd


def selection_sort(arr: list):
    operations = 0

    for i in range(len(arr)):
        min_el_idx = i
        for j in range(i + 1, len(arr)):
            operations += 1
            if arr[min_el_idx] > arr[j]:
                min_el_idx = j
        arr[i], arr[min_el_idx] = arr[min_el_idx], arr[i]

    return operations


def insertion_sort(arr: list):
    operations = 0

    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and key < arr[j]:
            operations += 1
            arr[j + 1] = arr[j]
            j -= 1
        else:
            operations += 1

        arr[j + 1] = key

    return operations


def merge_sort(arr: list):
    operations = 0
    if len(arr) > 1:

        mid = len(arr) // 2

        left = arr[:mid]
        right = arr[mid:]

        operations += merge_sort(left)
        operations += merge_sort(right)

        i = j = k = 0

        while i < len(left) and j < len(right):
            operations += 1
            if left[i] < right[j]:
                arr[k] = left[i]
                i += 1
            else:
                arr[k] = right[j]
                j += 1
            k += 1

        while i < len(left):
            arr[k] = left[i]
            i += 1
            k += 1

        while j < len(right):
            arr[k] = right[j]
            j += 1
            k += 1

    return operations


def shell_sort(arr):
    operations = 0
    arr_len = len(arr)
    gap = arr_len // 2

    while gap > 0:

        for i in range(gap, arr_len):
            buff = arr[i]
            j = i
            while j >= gap and arr[j - gap] > buff:
                arr[j] = arr[j - gap]
                j -= gap
                operations += 1
            else:
                operations += 1

            arr[j] = buff
        gap //= 2

    return operations


def testing_sort_time(arr: list):
    results = {}

    # Selection sort
    selection_sort_arr = arr.copy()
    selection_sort_time = time.time()
    selection_sort_op = selection_sort(selection_sort_arr)
    selection_sort_time = time.time() - selection_sort_time
    print(f"Selection sort[time: {selection_sort_time}s, operations: {selection_sort_op}]")
    results["selection sort"] = {"time": selection_sort_time, "operations": selection_sort_op}

    # Insertion sort
    insertion_sort_arr = arr.copy()
    insertion_sort_time = time.time()
    insertion_sort_op = insertion_sort(insertion_sort_arr)
    insertion_sort_time = time.time() - insertion_sort_time
    print(f"Insertion sort[time: {insertion_sort_time}s, operations: {insertion_sort_op}]")
    results["insertion sort"] = {"time": insertion_sort_time, "operations": insertion_sort_op}

    # Merge sort
    merge_sort_arr = arr.copy()
    merge_sort_time = time.time()
    merge_sort_op = merge_sort(merge_sort_arr)
    merge_sort_time = time.time() - merge_sort_time
    print(f"Merge sort[time: {merge_sort_time}s, operations: {merge_sort_op}]")
    results["merge sort"] = {"time": merge_sort_time, "operations": merge_sort_op}

    # Shell sort
    shell_sort_arr = arr.copy()
    shell_sort_time = time.time()
    shell_sort_op = shell_sort(shell_sort_arr)
    shell_sort_time = time.time() - shell_sort_time
    print(f"Shell sort[time: {shell_sort_time}s, operations: {shell_sort_op}]")
    results["shell sort"] = {"time": shell_sort_time, "operations": shell_sort_op}

    print()

    return results


def test_variants(var: int):
    length = 2 ** 7
    results = {}

    while length <= 2 ** 15:

        # from 0 to len
        if var == 1:
            arr = [_ for _ in range(length)]
        # from len to 0
        elif var == 2:
            arr = [_ for _ in range(length - 1, -1, -1)]
        # rand
        elif var == 3:
            arr = [_ for _ in range(length)]
            shuffle(arr)
        # from set 1, 2, 3
        elif var == 4:
            arr = [choice([1, 2, 3]) for _ in range(length)]
        # other
        else:
            arr = []

        print(f"- Length: {length}")
        results[length] = testing_sort_time(arr)

        length *= 2

    return results


def test():
    print("Tetsing.................\n"
          "________________________\n")

    results = {}

    testing_time = time.time()

    print("-- Test 1 (0 to len)")
    results["test 1 (0 to len)"] = test_variants(1)
    print()

    print("-- Test 2 (len to 0)")
    results["test 2 (len to 0)"] = test_variants(2)
    print()

    randoms = []
    for num in range(5):
        print(f"-- Test 3, part {num + 1} (random)")
        randoms.append(test_variants(3))
        print()

    randoms_average = randoms[0]
    for key in randoms_average.keys():
        for key_2 in randoms_average[key].keys():
            for key_3 in randoms_average[key][key_2].keys():
                for el in randoms[1:]:
                    randoms_average[key][key_2][key_3] += el[key][key_2][key_3]

    for key in randoms_average.keys():
        for key_2 in randoms_average[key].keys():
            for key_3 in randoms_average[key][key_2].keys():
                randoms_average[key][key_2][key_3] /= 5

    results["test 3 (random)"] = randoms_average

    print("-- Test 4 (values from set {1, 2, 3})")
    results["test 4 {1, 2, 3}"] = test_variants(4)
    print()

    testing_time = time.time() - testing_time

    writer = pd.ExcelWriter("result.xlsx")

    buff_op, buff_time = {}, {}
    for key in results.keys():
        for key_2 in results[key].keys():
            buff_op[key_2] = {}
            buff_time[key_2] = {}
            for key_3 in results[key][key_2].keys():
                buff_op[key_2][key_3] = results[key][key_2][key_3]["operations"]
                buff_time[key_2][key_3] = results[key][key_2][key_3]["time"]
        pd.DataFrame(buff_op).to_excel(writer, f"{key} op")
        pd.DataFrame(buff_time).to_excel(writer, f"{key} time")

    writer.save()

    print(f"Test complete!!!!!!!!!!!!!!!!!!\n"
          f"It takes {testing_time}s")


if __name__ == "__main__":
    test()
