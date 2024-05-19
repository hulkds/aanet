from clearml.automation import RandomSearch
from clearml.automation.optuna import OptimizerOptuna

serach_strategy = RandomSearch # choose between RandomSearch or OptimizerOptuna
project_name = 'aanet_depth_estimation'
task_name = 'Optuna-hyp-optimization' 
template_task_id = '1d8846763f1a42e8bd7416c90a93f8d3'
run_as_service = False
execution_queue = 'default'