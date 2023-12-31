import argparse
import sys

import pandas as pd
import numpy as np

from netZooPy.dragon import Scale, \
    estimate_penalty_parameters_dragon, \
    get_partial_correlation_dragon, \
    estimate_p_values_dragon


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', dest='matrix_a')
    parser.add_argument('-b', dest='matrix_b')
    parser.add_argument('-s', dest='sample_arrangement')
    return parser.parse_args()


def read_matrix(fpath):
    '''
    Reads the tab-delimited file at `fpath` and
    returns a pandas DataFrame. 
    '''
    return pd.read_table(fpath, sep='\t', index_col=0)


if __name__ == '__main__':
    args = parse_args()

    # Both of these matrices have N cols. The number
    # of rows/features is different, in general.
    df_a = read_matrix(args.matrix_a)
    df_b = read_matrix(args.matrix_b)

    if args.sample_arrangement == 'sample ID':
        # first check that the column sets are equivalent. If
        # not, fail immediately. We are strict here and won't
        # allow proper subsets
        diff_set = df_a.columns.symmetric_difference(df_b.columns)
        if len(diff_set) > 0:
            sys.stderr.write('Given your input option indicating that'
                ' the matrix columns should be compared by sample ID,'
                ' we require strict equivalence of sample IDs in both'
                ' matrices. We found the following samples which were'
                ' only represented in one of the matrices:'
                f' {", ".join(diff_set)}')
            sys.exit(1)
        else:
            # column sets were equivalent. Re-order the columns
            # of matrix B to match that of matrix A:
            df_b = df_b[df_a.columns]

    # zero-variance and nan values can cause issues downstream. Remove
    # these features.

    # calculate the std dev of each feature/row
    df_a_std = np.std(df_a.values, axis=1)
    df_b_std = np.std(df_b.values, axis=1)

    # check if the variance is smaller than the machine epsilon
    var_too_small_a = df_a_std < sys.float_info.epsilon
    var_too_small_b = df_b_std < sys.float_info.epsilon

    # can also have nan values so flag those
    var_is_na_a = np.isnan(df_a_std)
    var_is_na_b = np.isnan(df_b_std)

    # remove the rows/features which are either effectively
    # zero variance or nan
    keep_a = (~var_too_small_a) & (~var_is_na_a)
    keep_b = (~var_too_small_b) & (~var_is_na_b)
    df_a = df_a.iloc[keep_a]
    df_b = df_b.iloc[keep_b]

    # We need to transpose the dataframes
    # such that the features are in the COLUMNS,
    # which is transpose of the typical convention of WebMeV
    # where we have genes x samples in rows x columns, respectively.
    matrix_a = Scale(np.transpose(df_a.values))
    matrix_b = Scale(np.transpose(df_b.values))

    N0 = matrix_a.shape[0]
    N1 = matrix_b.shape[0]
    if N0 != N1:
        sys.stderr.write('The input matrices should have the same number'
                         f' of samples. We found {N0} and {N1} samples.'
                         ' Please check this.')
        sys.exit(1)

    feature_num_a = matrix_a.shape[1]
    feature_num_b = matrix_b.shape[1]

    lambdas, \
        lambdas_landscape = estimate_penalty_parameters_dragon(
                                        matrix_a, matrix_b)

    partial_corr = get_partial_correlation_dragon(matrix_a, matrix_b, lambdas)
    try:
        adj_p_vals, p_vals = estimate_p_values_dragon(partial_corr,
                                                  N0,
                                                  feature_num_a,
                                                  feature_num_b,
                                                  lambdas)
    except ValueError:
        sys.stderr.write('Caught an error which occurred during calculation of'
            ' the significant values. Sometimes, this can be caused by too few'
            ' samples.')
        sys.exit(1)
    
    # create dataframes from those numpy arrays:
    combined_index = np.hstack([df_a.index, df_b.index])
    partial_corr_df = pd.DataFrame(partial_corr,
                                   index=combined_index,
                                   columns=combined_index)
    padj_df = pd.DataFrame(adj_p_vals,
                                   index=combined_index,
                                   columns=combined_index)
    partial_corr_df.to_csv('dragon_partial_correlations.tsv', sep='\t')
    padj_df.to_csv('dragon_adj_pvals.tsv', sep='\t')
    
