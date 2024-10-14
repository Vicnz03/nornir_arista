from nornir.core.task import Result, Task
from nornir_arista.connections import CONNECTION_NAME
import logging
from .report import add_to_report
from time import sleep, time

logger = logging.getLogger(__name__)

def arista_config(task: Task, config: str, mode: str, session_name: str = '',  confirm: int = 1 , session_timestamp = True) -> Result:
    """
    Load config on remote devices using Arista EAPI
    Arguments:
      commands: commands to execute
      mode: compare, commit, config_only
    Returns:
      Result object with the following attributes set:
        * result (``dict``): result of the commands execution
    """

    task.host['config'] = config
    if 'password' in config and mode == 'commit':
        report_list = [[mode, 'config', 'hidden because include password']]
    else:
        report_list = [[mode, 'config', config]]

    if mode == 'config_only':
        add_to_report(task_host=task.host,report_list = report_list)
        return Result(host=task.host, diff='')

    try:
        dev = task.host.get_connection(CONNECTION_NAME, task.nornir.config) # get connection
    except Exception as e:
        logger.error(str(e))
        report_list.append([mode,'Error',str(e)])
        add_to_report(task_host=task.host,report_list = report_list)
        return Result(host=task.host, diff='') 
    
    no_space_session_name = session_name.replace(' ','_')
    try:
        if session_timestamp:
            dev._session_name = f'{no_space_session_name}_{int(time())}'
        else:
            dev._session_name = no_space_session_name
        dev.configure_session()
        dev.config(config.split('\n'))
        diff = dev.diff()
        if diff == '':
            task.host['compare'] = 'NO DIFF'
        else:
            task.host['compare'] = diff
        report_list.append([mode, 'compare',task.host['compare']])            

        if mode =='compare':
            dev.abort()
        elif mode == 'commit':
            logger.debug(task.host.name + ' :committing')
            if confirm != 0:
                dev.config(f'commit timer 00:{confirm}:00 ')
                sleep(5)
                logger.debug(task.host.name + ' :commit check')
                commit_result = dev.run_commands([f'configure session {dev._session_name} commit'])
            else:
                commit_result = dev.commit()
            if commit_result:
                task.host['commit'] = 'Successful'
                logger.debug(task.host.name + ' :Commit: Successful, saving config')
                dev.enable('write memory')
            else:
                task.host['commit'] = 'Failed'
                logger.debug(task.host.name + ' :Commit: Failed')
            report_list.append([mode, 'commit',task.host['commit']])

        else:
            report_list.append([mode,'Error','Wrong mode'])
            
    except Exception as e:
        logger.error(str(e))
        report_list.append([mode,'Error',str(e)])
    
    add_to_report(task_host=task.host,report_list = report_list)
    return Result(host=task.host, diff=task.host.get('compare','')) 