import pandas as pd
from .settings import BACKEND_DIR



def getTweetsByCategory(cat):
    train_filepath = BACKEND_DIR + "/outs/valid.test"
    df = pd.read_table(train_filepath, encoding="ISO-8859-1", header=None)

    df.columns = ['tweet_id', 'text', 'classification']

    #pred_filepath = BACKEND_DIR + "/svm_multiclass/pred3.out"
    pred_filepath = BACKEND_DIR + "/svm_multiclass_linux64/pred3.out"
    df_p = pd.read_table(pred_filepath, encoding="ISO-8859-1", header=None, sep=" ", usecols=[0])

    df_new = pd.concat([df, df_p], axis=1)

    df_new.columns = ['ID', 'TWEET', 'CATEGORY', 'CAT']
    filter = 'CAT=='+cat
    result_df = df_new[['TWEET', 'CAT']].query(filter)
    res = list(result_df['TWEET'])
    return res

