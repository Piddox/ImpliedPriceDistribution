from mixed_lognormal_option import MixedLognormalOption


def initialize_options(option_quotes, time_to_expiry, stock_price, interest_rate):
    options = []
    for option_quote in option_quotes.iterrows():
        strike = option_quote[1]['Strike']
        is_call = option_quote[1]['Type'] == 'Call'
        option = MixedLognormalOption(stock_price, strike, interest_rate, time_to_expiry, is_call)
        options.append(option)
    return options

