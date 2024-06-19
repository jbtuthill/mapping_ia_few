import urllib.parse

# Corn Grain Yield Bu/Acre
corng_y = (
    'source_desc=SURVEY' +  \
    '&sector_desc=CROPS' + \
    '&commodity_desc=CORN' + \
    '&statisticcat_desc=YIELD' + \
    '&util_practice_desc=GRAIN' + \
    '&' + urllib.parse.quote('short_desc=CORN, GRAIN - YIELD, MEASURED IN BU / ACRE') + \
    '&freq_desc=ANNUAL' + \
    '&reference_period_desc=YEAR' + \
    '&year__GE=1968' + \
    '&agg_level_desc=COUNTY' + \
    '&state_name=IOWA' + \
    '&county_code__LT=998' + \
    '&format=CSV'
)

# Soybean Yield Bu/Acre
soy_y = (
    'source_desc=SURVEY' +  \
    '&sector_desc=CROPS' + \
    '&commodity_desc=SOYBEANS' + \
    '&statisticcat_desc=YIELD' + \
    '&' + urllib.parse.quote('short_desc=SOYBEANS - YIELD, MEASURED IN BU / ACRE') + \
    '&freq_desc=ANNUAL' + \
    '&reference_period_desc=YEAR' + \
    '&year__GE=1968' + \
    '&agg_level_desc=COUNTY' + \
    '&state_name=IOWA' + \
    '&format=CSV'
)

# Corn Area Planted Acres
corng_pa = (
    'source_desc=SURVEY' +  \
    '&sector_desc=CROPS' + \
    '&commodity_desc=CORN' + \
    '&statisticcat_desc__LIKE=PLANTED' + \
    '&' + urllib.parse.quote('short_desc=CORN - ACRES PLANTED') + \
    '&unit_desc=ACRES' + \
    '&freq_desc=ANNUAL' + \
    '&reference_period_desc=YEAR' + \
    '&year__GE=1968' + \
    '&agg_level_desc=COUNTY' + \
    '&state_name=IOWA' + \
    '&county_code__LT=998' + \
    '&format=CSV'
)

# Corn Area Harvested Acres (grain)
corng_ha = (
    'source_desc=SURVEY' +  \
    '&sector_desc=CROPS' + \
    '&commodity_desc=CORN' + \
    '&util_practice_desc=GRAIN' + \
    '&statisticcat_desc__LIKE=HARVESTED' + \
    '&' + urllib.parse.quote('short_desc=CORN, GRAIN - ACRES HARVESTED') + \
    '&unit_desc=ACRES' + \
    '&freq_desc=ANNUAL' + \
    '&reference_period_desc=YEAR' + \
    '&year__GE=1968' + \
    '&agg_level_desc=COUNTY' + \
    '&state_name=IOWA' + \
    '&county_code__LT=998' + \
    '&format=CSV'
)            

# Soybean Area Planted Acres
soy_pa = (
    'source_desc=SURVEY' +  \
    '&sector_desc=CROPS' + \
    '&' + urllib.parse.quote('group_desc=FIELD CROPS') + \
    '&commodity_desc=SOYBEANS' + \
    '&statisticcat_desc__LIKE=PLANTED' + \
    '&' + urllib.parse.quote('short_desc=SOYBEANS - ACRES PLANTED') + \
    '&unit_desc=ACRES' + \
    '&freq_desc=ANNUAL' + \
    '&reference_period_desc=YEAR' + \
    '&year__GE=1968' + \
    '&agg_level_desc=COUNTY' + \
    '&state_name=IOWA' + \
    '&county_code__LT=998' + \
    '&format=CSV'
)            

# Soybean Area Harvested Acres
soy_ha = (
    'source_desc=SURVEY' +  \
    '&sector_desc=CROPS' + \
    '&' + urllib.parse.quote('group_desc=FIELD CROPS') + \
    '&commodity_desc=SOYBEANS' + \
    '&statisticcat_desc__LIKE=HARVESTED' + \
    '&' + urllib.parse.quote('short_desc=SOYBEANS - ACRES PLANTED') + \
    '&unit_desc=ACRES' + \
    '&freq_desc=ANNUAL' + \
    '&reference_period_desc=YEAR' + \
    '&year__GE=1968' + \
    '&agg_level_desc=COUNTY' + \
    '&state_name=IOWA' + \
    '&county_code__LT=998' + \
    '&format=CSV'
)           

