"""
Preprocess the wine quality dataset to prepare it for modeling.

The following steps are taken:
    * Add a categorical quality column based on the quality score
    * Split the data into train and test sets
    * Take all interactions between features plus original variables
    * Use feature selection library to eliminate duplicates and highly correlated features
"""
#%%
import argparse
import os
from itertools import combinations
import pandas as pd
from sklearn.model_selection import train_test_split
from feature_engine.selection import DropConstantFeatures, DropCorrelatedFeatures  # for dropping redundant features
from config_loader import PROJECT_ROOT, RAW_DATA_FILE

OUTPUT_DIR = PROJECT_ROOT / 'data' / 'processed'
OUTPUT_FILE = OUTPUT_DIR / 'winequality-red-processed.csv'

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)


def load_data(input_file: str) -> pd.DataFrame:
    return pd.read_csv(input_file)


def add_quality_category(df: pd.DataFrame) -> pd.DataFrame:
    df['quality_category'] = pd.cut(df['quality'], bins=[0, 4, 6, 10], labels=['low', 'mid', 'high'])
    return df


def add_interactions(df_in: pd.DataFrame) -> pd.DataFrame:

    df = df_in.copy()

    df.columns = ['_'.join(c.split()) for c in df.columns]

    # include all features in interaction terms since all are nonnull, continuous numeric
    feature_cols = [c for c in df.columns if c not in ('quality', 'quality_category')]

    # loop over non-repeated combinations of 2 features to get product
    for feat1, feat2 in combinations(feature_cols, 2):

        interaction_name = '|'.join([feat1, feat2])
        df[interaction_name] = df[feat1] * df[feat2]
    
    return df

def drop_redundant_features(df_in: pd.DataFrame) -> pd.DataFrame:

    df = df_in.copy()
    # preserve label column
    df_labels = df[['quality']]
    df_feat = df.drop(labels=['quality'], axis=1)

    orig_cols = df_feat.columns

    df_feat = DropConstantFeatures(tol=.98).fit_transform(df_feat)
    df_feat = DropCorrelatedFeatures(threshold=0.9, method='pearson').fit_transform(df_feat)

    # print the features that were dropped
    dropped_cols = set(df_feat.columns) - set(orig_cols)
    print(f"Features dropped for redundancy: {dropped_cols}")

    df = pd.concat([df_labels, df_feat], axis=1)

    return df

def split_data(df_in: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:

    df = df_in.copy()

    _, X_test, _, _ = train_test_split(
        df.drop(labels=['quality', 'quality_category'], axis=1),
        df['quality'],
        stratify=df['quality_category'],
        test_size=0.2
    )
    # add column that identifies test set
    df['test_set'] = False
    df.loc[X_test.index, 'test_set'] = True

    return df


def main(output_file: str):
    df = load_data(RAW_DATA_FILE)
    df = drop_redundant_features(df)
    df = add_quality_category(df)
    df = add_interactions(df)
    df = split_data(df)
    df.to_csv(output_file, index=False)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output_file', type=str, default=OUTPUT_FILE)
    args = parser.parse_args()
    main(args.output_file)