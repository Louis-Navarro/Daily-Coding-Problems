def main(nums, k):
    diffs = {}

    for num in nums:
        if diffs.get(num):
            return True
        
        diff = k - num
        diffs[diff] = num

    return False


if __name__ == '__main__':
    tests = ([10, 15, 3, 7], 17)
    res = main(*tests)
    print(res)
