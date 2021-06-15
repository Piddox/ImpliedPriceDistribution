import math
import numpy as np
from scipy.stats import norm


class DensityCalculator:
    def __init__(self, lambdas, final_sigmas, sigmas, stock_price, time_to_expiry):
        self.lambdas = lambdas
        self.final_sigmas = final_sigmas
        self.sigmas = sigmas
        self.k = len(lambdas)
        self.alphas = np.log(stock_price) + (self.final_sigmas - 0.5 * self.sigmas ** 2) * time_to_expiry
        self.betas = self.sigmas * math.sqrt(time_to_expiry)

    def density_function(self, x):
        probability_density = 0
        for j in range(0, self.k):
            probability_density = probability_density + \
                                  self.lambdas[j] / (x * self.betas[j]) * \
                                  norm.pdf((np.log(x) - self.alphas[j]) / self.betas[j])
        return probability_density

    def expected_value(self):
        return sum(self.lambdas * np.exp(self.alphas + 0.5 * np.power(self.betas, 2)))
