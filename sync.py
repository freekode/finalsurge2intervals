
class Synchronizer:
    def __init__(self, finalsurge_api, intervals_api):
        self.finalsurge_api = finalsurge_api
        self.intervals_api = intervals_api

    def sync_hrv(self):
        daily_vitals = self.finalsurge_api.get_daily_vitals()
        for day in daily_vitals:
            date = day['Date']
            hrv = day['HRV']
            if not hrv:
                continue

            self.intervals_api.send_wellness(date, {'readiness': hrv})
