from enum import Enum
import json

OPERATING_MODES = {
    1: 'Heating',
    2: 'Drying',
    3: 'Cooling',
    7: 'Fan',
    8: 'Auto'

}


class MELCloudDevice:

    def __init__(self, mel_data, debug=False):
        self.debug = debug
        if self.debug:
            print(json.dumps(mel_data))

        # Device identification information
        self.id: int = mel_data['DeviceID']
        self.building_id: int = mel_data['BuildingID']
        self.name: str = mel_data['DeviceName']

        # Store all data in devices to be queried as dict
        self._device = mel_data['Device']

        # Power status
        self.is_powered: bool = self._device['Power']
        self.is_standby: bool = self._device['InStandbyMode']

        # Energy information
        self.operation_mode: int = self._device['OperationMode']
        self.energy_consumed: int = self._device['CurrentEnergyConsumed']

        # Temperature measurements
        self.outdoor_temperature: float | None = self._device.get(
            'OutdoorTemperature', None)
        self.room_temperature: float | None = self._device.get(
            'RoomTemperature', None)
        self.set_temperature: float | None = self._device.get(
            'SetTemperature', None)

        # Other misc information
        self.wifi_signal_strength: int | None = self._device.get(
            'WifiSignalStrength', None)

    def get_energy_consumed(self):
        return self.energy_consumed

    def __str__(self) -> str:
        lines = []
        lines.append(f'{self.name}')
        if not self.is_powered:
            lines.append('NO POWER')
        elif self.is_standby:
            lines.append('IN STANDBY')
        else:
            lines.append(
                f'ACTIVE: {OPERATING_MODES.get(self.operation_mode, self.operation_mode)}')
        lines.append(f'Energy Consumed: {self.energy_consumed}')

        return '\n'.join(lines)
