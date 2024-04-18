heap = [26, 10, 16, None, None, 9, 8, None, None, None, None, 5, 4, 3, 5]
n = len(heap)

# Создаем временную структуру для хранения позиций элементов в исходной куче
positions = {value: index for index, value in enumerate(heap) if value is not None}

# Удаление None из кучи для сортировки
heap = [item for item in heap if item is not None]

# Сортировка кучи
heap.sort()

# Восстановление структуры дерева
sorted_heap = [None] * n
for value, index in positions.items():
    sorted_heap[index] = value

print("Отсортированная куча с восстановленной структурой:")
print(sorted_heap)
