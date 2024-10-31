"""Define test fixtures for Tile."""

from collections.abc import Generator
import json
from typing import Any
from unittest.mock import AsyncMock, Mock, patch

import pytest
from pytile.tile import Tile

from homeassistant.components.tile.const import DOMAIN
from homeassistant.const import CONF_PASSWORD, CONF_USERNAME
from homeassistant.core import HomeAssistant

from tests.common import MockConfigEntry, load_fixture

TEST_PASSWORD = "123abc"
TEST_USERNAME = "user@host.com"


@pytest.fixture(name="api")
def api_fixture(data_tile_details: dict[str, Any]) -> Mock:
    """Define a pytile API object."""
    tile = Tile(None, data_tile_details)
    tile.async_update = AsyncMock()

    return Mock(
        async_get_tiles=AsyncMock(
            return_value={data_tile_details["result"]["tile_uuid"]: tile}
        )
    )


@pytest.fixture(name="config_entry")
def config_entry_fixture(
    hass: HomeAssistant, config: dict[str, Any]
) -> MockConfigEntry:
    """Define a config entry fixture."""
    entry = MockConfigEntry(domain=DOMAIN, unique_id=config[CONF_USERNAME], data=config)
    entry.add_to_hass(hass)
    return entry


@pytest.fixture(name="config")
def config_fixture() -> dict[str, Any]:
    """Define a config entry data fixture."""
    return {
        CONF_USERNAME: TEST_USERNAME,
        CONF_PASSWORD: TEST_PASSWORD,
    }


@pytest.fixture(name="data_tile_details", scope="package")
def data_tile_details_fixture():
    """Define a Tile details data payload."""
    return json.loads(load_fixture("tile_details_data.json", "tile"))


@pytest.fixture(name="mock_pytile")
def mock_pytile_fixture(api: Mock) -> Generator[None]:
    """Define a fixture to patch pytile."""
    with (
        patch(
            "homeassistant.components.tile.config_flow.async_login", return_value=api
        ),
        patch("homeassistant.components.tile.async_login", return_value=api),
    ):
        yield


@pytest.fixture(name="setup_config_entry")
async def setup_config_entry_fixture(
    hass: HomeAssistant, config_entry: MockConfigEntry, mock_pytile: None
) -> None:
    """Define a fixture to set up tile."""
    assert await hass.config_entries.async_setup(config_entry.entry_id)
    await hass.async_block_till_done()
