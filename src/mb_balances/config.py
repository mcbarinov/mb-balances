"""Config models for mb-balances."""

from typing import Literal

from mm_clikit import TomlConfig
from pydantic import BaseModel, Field


class AssetConfig(BaseModel):
    """One [[assets]] entry — a coin/token to track on a given network."""

    model_config = TomlConfig.model_config

    ticker: str
    """Coin/token symbol, e.g. BTC, ETH, USDT."""

    network: str
    """Blockchain network identifier, e.g. bitcoin, ethereum, solana."""

    addresses: str
    """One or more addresses (newline-separated), or a group ref: 'group: name'."""

    label: str | None = None
    """Optional human label for this entry, e.g. exchange name or wallet purpose."""

    token: str | None = None
    """Token contract address for non-native tokens (e.g. ERC-20, Aptos token)."""

    decimals: int | None = None
    """Token decimal places — required when the API doesn't return it automatically."""

    share: str | None = None
    """Formula for partial ownership of the balance, e.g. '0.5(total - 100)'."""


class GroupConfig(BaseModel):
    """One [[groups]] entry — a named set of addresses for reuse across assets."""

    model_config = TomlConfig.model_config

    name: str
    """Group name, referenced as 'group: <name>' in asset addresses."""

    addresses: str
    """Newline-separated list of addresses."""


class Settings(BaseModel):
    """[settings] block — all fields optional, sensible defaults provided."""

    model_config = TomlConfig.model_config

    precision: int = 4
    """Decimal places for displayed balances."""

    show_price: bool = True
    """Fetch current prices and show USD (or other currency) values."""

    skip_empty: bool = False
    """Omit assets with a zero balance from output."""

    debug: bool = False
    """Print debug information during execution."""

    format: Literal["table", "json"] = "table"
    """Output format."""

    number_separator: str = ","
    """Thousands separator for formatted numbers."""

    currency: str = "usd"
    """Currency for total values, e.g. usd, eur, btc."""

    timeout: int = 30
    """HTTP request timeout in seconds."""

    proxies: str = ""
    """Proxy URLs (newline-separated). Lines starting with # are ignored."""


class Config(TomlConfig):
    """Top-level config loaded from a TOML file."""

    assets: list[AssetConfig]
    """List of assets to track."""

    groups: list[GroupConfig] = Field(default_factory=list)
    """Named address groups for reuse across multiple assets."""

    settings: Settings = Settings()
    """Global display and behavior settings."""
