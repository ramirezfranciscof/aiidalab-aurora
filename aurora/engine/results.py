import datetime
import aiida
from aiida import load_profile
from aiida.orm import Group, QueryBuilder, load_node
from aiida.plugins import CalculationFactory, DataFactory
import aiida_aurora.utils

load_profile()
BatteryCyclerExperiment = CalculationFactory('aurora.cycler')
BatterySampleData = DataFactory('aurora.batterysample')

def query_jobs(last_days=0, group='CalcJobs'):
    qb = QueryBuilder()
    qb.append(Group, filters={'label': group}, tag='g')
    qb.append(BatteryCyclerExperiment, with_group='g', tag='jobs',
             project=['id', 'label', 'ctime', 'attributes.process_label', 'attributes.state', 'attributes.status', 'extras.monitored'])
    qb.append(BatterySampleData, with_outgoing='jobs', tag='inps', project=['attributes.metadata.name'])
    if last_days:
        qb.add_filter('jobs', {'ctime': {'>=': datetime.datetime.now() - datetime.timedelta(days=last_days)}})
    qb.order_by({'jobs': {'ctime': 'desc'}})
    
    outputs = []
    for data in qb.dict():
        output_i = data['jobs']
        output_i['attributes.metadata.name'] = data['inps']['attributes.metadata.name']
        outputs.append(output_i)

    return outputs

def cycling_analysis(job_id):
    job_node = load_node(pk=job_id)
    data = aiida_aurora.utils.cycling_analysis.cycling_analysis(job_node)
    return data