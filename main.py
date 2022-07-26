import argparse
import sys
import yaml
import api
import sync

CONFIG_FILENAME = 'config.yaml'


def main():
    config = get_config()
    finalsurge_api = api.FinalSurgeApi(config['finalsurge']['username'], config['finalsurge']['password'])
    finalsurge_api.login()

    intervals_api = api.IntervalsApi(config['intervals']['api_key'], config['intervals']['athlete_id'])

    synchronizer = sync.Synchronizer(finalsurge_api, intervals_api)
    synchronizer.sync_values([sync.SyncValueType.HRV, sync.SyncValueType.RHR, sync.SyncValueType.WEIGHT])

def get_config():
    with open(CONFIG_FILENAME, 'r') as file:
        return yaml.safe_load(file)


if __name__ == '__main__':
    main()
