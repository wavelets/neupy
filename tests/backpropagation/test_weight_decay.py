import numpy as np

from neupy.layers import TanhLayer, StepOutputLayer
from neupy.algorithms import WeightDecay, Backpropagation

from data import xor_input_train, xor_target_train
from base import BaseTestCase


class WeightDecayTestCase(BaseTestCase):
    def test_backpropagation(self):
        weight1 = np.array([
            [-0.53980522, -0.64724144, -0.92496063],
            [-0.04144865, -0.60458235,  0.25735483],
            [0.08818209, -0.10212516, -1.46030816]
        ])
        weight2 = np.array([
            [0.54230442],
            [0.1393251],
            [1.59479241],
            [0.1479949]
        ])

        input_layer = TanhLayer(2, weight=weight1)
        hidden_layer = TanhLayer(3, weight=weight2)
        output = StepOutputLayer(1, output_bounds=(-1, 1))

        network = Backpropagation(
            input_layer > hidden_layer > output,
            step=0.3,
            decay_rate=0.0001,
            use_raw_predict_at_error=True,
            optimizations=[WeightDecay]
        )
        network.train(xor_input_train, xor_target_train, epochs=500)
        self.assertEqual(round(network.last_error_in(), 2), 0)
