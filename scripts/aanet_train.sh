#!/usr/bin/env bash

# Train on KITTI 2012 training set
CUDA_VISIBLE_DEVICES=0,1,2,3 python train.py \
--data_dir data/KITTI/kitti_2012/data_stereo_flow \
--dataset_name KITTI2012 \
--mode train_all \
--checkpoint_dir checkpoints/aanet_kitti12 \
--pretrained_aanet pretrained/aanet_kitti15-fb2a0d23.pth \
--batch_size 1 \
--val_batch_size 1 \
--img_height 336 \
--img_width 960 \
--val_img_height 384 \
--val_img_width 1248 \
--feature_type aanet \
--feature_pyramid_network \
--load_pseudo_gt \
--highest_loss_only \
--learning_rate 1e-4 \
--milestones 400,600,800,900 \
--max_epoch 5 \
--save_ckpt_freq 1 \
--no_validate
