# -*- coding: utf-8 -*-
"""
Created on Tue Jul 13 10:14:53 2021

@author: VTulus
"""
# other possible detection methods (currently not implemented)
# Univariate analysis:
# log-IQ method: taking log of data and then tukey_method
# z-score
# Median Absolute Deviation (MAD) method
# ???
# Multivariate analysis:
# Mahalanobis Distance method
# Robust Mahalanobis Distance method
# ???

__all__ = [
    # "tukey_method",
    # "tukey_method_bulk",
    # "mahalanobis_method",
    # "robust_mahalanobis_method",
    "make_full_df_after_outlier_detection_method",
]

import numpy as np
import pandas as pd
from scipy import stats
from sklearn.covariance import MinCovDet

# TODO: combine separate funcs into class methods


class OutlierDetector:
    def __init__(self, df_raw: pd.DataFrame) -> None:
        """
        Parameters
        ----------
        df_raw : pd.DataFrame
            DataFrame with at least 1 column with numerical data for outlier detection
        """
        self.df_raw = df_raw.copy()

    # TODO: combine `tukey_method` and `tukey_method_bulk` into 1 method
    # it should accept a list of column labels and fence str
    # and return df_treated, df_outliers and dict with k=column label, v=list of outliers
    # commented for now

    # def tukey_method(self, colname: str):
    #     """Return two lists of indices containing possible and probable outliers.

    #     Perform univariate detection of outliers based on Tukey's rule
    #     (https://www.wikiwand.com/en/Outlier) and return 2 lists of indices:
    #     1º list - indices (as in `self.df_raw`) of PROBABLE outliers,
    #         i.e. those laying "far out" (outside the outer fence).
    #     2º list - indices (as in `self.df_raw`) of POSSIBLE outliers,
    #         i.e. those laying outside the inner fence.
    #     Outer fence is defined as [Q1–3*IQR, Q3+3*IQR]
    #     Inner fence is defined as [Q1-1.5*IQR, Q3+1.5*IQR]
    #     For the list of POSSIBLE outliers the tighter fence is used,
    #     the list contains also all the PROBABLE outliers!

    #     Parameters
    #     ----------
    #     colname : str
    #         Column label where outliers have to be detected
    #         (only numeric values in column)

    #     Returns
    #     -------
    #     outliers_prob : list
    #         List of indices of probable outliers
    #     outliers_poss : list
    #         List of indices of possible outliers (contains also outliers_prob)

    #     References
    #     ----------
    #     Stephanie Glen. "Upper and Lower Fences"
    #         From StatisticsHowTo.com: Elementary Statistics for the rest of us!
    #         https://www.statisticshowto.com/upper-and-lower-fences/
    #     https://towardsdatascience.com/detecting-and-treating-outliers-in-python-part-1-4ece5098b755
    #     """
    #     if colname not in self.df_raw.columns:
    #         raise ValueError(
    #             "Passed `colname` not in ´self.df_raw.columns´. An existing column label must be passed."
    #         )
    #     # quartile 1 (25%) # pylint: disable=invalid-name
    #     Q1 = self.df_raw[colname].quantile(0.25)
    #     # quartile 3 (75%) # pylint: disable=invalid-name
    #     Q3 = self.df_raw[colname].quantile(0.75)
    #     # median = df_raw[colname].median()  # or quantile(0.50)
    #     IQR = Q3 - Q1  # inter-quartile range # pylint: disable=invalid-name
    #     inner_fence = 1.5 * IQR
    #     outer_fence = 3 * IQR
    #     # inner fence lower and upper end
    #     inner_fence_le = Q1 - inner_fence
    #     inner_fence_ue = Q3 + inner_fence
    #     # outer fence lower and upper end
    #     outer_fence_le = Q1 - outer_fence
    #     outer_fence_ue = Q3 + outer_fence

    #     outliers_prob = []
    #     outliers_poss = []
    #     for index in self.df_raw[colname].index:
    #         check_value = self.df_raw[colname][index]  # value from self.df_raw[colname]
    #         if check_value <= outer_fence_le or check_value >= outer_fence_ue:
    #             outliers_prob.append(index)
    #     for index in self.df_raw[colname].index:
    #         check_value = self.df_raw[colname][index]  # value from self.df_raw[colname]
    #         if check_value <= inner_fence_le or check_value >= inner_fence_ue:
    #             outliers_poss.append(index)

    #     return outliers_prob, outliers_poss

    # def tukey_method_bulk(self, outlier_detection_fence="tight"):
    #     """Split `self.df_raw` in two dataframes: (1)-filtered data, (2)-detected outliers.

    #     Perform univariate detection of outliers (https://www.wikiwand.com/en/Outlier)
    #     based on Tukey's rule for EACH OF the columns of the `self.df_raw` and return 2 dataframes:
    #     1º dataframe - with the shape of `self.df_raw` contains only filtered data (no outliers)
    #     2º dataframe - with the shape of `self.df_raw` contains only detected outliers.

    #     Parameters
    #     ----------
    #     self.df_raw : pandas.DataFrame
    #         Dataframe containing data of interest with (possible) outliers
    #         (only columns with numpy.numeric are accepted, otherwise ValueError is raised)
    #     outlier_detection_fence : str, default "tight"
    #         "tight"   sets all points outside inner fence (outside [Q1-1.5*IQR, Q3+1.5*IQR]) as outliers
    #         "relaxed" sets all points outside outer fence (outside [Q1–3.0*IQR, Q3+3.0*IQR]) as outliers

    #     Returns
    #     -------
    #     df_treated : pandas.DataFrame
    #         Dataframe (with shape of `self.df_raw`) containing only filtered data,
    #         empty cells are `np.nan`
    #     df_outliers : pandas.DataFrame
    #         Dataframe (with shape of `self.df_raw`) containing only detected outliers,
    #         empty cells are `np.nan`

    #     Note
    #     ----
    #     This function uses `tukey_method`
    #     """
    #     if self.df_raw.shape[1] > self.df_raw.select_dtypes(include=np.number).shape[1]:
    #         raise ValueError(
    #             "Passed `self.df_raw` contains non-numeric columns. "
    #             "Only `self.df_raw` with numeric columns is accepted!"
    #         )
    #     df_treated = self.df_raw.copy()
    #     df_outliers = self.df_raw.copy()

    #     for label in self.df_raw.columns:
    #         outliers_prob, outliers_poss = tukey_method(
    #             self.df_raw=self.df_raw, colname=label
    #         )  # call `tukey_method`
    #         if outlier_detection_fence == "tight":
    #             list_outliers = outliers_poss
    #         elif outlier_detection_fence == "relaxed":
    #             list_outliers = outliers_prob
    #         else:
    #             raise ValueError(
    #                 "Wrong `outlier_detection_fence` parameter."
    #                 "\n\t It can be either 'tight' for a fence using 1.5*IQR"
    #                 "\n\t or 'relaxed' for a fence using 3.0*IQR."
    #             )
    #         list_non_outliers = list(set(list(self.df_raw.index)) - set(list_outliers))
    #         df_treated.loc[list_outliers, label] = np.nan
    #         df_outliers.loc[list_non_outliers, label] = np.nan
    #     df_treated.sort_index(inplace=True)
    #     df_outliers.sort_index(inplace=True)
    #     return df_treated, df_outliers

    def mahalanobis_method(
        self, df_raw, alpha=0.001
    ):  # pylint: disable=too-many-locals
        """Split `df_raw` in two dataframes: (1)-filtered data, (2)-detected outliers.

        Perform multivariate detection of outliers (https://www.wikiwand.com/en/Outlier)
        based on Mahalanobis distances (MD) for ALL the columns of the `df_raw`
        and return 2 dataframes:
        1º dataframe - contains only filtered data (no outliers) + column with computed p_values
        2º dataframe - with the shape [`df_raw`rows, `df_raw`columns+1] contains
            only detected outliers + column with computed p_values

        Parameters
        ----------
        df_raw : pandas.DataFrame
            Dataframe containing data of interest with (possible) outliers,
            the multivariate detection algorithm will consider all passed columns
            in MD calculation (only columns with np.numeric are accepted,
                            otherwise ValueError is raised)
        alpha : float, default 0.001
            Significance level, the probability of the study rejecting the null hypothesis,
            given that the null hypothesis was assumed to be true

        Returns
        -------
        df_treated : pandas.DataFrame
            Dataframe containing only filtered data and a new column with computed p_values
        df_outliers : pandas.DataFrame
            Dataframe containing only detected outliers and a new column with computed p_values
        (outliers_ids, MD, cv) : tuple
            outliers_ids : list
                Sorted list of indices (as in `df_raw`) of detected outliers
            MD : Series
                Series of computed Mahalanobis distances
            cv : float
                Critical value of the Chi-squared distribution with k degrees of
                freedom and alpha significance level (k=number of independet variables)

        References
        ----------
        add...

        Adapted from
        ------------
        https://towardsdatascience.com/multivariate-outlier-detection-in-python-e946cfc843b3
        https://towardsdatascience.com/detecting-and-treating-outliers-in-python-part-2-3a3319ec2c33
        https://www.machinelearningplus.com/statistics/mahalanobis-distance/
        """
        if df_raw.shape[1] > df_raw.select_dtypes(include=np.number).shape[1]:
            raise ValueError(
                "Passed `df_raw` contains non-numeric columns. "
                "Only df_raw with numeric columns is accepted!"
            )
        # Compute M-Distance
        x_minus_mu = df_raw - np.mean(df_raw)
        x_minus_mu_trans = x_minus_mu.T
        cov = df_raw.cov()  # Covariance matrix
        inv_covmat = pd.DataFrame(np.linalg.inv(cov.values), cov.columns, cov.index)
        mahal = x_minus_mu.dot(inv_covmat).dot(x_minus_mu_trans)
        MDsquared = pd.Series(  # pylint: disable=invalid-name
            np.diag(mahal), index=mahal.index
        )
        MD = pd.Series(
            np.sqrt(MDsquared), index=MDsquared.index  # pylint: disable=invalid-name
        )
        # Compute P-Values
        p_value = pd.Series(
            1 - stats.chi2.cdf(MDsquared, df=df_raw.shape[1]), index=MDsquared.index
        )
        # Compute critival value
        cv = stats.chi2.ppf(  # pylint: disable=invalid-name
            (1 - alpha), df=df_raw.shape[1]
        )  # critical value, with degrees of freedom = number of variables
        # Detect outliers
        # either using p_values
        #     p_outliers = []
        #     for index in p_value.index:
        #         p = p_value[index]
        #         if p <= alpha:
        #             p_outliers.append(index)
        #             print(index, p)
        #         else:
        #             continue
        # or using the cv
        list_outliers = []
        for index in MDsquared.index:
            value = MDsquared[index]
            if value > cv:  # reject H0 hypothesis which is "value is not an outlier"
                list_outliers.append(index)
            else:
                continue
        list_non_outliers = list(set(list(df_raw.index)) - set(list_outliers))

        df_treated = df_raw.loc[list_non_outliers]
        df_treated["p_value"] = p_value[list_non_outliers]
        df_outliers = df_raw.loc[list_outliers]
        df_outliers["p_value"] = p_value[list_outliers]

        return df_treated, df_outliers, (sorted(list_outliers), MD, cv)


