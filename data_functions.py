import configparser
from datetime import datetime
import pandas as pd


def read_user_settings():
    config = configparser.ConfigParser()
    config.read('settings.ini')
    report_date = datetime.strptime(config['settings']['report_date'], '%d-%m-%Y').date()
    expiry_date = datetime.strptime(config['settings']['expiry_date'], '%d-%m-%Y').date()
    number_of_lognormal_distributions = int(config['settings']['number_of_lognormal_distributions'])
    tolerance = float(config['settings']['tolerance'])
    max_iterations = int(config['settings']['max_iterations'])
    file_path_option_quotes = config['settings']['file_path_option_quotes']
    file_path_option_quotes = file_path_option_quotes.replace('[[expiry_date]]', datetime.strftime(expiry_date, '%Y%m%d'))
    file_path_option_quotes = file_path_option_quotes.replace('[[report_date]]', datetime.strftime(report_date, '%Y%m%d'))
    file_path_stock_prices = config['settings']['file_path_stock_prices']
    return report_date, expiry_date, number_of_lognormal_distributions, tolerance, max_iterations, \
        file_path_option_quotes, file_path_stock_prices


def read_market_quotes(file_path_option_quotes, file_path_stock_prices, report_date):
    options = pd.read_csv(file_path_option_quotes, skipfooter=1, engine='python')
    stock_prices = pd.read_csv(file_path_stock_prices)
    stock_price = stock_prices[stock_prices['Date'] == str(report_date)]['Price'][0]
    interest_rate = 0
    return options, stock_price, interest_rate
