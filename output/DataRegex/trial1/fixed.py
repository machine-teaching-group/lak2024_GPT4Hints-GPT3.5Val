def student_grades():
  import re
  with open ("assets/grades.txt", "r") as f:
    grades=f.read()

  ### FIX CODE BELOW
  re_pattern="(\w+ \w+)(?=: B)"
  matches=re.findall(re_pattern,grades)
  ### FIX CODE ABOVE

  return matches