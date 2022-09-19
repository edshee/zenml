#  Copyright (c) ZenML GmbH 2021. All Rights Reserved.
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
"""Initialization of the GCP ZenML integration.

The GCP integration submodule provides a way to run ZenML pipelines in a cloud
environment. Specifically, it allows the use of cloud artifact stores
and provides an `io` module to handle file operations on Google Cloud Storage
(GCS).

Additionally, the GCP secrets manager integration submodule provides a
way to access the GCP secrets manager from within your ZenML Pipeline runs.

The Vertex AI integration submodule provides a way to run ZenML pipelines in a
Vertex AI environment.
"""

from typing import List, Type

from zenml.integrations.constants import GCP
from zenml.integrations.integration import Integration
from zenml.stack import Flavor

GCP_ARTIFACT_STORE_FLAVOR = "gcp"
GCP_SECRETS_MANAGER_FLAVOR = "gcp_secrets_manager"
GCP_VERTEX_ORCHESTRATOR_FLAVOR = "vertex"
GCP_VERTEX_STEP_OPERATOR_FLAVOR = "vertex"


class GcpIntegration(Integration):
    """Definition of Google Cloud Platform integration for ZenML."""

    NAME = GCP
    REQUIREMENTS = [
        "kfp==1.8.9",
        "gcsfs",
        "google-cloud-secret-manager",
        "google-cloud-aiplatform>=1.11.0",
    ]

    @classmethod
    def flavors(cls) -> List[Type[Flavor]]:
        """Declare the stack component flavors for the GCP integration.

        Returns:
            List of stack component flavors for this integration.
        """
        from zenml.integrations.gcp.flavors import (
            GCPArtifactStoreFlavor,
            GCPSecretsManagerFlavor,
            VertexOrchestratorFlavor,
            VertexStepOperatorFlavor,
        )

        return [
            VertexOrchestratorFlavor,
            VertexStepOperatorFlavor,
            GCPSecretsManagerFlavor,
            GCPArtifactStoreFlavor,
        ]


GcpIntegration.check_installation()
