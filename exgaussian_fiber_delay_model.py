#from netsquid.util import simtools
#from netsquid.components.models.model import Model, ModelCompositionException
from netsquid.components.models.delaymodels import FibreDelayModel
from netsquid.util.constrainedmap import positive_constr, nonnegative_constr
import random

class ExGaussianFibreDelayModel(FibreDelayModel):

    def __init__(self, c=200000, mu=0, sigma=1, lambd=1, **kwargs):
        super().__init__(**kwargs)
        self.add_property('c', c,
                          value_type=(int, float),
                          value_constraints=positive_constr)
        self.add_property('gaussian_mu', mu,
                          value_type=(int, float),
                          value_constraints=nonnegative_constr)
        self.add_property('gaussian_std', sigma,
                          value_type=(int, float),
                          value_constraints=nonnegative_constr)
        self.add_property('exp_lambda', lambd,
                          value_type=(int, float),
                          value_constraints=nonnegative_constr)
        self.required_properties = ['length']

    @property
    def c(self):
        """float: fixed speed of photons through the channel."""
        return self.properties['c']

    @c.setter
    def c(self, value):
        self.properties['c'] = value

    @property
    def mu(self):
        """float: Mean reaction delay."""
        return self.properties['gaussian_mu']

    @mu.setter
    def gaussian_mu(self, value):
        self.properties['gaussian_mu'] = value

    @property
    def sigma(self):
        """float: Standard deviation of reaction delay."""
        return self.properties['gaussian_std']

    @sigma.setter
    def sigma(self, value):
        self.properties['gaussian_std'] = value

    @property
    def lambd(self):
        """float: Exponential decay of reaction delay."""
        return self.properties['exp_lambda']

    @lambd.setter
    def lambd(self, value):
        self.properties['exp_lambda'] = value

    def get_mean(self, **kwargs):
       
        return self.generate_delay(**kwargs)

    def set_mean(self, value):
        
        raise NotImplementedError

    def get_std(self, **kwargs):
        
        return 0

    def generate_delay(self, **kwargs):
       
        propagation_delay = 1e9 * kwargs['length'] / self.c
        reaction_delay = self._generate_ex_gaussian()
        return propagation_delay + reaction_delay
    
    def _generate_ex_gaussian(self):
        """generate ex-gaussian distributed delay"""
        # exponential part
        exp_component = random.expovariate(self.lambd)
        # gaussian part
        gauss_component = random.gauss(self.mu, self.sigma)
        return exp_component + gauss_component
