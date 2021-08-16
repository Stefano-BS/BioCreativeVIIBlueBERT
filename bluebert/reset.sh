#!/bin/bash
rm bert_config.json
rm bert_model.ckpt.data-00000-of-00001
rm bert_model.ckpt.index
rm bert_model.ckpt.meta
rm checkpoint
rm vocab.txt

cp vanilla/* .