# Hogs
hogs = (
    urllib.parse.quote('sector_desc=ANIMALS & PRODUCTS') + \
    '&group_desc=LIVESTOCK' + \
    '&commodity_desc=HOGS' + \
    '&statisticcat_desc=INVENTORY' + \
    '&domain_desc=TOTAL' + \
    '&' + urllib.parse.quote('domaincat_desc=NOT SPECIFIED') + \
    '&unit_desc=HEAD' + \
    '&year__GE=1968' + \
    '&agg_level_desc=COUNTY' + \
    '&state_name=IOWA' + \
    '&county_code__LT=998' + \
    '&format=CSV'
)                

# Breeding Hogs Inventory - sows + boars ratio 20:1 and # Hogs Sales
hogs_others = (
    urllib.parse.quote('sector_desc=ANIMALS & PRODUCTS') + \
    '&group_desc=LIVESTOCK' + \
    '&commodity_desc=HOGS' + \
    '&' + urllib.parse.quote('util_practice_desc= BREEDING') + \
    '&' + urllib.parse.quote('domaincat_desc=NOT SPECIFIED') + \
    '&unit_desc=HEAD' + \
    '&year__GE=1968' + \
    '&agg_level_desc=COUNTY' + \
    '&state_name=IOWA' + \
    '&county_code__LT=998' + \
    '&format=CSV'
)                

# Beef Cows
beef = (
    urllib.parse.quote('sector_desc=ANIMALS & PRODUCTS') + \
    '&group_desc=LIVESTOCK' + \
    '&commodity_desc=CATTLE' + \
    '&class_desc__LIKE=BEEF' + \
    '&statisticcat_desc=INVENTORY' + \
    '&domain_desc=TOTAL' + \
    '&' + urllib.parse.quote('domaincat_desc=NOT SPECIFIED') + \
    '&unit_desc=HEAD' + \
    '&year__GE=1968' + \
    '&agg_level_desc=COUNTY' + \
    '&state_name=IOWA' + \
    '&county_code__LT=998' + \
    '&format=CSV'
)

# Milk
milk = (
    urllib.parse.quote('sector_desc=ANIMALS & PRODUCTS') + \
    '&group_desc=LIVESTOCK' + \
    '&commodity_desc=CATTLE' + \
    '&class_desc__LIKE=MILK' + \
    '&statisticcat_desc=INVENTORY' + \
    '&domain_desc=TOTAL' + \
    '&' + urllib.parse.quote('domaincat_desc=NOT SPECIFIED') + \
    '&unit_desc=HEAD' + \
    '&year__GE=1968' + \
    '&agg_level_desc=COUNTY' + \
    '&state_name=IOWA' + \
    '&county_code__LT=998' + \
    '&format=CSV'
)

# All cattle
other_cattle = (
    urllib.parse.quote('sector_desc=ANIMALS & PRODUCTS') + \
    '&group_desc=LIVESTOCK' + \
    '&commodity_desc=CATTLE' + \
    '&' +urllib.parse.quote('class_desc=INCL CALVES') + \
    '&statisticcat_desc=INVENTORY' + \
    '&unit_desc=HEAD' + \
        '&' +urllib.parse.quote('short_desc=CATTLE, INCL CALVES - INVENTORY') + \
        '&domain_desc=TOTAL' + \
    '&year__GE=1968' + \
    '&agg_level_desc=COUNTY' + \
    '&state_name=IOWA' + \
    '&county_code__LT=998' + \
    '&format=CSV'
)

# Steers
steers = (
    urllib.parse.quote('sector_desc=ANIMALS & PRODUCTS') +
    '&group_desc=LIVESTOCK' +
    '&commodity_desc=CATTLE' +
    '&' + urllib.parse.quote('prodn_practice_desc=ON FEED') +
    '&' + urllib.parse.quote('short_desc__LIKE=CATTLE, ON FEED - INVENTORY') +
    '&domain_desc=TOTAL' +
    '&unit_desc=HEAD' +
    '&year__GE=1968' +
    '&agg_level_desc=COUNTY' +
    '&state_name=IOWA' +
    '&county_code__LT=998' +
    '&format=CSV'
)

# Cattle on Feed Sold
onfeed_sold = (
    urllib.parse.quote('sector_desc=ANIMALS & PRODUCTS') +
    '&group_desc=LIVESTOCK' +
    '&commodity_desc=CATTLE' +
    '&' + urllib.parse.quote('statisticcat_desc=SALES FOR SLAUGHTER') +
    '&' + urllib.parse.quote('short_desc__LIKE=CATTLE, ON FEED - SALES FOR SLAUGHTER, MEASURED IN HEAD') +
    '&domain_desc=TOTAL' +
    '&unit_desc=HEAD' +
    '&year__GE=1968' +
    '&agg_level_desc=COUNTY' +
    '&state_name=IOWA' +
    '&county_code__LT=998' +
    '&format=CSV'
)