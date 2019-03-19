import numpy as np
import pandas as pd

def melt_symmetric_matrix(df, value_name = 'value',
                          drop_diag = True, ascending = False):
    """Melt and sort a symmetric DataFrame

    Useful for pd.DataFrame.corr(), pd.DataFrame.covar(), etc.

    returns: pd.DataFrame
    """
    assert np.allclose(df, df.T, atol=1e-8), 'df failed symmetry check'

    if drop_diag:
        mask = np.tril(np.ones(df.shape)).astype(np.bool)
    else:
        mask = ~np.tril(np.ones(df.shape)).astype(np.bool)

    df = (df.mask(mask)
            .stack()
            .reset_index()
            .rename(columns={0:value_name})
            .assign(sort = lambda x: x[value_name].abs())
            .sort_values('sort', ascending=ascending)
            .drop(columns=['sort'])
            .reset_index(drop=True))

    return df
