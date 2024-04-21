from dataclasses import dataclass


@dataclass
class DriverOptions:
    user_multi_procs: bool | None = None
    log_level: str | None = None
    headless: bool | None = None
    user_agent: str | None = None
    disable_notifications: bool = True
