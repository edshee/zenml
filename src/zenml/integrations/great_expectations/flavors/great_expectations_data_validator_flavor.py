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
"""Great Expectations data validator flavor."""

import os
from typing import TYPE_CHECKING, Any, Dict, Optional, Type

from pydantic import validator

from zenml.data_validators.base_data_validator import (
    BaseDataValidatorConfig,
    BaseDataValidatorFlavor,
)
from zenml.integrations.great_expectations import (
    GREAT_EXPECTATIONS_DATA_VALIDATOR_FLAVOR,
)
from zenml.io import fileio

if TYPE_CHECKING:
    from zenml.integrations.great_expectations.data_validators import (
        GreatExpectationsDataValidator,
    )


class GreatExpectationsDataValidatorConfig(BaseDataValidatorConfig):
    """Config for the Great Expectations data validator.

    Attributes:
        context_root_dir: location of an already initialized Great Expectations
            data context. If configured, the data validator will only be usable
            with local orchestrators.
        context_config: in-line Great Expectations data context configuration.
        configure_zenml_stores: if set, ZenML will automatically configure
            stores that use the Artifact Store as a backend. If neither
            `context_root_dir` nor `context_config` are set, this is the default
            behavior.
        configure_local_docs: configure a local data docs site where Great
            Expectations docs are generated and can be visualized locally.
    """

    context_root_dir: Optional[str] = None
    context_config: Optional[Dict[str, Any]] = None
    configure_zenml_stores: bool = False
    configure_local_docs: bool = True

    @validator("context_root_dir")
    def _ensure_valid_context_root_dir(
        cls, context_root_dir: Optional[str] = None
    ) -> Optional[str]:
        """Ensures that the root directory is an absolute path and points to an existing path.

        Args:
            context_root_dir: The context_root_dir value to validate.

        Returns:
            The context_root_dir if it is valid.

        Raises:
            ValueError: If the context_root_dir is not valid.
        """
        if context_root_dir:
            context_root_dir = os.path.abspath(context_root_dir)
            if not fileio.exists(context_root_dir):
                raise ValueError(
                    f"The Great Expectations context_root_dir value doesn't "
                    f"point to an existing data context path: {context_root_dir}"
                )
        return context_root_dir


class GreatExpectationsDataValidatorFlavor(BaseDataValidatorFlavor):
    """Great Expectations data validator flavor."""

    @property
    def name(self) -> str:
        return GREAT_EXPECTATIONS_DATA_VALIDATOR_FLAVOR

    @property
    def config_class(self) -> Type[GreatExpectationsDataValidatorConfig]:
        return GreatExpectationsDataValidatorConfig

    @property
    def implementation_class(self) -> Type["GreatExpectationsDataValidator"]:
        from zenml.integrations.great_expectations.data_validators import (
            GreatExpectationsDataValidator,
        )

        return GreatExpectationsDataValidator
