import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

def top_correlated(df, nb_features, threshold, correlation_method=3):
    """Select top 20 correlated features from DataFrame"""
    # select settle prices only
    keep_col = [0, 2] + list(range(7, 557, 4))
    selected_columns = df.iloc[:, keep_col].columns
    
    # compute correlation matrix
    df_cor = pd.DataFrame(columns=['pearson', 'spearman', 'kendall'])
    df_cor['pearson'] = df[selected_columns].corr(method='pearson')['p1']
    df_cor['spearman'] = df[selected_columns].corr(method='spearman')['p1']
    df_cor['kendall'] = df[selected_columns].corr(method='kendall')['p1']
    df_cor['score'] = (abs(df_cor['pearson']) + abs(df_cor['spearman']) 
        + abs(df_cor['kendall'])) / 3
    
    # sort depending on the correlation_method 
    col = df_cor.columns[correlation_method]
    df_cor_sorted = df_cor.sort_values(by=col, ascending=False)[col]    
    
    # retrieve the top nb_features correlated with p1
    selected_features = df_cor_sorted.index[:nb_features] 
    
    # eliminate features that are too correlated to each other
    df_cor_count = df_cor.loc[selected_features].copy()
    df_cor_count[df_cor_count < threshold] = 0
    df_cor_count[df_cor_count >= threshold] = 1
    df_cor_count = df_cor_count.sum(axis=1)
    df_cor_count = df_cor_count[df_cor_count > 0]
    df_cor_count = df_cor_count.sort_values(ascending=False)
    
    # keep 20 at most
    limit = min(20, len(df_cor_count))
    selected_features = df_cor_count.index[:limit]

    return selected_features

def pca_selection(df, n=20):
    """Perform PCA to reduce then number of features"""
    # first scale data
    X = df.values
    scaler = StandardScaler()
    X_sc = scaler.fit_transform(X)
    
    # PCA
    pca = PCA(n_components=n)
    X_pca = pca.fit_transform(X_sc)
    
    return pd.DataFrame(X_pca, index=df.index)

def reformat_as_sequence(df, input_seq_len, output_seq_len):
    """Reformat the dataframe with rows as sequences"""
    # columns of the reformatted dataframe
    cols= ['date_t']
    for i in range(input_seq_len-1, 0, -1):
        cols += ['p1_(t-{})'.format(i)]
    cols += ['p1_t']
    for i in range(1, output_seq_len+1):
        cols += ['p1_(t+{})'.format(i)]
    df_reformat = pd.DataFrame(columns=cols)
    
    # t will slide through the time series and create a row
    lim = len(df) - output_seq_len
    for t in range(input_seq_len, lim):
        row = [df['date'].iloc[t]] + list(df['p1'].iloc[t-input_seq_len:t+output_seq_len].values)
        df_reformat.loc[t] = row
    return df_reformat