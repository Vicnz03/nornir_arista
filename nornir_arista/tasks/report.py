def add_to_report(task_host,report_list):
    report_prefix = [task_host.name, task_host.hostname]
    if 'report_details' not in task_host.data:
        task_host['report_details'] = []
    for row in report_list:
        task_host['report_details'].append(report_prefix + row)