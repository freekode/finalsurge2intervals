from array import array
from traceback import print_tb
import api
import enum

class SyncValueType(enum.Enum):
    HRV = ['HRV', 'readiness']
    RHR = ['Resting HR', 'restingHR']
    WEIGHT = ['Weight', 'weight']

class Synchronizer:
    def __init__(self, finalsurge_api: api.FinalSurgeApi, intervals_api: api.IntervalsApi, sync_past_days):
        self.finalsurge_api = finalsurge_api
        self.intervals_api = intervals_api
        self.sync_past_days = sync_past_days

    def sync_values(self, value_types_to_sync):
        fs_wellness = self.finalsurge_api.get_wellness(self.sync_past_days)
        for fs_day in fs_wellness:
            date = fs_day['Date']
            in_day = self.intervals_api.get_wellness(date)

            in_update_data = {}
            for value_type_to_sync in value_types_to_sync:
                fs_value_key = value_type_to_sync.value[0]
                in_value_key = value_type_to_sync.value[1]
                fs_value = fs_day[fs_value_key]
                in_value = in_day[in_value_key]

                if fs_value and not in_value:
                    in_update_data[in_value_key] = self._parse_value(fs_value, value_type_to_sync)
        
            if not in_update_data:
                continue

            # print(in_update_data)
            self.intervals_api.update_wellness(date, in_update_data)
            print('synced for ' + date)

    def _parse_value(self, value, value_type_to_sync: SyncValueType):
        if SyncValueType.RHR is value_type_to_sync:
            return value[:-3].strip()
        return value