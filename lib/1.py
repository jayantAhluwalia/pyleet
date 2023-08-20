def solve(nums, target):
    sums = {}
    target = target[0]
    for idx, num in enumerate(nums):
        diff = target - num
        if diff in sums:
            return f"[{sums[diff]}, {idx}]"
        sums[num] = idx
    return