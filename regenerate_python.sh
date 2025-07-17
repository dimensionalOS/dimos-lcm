#!/usr/bin/env bash
rm -r python_lcm_msgs/lcm_msgs/
./lcm_batch_processor.sh -v -p lcm_files -o python_lcm_msgs/lcm_msgs/
python python_lcm_msgs/fix_imports.py
