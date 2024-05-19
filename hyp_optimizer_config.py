from clearml.automation import RandomSearch
from clearml.automation.optuna import OptimizerOptuna

serach_strategy = OptimizerOptuna # choose between RandomSearch or OptimizerOptuna
project_name = 'aanet_depth_estimation'
task_name = 'Optuna-hyp-optimization' 
template_task_id = '9fe9d687ce3f4f15b1c3f4a13a01d024'
run_as_service = False
execution_queue = 'default'