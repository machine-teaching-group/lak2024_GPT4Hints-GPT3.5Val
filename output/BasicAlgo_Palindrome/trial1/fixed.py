#User function Template for python3
class Solution:
  def reverse(self, b, e, S):
    while b < e:
      S[b], S[e] = S[e], S[b]
      e = e - 1
      b = b + 1
    return S

  def isPalindrome(self, S):
    S = list(S)
    beg = 0
    end = len(S) - 1
    rev = self.reverse(beg,end,S.copy())
    if S == rev:
      return 1
    return 0

#{ Driver Code Starts
#Initial Template for Python 3
if __name__ == '__main__':
  T=int(input())
  for i in range(T):
    S = input()
    ob = Solution()
    answer = ob.isPalindrome(S)
    print(answer)
# } Driver Code Ends