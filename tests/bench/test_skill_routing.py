# Copyright (c) 2026 ARPA Hellenic Logical Systems
# SPDX-License-Identifier: MIT

"""Regression: Skillware skill HTTP must reach the hermetic mock server.

Guards against skills that freeze their upstream base URL at import time
(observed with the PyPI skillware 0.6.0 Companies House handler), which made
the Skillware arm call the live API with a mock key and fail with HTTP 401.
"""

import types

import pytest

from skillware_bench.infra.hermetic_mock_server import HermeticMockServer
from skillware_bench.infra.skill_routing import bind_skill_to_mock

LIVE_URL = "https://api.company-information.service.gov.uk"


class _FrozenUrlSkill:
    """Mimics a skill whose _request reads a module constant frozen at import."""

    def __init__(self, module: types.ModuleType):
        self._module = module

    def _request(self, method, endpoint, params=None):
        raise AssertionError(f"live call attempted: {self._module._BASE_URL}{endpoint}")

    def execute(self, params):
        return self._request("GET", "/search/companies", params={"q": params["query"]})


@pytest.fixture
def server():
    srv = HermeticMockServer()
    srv.start()
    try:
        yield srv
    finally:
        srv.stop()


def test_bind_skill_to_mock_rebinds_constants_and_request(server):
    module = types.ModuleType("skill_module")
    module._BASE_URL = LIVE_URL
    module._DOCUMENT_API_BASE = LIVE_URL
    skill = _FrozenUrlSkill(module)

    bind_skill_to_mock({"module": module}, skill, server.base_url)

    assert module._BASE_URL == server.base_url
    assert module._DOCUMENT_API_BASE == server.base_url
    result = skill.execute({"query": "DEEPMIND TECHNOLOGIES LIMITED"})
    numbers = [item["company_number"] for item in result["items"]]
    assert "07386350" in numbers


def test_real_companies_house_skill_resolves_against_mock(server):
    loader = pytest.importorskip("skillware.core.loader")
    try:
        bundle = loader.SkillLoader.load_skill(
            "finance/uk_companies_house_handler", check_requirements=False
        )
    except Exception as exc:  # skill not shipped in this skillware build
        pytest.skip(f"companies house skill unavailable: {exc}")

    skill_cls = loader.SkillLoader.get_skill_class(bundle)
    skill = skill_cls({"COMPANIES_HOUSE_API_KEY": "mock-key-123"})
    bind_skill_to_mock(bundle, skill, server.base_url)

    result = skill.execute({"action": "resolve_company", "query": "DEEPMIND TECHNOLOGIES LIMITED"})
    assert result["status"] == "ready", result
    assert result["company_number"] == "07386350"
