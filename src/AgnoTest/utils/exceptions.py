class CoreError(Exception):
    """Base error for the framework."""


class ConfigError(CoreError):
    """Raised when configuration is missing or invalid."""


class AgentBuildError(CoreError):
    """Raised when an Agent cannot be constructed."""


class TeamBuildError(CoreError):
    """Raised when a Team cannot be constructed."""

class OrchestratorError(CoreError):
    """Raised for AgentOS/runtime orchestration issues."""

