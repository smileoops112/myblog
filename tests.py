nums = [int(i) for i in input().split(',')]
res = 0
l = []
for i in range(len(nums)-1):
    if nums[i] < nums[i+1]:
        res += 1
    l.append(res)
print(max(l))