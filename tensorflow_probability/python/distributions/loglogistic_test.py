# Copyright 2020 The TensorFlow Probability Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ============================================================================
"""Tests for LogLogistic."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

# Dependency imports

import numpy as np
import tensorflow.compat.v2 as tf
from scipy import stats

from tensorflow_probability.python import distributions as tfd
from tensorflow_probability.python.internal import test_util


@test_util.test_all_tf_execution_regimes
class LogLogiticTest(test_util.TestCase):

  def setUp(self):
    self._rng = np.random.RandomState(123)

  def testLogLogisticMean(self):
    scale = np.float32([3., 1.5, 0.75])
    concentration = np.float32([0.4, 1.1, 2.1])
    dist = tfd.LogLogistic(scale=scale, concentration=concentration,
                           validate_args=True)

    self.assertAllClose(
      self.evaluate(dist.mean()),
      stats.fisk.mean(loc=0., scale=scale, c=concentration)
    )

  def testLogLogisticMeanNoNanAllowed(self):
    scale = np.float32([3., 1.5, 0.75])
    concentration = np.float32([0.4, 1.1, 2.1])
    dist = tfd.LogLogistic(scale=scale, concentration=concentration,
                           validate_args=True, allow_nan_stats=False)

    with self.assertRaisesOpError('Condition x < y.*'):
      self.evaluate(dist.mean())

  def testLogLogisticVariance(self):
    scale = np.float32([3., 1.5, 0.75])
    concentration = np.float32([0.4, 1.1, 2.1])
    dist = tfd.LogLogistic(scale=scale, concentration=concentration,
                           validate_args=True)

    self.assertAllClose(
      self.evaluate(dist.variance()),
      stats.fisk.var(loc=0., scale=scale, c=concentration)
    )
    self.assertAllClose(
      self.evaluate(dist.stddev()),
      stats.fisk.std(loc=0., scale=scale, c=concentration)
    )

  def testLogLogisticVarianceNoNanAllowed(self):
    scale = np.float32([3., 1.5, 0.75])
    concentration = np.float32([0.4, 1.1, 2.1])
    dist = tfd.LogLogistic(scale=scale, concentration=concentration,
                           validate_args=True, allow_nan_stats=False)

    with self.assertRaisesOpError('Condition x < y.*'):
      self.evaluate(dist.mean())

    with self.assertRaisesOpError('Condition x < y.*'):
      self.evaluate(dist.stddev())

  def testLogLogisticMode(self):
    scale = np.float32([3., 1.5, 0.75])
    concentration = np.float32([0.4, 1.1, 2.1])
    dist = tfd.LogLogistic(scale=scale, concentration=concentration,
                           validate_args=True)
    mode = scale * ((concentration - 1.) / (concentration + 1.)
                    ) ** (1. / concentration)
    mode[0] = 0.
    self.assertAllClose(
      self.evaluate(dist.mode()),
      mode
    )

  def testLogLogisticEntropy(self):
    scale = np.float32([3., 1.5, 0.75])
    concentration = np.float32([0.4, 1.1, 2.1])
    dist = tfd.LogLogistic(scale=scale, concentration=concentration,
                           validate_args=True)

    self.assertAllClose(
      self.evaluate(dist.entropy()),
      stats.fisk.entropy(loc=0., scale=scale, c=concentration)
    )

  def testLogLogisticSample(self):
    scale, concentration = 1.5, 3.
    dist = tfd.LogLogistic(scale=scale, concentration=concentration,
                           validate_args=True)
    samples = self.evaluate(dist.sample(6000, seed=test_util.test_seed()))
    self.assertAllClose(np.mean(samples),
                        self.evaluate(dist.mean()),
                        atol=0.1)
    self.assertAllClose(np.std(samples),
                        self.evaluate(dist.stddev()),
                        atol=0.5)

  def testLogLogisticPDF(self):
    scale = 1.5
    concentration = 0.4
    dist = tfd.LogLogistic(scale=scale, concentration=concentration,
                           validate_args=True)

    x = np.array([1e-4, 1.0, 2.0], dtype=np.float32)

    pdf = dist.prob(x)

    self.assertAllClose(
      self.evaluate(pdf),
      stats.fisk.pdf(x, loc=0., scale=scale, c=concentration)
    )

  def testLogLogisticLogPDF(self):
    scale = 1.5
    concentration = 0.4
    dist = tfd.LogLogistic(scale=scale, concentration=concentration,
                           validate_args=True)

    x = np.array([1e-4, 1.0, 2.0], dtype=np.float32)

    log_pdf = dist.log_prob(x)

    self.assertAllClose(
      self.evaluate(log_pdf),
      stats.fisk.logpdf(x, loc=0., scale=scale, c=concentration)
    )

  def testLogLogisticCDF(self):
    scale = 1.5
    concentration = 0.4
    dist = tfd.LogLogistic(scale=scale, concentration=concentration,
                           validate_args=True)

    x = np.array([1e-4, 1.0, 2.0], dtype=np.float32)

    cdf = dist.cdf(x)
    self.assertAllClose(
      self.evaluate(cdf),
      stats.fisk.cdf(x, loc=0., scale=scale, c=concentration)
    )

  def testLogLogisticLogCDF(self):
    scale = 1.5
    concentration = 0.4
    dist = tfd.LogLogistic(scale=scale, concentration=concentration,
                           validate_args=True)

    x = np.array([1e-4, 1.0, 2.0], dtype=np.float32)

    log_cdf = dist.log_cdf(x)
    self.assertAllClose(
      self.evaluate(log_cdf),
      stats.fisk.logcdf(x, loc=0., scale=scale, c=concentration)
    )

  def testLogLogisticLogSurvival(self):
    scale = 1.5
    concentration = 0.4
    dist = tfd.LogLogistic(scale=scale, concentration=concentration,
                           validate_args=True)

    x = np.array([1e-4, 1.0, 2.0], dtype=np.float32)

    logsf = dist.log_survival_function(x)
    self.assertAllClose(
      self.evaluate(logsf),
      stats.fisk.logsf(x, loc=0., scale=scale, c=concentration)
    )

  def testAssertValidSample(self):
    dist = tfd.LogLogistic(scale=[1., 1., 4.], concentration=2.,
                           validate_args=True)
    with self.assertRaisesOpError('Sample must be non-negative.'):
      self.evaluate(dist.cdf([3., -0.2, 1.]))

  def testSupportBijectorOutsideRange(self):
    dist = tfd.LogLogistic(scale=1., concentration=2., validate_args=True)
    with self.assertRaisesOpError('must be greater than or equal to 0'):
      dist._experimental_default_event_space_bijector().inverse(
          [-4.2, -1e-6, -1.3])

if __name__ == '__main__':
  tf.test.main()
