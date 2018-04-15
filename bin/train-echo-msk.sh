#!/bin/sh
set -xe
if [ ! -f DeepSpeech.py ]; then
    echo "Please make sure you run this from DeepSpeech's top level directory."
    exit 1
fi;



python -u DeepSpeech.py \
  --train_files "/tmp/echo-msk-dataset/echo-msk-train.csv" \
  --dev_files "/tmp/echo-msk-dataset/echo-msk-dev.csv" \
  --test_files "/tmp/echo-msk-dataset/echo-msk-test.csv" \
  --train_batch_size 32 \
  --dev_batch_size 16 \
  --test_batch_size 16 \
  --learning_rate 0.0001 \
  --epoch 35 \
  --display_step 0 \
  --validation_step 1 \
  --dropout_rate 0.20 \
  --default_stddev 0.046875 \
  --n_hidden 1024 \
  --checkpoint_dir /assets/network/echo_msk/checkpoint_dir_echo_msk_1024/ \
  --export_dir /assets/network/echo_msk/export_dir_echo_msk_1024/ \
  --summary_dir /assets/network/echo_msk/summary_echo_msk \
  --summary_sec 60 \
  --log_level 1 \
  --limit_train 100000  \
  --limit_dev 10000  \
  --limit_test 10000  \
  --report_count 1000 \
  --xla=False \
  --use_warpctc=True \
  --log_telegram=True \
  "$@"