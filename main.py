from data_functions import read_user_settings, read_market_quotes
from option_functions import initialize_options
from calibration import calibrate_parameters
from report import generate_report
import numpy as np

# read user settings
report_date, expiry_date, number_of_lognormal_distributions, tolerance, \
    max_iterations, file_path_option_quotes, file_path_stock_prices = read_user_settings()
time_to_expiry = np.busday_count(report_date, expiry_date) / 252
# read market data
option_quotes, stock_price, interest_rate = read_market_quotes(file_path_option_quotes, file_path_stock_prices, report_date)
# initialize model options
options = initialize_options(option_quotes, time_to_expiry, stock_price, interest_rate)
# fit model option prices to market option prices
calibration_results, lambdas, final_sigmas, sigmas, model_prices = calibrate_parameters(option_quotes, options, number_of_lognormal_distributions, tolerance, max_iterations, time_to_expiry, interest_rate)
# generate report
generate_report(calibration_results, lambdas, final_sigmas, sigmas, model_prices, option_quotes, stock_price, time_to_expiry, report_date, expiry_date)
pass
