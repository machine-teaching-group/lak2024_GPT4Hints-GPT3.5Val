def chickenpox_by_sex():
  import pandas as pd
  import numpy as np
  df = pd.read_csv('assets/data.csv', index_col=0)
  male = df[df['SEX'] == 1]
  vac_m = male[male['P_NUMVRC'] == 1]
  cpox_m = vac_m[vac_m['HAD_CPOX'] == 1]
  no_m = vac_m[vac_m['HAD_CPOX'] == 2]
  total_cpox_m = cpox_m['SEX'].count()
  total_nocpox_m = no_m['SEX'].count()
  m = total_cpox_m/total_nocpox_m

  female = df[df['SEX'] == 2]
  vac_f = female[female['P_NUMVRC'] >= 1]
  cpox_f = vac_f[vac_f['HAD_CPOX'] == 1]
  no_f = vac_f[vac_f['HAD_CPOX'] == 2]
  total_cpox_f = cpox_f['SEX'].count()
  total_nocpox_f = no_f['SEX'].count()
  f = total_cpox_f/total_nocpox_f

  ans={"male":  m,
       "female": f}

  return ans
