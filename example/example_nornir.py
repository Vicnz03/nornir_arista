from nornir import InitNornir
from nornir.core.plugins.connections import ConnectionPluginRegister
from nornir_arista.tasks.arista_get import arista_get
from nornir_arista.tasks.arista_config import arista_config
from nornir_arista.connections import nornir_arista
from nornir_utils.plugins.functions import print_result

ConnectionPluginRegister.register("nornir_arista", nornir_arista)
nr = InitNornir(
    runner={
        "plugin": "threaded",
        "options": {
            "num_workers": 100,
        },
    },
    inventory={
        "plugin": "SimpleInventory",
        "options": {
            "host_file": "inventory/hosts.yaml"
        },
    },
)

nr.inventory.defaults.username = 'xxx'
nr.inventory.defaults.password = 'xxxxx'

result = nr.run(
    task=arista_get, commands=["show uptime","show version"]
)

print_result(result)

config = '''
interface Ethernet29
description "This is a test4"
'''
result = nr.run(task=arista_config, config=config, mode='commit', commit_comments='This_is_a_test3', confirm=0)

print_result(result)