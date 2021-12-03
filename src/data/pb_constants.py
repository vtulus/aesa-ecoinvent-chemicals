# -*- coding: utf-8 -*-
"""
Created on Mon Aug  2 13:31:09 2021

@author: VTulus
"""

__all__ = ["SOS_PB_LCIA", "SOS_PB_SALA", "CURRENT_PB_SCORE"]

# =============================================================================
# In this file:
# - Ranges of Safe Operating Space for each PB:
#   {category: value} # 'unit'
# - Current total anthropogenic scores on each PB
#   (for Ryberg et al. method)
#   The GHG-related PBs are projected to 2300...
# =============================================================================

# SOS for PBs-LCIA method (based on Ryberg et al. 2018)
SOS_PB_LCIA = {
    "Climate change - CO2 concentration": 72.0,  # 'ppm'
    "Climate change - Energy imbalance": 1.00,  # 'Wm-2
    "Stratospheric ozone depletion": 14.5,  # 'DU'
    "Ocean acidification": 0.69,  # 'Omega Aragon'
    "Biogeochemical flows - P": 9.90,  # 'Tg P'
    "Biogeochemical flows - N": 62.0,  # 'Tg N'
    "Land-system change - Global": 25.0,  # '%'
    "Freshwater use - Global": 4000.0,  # 'km3'
    "Change in biosphere integrity - BII loss": 10.0,  # '% BII loss'
}

# SOS for PBs - Alternative method (based on Sala et al. 2020)
SOS_PB_SALA = {
    "Climate change": 6.81e12,  # kg CO2 eq
    "Ozone depletion": 5.39e08,  # kg CFC11 eq
    "Ionising radiation, HH": 5.79e14,  # kBq U-235 eq
    "Photochemical ozone formation, HH": 4.07e11,  # kg NMVOC eq
    "Respiratory inorganics": 5.68e05,  # disease incidence.
    "Non-cancer human health effects": 4.50e06,  # CTUh
    "Cancer human health effects": 1.06e06,  # CTUh
    "Acidification terrestrial and freshwater": 1.00e12,  # mol H+ eq
    "Eutrophication freshwater": 5.81e09,  # kg P eq
    "Eutrophication marine": 2.01e11,  # kg N eq
    "Eutrophication terrestrial": 6.13e12,  # mol N eq
    "Ecotoxicity freshwater": 1.31e14,  # CTUe
    "Land use - Erosion": 1.27e13,  # kg soil loss
    "Water scarcity": 1.82e14,  # m3 deprivation
    "Resource use, energy carriers": 2.24e14,  # MJ
    "Resource use, mineral and metals": 2.19e08,  # kg Sb eq
}

CURRENT_PB_SCORE = {
    "Climate change - CO2 concentration": 1085.0,  # 'ppm'
    "Climate change - Energy imbalance": 14.8,  # 'Wm-2
    "Stratospheric ozone depletion": 7.00,  # 'DU'
    "Ocean acidification": 3.32,  # 'Omega Aragon'
    "Biogeochemical flows - P": 20.9,  # 'Tg P'
    "Biogeochemical flows - N": 150.0,  # 'Tg N'
    "Land-system change - Global": 38.0,  # '%'
    "Freshwater use - Global": 2600.0,  # 'km3'
    "Change in biosphere integrity - BII loss": 26.8,  # '% BII loss'
}
