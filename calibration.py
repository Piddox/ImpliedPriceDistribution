import math
import numpy as np
from scipy.optimize import minimize


def calibrate_parameters(option_quotes, options, number_of_lognormal_distributions, tolerance, max_iterations,
                         time_to_expiry, interest_rate):
    k = number_of_lognormal_distributions
    pc = PenaltyCalculator(option_quotes, options, k, time_to_expiry, interest_rate)
    x0 = set_initial_guess_parameters(k)
    cons = ({'type': 'ineq', 'fun': constraint_lambdas, 'args': (k,)})
    bounds = ((0, 1),)*(k-1) + ((0, None),)*(k-1) + ((0, None),)*k
    result = minimize(pc.penalty_function, x0, method="SLSQP", options={'ftol': tolerance, 'maxiter': max_iterations},
                      bounds=bounds, constraints=cons)
    lambdas, final_sigmas, sigmas = add_dependant_variables_to_free_variables(result.x, k, time_to_expiry,
                                                                             interest_rate)
    print(result)
    print('lambdas :')
    print(lambdas)
    print('final_sigmas :')
    print(final_sigmas)
    print('sigmas :')
    print(sigmas)
    model_prices = calculate_model_prices(options, k, lambdas, final_sigmas, sigmas)
    return result, lambdas, final_sigmas, sigmas, model_prices


def set_initial_guess_parameters(k):
    lambdas0 = [1/k] * (k-1)
    final_sigmas0 = [0] * (k-1)
    sigmas0 = [2.10] * k
    x0 = np.asarray(lambdas0 + final_sigmas0 + sigmas0)
    return x0


def add_dependant_variables_to_free_variables(x, k, T, r):
    if k > 1:
        lambdas = np.concatenate((x[0:k - 1], np.array([1 - sum(x[0:k - 1])])))
        final_sigmas = x[k - 1:2 * (k - 1)]
        sum_of_weighted_lambdas = sum(lambdas[0:k-1] * np.exp(final_sigmas[0:k-1] * T))
        sum_of_lambdas = sum(lambdas[0:k-1])
        final_sigma_k = 1 / T * np.log((math.exp(r * T) - sum_of_weighted_lambdas) / (1 - sum_of_lambdas))
        final_sigmas = np.append(final_sigmas, final_sigma_k)
    else:
        lambdas = np.array([1])
        final_sigmas = np.array([r])
    sigmas = np.array(x[2 * (k - 1):])
    return lambdas, final_sigmas, sigmas


def constraint_lambdas(x0, k):
    return 1 - sum(x0[0:k-1])


def calculate_model_prices(options, k, lambdas, final_sigmas, sigmas):
    prices = []
    for option in options:
        prices.append(option.price(k, lambdas, sigmas, final_sigmas))
    return prices


class PenaltyCalculator:
    def __init__(self, option_quotes, options, number_of_lognormal_distributions, time_to_expiry, interest_rate):
        self.option_quotes = option_quotes
        self.options = options
        self.k = number_of_lognormal_distributions
        self.time_to_expiry = time_to_expiry
        self.interest_rate = interest_rate

    def penalty_function(self, x):
        lambdas, final_sigmas, sigmas = add_dependant_variables_to_free_variables(x, self.k, self.time_to_expiry, self.interest_rate)
        i = 0
        penalty = 0
        for option_quote in self.option_quotes.iterrows():
            market_price = option_quote[1]['Midpoint']
            model_price = self.options[i].price(self.k, lambdas, sigmas, final_sigmas)
            volume = int(option_quote[1]['Volume'].replace(',', ''))
            penalty = penalty + volume * (market_price - model_price) ** 2
            i = i + 1
        return penalty / 1000
