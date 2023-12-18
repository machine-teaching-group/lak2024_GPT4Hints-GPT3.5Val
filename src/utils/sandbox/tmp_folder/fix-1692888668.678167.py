def chickenpox_by_sex():
    import pandas as pd

    df = pd.read_csv("assets/NISPUF17.csv")
    return {
        "male": len(df[(df["P_NUMVRC"] >= 1) & (df["HAD_CPOX"] == 1) & (df["SEX"] == 1)])
        / len(df[(df["P_NUMVRC"] >= 1) & (df["HAD_CPOX"] == 2) & (df["SEX"] == 1)]),
        "female": len(df[(df["P_NUMVRC"] >= 1) & (df["HAD_CPOX"] == 1) & (df["SEX"] == 2)])
        / len(df[(df["P_NUMVRC"] >= 1) & (df["HAD_CPOX"] == 2) & (df["SEX"] == 2)]),
    }
    raise NotImplementedError()
