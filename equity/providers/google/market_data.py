# A dictionary pairing each market to its relevant currency.
market_currencies = {
    'NYSE': 'USD',  # USA
    'NASDAQ': 'USD',  # USA
    'TPE': 'TWD',  # Taiwan
    'KPX': 'KRW',  # ROK (South Korea)
    'BVMF': 'BRL',  # Brazil
    'SHA': 'CNY',  # People's Republic of China (PRC)
    'IDX': 'IDR',  # Indonesia
    'WSE': 'PLN',  # Poland
    'ETR': 'EUR',  # Germany
    'IST': 'TRY',  # Turkey
    'NZE': 'NZD',  # New Zealand
    'LON': 'GBX',  # United Kingdom (exception to ISO4217)
    'TYO': 'JPY',  # Japan
    'HKG': 'HKD',  # Hong Kong SAR
    'NSE': 'INR',  # India
    'KLSE': 'MYR',  # Malaysia
    'SHE': 'CNY',  # People's Republic of China (PRC)
    'ASX': 'AUD',  # Australia
    'BIT': 'EUR',  # Italy
    'BKK': 'THB',  # Thailand
    'TSE': 'CAD',  # Canada
    'TADAWUL': 'SAR',  # Saudi Arabia
    'TLV': 'ILA',  # Israel (exception to ISO4217)
    'STO': 'SEK',  # Sweden
    'CVE': 'CAD',  # Canada
    'CPH': 'DKK',  # Denmark
    'SGX': 'SGD',  # Singapore
    'CNSX': 'CAD',  # Canada
    'AMS': 'EUR',  # Netherlands
    'FRA': 'EUR',  # Germany
    'EPA': 'EUR',  # France
    'SWX': 'CHF',  # Switzerland
    'HEL': 'EUR',  # Finland
    'KOSDAQ': 'KRW',  # ROK (South Korea)
    'BOM': 'INR',  # India
    'BME': 'EUR',  # Spain
    'JSE': 'ZAC',  # South Africa (exception to ISO4217)
    'BMV': 'MXN',  # Mexico
    'BCBA': 'ARS',  # Argentina
    'VIE': 'EUR',  # Austria
    'EBR': 'EUR',  # Belgium
    'ELI': 'EUR',  # Portugal
    'ICE': 'ISK',  # Iceland
    'TAL': 'EUR',  # Estonia
    'VSE': 'EUR',  # Lithuania
    'OTCMKTS': 'USD',  # USA
    'NYSEARCA': 'USD',  # USA
    'NYSEAMERICAN': 'USD',  # USA
    'MUTF': 'USD',  # USA
    'MUTF_IN': 'INR',  # India
    'BATS': 'USD',  # USA
    'CBOT': 'USD',  # USA
    'CME_EMINIS': 'USD',  # USA
    'NYMEX': 'USD'  # USA
}

# An array that holds each of the possible unique currencies + the ISO4217 counterparts to cases such as GBX/ZAC.
# To be used for the market cap to filter currency from string to i.e. multiply 8.64(B) by 1bn to get as an integer.
each_unique_currency = ['USD', 'TWD', 'KRW', 'BRL', 'CNY', 'IDR', 'PLN', 'EUR', 'TRY', 'NZD', 'GBX', 'GBP', 'JPY', 'HKD',
                        'INR', 'MYR', 'AUD', 'THB', 'CAD', 'SAR', 'ILA', 'ILS', 'SEK', 'DKK', 'SGD', 'CHF', 'ZAC', 'ZAR', 'MXN', 'ARS', 'ISK']

# A list of ISO4217 currency codes.
iso4217_currencies = ['AED', 'AFN', 'ALL', 'AMD', 'ANG', 'AOA', 'ARS', 'AUD', 'AWG', 'AZN', 'BAM', 'BBD', 'BDT', 'BGN', 'BHD', 'BIF', 'BMD', 'BND', 'BOB', 'BRL', 'BSD', 'BTN', 'BWP', 'BYN', 'BZD', 'CAD', 'CDF', 'CHF', 'CLP', 'CNY', 'COP', 'CRC', 'CUC', 'CUP', 'CVE', 'CZK', 'DJF', 'DKK', 'DOP', 'DZD', 'EGP', 'ERN', 'ETB', 'EUR', 'FJD', 'FKP', 'GBP', 'GEL', 'GGP', 'GHS', 'GIP', 'GMD', 'GNF', 'GTQ', 'GYD', 'HKD', 'HNL', 'HRK', 'HTG', 'HUF', 'IDR', 'ILS', 'IMP', 'INR', 'IQD', 'IRR', 'ISK', 'JEP', 'JMD', 'JOD', 'JPY', 'KES', 'KGS', 'KHR', 'KMF', 'KPW', 'KRW', 'KWD', 'KYD', 'KZT',
                      'LAK', 'LBP', 'LKR', 'LRD', 'LSL', 'LYD', 'MAD', 'MDL', 'MGA', 'MKD', 'MMK', 'MNT', 'MOP', 'MRU', 'MUR', 'MVR', 'MWK', 'MXN', 'MYR', 'MZN', 'NAD', 'NGN', 'NIO', 'NOK', 'NPR', 'NZD', 'OMR', 'PAB', 'PEN', 'PGK', 'PHP', 'PKR', 'PLN', 'PYG', 'QAR', 'RON', 'RSD', 'RUB', 'RWF', 'SAR', 'SBD', 'SCR', 'SDG', 'SEK', 'SGD', 'SHP', 'SLL', 'SOS', 'SPL', 'SRD', 'STN', 'SVC', 'SYP', 'SZL', 'THB', 'TJS', 'TMT', 'TND', 'TOP', 'TRY', 'TTD', 'TVD', 'TWD', 'TZS', 'UAH', 'UGX', 'USD', 'UYU', 'UZS', 'VEF', 'VND', 'VUV', 'WST', 'XAF', 'XCD', 'XDR', 'XOF', 'XPF', 'YER', 'ZAR', 'ZMW', 'ZWD']
