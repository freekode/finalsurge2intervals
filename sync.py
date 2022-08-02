import api
import enum
from datetime import date

class SyncValueType(enum.Enum):
    HRV = ['HRV', 'hrv']
    RHR = ['Resting HR', 'restingHR']
    WEIGHT = ['Weight', 'weight']

class Synchronizer:
    def __init__(self, finalsurge_api: api.FinalSurgeApi, intervals_api , sync_past_days):
        self.finalsurge_api = finalsurge_api
        self.intervals_api = intervals_api
        self.sync_past_days = sync_past_days

    def sync_values(self, value_types_to_sync):
        fs_wellness_days = self.finalsurge_api.get_wellness(self.sync_past_days)
        for fs_wellness_day in fs_wellness_days:
            current_date = fs_wellness_day['Date']
            in_wellness_day = self.intervals_api.wellness(date.fromisoformat(current_date))

            wellness_udpated = False
            for value_type_to_sync in value_types_to_sync:
                fs_value_key = value_type_to_sync.value[0]
                in_value_key = value_type_to_sync.value[1]
                fs_value = fs_wellness_day[fs_value_key]
                in_value = in_wellness_day[in_value_key]

                if fs_value and not in_value:
                    in_wellness_day[in_value_key] = self._parse_value(fs_value, value_type_to_sync)
                    wellness_udpated = True

            if not wellness_udpated:
                continue

            self.intervals_api.wellness_put(in_wellness_day)
            print('synced for ' + current_date)

    def _parse_value(self, value, value_type_to_sync: SyncValueType):
        if SyncValueType.RHR is value_type_to_sync:
            return value[:-3].strip()
        return value