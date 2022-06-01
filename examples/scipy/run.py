#  Copyright (c) ZenML GmbH 2022. All Rights Reserved.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at:
#
#       https://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
#  or implied. See the License for the specific language governing
#  permissions and limitations under the License.
from pipelines.training_pipeline.training_pipeline import scipy_example_pipeline
from steps.loader.loader_step import importer
from steps.predictor.predictor_step import predictor
from steps.trainer.trainer_step import trainer
from steps.vectorizer.vectorizer_step import vectorizer

if __name__ == "__main__":
    run = scipy_example_pipeline(importer=importer(),
               vectorizer=vectorizer(),
               trainer=trainer(),
               predictor=predictor())
    run.run()
