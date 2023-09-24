import requests
import json
from datetime import datetime

from .device import MELCloudDevice

API_ROOT_URI = 'https://app.melcloud.com'


class MELCloudClient:
    def __init__(self, email: str = '', password: str = '', debug=False):
        self.debug = debug
        self.email: str = email
        self.app_version: str = '1.28.1.0'
        self.token: str | None = self.login(password)
        self.auth_headers: dict = {
            'X-MitsContextKey': self.token
        }

        self.devices: [MELCloudDevice] = self._fetch_devices()

    def login(self, password):
        login_json = {
            "Email": self.email,
            "Password": password,
            "AppVersion": self.app_version
        }

        r = requests.post(
            API_ROOT_URI + '/Mitsubishi.Wifi.Client/Login/ClientLogin',
            json=login_json
        )
        if r.status_code == 200:
            return r.json().get('LoginData').get('ContextKey')
        else:
            return

    def _fetch_devices(self):
        r = requests.get(
            API_ROOT_URI + '/Mitsubishi.Wifi.Client/User/ListDevices',
            headers=self.auth_headers
        )
        devices = []
        if r.status_code == 200:
            data = r.json()
            for building in data:
                for device in building.get('Structure').get('Devices'):
                    devices.append(MELCloudDevice(device, debug=self.debug))

        return devices

    def get_devices(self) -> [MELCloudDevice]:
        return self.devices

    def get_device_state(self, device):
        print(device.id, device.building_id)
        r = requests.get(
            API_ROOT_URI +
            f'/Mitsubishi.Wifi.Client/Device/Get?id={device.id}&buildingID={device.building_id}',
            headers=self.auth_headers
        )
        return r.json()

    def update(self):
        self.devices = self._fetch_devices()

    def get_history_report(self, device, from_date, to_date):
        r = requests.post(
            API_ROOT_URI + f'/Mitsubishi.Wifi.Client/EnergyCost/Report',
            headers=self.auth_headers,
            json={
                "DeviceId": device.id,
                "FromDate": from_date.strftime("%Y-%m-%dT00:00:00"),
                "ToDate": to_date.strftime("%Y-%m-%dT00:00:00"),
                "UseCurrency": 'kWh'
            })

        if r.status_code == 200:
            result = r.json()
            time_start = int(datetime.strptime(
                result.get('FromDate'),
                '%Y-%m-%dT%H:%M:%S'
            ).timestamp() * 10**9)
            unit = result.get('CurrencySymbol', 'kWh')
            labels = result.get('Labels')

            data = {}
            for i, label in enumerate(labels):
                if result.get('LabelType') == 0:    # Hours
                    timestamp = (time_start + i * 60 * 60 * 10**9)
                elif result.get('LabelType') == 1:  # Days
                    timestamp = (time_start + i * 24 * 60 * 60 * 10**9)
                else:
                    raise ValueError('Label type not known')

                data[timestamp] = {
                    'heating': result.get('Heating')[i],
                    'cooling': result.get('Cooling')[i],
                    'dry': result.get('Dry')[i],
                    'auto': result.get('Auto')[i],
                    'fan': result.get('Fan')[i],
                    'other': result.get('Other')[i],
                }

            return data
