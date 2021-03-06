from sklearn import datasets, preprocessing, metrics
from sklearn.cross_validation import train_test_split
from sklearn.pipeline import Pipeline
from neupy import algorithms, layers, ensemble
from neupy.functions import rmsle

from base import BaseTestCase


class SklearnCompatibilityTestCase(BaseTestCase):
    verbose = False

    def test_pipeline(self):
        dataset = datasets.load_diabetes()
        target_scaler = preprocessing.MinMaxScaler()

        x_train, x_test, y_train, y_test = train_test_split(
            dataset.data,
            target_scaler.fit_transform(dataset.target),
            train_size=0.85
        )

        network = algorithms.Backpropagation(
            connection=[
                layers.SigmoidLayer(10),
                layers.SigmoidLayer(40),
                layers.OutputLayer(1),
            ],
            use_bias=True,
            show_epoch=100
        )
        pipeline = Pipeline([
            ('min_max_scaler', preprocessing.MinMaxScaler()),
            ('backpropagation', network),
        ])
        pipeline.fit(x_train, y_train, backpropagation__epochs=1000)
        y_predict = pipeline.predict(x_test)

        error = rmsle(target_scaler.inverse_transform(y_test),
                      target_scaler.inverse_transform(y_predict).round())
        self.assertAlmostEqual(0.4481, error, places=4)

    def test_ensemble(self):
        data, target = datasets.make_classification(300, n_features=4,
                                                    n_classes=2)
        x_train, x_test, y_train, y_test = train_test_split(
            data, target, train_size=0.7
        )

        dan = ensemble.DynamicallyAveragedNetwork([
            algorithms.RPROP((4, 100, 1), step=0.1, maximum_step=1),
            algorithms.Backpropagation((4, 5, 1), step=0.1),
            algorithms.ConjugateGradient((4, 5, 1), step=0.01),
        ])

        pipeline = Pipeline([
            ('min_max_scaler', preprocessing.StandardScaler()),
            ('dan', dan),
        ])
        pipeline.fit(x_train, y_train, dan__epochs=500)

        result = pipeline.predict(x_test)
        ensemble_result = metrics.accuracy_score(y_test, result)
        self.assertAlmostEqual(0.9222, ensemble_result, places=4)
