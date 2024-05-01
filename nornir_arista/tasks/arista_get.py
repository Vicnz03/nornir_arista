from typing import List
from nornir.core.task import Result, Task
from nornir_arista.connections import CONNECTION_NAME
import logging
from .report import add_to_report
import json

logger = logging.getLogger(__name__)

def arista_get(task: Task, commands: List[str], encoding='json') -> Result:
    """
    Run commands on remote devices using Arista EAPI
    Arguments:
      commands: commands to execute
    Returns:
      Result object with the following attributes set:
        * result (``dict``): result of the commands execution
    """
    report_list = []
    result = {}
    try:
        dev = task.host.get_connection(CONNECTION_NAME, task.nornir.config)
        dev_result = dev.enable(commands, encoding=encoding)
    except Exception as e:
        logger.error(str(e))
        report_list.append(['get', 'Failed', str(e)])
        add_to_report(task_host=task.host, report_list=report_list)
        return Result(host=task.host, result={'Failed', str(e)})
    
    
    for res in dev_result:
        if encoding == 'json':
          str_result = json.dumps(res['result'], indent=2)
          result[res['command']] = res['result']
        else:
          str_result = res['result']['output']
          result[res['command']] = res['result']['output']
          
        report_list.append(['get', res['command'], str_result])
    add_to_report(task_host = task.host,report_list = report_list)
    
    return Result(host=task.host, result=result)