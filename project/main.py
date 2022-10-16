import tuyapower
import json
import prometheus_client as prom
from prometheus_client import REGISTRY, Metric, start_http_server
import time
import os

REGISTRY.unregister(prom.PROCESS_COLLECTOR)
REGISTRY.unregister(prom.PLATFORM_COLLECTOR)
REGISTRY.unregister(prom.GC_COLLECTOR)

PLUGID = os.environ.get('PLUGID')
PLUGIP = os.environ.get('PLUGIP')
PLUGKEY = os.environ.get('PLUGKEY')
PLUGVERS = os.environ.get('PLUGVERS')

raw = tuyapower.deviceJSON(PLUGID, PLUGIP, PLUGKEY, PLUGVERS)

class EnergyCollector(object):
    def __init__(self):
        self._endpoint = '9300'

    def collect(self):
        raw = tuyapower.deviceJSON(PLUGID, PLUGIP, PLUGKEY, PLUGVERS)
        data = json.loads(raw)

        voltage = Metric('voltage', 'Dispaly current voltage in V', 'gauge')
        voltage.add_sample('voltage', value=data['voltage'], labels={})
        power = Metric('power', 'Dispaly current power in W', 'gauge')
        power.add_sample('power', value=data['power'], labels={})
        current_ma = Metric('current_ma', 'Dispaly current mA in mA', 'gauge')
        current_ma.add_sample('current_ma', value=data['current'], labels={})

        yield voltage
        yield power
        yield current_ma

if __name__ == '__main__':
    start_http_server(9300)
    REGISTRY.register(EnergyCollector())
    while True:
        time.sleep(30)