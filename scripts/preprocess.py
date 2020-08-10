import sys
import os
import re
import logging
import gc

import pandas as pd
import numpy as np

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s:%(levelname)s:%(message)s",
                    datefmt="%m/%d/%Y %I:%M:%S")

logger = logging.getLogger(__name__)

DATA_PATH = '../data/'

def read_df(filename):
    logger.info(f"Loading csv file {filename} to memory.")

    filepath = os.path.join(DATA_PATH, 'raw', filename)
    df = (
        pd.read_csv(filepath, engine='c', parse_dates=['time'])
          .assign(turnstile=lambda df: df['ca'] + '-' + df['unit'] + '-' + df['scp'])
    )

    return df


def create_diff_df(df):
    logger.info("Creating df with diff calculation for entries and exits.")

    df_diff = (
        df
        .set_index(['turnstile', 'time'])[['entries', 'exits']]
        .groupby('turnstile')
        .diff()
    )

    return df_diff


def filter_out_inconsistencies(df, upper):
    logger.info("Removing inconsistencies for series.")

    for col in ['entries', 'exits']:
        df[col] = df[col].where(df[col] > 0, 0)
        df[col] = df[col].where(df[col] < upper, 0)

        logger.info(f"Negative values and higher than 10,000 being replaced by zero for {col}")
    
    return df

def capping_outliers(df):
    logger.info("Capping outliers after removing inconsistencies.")

    for col in ['entries', 'exits']:
        _, upper = np.percentile(df[col].dropna().values, [1, 99])

        df[col] = df[col].clip(lower=0, upper=upper)
        logger.info(f"Clipping outliers for {col}. Boundary values: {(0, upper)}")
    
    return df

def resample(df, frequency):
    logger.info(f"Resampling data to frequency: {frequency}")

    df_resampled = (
        df
        .groupby([pd.Grouper(freq=frequency, level='time'), 'turnstile']).sum()
    )

    return df_resampled

def merge(df_raw, df_resampled):
    logger.info("Merging resampled data set with original one to get station, linename, and division columns")

    original_cols = ['turnstile', 'station', 'linename', 'division']

    df_filtered = (
        df_raw
            .loc[:, original_cols]
            .drop_duplicates(subset='turnstile')
            .set_index("turnstile")
    )

    df_merged = (
        df_resampled
            .join(df_filtered)
            .reset_index()
    )
    
    assert df_merged.shape[0] == df_resampled.shape[0]

    return df_merged
def save_data(df, year):
    logger.info(f"Saving new preprocessed data.")

    filename = f"{year}_resampled.csv.gz"
    filepath = os.path.join(DATA_PATH, 'preprocessed', filename)
    
    df.to_csv(filepath, 
              compression='gzip',
              index=False)


if __name__=='__main__':
    logger.info("Starting program.")
    
    filenames, frequency = sys.argv[1:-1], sys.argv[-1]

    for filename in filenames:
        year_regex = re.compile(re.compile(r'(\d+).csv.gz'))
        year_groups = year_regex.findall(filename)

        UPPER = 10_000
        logger.info(f"Processing file for year: {year_groups[0]}")

        if year_groups:
            df_raw = read_df(filename)
            df = create_diff_df(df_raw)
            df = filter_out_inconsistencies(df, UPPER)
            df = capping_outliers(df)
            df_resampled = resample(df, frequency)
            df_merged = merge(df_raw, df_resampled)

            save_data(df_merged, year_groups[0])

            del df_raw, df, df_resampled, df_merged
            gc.collect()
