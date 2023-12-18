class Solution:
    def count_divisors(self, N):
        cnt = 0
        if N != 6:
            ceil = int(N**0.5) + 1
            for i in range(1, ceil + 1):
                if N % i == 0:
                    if i % 3 == 0:
                        cnt = cnt + 1
                    if (N/i) % 3 == 0:
                        if N/i > i :
                            cnt = cnt + 1
            return cnt
        else :
            return 2

#{
 # Driver Code Starts
if __name__ == '__main__':
    t = int (input ())
    for _ in range (t):
        N = int(input())


        ob = Solution()
        print(ob.count_divisors(N))
# } Driver Code Ends