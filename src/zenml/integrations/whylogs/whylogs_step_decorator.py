#  Copyright (c) ZenML GmbH 2022. All Rights Reserved.
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
"""Implementation of the whylogs step decorator."""

import functools
from typing import (
    Any,
    Callable,
    Dict,
    Optional,
    Type,
    TypeVar,
    Union,
    cast,
    overload,
)

from zenml.integrations.whylogs.whylogs_context import WhylogsContext
from zenml.steps import BaseStep
from zenml.steps.step_context import StepContext
from zenml.steps.utils import STEP_INNER_FUNC_NAME

# step entrypoint type
F = TypeVar("F", bound=Callable[..., Any])

# step class type
S = TypeVar("S", bound=Type[BaseStep])


@overload
def enable_whylogs(
    _step: S,
) -> S:
    ...


@overload
def enable_whylogs(
    *,
    project: Optional[str] = None,
    pipeline: Optional[str] = None,
    tags: Optional[Dict[str, str]] = None,
) -> Callable[[S], S]:
    ...


def enable_whylogs(
    _step: Optional[S] = None,
    *,
    project: Optional[str] = None,
    pipeline: Optional[str] = None,
    tags: Optional[Dict[str, str]] = None,
) -> Union[S, Callable[[S], S]]:
    """Decorator to enable whylogs profiling for a step function.

    Apply this decorator to a ZenML pipeline step to enable whylogs profiling.
    The decorated function will be given access to a StepContext `whylogs`
    field that facilitates access to the whylogs dataset profiling API,
    like so:

    ```python
    @enable_whylogs
    @step(enable_cache=True)
    def data_loader(
        context: StepContext,
    ) -> Output(data=pd.DataFrame, profile=DatasetProfile,):
        ...
        data = pd.DataFrame(...)
        profile = context.whylogs.profile_dataframe(data, dataset_name="input_data")
        ...
        return data, profile
    ```

    You can also use this decorator with our class-based API like so:
    ```
    @enable_whylogs
    class DataLoader(BaseStep):
        def entrypoint(
            self,
            context: StepContext
        ) -> Output(data=pd.DataFrame, profile=DatasetProfile,):
            ...
    ```

    Args:
        _step: The decorated step class.
        project: optional project name to use for the whylogs session
        pipeline: optional pipeline name to use for the whylogs session
        tags: optional list of tags to apply to all profiles generated by this
            step

    Returns:
        the inner decorator which enhaces the input step class with whylogs
        profiling functionality
    """

    def inner_decorator(_step: S) -> S:
        source_fn = getattr(_step, STEP_INNER_FUNC_NAME)
        new_entrypoint = whylogs_entrypoint(project, pipeline, tags)(source_fn)
        if _step._created_by_functional_api():
            # If the step was created by the functional API, the old entrypoint
            # was a static method -> make sure the new one is as well
            new_entrypoint = staticmethod(new_entrypoint)

        setattr(_step, STEP_INNER_FUNC_NAME, new_entrypoint)
        return _step

    if _step is None:
        return inner_decorator
    else:
        return inner_decorator(_step)


def whylogs_entrypoint(
    project: Optional[str] = None,
    pipeline: Optional[str] = None,
    tags: Optional[Dict[str, str]] = None,
) -> Callable[[F], F]:
    """Decorator for a step entrypoint to enable whylogs.

    Apply this decorator to a ZenML pipeline step to enable whylogs profiling.
    The decorated function will be given access to a StepContext `whylogs`
    field that facilitates access to the whylogs dataset profiling API,
    like so:

    .. highlight:: python
    .. code-block:: python

        @step(enable_cache=True)
        @whylogs_entrypoint()
        def data_loader(
            context: StepContext,
        ) -> Output(data=pd.DataFrame, profile=DatasetProfile,):
            ...
            data = pd.DataFrame(...)
            profile = context.whylogs.profile_dataframe(data, dataset_name="input_data")
            ...
            return data, profile

    Args:
        project: optional project name to use for the whylogs session
        pipeline: optional pipeline name to use for the whylogs session
        tags: optional list of tags to apply to all profiles generated by this
            step

    Returns:
        the input function enhanced with whylogs profiling functionality
    """

    def inner_decorator(func: F) -> F:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:  # noqa

            for arg in args + tuple(kwargs.values()):
                if isinstance(arg, StepContext):
                    arg.__dict__["whylogs"] = WhylogsContext(
                        arg, project, pipeline, tags
                    )
                    break
            return func(*args, **kwargs)

        return cast(F, wrapper)

    return inner_decorator