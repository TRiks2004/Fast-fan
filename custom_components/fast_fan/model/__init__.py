from miio import MiotDevice
import asyncio
from custom_components.fast_fan.model.spiid import SPIID

class Device:

    def __init__(self, object: MiotDevice) -> None:
        self.object = object
        self.info = self.object.info()

        self.manufacturer, self.device, self.model, *obj = self.info.model.split(".")
                        

    async def _get(
        self, *, _command: SPIID
    ) -> int | float | bool | str:
        _values = await asyncio.to_thread(
            self.object.get_property_by,
            siid=_command.siid,
            piid=_command.piid
        )

        _value = _values[0]
        _code = _value.get('code')

        if _code is None or _code != 0:
            raise Exception(f'Error code: {_code}')

        return _value.get('value')

    async def _set(
        self, *, _command: SPIID,
        value: int | float | bool | str, timeout: int = 1
    ) -> None:
        await asyncio.to_thread(
            self.object.set_property_by,
            siid=_command.siid,
            piid=_command.piid,
            value=value
        )
