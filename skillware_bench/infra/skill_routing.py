# Copyright (c) 2026 ARPA Hellenic Logical Systems
# SPDX-License-Identifier: MIT

"""Route loaded Skillware skill HTTP traffic to the hermetic mock server.

Some published Skillware wheels freeze upstream API base URLs as module-level
constants at import time (for example ``_BASE_URL`` in
``finance/uk_companies_house_handler``). Setting environment variables after
import therefore has no effect, and the skill silently calls the live API.
This helper rebinds those constants on the loaded module and, when the skill
exposes a ``_request(method, endpoint, params=None)`` HTTP layer, rebinds it on
the instance so every call is deterministically served by the mock server,
independent of the installed ``skillware`` version.
"""

from typing import Any, Dict, Optional

import requests

_URL_CONSTANTS = ("_BASE_URL", "BASE_URL", "_DOCUMENT_API_BASE", "DOCUMENT_API_BASE")


def bind_skill_to_mock(
    skill_bundle: Dict[str, Any],
    skill_instance: Any,
    base_url: str,
    api_key: str = "mock-key-123",
    timeout: float = 15.0,
) -> None:
    """Point a loaded skill module and instance at ``base_url``."""
    module = skill_bundle.get("module")
    if module is not None:
        for attr in _URL_CONSTANTS:
            if hasattr(module, attr):
                setattr(module, attr, base_url)

    if skill_instance is None or not callable(getattr(skill_instance, "_request", None)):
        return

    def _hermetic_request(
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        clean_params = {k: v for k, v in params.items() if v is not None} if params else None
        response = requests.request(
            method,
            f"{base_url}/{endpoint.lstrip('/')}",
            auth=(api_key, ""),
            params=clean_params,
            timeout=timeout,
        )
        response.raise_for_status()
        return response.json()

    skill_instance._request = _hermetic_request