def robust_mahalanobis_method(
    df_raw, alpha=0.001, support_fraction=None
):  # pylint: disable=too-many-locals
    """Split `df_raw` in two dataframes: (1)-filtered data, (2)-detected outliers.

    Perform multivariate detection of outliers (https://www.wikiwand.com/en/Outlier)
    based on Mahalanobis distances (MD) and robust covariance determinant (RCD)
    for ALL the columns of the `df_raw` and return 2 dataframes:
    1º dataframe - contains only filtered data (no outliers) + column with computed p_values
    2º dataframe - with the shape [`df_raw`rows, `df_raw`columns+1] contains
        only detected outliers + column with computed p_values

    Parameters
    ----------
    df_raw : pandas.DataFrame
        Dataframe containing data of interest with (possible) outliers,
        the multivariate detection algorithm will consider all passed columns
        in MD calculation (only columns with np.numeric are accepted,
                           otherwise ValueError is raised)
    alpha : float, default 0.001
        Significance level, the probability of the study rejecting the null hypothesis,
        given that the null hypothesis was assumed to be true
    support_fraction : float, default None
        description reproduced from `MinCovDet`:
        "The proportion of points to be included in the support of the raw
        MCD estimate. Default is None, which implies that the minimum value
        of support_fraction will be used within the algorithm:
        `(n_sample + n_features + 1) / 2`.
        The parameter must be in the range (0, 1)."

    Returns
    -------
    df_treated : pandas.DataFrame
        Dataframe containing only filtered data and a new column with computed p_values
    df_outliers : pandas.DataFrame
        Dataframe containing only detected outliers and a new column with computed p_values
    (outliers_ids, MD, cv) : tuple
        outliers_ids : list
            Sorted list of indices (as in `df_raw`) of detected outliers
        MD : Series
            Series of computed Mahalanobis distances
        cv : float
            Critical value of the Chi-squared distribution with k degrees of
            freedom and alpha significance level (k=number of independet variables)

    References
    ----------
    add...

    Adapted from
    ------------
    https://towardsdatascience.com/detecting-and-treating-outliers-in-python-part-2-3a3319ec2c33
    """
    if df_raw.shape[1] > df_raw.select_dtypes(include=np.number).shape[1]:
        raise ValueError(
            "Passed `df_raw` contains non-numeric columns. "
            "Only df_raw with numeric columns is accepted!"
        )
    # Compute minimum covariance determinant
    rng = np.random.RandomState(0)  # pylint: disable=no-member
    real_cov = np.cov(df_raw.values.T)
    X = rng.multivariate_normal(
        mean=np.mean(df_raw, axis=0),  # pylint: disable=invalid-name
        cov=real_cov,
        size=506,
    )
    cov = MinCovDet(random_state=0, support_fraction=support_fraction).fit(X)
    mcd = cov.covariance_  # robust covariance metric
    robust_mean = cov.location_  # robust mean
    inv_covmat = pd.DataFrame(np.linalg.inv(mcd), df_raw.columns, df_raw.columns)

    # Compute M-Distance
    x_minus_mu = df_raw - robust_mean
    x_minus_mu_trans = x_minus_mu.T
    mahal = x_minus_mu.dot(inv_covmat).dot(x_minus_mu_trans)
    MDsquared = pd.Series(  # pylint: disable=invalid-name
        np.diag(mahal), index=mahal.index
    )
    MD = pd.Series(
        np.sqrt(MDsquared), index=MDsquared.index  # pylint: disable=invalid-name
    )
    # Compute P-Values
    p_value = pd.Series(
        1 - stats.chi2.cdf(MDsquared, df=df_raw.shape[1]), index=MDsquared.index
    )
    # Compute critival value
    cv = stats.chi2.ppf(  # pylint: disable=invalid-name
        (1 - alpha), df=df_raw.shape[1]
    )  # critical value, with degrees of freedom = number of variables
    # Detect outliers
    # either using p_values
    #     p_outliers = []
    #     for index in p_value.index:
    #         p = p_value[index]
    #         if p <= alpha:
    #             p_outliers.append(index)
    #             print(index, p)
    #         else:
    #             continue
    # or using the cv
    list_outliers = []
    for index in MDsquared.index:
        value = MDsquared[index]
        if value > cv:  # reject H0 hypothesis which is "value is not an outlier"
            list_outliers.append(index)
        else:
            continue
    list_non_outliers = list(set(list(df_raw.index)) - set(list_outliers))

    df_treated = df_raw.loc[list_non_outliers]
    df_treated["p_value"] = p_value[list_non_outliers]
    df_outliers = df_raw.loc[list_outliers]
    df_outliers["p_value"] = p_value[list_outliers]

    return df_treated, df_outliers, (sorted(list_outliers), MD, cv)


def make_full_df_after_outlier_detection_method(df_original, df_treated):
    """Combine metadata columns with data after application of outlier detection method.

    Returns a combined dataframe of outlier free data or dataframe of outliers only.

    Parameters
    ----------
    df_original : pandas.DataFrame
        Should contain the original dataframe (with all the columns or
        only selected ones) before the application of the outlier detection method,
        e.g. df_full_before_detecting_outliers or
        df_full_before_detecting_outliers[lst_metadata]
        If full dataframe is passed, the duplicated columns will be dropped,
        keeping the last appearance
    df_treated : pandas.DataFrame
        Should contain dataframe without outliers obtained from an outlier detecting method,
        this dataframe will only contain columns considered for outlier detection,
        use that dataframe as it is

    Returns
    -------
    df_new : pandas.DataFrame
        Concatenation of passed dataframes on axis=1, removing any duplicated column(s)
        (`keep='last'`)
    """
    df_or = df_original.copy()
    df_tr = df_treated.copy()

    df_new = pd.concat([df_or, df_tr], axis=1)
    df_new = df_new.loc[:, ~df_new.columns.duplicated(keep="last")]

    return df_new.dropna(how="all", subset=df_tr.columns.tolist())
