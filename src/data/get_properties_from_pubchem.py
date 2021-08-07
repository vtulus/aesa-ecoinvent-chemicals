# -*- coding: utf-8 -*-
"""
Created on Thu Jul 15 08:24:54 2021

@author: VTulus
"""
__all__ = ["get_properties_from_pubchem"]

import pandas as pd
import pubchempy as pcp

if __package__:
    from ..utils.progressbar import progressbar
# else:
    # Path(Path(__file__).parents[1], "utils", "progessbar") progressbar
    # doesn't work with relative import...


def get_properties_from_pubchem(
    df_in: pd.DataFrame,
    cas_column: str = "referenceProduct_casNumber",
    name_column: str = "referenceProduct",
) -> pd.DataFrame:
    """Queries PubChem database for chemical properties.

    Queries are performed using pubchempy module
    (https://pubchempy.readthedocs.io/en/latest/).
    Attempts to find the chemical compound using the provided *CAS number*.
    If the search is unsuccessful, searches by the provided *product name*.
    The field "name" of `pcp.get_compounds()` looks for (almost) an exact match
    (it is not case-sensitive and ignores spaces)
    Returns a dataframe with reference product name, CAS number, number of matches
    if any, molecular fromula and weight, IUPAC nomenclature, molecular complexity
    and synonyms.

    Parameters
    ----------
    df_in : pandas.DataFrame
        Dataframe with (at least) 2 column labels: `cas_column` and `name_column`
    cas_column: str, default "referenceProduct_casNumber"
        Label of a column containing CAS numbers
    name_column : str, default "referenceProduct"
        Label of a column containing product/compound names
        Note: `name_column` will not be very effective on columns other than
        "referenceProduct" because of how splitting is performed

    Returns
    -------
    df_properties : pandas.DataFrame
        Dataframe with properties extracted from PubChem database,
        the index being the items of `name_column` and its column labels being
        `referenceProduct_casNumber` - CAS number of the compound (if found)
        `pubchem_match` - info "WAS A MATCH FOUND IN db?"
        `num_matches` - number of matches in PubChem db
        `MF` - molecular formula of the compounds
        `MW` - molecular weight of the compounds in g/mol
        `iupac` - names according to IUPAC nomenclature
        `complexity` - molecular complexity ratings computed using the
            Bertz/Hendrickson/Ihlenfeldt formula
        `synonyms` - list of synonyms of the compound

    Notes
    -----
    More detailed API info https://pubchemdocs.ncbi.nlm.nih.gov/pug-rest$_Toc494865567
    Details about complexity of a compound https://pubchemdocs.ncbi.nlm.nih.gov/glossary$Complexity
    """
    dict_prop = {}
    for idx in progressbar(df_in.index):
        temp_dict = {}
        product = df_in[name_column][idx]  # reference product
        cas = df_in[cas_column][idx]  # cas number

        temp_dict["referenceProduct_casNumber"] = cas

        # remove everything after comma
        clean_product, *_ = product.split(", ")

        if not pd.isna(cas):  # if cas number exists,
            # try matching PubChem database against CAS number
            comp, temp_dict["pubchem_match"] = _find_compound(
                search_by=("by CAS", cas))
            if len(comp) == 0:  # if no match,
                # try matching by name
                comp, temp_dict["pubchem_match"] = _find_compound(
                    search_by=("by NAME", clean_product))
        else:  # if no cas number,
            # try matching PubChem database against the name of the reference
            # product (partially)
            comp, temp_dict["pubchem_match"] = _find_compound(
                search_by=("by NAME", clean_product))

        try:
            temp_dict["num_matches"] = len(comp)
            temp_dict["MF"] = comp[0].molecular_formula
            temp_dict["MW"] = comp[0].molecular_weight
            temp_dict["iupac"] = comp[0].iupac_name
            temp_dict["complexity"] = comp[0].complexity
            # (using Bertz/Hendrickson/Ihlenfeldt formula)
            # look here for more https://pubchemdocs.ncbi.nlm.nih.gov/glossary$Complexity
            temp_dict["synonyms"] = comp[0].synonyms
        except:  # pylint: disable=bare-except
            pass

        dict_prop[product] = temp_dict

    df_properties = pd.DataFrame.from_dict(
        dict_prop,
        orient="index",
        columns=[
            "referenceProduct_casNumber",
            "pubchem_match",
            "num_matches",
            "MF",
            "MW",
            "iupac",
            "complexity",
            "synonyms",
        ],
    )
    return df_properties


def _find_compound(search_by: tuple):
    """Query PubChem with `pcp.get_compounds()`.

    Retrives specified compound records from PubChem.
    Internal function, supposed to be used in `get_properties_from_pubchem()`

    Parameters
    ----------
    search_by : tuple
        Tuple of 2 str, search_by[0]="by ..." and search_by[1]=identifier passed
        to `get_properties_from_pubchem()`, used as a search query.

    Returns
    -------
    comp :
        Object with specified compound records from PubChem
    pubchem_match: str
        Match info
    """
    pubchem_match = None
    token = search_by[0]  # e.g. "by CAS", "by NAME", etc
    item = search_by[1]  # e.g. CAS number, chemical name

    comp = pcp.get_compounds(
        item, namespace="name", searchtype=None, as_dataframe=False)
    if len(comp) == 0:
        pubchem_match = "No match"
    elif len(comp) == 1:
        pubchem_match = token
    else:
        pubchem_match = "WARNING: multiple matches {}".format(token)

    return comp, pubchem_match
