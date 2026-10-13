"""Simulation crucibles and benchmark suites for Skillware-Bench."""

from skillware_bench.suites.gmail_crucible import GmailWorkflowCrucible
from skillware_bench.suites.companies_house_crucible import CompaniesHouseCrucible
from skillware_bench.suites.wallet_screening_crucible import WalletScreeningCrucible
from skillware_bench.suites.constitution_crucible import ConstitutionStressCrucible
from skillware_bench.suites.chained_pipeline_crucible import ChainedPipelineCrucible

ALL_CRUCIBLES = {
    "gmail": GmailWorkflowCrucible,
    "companies_house": CompaniesHouseCrucible,
    "wallet_screening": WalletScreeningCrucible,
    "constitution": ConstitutionStressCrucible,
    "chained_pipeline": ChainedPipelineCrucible,
}
