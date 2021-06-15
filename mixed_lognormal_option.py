import math
import numpy as np
from scipy.stats import norm


class MixedLognormalOption:
    def __init__(self, stock_price, strike, interest_rate, time_to_expiry, is_call):
        self.stock_price = stock_price
        self.strike = strike
        self.interest_rate = interest_rate
        self.time_to_expiry = time_to_expiry
        self.is_call = is_call

    def price(self, k, lambdas, sigmas, final_sigmas):
        price = 0
        if self.is_call:
            for j in range(0, k):
                d_1 = self.d1(self.stock_price, self.strike, final_sigmas[j], sigmas[j], self.time_to_expiry)
                d_2 = self.d2(self.stock_price, self.strike, final_sigmas[j], sigmas[j], self.time_to_expiry)
                price = price + lambdas[j] * \
                        (self.stock_price * math.exp((final_sigmas[j] - self.interest_rate) * self.time_to_expiry) *
                         norm.cdf(d_1) - self.strike * math.exp(- self.interest_rate * self.time_to_expiry) *
                         norm.cdf(d_2))
        else:
            for j in range(0, k):
                price = price + lambdas[j] *\
                        (self.strike * math.exp(- self.interest_rate * self.time_to_expiry) *
                         norm.cdf(-1 * self.d2(self.stock_price, self.strike, final_sigmas[j], sigmas[j], self.time_to_expiry))
                         - self.stock_price * math.exp((final_sigmas[j] - self.interest_rate) * self.time_to_expiry) *
                         norm.cdf(-1 * self.d1(self.stock_price, self.strike, final_sigmas[j], sigmas[j], self.time_to_expiry)))
        return price

    def implied_volatility(self, ):
        pass

    @staticmethod
    def d1(S, K, final_sigma, sigma, T):
        return (np.log(S / K) + (final_sigma + 0.5 * sigma ** 2) * T)/(sigma * math.sqrt(T))

    def d2(self, S, K, final_sigma, sigma, T):
        return self.d1(S, K, final_sigma, sigma, T) - sigma * math.sqrt(T)
