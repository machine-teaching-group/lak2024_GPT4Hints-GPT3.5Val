#User function Template for python3

class Solution:
    def nFibonacci(self, N):
        ans=[0, 1, 1]  # Initialize the list with the first 3 terms of the Fibonacci series
        if N == 0:
            return [0]  # If N is 0, return list with only 0
        if N == 1:
            return ans  # If N is 1, return the initialized list
        a = 1
        b = 1
        c = a + b
        while c <= N:
            ans.append(c)
            a, b = b, c
            c = a + b
        return ans


#{
 # Driver Code Starts
#Initial Template for Python 3

if __name__=='__main__':
    t=int(input())
    for _ in range(t):
        N=int(input())
        ob=Solution()
        ans=ob.nFibonacci(N)
        for i in ans:
            print(i,end=" ")
        print()
# } Driver Code Ends

