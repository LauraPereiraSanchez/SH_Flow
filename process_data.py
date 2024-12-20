import glob
import argparse
import uproot
import pandas  as pd
import matplotlib.pyplot as plt


def parse():

    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--directory", type=str, default="/fs/ddn/sdf/group/atlas/d/lapereir/SH/Signals_NormFlows/")
    parser.add_argument("-t", "--tree_name", type=str, default="CollectionTree")


    return parser.parse_args()


def GetParameters(sample_name, var=False):

    if var == True:

        sample_name = sample_name.split("_X")[-1]

        X = int(sample_name.split("_S")[0])

        S = int(sample_name.split("_S")[-1])

        return X, S, 0
    
    # defined for sample names format:
    #          mc16d.Py8_XHS_X875_S200_HyySbb_AF2.root

    sample_name = sample_name.split("/")[-1]
    
    c = sample_name.split(".")[0] # campaign

    X = int(sample_name.split("_")[2].split("X")[-1])

    S = int(sample_name.split("_")[3].split("S")[-1])

    return X, S, c
    

def main():

    cfg = parse()

    paths = glob.glob(cfg.directory+"/mc16e*.root")

    presel = "((HGamEventInfoAuxDyn.isPassed == 1) & (HGamEventInfoAuxDyn.yybb_btag77_cutFlow > 6) & (HGamEventInfoAuxDyn.m_yy*0.001 > 120) & (HGamEventInfoAuxDyn.m_yy*0.001 < 130))"

    #variables = ["HGamEventInfoAuxDyn.crossSectionBRfilterEff","HGamEventInfoAuxDyn.weight","HGamEventInfoAuxDyn.yybb_weight", ,"HGamEventInfoAuxDyn.weightFJvt"]

    variables = ["EventInfoAuxDyn.eventNumber"]

    dataframes = []

    for path in paths:

        for s in final_1bjet:
            if s in path:
                paths.remove(path)
                continue

        print(path)
        mX, mS, c =  GetParameters(path)
        #variables.append("HGamEventInfoAuxDyn.yybb_SH_BCal_PNN_Score_X"+str(mX)+"_S"+str(mS))
        tmp_variables = variables + ["HGamEventInfoAuxDyn.yybb_SH_BCal_PNN_Score_X"+str(mX)+"_S"+str(mS)]
    
        #print("variables to add ")
        #print(variables)

        #for path in paths:

        
        with uproot.open(path+":"+cfg.tree_name) as t:

            try:
                tmp_variables = variables + ["HGamEventInfoAuxDyn.yybb_SH_BCal_PNN_Score_X"+str(mX)+"_S"+str(mS)]
                df = t.arrays(tmp_variables, presel, library="pd")
            except:
                continue

        old_names = df.columns

        real_mX, real_mS, c =  GetParameters(path)

        for v in old_names:

            if "PNN" in v: 
                
                df = df.rename(columns={v: "PNN_score"})

                mX, mS, _ =  GetParameters(v, var=True)
                
                df["target_mX"] = mX
                
                df["target_mS"] = mS
                
                df["mode"] = 0

                if (mX == real_mX) and (mS == real_mS):
                    df["mode"] = 1
                
            if "eventNumber" in v:
                df = df.rename(columns={v: "eventNumber"})

        df["real_mX"] = real_mX

        df["real_mS"] = real_mS

        df["mc"] = c

        df["signal"] = "X"+str(real_mX)+"_S"+str(real_mS)
        
        dataframes.append(df)

        #print(df.columns)
        #print(df)

    final_df = pd.concat(dataframes, ignore_index=True)

    #final_df[final_df["eventNumber"] % 4 >3]
    
    print(final_df)

    final_df.to_parquet("data.parquet", engine="fastparquet")  # Specify the Parquet engine

    #combined_set = set(final_df["real_mX"].astype(str) + "_" + final_df["real_mS"].astype(str))
    combined_set = set(final_df["signal"])
    

    print(combined_set)


    # Count occurrences of unique values in the column
    value_counts = final_df["signal"].value_counts()
    
    # Create a pie chart
    plt.figure(figsize=(6, 6))
    plt.pie(value_counts, labels=value_counts.index, autopct='%1.1f%%')
    plt.title("Signals")
    plt.savefig("signals.png", format="png", dpi=300)  # Save as PNG with high resolution   

    return


final_1bjet = [
"X190_S15",
"X200_S15",
"X210_S15",
"X220_S15",
"X230_S15",
"X240_S15",
"X250_S15",
"X350_S30",
"X375_S30",
"X400_S30",
"X425_S30",
"X450_S30",
"X475_S30",
"X500_S30",
"X525_S40",
"X550_S40",
"X550_S50",
"X575_S40",
"X575_S50",
"X600_S40",
"X600_S50",
"X650_S50",
"X700_S50",
"X750_S50",
"X800_S70",
"X850_S70",
"X900_S70",
"X950_S70",
"X1000_S70"
]


if __name__ == "__main__":
    main()

