#User function Template for python3
class Solution:
  def merge(self, S1, S2):
    l1=len(S1)
    l2=len(S2)
    if l1>l2:
      res=""
      dif=l1-l2
      x=S1[:l2]
      y=S2
      d=[(i,j) for i,j in zip(x,y)]
      for i in d:
        for j in i:
          res+=j
      return res+S1[l2:]
    elif l1<l2:
      res=""
      dif=l2-l1
      x=S1
      y=S2[l1:]
      d=[(i,j)for i,j in zip(x,y)]
      for i in d:
        for j in i:
          res+=j
      return res+S2[l1:]
    else:
      res=""
      x=S1
      y=S2
      d=[(i,j)for i,j in zip(x,y)]
      for i in d:
        for j in i:
          res+=j
      return res

#{ Driver Code Starts
#Initial Template for Python 3
if __name__ == '__main__':
    t = int(input())
    for _ in range(t):
        S1,S2 = map(str,input().strip().split())
        ob = Solution()
        print(ob.merge(S1, S2))
# } Driver Code Ends