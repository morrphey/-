
# ЗАДАНИЕ 1. Анаграммы в списке

def group_anagrams(words):
    groups = {}                         
    for word in words:
        key = "".join(sorted(word))     
        if key not in groups:
            groups[key] = []
        groups[key].append(word)

    return list(groups.values())         


words = ["listen", "silent", "enlist", "google", "gooegl", "abc", "cab", "bac"]
print("1. Анаграммы:", group_anagrams(words))


# ЗАДАНИЕ 2. Словарь частот символов

def char_frequency(text):
    text = text.lower()                 
    freq = {}

    for ch in text:
        if ch == " ":                    
            continue
        if ch not in freq:
            freq[ch] = 0
        freq[ch] += 1                    

    return freq


text = "The quick brown fox jumps over the lazy dog"
print("\n2. Частоты символов:", char_frequency(text))

# ЗАДАНИЕ 3. Валидатор скобок (стек)

def is_valid_brackets(s):
    stack = []
    pairs = {")": "(", "]": "[", "}": "{"}   

    for ch in s:
        if ch in "([{":                       
            stack.append(ch)
        elif ch in ")]}":                      
            if not stack or stack[-1] != pairs[ch]:
                return False
            stack.pop()                       
    return len(stack) == 0    # стек должен быть пуст


print("\n3. Валидатор скобок:")
print("  (([]){}[]) →", is_valid_brackets("(([]){}[])"))
print("  ([)]       →", is_valid_brackets("([)]"))
# ЗАДАНИЕ 4. Слияние словарей

def merge_dicts(list_of_dicts):
    result = {}

    for d in list_of_dicts:            
        for key, value in d.items():     
                result[key] = 0
            result[key] += value         

    return result


dicts = [{"a": 2, "b": 3}, {"a": 4, "c": 5}]
print("\n4. Слияние словарей:", merge_dicts(dicts))

# ЗАДАНИЕ 5. Палиндром по словам
def can_form_palindrome(words):
    counts = {}  # считаем, сколько раз встречается каждое слово

    for w in words:
        if w not in counts:
            counts[w] = 0
        counts[w] += 1

    middle_used = False 

    for word, count in counts.items():
        reverse = word[::-1]            

        if word == reverse:       
            if count % 2 != 0:   # нечётное количество — может быть только в центре
                if middle_used:
                    return False
                middle_used = True
        else:
            if reverse in counts:
                if counts[word] != counts[reverse]:   # пар должно быть поровну
                    return False
            else:
                return False  # нет пары — палиндром невозможен

    return True


print("\n5. Палиндром по словам:")
print("  ['ab','ba','cc'] →", can_form_palindrome(["ab", "ba", "cc"]))
print("  ['ab','cd']      →", can_form_palindrome(["ab", "cd"]))

# ЗАДАНИЕ 6. Калькулятор выражений

import re   # модуль для работы с регулярными выражениями

def calculate(expression):
  
    allowed = re.fullmatch(r"[\d\+\-\*\/\(\)\.\s]+", expression) # строка должна содержит только разрешённые символы
    if not allowed:
        return "Ошибка: недопустимые символы в выражении"

    try:
        result = eval(expression)    
        return result
    except ZeroDivisionError:
        return "Ошибка: деление на ноль"
    except Exception:
        return "Ошибка: некорректное выражение"


print("\n6. Калькулятор:")
print("  2 + 3 * (4 - 1) =", calculate("2 + 3 * (4 - 1)"))
print("  10 / 2 + 5      =", calculate("10 / 2 + 5"))
print("  2abc            =", calculate("2abc"))

#ЗАДАНИЕ 7. Группировка по длине

def group_by_length(words):
    groups = {}

    for word in words:
        length = len(word)         
        if length not in groups:
            groups[length] = []
        groups[length].append(word)

    return groups

words7 = ["cat", "dog", "elephant", "bee", "ant"]
print("\n7. Группировка по длине:", group_by_length(words7))

#ЗАДАНИЕ 8. Частотный список слов
# collections.Counter автоматически считает количество элементов.
import string               
from collections import Counter

def top_words(text, n=3):
    text = text.lower()  # нижний регистр

   
    clean = "" # убираем знаки препинания
    for ch in text:
        if ch not in string.punctuation:#string.punctuation все знаки препинания
            clean += ch

    words = clean.split() # разбиваем строку на слова
    counter = Counter(words)# считаем каждое слово
    return counter.most_common(n)# топ n самых частых
user_text = input("\n8. Введите строку для подсчёта топ-слов: ")
print("   Топ-3 слова:", top_words(user_text))
# ЗАДАНИЕ 9. Класс "Студент"

class Student:
    def __init__(self, name):
        self.name = name
        self.grades = []  # пустой список оценок

    def add_grade(self, grade):
        self.grades.append(grade)

    def average(self):
        if not self.grades:  # если оценок нет — среднее 0
            return 0
        return sum(self.grades) / len(self.grades)

    def __str__(self): # как объект выглядит при print()
        return f"Студент: {self.name}, оценки: {self.grades}, среднее: {self.average():.2f}"

print("\n9. Класс Студент:")
students = [Student("Алиса"), Student("Боря"), Student("Вера")]
students[0].add_grade(5); students[0].add_grade(4); students[0].add_grade(5)
students[1].add_grade(3); students[1].add_grade(3); students[1].add_grade(4)
students[2].add_grade(5); students[2].add_grade(5); students[2].add_grade(5)

for s in students:
    print(" ", s)
# ЗАДАНИЕ 10. Проверка Судоку
def is_valid_sudoku(board):

    def has_no_duplicates(cells):
        """Возвращает True, если среди непустых клеток нет повторений."""
        nums = [c for c in cells if c != "."] # убираем точки
        return len(nums) == len(set(nums))  # set убирает дубли, длины должны совпасть
    #строки
    for row in board:
        if not has_no_duplicates(row):
            return False
    #столбцы
    for col in range(9):
        column = [board[row][col] for row in range(9)]   # собираем столбец
        if not has_no_duplicates(column):
            return False
    # блоки 3×3
    for block_row in range(3):# номер блока по вертикали: 0, 1, 2
        for block_col in range(3):# номер блока по горизонтали: 0, 1, 2
            block = []
            for r in range(3):
                for c in range(3):
                    block.append(board[block_row * 3 + r][block_col * 3 + c])
            if not has_no_duplicates(block):
                return False

    return True

board = [
    ["5","3",".",".","7",".",".",".","."],
    ["6",".",".","1","9","5",".",".","."],
    [".","9","8",".",".",".",".","6","."],
    ["8",".",".",".","6",".",".",".","3"],
    ["4",".",".","8",".","3",".",".","1"],
    ["7",".",".",".","2",".",".",".","6"],
    [".","6",".",".",".",".","2","8","."],
    [".",".",".","4","1","9",".",".","5"],
    [".",".",".",".","8",".",".","7","9"],
]
print("\n10. Судоку корректна:", is_valid_sudoku(board))
