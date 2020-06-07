class Solution:

    def __init__(self, N):
        self.N = N
        self.memory = set()

    def record(self, order_id):
        self.memory.add(order_id)
        if len(self.memory) > self.N:
            self.memory.remove(self.memory[0])

    def get_last(self, i):
        return self.memory[-i]


if __name__ == '__main__':
    tests = ()
    main = Solution()

    for id in tests[0]:
        main.record(id)
    res = main.get_last(tests[1])

    print(res)
