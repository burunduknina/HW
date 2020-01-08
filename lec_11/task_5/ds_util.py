import argparse
import os
import re

import validators


def create_parser():
    parser = argparse.ArgumentParser(
        description='''Utility to help data scientists train models.'''
    )

    parser.add_argument(
        '-m', '--model',
        required=True,
        choices=['DT', 'RF', 'GBM', 'PCA'],
        type=str,
        help='Model name. Possible values: DT, RF, GBM, PCA',
    )

    parser.add_argument(
        '-sp', '--splitter',
        choices=['best', 'random'],
        default='best',
        type=str,
        help='The strategy used to choose the split at each node. '
             'Used for DT model.',
    )

    parser.add_argument(
        '-cr', '--criterion',
        choices=['gini', 'entropy'],
        default='gini',
        type=str,
        help='The function to measure the quality of a split.'
             'Used for DT, RF and GBM models.',
    )

    parser.add_argument(
        '-md', '--max_depth',
        default=3,
        type=int,
        help='Maximum depth of the individual regression estimators.'
             'Used for DT, RF and GBM models.',
    )

    parser.add_argument(
        '-mf', '--max_features',
        type=str,
        help='The number of features to consider when looking for the best '
             'split. Used for DT, RF and GBM models.',
    )

    parser.add_argument(
        '-msl', '--min_samples_leaf',
        default=1.0,
        type=float,
        help='The minimum number of samples required to be at a leaf node.'
             'Used for DT, RF and GBM models.',
    )

    parser.add_argument(
        '-mss', '--min_samples_split',
        default=2.0,
        type=float,
        help='The minimum number of samples required to split an internal node'
             'Used for DT, RF and GBM models.',
    )

    parser.add_argument(
        '-ne', '--n_estimators',
        default=100,
        type=int,
        help='The number of trees in the forest. Used for RF and GBM models.',
    )

    parser.add_argument(
        '-lo', '--loss',
        choices=['deviance', 'exponential'],
        default='deviance',
        type=str,
        help='Loss function to be optimized. Used for GBM model.',
    )

    parser.add_argument(
        '-lr', '--learning_rate',
        default=0.1,
        type=float,
        help='Learning rate shrinks the contribution of each tree.'
             'Used for GBM model.',
    )

    parser.add_argument(
        '-ss', '--subsample',
        default=1.0,
        type=float,
        help='The fraction of samples to be used for fitting the individual '
             'base learners. Used for GBM model.',
    )

    parser.add_argument(
        '-nc', '--n_components',
        type=int,
        help='Number of measurements. Used for PCA model.',
    )

    parser.add_argument(
        '-i', '--input',
        required=True,
        type=str,
        help='Path to input dataset.',
    )

    parser.add_argument(
        '-o', '--output',
        type=str,
        help='Path to the folder where the trained model will be stored.',
    )

    parser.add_argument(
        '-c', '--compression',
        type=str,
        help='Compression algorithm for trained model',
    )

    return parser


def check_input(path):
    if not os.path.exists(path):
        raise ValueError('Incorrect input path.')
    elif os.path.isfile(path) \
            and re.search(r'\.\w+$', path).group(0) not in EXT:
        raise ValueError('Invalid input file format.')
    return path


def check_output(path):
    if path is None:
        return '.'
    if os.path.exists(path):
        if not os.path.isdir(path):
            raise ValueError(
                'Output path should lead to the folder, not to the file.')
    elif not validators.url(path) or path.find('s3') == -1:
        raise ValueError('Output should be exist folder or valid s3 url.')
    return path


if __name__ == '__main__':
    EXT = ['.csv', '.parquet', '.json', '.tar.gz', '.tar.bz2', '.zip', '.py']
    ds_parser = create_parser()
    namespace = ds_parser.parse_args()
    input_path = check_input(namespace.input)
    output_path = check_output(namespace.output)
