#!/bin/bash

# 'LGAI-EXAONE/EXAONE-3.5-2.4B-Instruct', 'meta-llama/Llama-3.2-3B-Instruct', 'Bllossom/llama-3.2-Korean-Bllossom-3B'
MODEL='LGAI-EXAONE/EXAONE-3.5-2.4B-Instruct'
# 'culture', 'education'
DOMAIN='culture'

python main.py \
  --model "$MODEL" \
  --domain "$DOMAIN"