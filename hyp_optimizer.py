from clearml import Task
from clearml.automation import (
    DiscreteParameterRange,
    HyperParameterOptimizer,
    UniformParameterRange,
)

import hyp_optimizer_config as hyp_optimizer_config


# define call back function
def job_complete_callback(
    job_id,                 # type: str
    objective_value,        # type: float
    objective_iteration,    # type: int
    job_parameters,         # type: dict
    top_performance_job_id  # type: str
):
    print('Job completed!', job_id, objective_value, objective_iteration, job_parameters)
    if job_id == top_performance_job_id:
        print('WOOT WOOT we broke the record! Objective reached {}'.format(objective_value))


# connecting ClearML with the current process,
# from here on everything is logged automatically
task = Task.init(project_name=hyp_optimizer_config.project_name,
                 task_name=hyp_optimizer_config.task_name,
                 task_type=Task.TaskTypes.optimizer,
                 reuse_last_task_id=False)

# experiment template to optimize in the hyper-parameter optimization
args = {
    'template_task_id': hyp_optimizer_config.template_task_id,
    'run_as_service': hyp_optimizer_config.run_as_service,
}
args = task.connect(args)

# Get the template task experiment that we want to optimize
if not args['template_task_id']:
    args['template_task_id'] = Task.get_task(
        project_name=hyp_optimizer_config.project_name, task_name=hyp_optimizer_config.task_name).id

# Set default queue name for the Training tasks themselves.
# later can be overridden in the UI
execution_queue = hyp_optimizer_config.execution_queue

hyp_optimizer = HyperParameterOptimizer(
    base_task_id=args['template_task_id'],
    # hyperparameters to optimize
    hyper_parameters=[
        DiscreteParameterRange('Args/learning_rate', values=[1e-3, 3e-3, 6e-3]),
        DiscreteParameterRange('Args/num_downsample', values=[1, 2]),
        DiscreteParameterRange('Args/no_feature_mdconv', values=[True, False]),
        # UniformParameterRange('Args/lr_decay_gamma', min_value=0.45, max_value=0.55)
    ],
    # this is the objective metric we want to maximize/minimize
    objective_metric_title='train',
    objective_metric_series='epe',
    # now we decide if we want to maximize it or minimize it (this is a loss so we minimize)
    objective_metric_sign='min',
    # if you have a powerful machine you can set this to more than 1
    max_number_of_concurrent_tasks=1,
    # optimizer strategy
    optimizer_class=hyp_optimizer_config.serach_strategy,
    # select an execution queue to schedule the experiments for execution when using clearml agent
    execution_queue=execution_queue,
    # check the experiments every 30 min
    pool_period_min=30,
    # set the minimum number of iterations for an experiment, before early stopping.
    min_iteration_per_job=100,
)

# if we are running as a service, just enqueue ourselves into the services queue and let it run the optimization
if args['run_as_service']:
    # if this code is executed by `clearml-agent` the function call does nothing.
    # if executed locally, the local process will be terminated, and a remote copy will be executed instead
    task.execute_remotely(queue_name='services', exit_process=True)
# report update every 5 min
hyp_optimizer.set_report_period(5)
# start the optimization process, callback function to be called every time an experiment is completed
# this function returns immediately
# an_optimizer.start(job_complete_callback=job_complete_callback)
# you can also use the line below instead to run all the optimizer tasks locally, without using queues or agent
hyp_optimizer.start_locally(job_complete_callback=job_complete_callback)
# wait until process is done (notice we are controlling the optimization process in the background)
hyp_optimizer.wait()
# optimization is completed, print the top performing experiments id
top_exp = hyp_optimizer.get_top_experiments(top_k=3)
print('top performing experiments id: /n', [t.id for t in top_exp])
# make sure background optimization stopped
hyp_optimizer.stop()

print('We are done, good bye')