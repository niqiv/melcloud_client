# Mitsubishi MELCloud Client

Import client and initialize it by logging in

```python
    from melcloud_client import MELCloudClient

    client = MELCloudClient(email='example@example.com', password='<password>')
```

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
