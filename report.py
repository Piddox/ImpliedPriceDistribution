import matplotlib.pyplot as plt
from densitycalculator import DensityCalculator
import numpy as np
from scipy.interpolate import interp1d
from datetime import datetime


def generate_report(calibration_results, lambdas, final_sigmas, sigmas, model_prices, option_quotes, stock_price,
                    time_to_expiry, report_date, expiry_date):
    show_density_function(lambdas, final_sigmas, sigmas, stock_price, time_to_expiry, report_date, expiry_date)
    show_prices(model_prices, option_quotes)
    plt.show()


def show_density_function(lambdas, final_sigmas, sigmas, stock_price, time_to_expiry, report_date, expiry_date):
    dc = DensityCalculator(lambdas, final_sigmas, sigmas, stock_price, time_to_expiry)
    stock_prices = np.arange(10, 510, 5)
    f = interp1d(stock_prices, dc.density_function(stock_prices), kind='quadratic')
    x = np.linspace(stock_prices.min(), stock_prices.max(), 500)
    y = f(x)
    plt.figure()
    plt.title('pdf of GME share price at ' + datetime.strftime(expiry_date, '%d-%m-%Y') + ' based on option data of ' +
              datetime.strftime(report_date, '%d-%m-%Y'))
    plt.plot(x, y, 'b', label='probability density function (pdf)')
    label_expected_value = 'Expected value: $' + str(dc.expected_value())
    plt.plot(dc.expected_value(), dc.density_function(dc.expected_value()), 'bo', label=label_expected_value)
    label_share_price = 'Share price at ' + datetime.strftime(report_date, '%d-%m-%Y') + ': $' + str(stock_price)
    plt.axvline(x=stock_price, c='r', label=label_share_price)
    plt.legend(loc='upper right', fontsize='x-small')


def show_prices(model_prices, option_quotes):
    option_quotes['model price'] = model_prices
    show_prices_call_or_put(option_quotes, 'Call')
    show_prices_call_or_put(option_quotes, 'Put')


def show_prices_call_or_put(option_quotes, type_of_option):
    options = option_quotes[option_quotes['Type'] == type_of_option]
    strikes = options['Strike']
    model_prices = options['model price']
    market_prices = options['Midpoint']
    differences = model_prices / market_prices - 1
    fig, ax1 = plt.subplots()
    ax2 = ax1.twinx()
    plt.title(type_of_option + ' options prices and price differences %')
    ax1.plot(strikes, model_prices, 'b', label="Model price")
    ax1.plot(strikes, market_prices, 'r', label="Market price")
    ax2.plot(strikes, differences, 'k', label="Price differences %")
    ax1.set_xlabel('Strike price')
    ax1.set_ylabel('Price level', color='k')
    ax2.set_ylabel('Price difference %', color='k')
    legend_location = 'upper right' if type_of_option == 'Call' else 'lower right'
    handles, labels = [(a + b) for a, b in zip(ax1.get_legend_handles_labels(), ax2.get_legend_handles_labels())]
    ax1.legend(handles, labels, loc=legend_location)
