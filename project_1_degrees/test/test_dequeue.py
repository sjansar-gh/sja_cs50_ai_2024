import collections

# initializing deque
de = collections.deque([6, 1, 2, 3, 4])
print("deque: ", de)

# using pop() to delete element from right end
# deletes 4 from the right end of deque
elem = de.pop()
print('First elem deleted: ', elem)

# printing modified deque
print("\nThe deque after deleting from right is: ")
print(de)

# using popleft() to delete element from left end
# deletes 6 from the left end of deque
de.popleft()

# printing modified deque
print("\nThe deque after deleting from left is : ")
print(de)

dq = collections.deque([])
dq.appendleft('Apple')
dq.appendleft('Orange')
dq.appendleft('Banana')
dq.appendleft('Cherries')
dq.appendleft('Strawberries')

print('dq has Banana:', 'Banana' in dq)
print('dq has Banana:', bool(dq.count('Banana')))

print('dq: ', dq)
fruit = dq.pop()
print('popped fruit: ', fruit)
print('dq after first fruit deleted')
print(dq)

for i in range(len(dq)):
    print('fruit: ', dq.pop())

print('dq: ', dq)
print('dq count: ', len(dq))