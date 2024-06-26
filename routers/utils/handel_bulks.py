import os
from datetime import datetime
from typing import List
from sortedcontainers import SortedList


def read_in_bulks(data_source: str = "sources", num: int = 1000) -> List[dict]:
    file_path = os.path.join(data_source, 'fake_cloud_events.csv')
    with open(file_path, "r") as f:
        next(f)
        while True:
            chunk = SortedList(key=lambda x: (x['event_id'], x['request_id'], x['event_type']))
            try:
                for _ in range(num):
                    line = next(f)
                    row_values = line.strip().split(';')
                    event_id, request_id, event_type, event_timestamp, affected_assets = row_values
                    event_timestamp = datetime.strptime(event_timestamp, '%Y-%m-%d %H:%M:%S')
                    row_dict = {'event_id': event_id, 'request_id': request_id, 'event_type': event_type,
                                'event_timestamp': event_timestamp, 'affected_assets': affected_assets}
                    chunk.add(row_dict)
            except StopIteration:
                if chunk:
                    yield chunk
                break
            yield chunk
