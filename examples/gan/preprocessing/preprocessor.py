#  Copyright (c) maiot GmbH 2020. All Rights Reserved.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at:
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
#  or implied. See the License for the specific language governing
#  permissions and limitations under the License.

from typing import Dict

import tensorflow as tf

from zenml.core.steps.preprocesser import BasePreprocesserStep


def decode_and_reshape_image(input_):
    densed = tf.sparse.to_dense(input_)
    image = tf.map_fn(lambda x: tf.io.decode_image(x[0], channels=3), densed,
                      dtype=tf.uint8)
    image = (tf.cast(image, tf.float32) / 127.5) - 1
    image = tf.reshape(image, [-1, 256, 256, 3])
    return image


class GANPreprocessor(BasePreprocesserStep):

    def __init__(self, **unused_kwargs):

        super(GANPreprocessor, self).__init__(**unused_kwargs)

    def preprocessing_fn(self, inputs: Dict):

        outputs = {}

        for k, v in inputs.items():
            if k == "image":
                result = decode_and_reshape_image(v)
                result = tf.cast(result, dtype=tf.float32)
                outputs[k + "_xf"] = result

        return outputs
