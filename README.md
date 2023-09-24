# Mitsubishi MELCloud Client

# Installation

Client can be installed via `pip` directly from GitHub using command

```
pip install git+https://github.com/niqiv/melcloud_client.git
```

or locally for development after pulling directory, using commands

```
git clone https://github.com/niqiv/melcloud_client.git
cd melcloud_client
pip install -e .
```

# Usage

Import client and initialize it by logging in

```python
    from melcloud_client import MELCloudClient

    client = MELCloudClient(email='example@example.com', password='<password>')
```

When initializing the client, user can define to enable debugging, which prints out more information about the client and devices by adding debug flag
`MELCloudClient(debug=True')`.

Show all devices in MELCloud

```python
devices = client.get_devices()
for i in devices:
    print(i)
    energy_consumed = i.get_energy_consumed()
    print(energy_consumed)
```

Get history report for time period fron yesterday to today

```python
from datetime import datetime, timedelta
report = client.get_history_report(
    devices[0],
    datetime.utcnow() - timedelta(days=1),
    datetime.utcnow())
```

# Types

## MELCloudClient

Has basic funcitonality to fetch data from MELCloud

## MELCloudDevice

Is a basic data type to store data from MELCloud
