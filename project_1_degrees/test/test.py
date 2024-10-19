days = { "Sun", "Mon" } # set - does not take duplicates

print('days: ', len(days))
for d in days:
    print(d)

days.add("Mon")

print()
for d in days:
    print(d)

print()
# set to list
days_list = list(days) # list can take duplicates and maintain order
days_list.append("Mon")
days_list.append("Tue")
for d in days_list:
    print(d)

arr = [1,2,3,4,5]
print(arr[-1]) # -1 last element
print(arr[-3]) # 3rd last element
print(arr[:3]) # 0 to 3rd element

print(arr[-5:]) # -5 = 0 in this list



