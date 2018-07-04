from models.jnmf.JnmfClass import JointNmfClass
import numpy as np


class IntegrativeNmfClass(JointNmfClass):
    def __init__(self, x: dict, k: int, lamb: int):
        """Initializes the class with Integrative NMF algorithm parameters
        
        Arguments:
            x {dict} -- [Dictionary of the data]
            k {int} -- [Rank]
            lamb {int} -- [Hyper-parameter for the Integrative NMF algorithm that controls the rate of learning]
        """
        super().__init__(x, k)
        self.v = None
        self.lamb = lamb
        self.slamb = None

    def initialize_wh(self):
        number_of_samples = list(self.x.values())[0].shape[0]
        self.w = np.random.rand(number_of_samples, self.k)

        self.v = {}
        self.h = {}
        for key in self.x:
            self.h[key] = np.random.rand(self.k, self.x[key].shape[1])
            self.v[key] = np.random.rand(number_of_samples, self.k)

    def update_weights(self):
        w = self.w
        v = self.v
        h = self.h
        numerator = np.zeros(w.shape)
        denominator = np.zeros(w.shape)

        for key in self.x:
            numerator = numerator + np.dot(self.x[key], h[key].T)
            denominator = denominator + np.dot(w+v[key], np.dot(h[key], h[key].T))

            self.h[key] = h[key] * np.dot((w + v[key]).T, self.x[key]) / (np.dot(np.dot((w+v[key]).T, w+v[key]), h[key]) + self.lamb * np.dot(v[key].T, np.dot(v[key], h[key])))
            self.v[key] = np.dot(self.x[key], h[key].T)/ (np.dot(w+v[key], np.dot(h[key], h[key].T)) + self.lamb * np.dot(v[key], np.dot(h[key], h[key].T)))

        self.w = self.w * numerator / denominator
        self.calc_error()