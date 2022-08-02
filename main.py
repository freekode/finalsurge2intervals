import argparse
import sys
import yaml
import api
import sync
from intervalsicu import Intervals


CONFIG_FILENAME = 'config.yaml'


def main():
    config = get_config()
    finalsurge_api = api.FinalSurgeApi(config['finalsurge']['username'], config['finalsurge']['password'])
    finalsurge_api.login()

    intervals_api = Intervals(config['intervals']['athlete_id'], config['intervals']['api_key'])

    synchronizer = sync.Synchronizer(finalsurge_api, intervals_api, config['sync_past_days'])
    synchronizer.sync_values([sync.SyncValueType.HRV])

def get_config():
    with open(CONFIG_FILENAME, 'r') as file:
        return yaml.safe_load(file)


if __name__ == '__main__':
    main()
