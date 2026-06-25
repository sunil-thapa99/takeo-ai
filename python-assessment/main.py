'''
Python Assessment
Section A - Strings
Q1
Write a program to reverse a string without using slicing.
Example: Input: “python” Output: “nohtyp”
'''
s = input("Enter string: ")
rev = ""

for ch in s:
    rev = ch + rev

print(rev)

'''
Q2
Find the first non-repeating character in a string.
Example: Input: “programming” Output: “p”
'''
s = input("Enter string: ")

for ch in s:
    if s.count(ch) == 1:
        print(ch)
        break
'''
Q3
Check if a string is a palindrome.
Example: Input: “madam” Output: True
'''
s = input("Enter string: ")

rev = ""
for ch in s:
    rev = ch + rev

print(s == rev)
'''
Q4
Count the frequency of each character in a string.
Example: Input: “hello” Output: h:1 e:1 l:2 o:1
'''
s = input("Enter string: ")

freq = {}

for ch in s:
    freq[ch] = freq.get(ch, 0) + 1

for k, v in freq.items():
    print(f"{k}:{v}")
'''
Q5
Remove duplicate characters from a string while preserving order.
Example: Input: “programming” Output: “progamin”

'''
s = input("Enter string: ")

result = ""

for ch in s:
    if ch not in result:
        result += ch

print(result)
'''
Section B - Lists
Q6
Remove duplicates from a list without using set().
Example: Input: [1,2,2,3,4,4] Output: [1,2,3,4]
'''
lst = [1,2,2,3,4,4]

result = []

for i in lst:
    if i not in result:
        result.append(i)

print(result)
'''
Q7
Find the second largest number in a list.
Example: Input: [10,20,5,30,25] Output: 25
'''
lst = [10,20,5,30,25]

largest = second = float('-inf')

for num in lst:
    if num > largest:
        second = largest
        largest = num
    elif num > second and num != largest:
        second = num

print(second)
'''
Q8
Find all duplicate elements in a list.
Example: Input: [1,2,3,2,4,5,1] Output: [1,2]
'''
lst = [1,2,3,2,4,5,1]

duplicates = []

for i in lst:
    if lst.count(i) > 1 and i not in duplicates:
        duplicates.append(i)

print(duplicates)
'''
Q9
Rotate a list by K positions.
Example: Input: [1,2,3,4,5], K=2 Output: [4,5,1,2,3]
'''
lst = [1,2,3,4,5]
k = 2

k = k % len(lst)

result = lst[-k:] + lst[:-k]

print(result)
'''
Q10
Find the intersection of two lists.
Example: Input: [1,2,3,4] [3,4,5,6]
Output: [3,4]

'''
l1 = [1,2,3,4]
l2 = [3,4,5,6]

result = []

for i in l1:
    if i in l2:
        result.append(i)

print(result)
'''
Section C - Dictionary
Q11
Count frequency of elements in a list using a dictionary.
Example: Input: [1,2,2,3,3,3] Output: {1:1, 2:2, 3:3}
'''
lst = [1,2,2,3,3,3]

freq = {}

for num in lst:
    freq[num] = freq.get(num, 0) + 1

print(freq)
'''
Q12
Find the key having the maximum value.
Example: {“A”:100,“B”:500,“C”:300}
Output: B
'''
d = {"A":100, "B":500, "C":300}

max_key = max(d, key=d.get)

print(max_key)
'''
Q13
Reverse a dictionary.
Example: {“a”:1,“b”:2}
Output: {1:“a”,2:“b”}
'''
d = {"a":1, "b":2}

rev = {}

for k, v in d.items():
    rev[v] = k

print(rev)
'''
Q14
Merge two dictionaries.
Example: d1={“a”:1} d2={“b”:2}
Output: {“a”:1,“b”:2}
'''
d1 = {"a":1}
d2 = {"b":2}

d1.update(d2)

print(d1)
'''
Q15
Count word frequency in a sentence using dictionary.
Example: Input: “python is good python is easy”
Output: { “python”:2, “is”:2, “good”:1, “easy”:1 }

'''
sentence = "python is good python is easy"

words = sentence.split()

freq = {}

for word in words:
    freq[word] = freq.get(word, 0) + 1

print(freq)
'''
Section D - Loops
Q16
Print the following pattern:
   **
'''
for i in range(2):
    print("*" * 2)
'''
Q17
Print multiplication table of a given number.
Example: Input: 5
Output: 5 x 1 = 5 … 5 x 10 = 50
'''
n = int(input("Enter number: "))

for i in range(1, 11):
    print(f"{n} x {i} = {n*i}")
'''
Q18
Find factorial using for loop.
Input: 5 Output: 120
'''
n = int(input("Enter number: "))

fact = 1

for i in range(1, n + 1):
    fact *= i

print(fact)
'''
Q19
Find all prime numbers between 1 and 100.
'''
for num in range(2, 101):
    prime = True

    for i in range(2, int(num**0.5) + 1):
        if num % i == 0:
            prime = False
            break

    if prime:
        print(num, end=" ")
'''
Q20
Generate Fibonacci series up to N terms.
Example: Input: 8
Output: 0 1 1 2 3 5 8 13
'''
n = int(input("Enter terms: "))

a, b = 0, 1

for _ in range(n):
    print(a, end=" ")
    a, b = b, a + b
'''
Section E - Interview Coding Questions
Q21
Find the first non-repeating number in a list.
Input: [1,2,3,4,5,1,2,3]
Output: 4
'''
lst = [1,2,3,4,5,1,2,3]

for num in lst:
    if lst.count(num) == 1:
        print(num)
        break
'''
Q22
Find the Nth non-repeating number in a list.
Input: [1,2,3,4,5,1,2,3] N = 2
Output: 5
'''
lst = [1,2,3,4,5,1,2,3]
n = 2

non_repeat = []

for num in lst:
    if lst.count(num) == 1:
        non_repeat.append(num)

if n <= len(non_repeat):
    print(non_repeat[n-1])
else:
    print("Not found")
'''
Q23
Check whether two strings are anagrams.
Input: “listen” “silent”
Output: True
'''
s1 = "listen"
s2 = "silent"

print(sorted(s1) == sorted(s2))
'''
Q24
Find missing number from array.
Input: [1,2,3,5]
Output: 4
'''
lst = [1,2,3,5]

n = len(lst) + 1

expected = n * (n + 1) // 2
actual = sum(lst)

print(expected - actual)
'''
Q25
Find top occurring element in a list.
Input: [1,2,2,3,3,3,4]
Output: 3
'''
lst = [1,2,2,3,3,3,4]

freq = {}

for num in lst:
    freq[num] = freq.get(num, 0) + 1

top = max(freq, key=freq.get)

print(top)
