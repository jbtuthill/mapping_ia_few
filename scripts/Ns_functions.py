import pandas as pd

def calculate_manure_n(row):
    """
    Calculate Manure Nitrogen (ManureN_kg_ha) for each row considering storage loss.

    Parameters:
    - row (Series): A pandas Series containing the data for one row.

    Returns:
    - manure_n (float): Calculated manure nitrogen in kg/ha.
    """
    hogs_sows = row['hogs_sow']
    hogs_boars = row['hogs_boars']
    hogs_fin = row['hogs_fin']
    milk_cows = row['milk']
    beef_cows = row['beef']
    milk_cows_150 = row['dairy_150']
    milk_cows_440 = row['dairy_400']
    beef_bulls = row['bulls']
    calf = row['steers']
    cattle_fin = row['fin_cattle']
    soybeans_acres = row['soy_pa']
    corn_acres = row['corng_pa']
    
    # Calculate manure nitrogen based on various animal categories
    manure_n = (hogs_sows * 0.036 * 365 +
                hogs_boars * 0.022 * 365 +
                hogs_fin * 0.028 * 180 +
                milk_cows * 0.2 * 365 +
                beef_cows * 0.029 * 365 +
                milk_cows_150 * 0.031 * 200 +
                milk_cows_440 * 0.060 * 365 +
                beef_bulls * 0.029 * 365 +
                calf * 0.019 * 365 +
                cattle_fin * 0.089 * 365) / (0.404686 * (soybeans_acres + corn_acres))
        
    return round(manure_n, 1)

def calculate_fix_n(row):
    """
    Calculate fixation nitrogen (FixN_kg_ha) for each row.

    Parameters:
    - row (Series): A pandas Series containing the data for one row.

    Returns:
    - fix_n (float): Calculated fixation nitrogen in kg/ha.
    """
    soybeans_yield = row['soy_y']
    soybeans_acres = row['soy_pa']
    corn_acres = row['corng_pa']
    
    fix_n = ((soybeans_yield / 15) * 81.1 - 98.5) * (soybeans_acres / (soybeans_acres + corn_acres)) #soybeans_yield / 15 because the FN equation provided by Barry et al. (1993) gives FN in tons/ha. Hence, for soybeans 1bu/ac = 0.06725tons/ha = 1/15
    
    return round(fix_n, 1)

def calculate_grain_n(row):
    """
    Calculate grain nitrogen (GrainN_kg_ha) for each row.

    Parameters:
    - row (Series): A pandas Series containing the data for one row.

    Returns:
    - grain_n (float): Calculated grain nitrogen in kg/ha.
    """
    soybeans_yield = row['soy_y']
    corn_yield = row['corng_y']
    soybeans_acres_h = row['soy_ha']
    corn_acres_h = row['corng_ha']
    
    grain_n = ((soybeans_yield * 67.25 * 6.4 / 100 * soybeans_acres_h * 0.404686) +
               (corn_yield * 62.77 * 1.18 / 100 * corn_acres_h * 0.404686)) / (0.404686 * (soybeans_acres_h + corn_acres_h))
    
    return round(grain_n, 1)

def calculate_ns(row):
    """
    Calculate nitrogen surplus (NS_kg_ha) for each row.

    Parameters:
    - row (Series): A pandas Series containing the data for one row.

    Returns:
    - ns (float): Calculated nitrogen surplus in kg/ha.
    """
    commercial = row['CN']
    manure = row['MN']
    grain = row['GN']
    fix = row['FN']
    
    ns = commercial + manure + fix - grain
    
    return round(ns, 1)

def calculate_manure_n_no_storage_loss(row):
    """
    Calculate Manure Nitrogen (ManureN_kg_ha) for each row without considering storage loss. Previous IFEWs version.

    Parameters:
    - row (Series): A pandas Series containing the data for one row.

    Returns:
    - manure_n (float): Calculated manure nitrogen in kg/ha without storage loss.
    """
    hogs = row['hogs']
    milk_cows = row['milk']
    beef_cows = row['beef']
    heifer_steers = (row['cattle'] - (row['beef'] + row['milk'])) * 0.5
    slaughter_cattle = (row['cattle'] - (row['beef'] + row['milk'])) * 0.5
    soybeans_acres = row['soy_pa']
    corn_acres = row['corng_pa']
    
    # Calculate manure nitrogen without considering storage loss
    manure_n = (hogs * 0.027 * 365 +
                milk_cows * 0.204 * 365 +
                beef_cows * 0.15 * 365 +
                heifer_steers * 0.1455 * 365 +
                slaughter_cattle * 0.104 * 170) / (0.404686 * (soybeans_acres + corn_acres))
        
    return round(manure_n, 1)
