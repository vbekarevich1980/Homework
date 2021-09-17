# Task 1.6 (1.8)
# Write a program which makes a pretty print of a part of the multiplication table.
# Examples:

# Input:
# a = 2
# b = 4
# c = 3
# d = 7

# Output:
#	3	4	5	6	7
# 2	6	8	10	12	14
# 3	9	12	15	18	21
# 4	12	16	20	24	28

a = 1
b = 4
c = 3
d = 10

# Method 1
line1 = '\t' + '\t'.join([str(i) for i in range(c, d + 1)])
print(line1)

for i in range(a, b + 1):
    print(str(i) + '\t' + '\t'.join([str(i * j) if len(str(i * j)) == 2 else str(i * j) + ' ' for j in range(c, d + 1)]))
