from datetime import datetime, timedelta
from influxdb import InfluxDBClient
from influxdb.exceptions import InfluxDBServerError
import os

from melcloud_client import MELCloudClient

client = InfluxDBClient(
    host=os.environ['INFLUX_ADDR'] if (
        'INFLUX_ADDR' in os.environ) else 'localhost',
    port=os.environ['INFLUX_PORT'] if ('INFLUX_PORT' in os.environ) else 8086,
    database=os.environ['INFLUX_DB'] if (
        'INFLUX_DB' in os.environ) else 'melcloud',
)


def save_measurements(data):
    body = []
    for timestamp in data:
        for mode in data[timestamp]:

            tmp = {
                'measurement': 'energy',
                'time': timestamp,
                'tags': {
                    'location': 'living room',
                    'mode': mode
                },
                'fields': {
                    'energy_used': data[timestamp][mode]
                }
            }
            body.append(tmp)

    client.write_points(body)
    return len(body)


def main():
    client = MELCloudClient(
        email='<EMAIL>', password='<PASSWORD>')
    device = client.get_devices()[0]
    data = client.get_history_report(
        device,
        datetime.utcnow() - timedelta(days=0),
        datetime.utcnow() - timedelta(days=0)
    )

    points_written = save_measurements(data)

    now = datetime.now()
    print('[{}] melcloud: Successfully fetched {} datapoints.'.format(
        now.strftime('%Y-%m-%d %H:%M:%S'),
        points_written
    ))


if __name__ == '__main__':
    main()
