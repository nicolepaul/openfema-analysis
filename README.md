# OpenFEMA Data Analysis

## Overview

This [notebook](/get_openfema_data.ipynb) can be used and adapted to work with [**OpenFEMA datasets**](https://www.fema.gov/about/openfema/data-sets) related to the  Individuals and Households Program (IHP). The [python functions](/query.py) within the repository can also be adapted to eventually support other available datasets from OpenFEMA (e.g., disaster information, public assistance).

## Supported datasets

The following Individuals and Households Programs (IHP) datasets are currently supported:
* **'HousingAssistanceOwners'**: Housing Assistance Program Data - Owners [V2](https://www.fema.gov/openfema-data-page/housing-assistance-program-data-owners-v2)
* **'HousingAssistanceRenters'**: Housing Assistance Program Data - Renters [V2](https://www.fema.gov/openfema-data-page/housing-assistance-program-data-renters-v2)
* **'IndividualsAndHouseholdsProgramValidRegistrations'**: Individuals and Households Program - Valid Registrations [V1](https://www.fema.gov/openfema-data-page/individuals-and-households-program-valid-registrations-v1)

## Disclaimer

This product uses the FEMA OpenFEMA API, but is not endorsed by FEMA. The Federal Government or FEMA cannot vouch for the data or analyses derived from these data after the data have been retrieved from the Agency's website(s).