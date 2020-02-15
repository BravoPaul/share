VALUE = 2000000
EARNING_RATE = 0.1
TIME = 20

sum = VALUE
list_sum = []
list_sum.append(sum)
for i in range(TIME):
    sum = (1+EARNING_RATE)*sum
    list_sum.append(sum)



print(sum)
print(list_sum)