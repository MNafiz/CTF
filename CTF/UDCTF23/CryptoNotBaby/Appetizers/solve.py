

def isSubsetSum(arr, n, sum):
    print("enter")
    subset =[set() for i in range(n + 1)]
    
    # If sum is 0, then answer is true
    for i in range(n + 1):
        subset[i].add(0)
    # Fill the subset table in bottom up manner
    for i in range(1, n + 1):
        # print(i)
        for c in subset[i-1]:
            subset[i].add(c)
            if c+arr[i-1] <= sum:
                subset[i].add(c+arr[i-1])
    print("done")
    assert(sum in subset[n])
    d = [0 for i in range(n)]
    cur = sum

    for i in range(n, 0, -1):
        # print(i)
        if cur in subset[i-1]:
            d[i-1] = 0
        elif cur-arr[i-1] in subset[i-1]:
            d[i-1]=1
            cur -= arr[i-1]
        else:
            print("error")
    return d


def dnc(arr, tot):
    n = len(arr)//2
    left = {0}
    for i in range(n):
        temp = set()
        for s in left:
            if (s+arr[i] <= tot):
                temp.add(s+arr[i])
        left.update(temp)

    # print(len(left))

    right = {0}
    for i in range(n, len(arr)):
        temp = set()
        for s in right:
            if (s+arr[i] <= tot):
                temp.add(s + arr[i])
        right.update(temp)


    left = list(left)
    left.sort()
    # print(len(left), len(right))
    for c in right:
        tar = tot - c
        l = 0
        r = len(left)-1
        while l<r:
            mid = (l+r)//2
            if left[mid] > tar:
                r = mid
            elif left[mid] < tar:
                l = mid + 1
            else:
                l = mid
                r = mid
        if left[l] == tar:
            d1 = isSubsetSum(arr[:n], n, tar)
            d2 = isSubsetSum(arr[n:], len(arr[n:]), c)
            print(d1, d2)
            return d1+d2
        
choices = [19728964, 30673077, 137289540, 195938621, 207242611, 237735979, 298141799, 302597011, 387047012, 405520686, 424852916, 461998372, 463977415, 528505766, 557896298, 603269308, 613528675, 621228168, 654758801, 670668388, 741571487, 753993381, 763314787, 770263388, 806543382, 864409584, 875042623, 875651556, 918697500, 946831967]
target = 7627676296


hasil = dnc(choices,target)
flag = [choices[i] for i in range(len(choices)) if hasil[i]]
print("_".join(map(str,flag)))

# UDCTF{19728964_30673077_137289540_195938621_237735979_302597011_463977415_603269308_654758801_670668388_763314787_806543382_875651556_918697500_946831967}