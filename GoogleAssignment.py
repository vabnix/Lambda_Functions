from collections import Counter

original_list = [5, 5, 6, 7, 8, 8, 9, 1, 1, 2, 2, 3, 3, 4, 4, 4]
element_counter = Counter(original_list)
minion = []


def element_count(data):
    count = {}
    for element in data:
        count[element] = count.get(element, 0) + 1
    return count


def solution(data, n):
    my_counter = element_count(data)
    for element in data:
        if my_counter[element] <= n:
            minion.append(element)
    return minion

print(solution(original_list, 2))
