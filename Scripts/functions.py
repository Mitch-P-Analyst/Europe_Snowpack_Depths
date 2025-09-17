# 02_EDA

# Get Month Name

import calendar

def get_month_name(month_number) -> str | None:
    """
    Convert month number (1..12) to abbreviated name like 'Jan'.
    Returns None for invalid inputs.
    """
    try:
        m = int(month_number)
        if 1 <= m <= 12:
            return calendar.month_abbr[m]   # 'Jan', 'Feb', ...
    except (TypeError, ValueError):
        pass
    return None
    

# Get Country Abreviation

COUNTRY_ABR = {
    'Austria': 'AT',
    'France': 'FR',
    'Germany': 'DE',
    'Italy': 'IT',
    'Slovenia': 'SI',
    'Switzerland': 'CH',
}

def get_country_abr(country_name: str) -> str:
    """
    Map full country name to ISO-like abbreviation; 
    fall back to original name if not found.
    """
    return COUNTRY_ABR.get(country_name, country_name)
    
