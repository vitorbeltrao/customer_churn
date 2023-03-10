'''
Author: Vitor Abdo

This .py file is to do the ETL step to make possible the next
step that is the preprocessing and model training
'''
import logging
import pandas as pd
from sklearn.model_selection import train_test_split
from decouple import config


logging.basicConfig(
    filename='./logs/logs_system_funcs.log',
    level=logging.INFO,
    filemode='w',
    format='%(name)s - %(levelname)s - %(message)s')


# config
VARS_TO_DROP = config(
    'VARS_TO_DROP', cast=lambda v: [
        s.strip() for s in v.split(',')])
TARGET_BEFORE_ETL = config('TARGET_BEFORE_ETL')
TARGET_AFTER_ETL = config('TARGET_AFTER_ETL')
TEST_SIZE = config('TEST_SIZE', cast=float)
SEED = config('SEED', cast=int)
DATASET = config('DATASET')
TRAIN_DATASET = config('TRAIN_DATASET')
TEST_DATASET = config('TEST_DATASET')


def import_data(file_path: str) -> pd.DataFrame:
    '''Load dataset for the csv found at the path

    :param file_path: (str)
    A path to the csv

    :return: (dataframe)
    Pandas dataframe
    '''
    try:
        raw_df = pd.read_csv(file_path)
        logging.info("Execution of import_data: SUCCESS")
        return raw_df
    except FileNotFoundError:
        logging.error("Execution of import_data: The file wasn't found")
        return None


def transform_data(raw_df: pd.DataFrame) -> pd.DataFrame:
    '''Transform the raw dataset doing two steps of transformation.
    The first transformation is to transform the target variable in
    numeric. The second transformation is to drop some variables that
    we dont want to use in the model.

    :param df: (dataframe)
    The raw dataframe imported

    :return: (dataframe)
    Pandas dataframe transformed
    '''
    try:
        df_transformed = raw_df.copy()
        df_transformed[TARGET_AFTER_ETL] = raw_df[TARGET_BEFORE_ETL].apply(
            lambda val: 0 if val == "Existing Customer" else 1)
        df_transformed.drop(VARS_TO_DROP, axis=1, inplace=True)
        logging.info("Execution of transform_data: SUCCESS")
        return df_transformed
    except KeyError:
        logging.error(
            "Execution of transform_data: Any variable subject to the transformations not found")
        return None


def split_dataset(df_transformed: pd.DataFrame) -> pd.DataFrame:
    '''Function to split the transformed dataset in train and test.

    :param df_transformed: (dataframe)
    The transformed dataset

    :return:
    None
    '''
    try:
        train_set, test_set = train_test_split(
            df_transformed, test_size=TEST_SIZE, random_state=SEED)
        train_set.to_csv(TRAIN_DATASET, index=False)
        test_set.to_csv(TEST_DATASET, index=False)
        logging.info("Execution of split_dataset: SUCCESS")
        return train_set, test_set
    except OSError:
        logging.error(
            "Execution of split_dataset: Cannot save file into a non-existent directory")
        return None


if __name__ == "__main__":
    logging.info('About to start the etl step of the system')

    RAW_DF = import_data(DATASET)
    print('The import_data function has been executed')

    DF_TRANSFORMED = transform_data(RAW_DF)
    print('The transform_data function has been executed')

    split_dataset(DF_TRANSFORMED)
    print('The split_dataset function has been executed: Executed System!')
    logging.info('Done executing the etl step')