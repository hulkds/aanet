# AANet with ClearML

Test AANet training with ClearML.
More information on AANet can be found [here](README_official.md)

For this test you can use pretrained model on KITTI2015 dataset to finetune on KITTI2012 dataset. The folder structure is simplified as follows:
```
data
├── KITTI
│   ├── kitti_2012
│   │   └── data_stereo_flow
pretrained
├── aanet_kitti15-fb2a0d23.pth
```
Pretrained model can be downloaded [here](MODEL_ZOO.md). 

KITTI2012 dataset can be found here [KITTI 2012](http://www.cvlibs.net/datasets/kitti/eval_stereo_flow.php?benchmark=stereo). You can also download the pseudo ground truth supervision introduced in AANet paper here [KITTI 2012](https://drive.google.com/open?id=1ZJhraqgY1sL4UfHBrVojttCbvNAXfdj0) and put it in `kitti_2012/data_stereo_flow/training` directory. 

## Installation

1. Create and activate conda environment

    `conda env create -f environment.yml`

    `conda activate aanetenv`
2. Build deformable convolution:

    `cd nets/deform_conv`

    `bash build.sh`

## Training with clearml

1. Following this document to install clearml [local python](https://clear.ml/docs/latest/docs/getting_started/ds/ds_first_steps#local-python)

2. Run training script

    `bash scripts/aanet_train.sh`
    
    Training experiment will be logged on Clearml server with [Clearml Web UI](https://clear.ml/docs/latest/docs/webapp/webapp_overview/)

## Hyperparameters Opimization with Clearml

After running the first train baseline, we can now perform hyperparameters optimization based on the first training.

The configuration file for hyperparameters optimization is found here [hyp_optimizer_config](hyp_optimizer_config.py). The important thing is `template_task_id` (can be found on Clearml Web UI), Clearml will perform the optimization based on this.

If using Optuna optimizer, we need to install optuna:

`pip install optuna`

We can now perform hyperparameters optimization LOCALLY:

`python3 hyp_optimizer.py`

We can also perform hyperparameters optimization remotely (ex: on clearml server) using [Clearml Agent](https://clear.ml/docs/latest/docs/clearml_agent) by uncomment this [line](hyp_optimizer.py#L81) and:

1. Following this [document](https://clear.ml/docs/latest/docs/clearml_agent/) to install and configure clearml-agent.

2. Run hyperparameters optimization, this will enqueue all the tasks but not run the tasks:

    `python3 hyp_optimizer.py`

3. Run clearml-agent to execute enqueued tasks:

    `clearml-agent daemon --queue default`

## Encountered problem

- When creating conda environment with official environment.yml:
    ``` 
    Solving environment: failed
    ResolvePackageNotFound: 
    - torchvision==0.4.0=py37_cu100
    - pytorch==1.2.0=py3.7_cuda10.0.130_cudnn7.6.2_0
    - openssl==1.1.1=h7b6447c_0 
    ```
    New environment.yml have been simplified in this [commit](https://github.com/hulkds/aanet/commit/9668946700ca27d4703cb5536f8336d797de43d1).

- When building deformable convolution:
    ``` 
    error: command '/usr/local/cuda/bin/nvcc' failed with exit status 1
    ```
    This is because cudatoolkit version installed in conda environment is not compatible with gcc and g++ version.
    
    To fix this we can install gcc-9 and g++-9 and enable auto mode:
    
    `sudo apt install gcc-9 g++-9`

    `sudo update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-9 60`

    `sudo update-alternatives --install /usr/bin/g++ g++ /usr/bin/g++-9 60`

    `sudo update-alternatives --auto gcc`

    `sudo update-alternatives --auto g++`

    /!\ Maybe you also need to remove gcc-11 and g++-11

## Useful link
- https://github.com/pytorch/pytorch/blob/main/RELEASE.md
- https://celikmustafa89.medium.com/python-torch-and-torchvision-compatibility-list-305ad80b243f
- https://stackoverflow.com/questions/6622454/cuda-incompatible-with-my-gcc-version
- https://discuss.pytorch.org/t/build-error-in-pytorch-vision/135379/5
- https://github.com/pytorch/pytorch/releases
