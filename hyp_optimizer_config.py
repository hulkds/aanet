from clearml.automation import RandomSearch
from clearml.automation.optuna import OptimizerOptuna

serach_strategy = RandomSearch # choose between RandomSearch or OptimizerOptuna
project_name = 'aanet_depth_estimation'
task_name = 'Optuna-hyp-optimization' 
template_task_id = '07d47e41c23f4a5da2bd14ab68a7694e'
run_as_service = False
execution_queue = 'default'