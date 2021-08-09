import os
import tensorflow as tf
flags = tf.flags
FLAGS = flags.FLAGS

print("La prima opzione nella lista è quella di default, ottenibile con input vuoto")
nohup = input("nohup: [si no] ")
nohup = "nohup" if not nohup else ""
train = input("train: [true false] ")
train = "true" if not train else train
predict = input("predict: [true false]")
predict = "true" if not predict else predict
doeval = input("eval: [false true]")
doeval = "false" if not doeval else doeval
inputfile = input("input file (null for bluebert/bert_model.ckpt): ")
inputfile = "bluebert/bert_model.ckpt" if not inputfile else inputfile
epoche = input("epoche: [3.0 ..]")
epoche = "3.0" if not epoche else epoche

# tbc = input("batch size: [32 ..]")
# tbc = 32 if not tbc else int(tbc)
# flags.DEFINE_integer("train_batch_size", tbc, "Total batch size for training.")
# ebc = input("eval size: [8 ..]")
# ebc = 8 if not ebc else int(ebc)
# flags.DEFINE_integer("eval_batch_size", ebc, "Total batch size for eval.")
# pbc = input("predict size: [8 ..]")
# pbc = 8 if not pbc else int(pbc)
# flags.DEFINE_integer("predict_batch_size", pbc, "Total batch size for predict.")
# lrate = input("learning rate: [5e-5 ..]")
# lrate = 5e-5 if not lrate else float(lrate)
# flags.DEFINE_float("learning_rate", lrate, "The initial learning rate for Adam.")
# wpo = input("warmup portion: [0.1 ..]")
# wpo = .1 if not wpo else float(wpo)
# flags.DEFINE_float("warmup_proportion", wpo, "Proportion of training to perform linear learning rate warmup for. E.g., 0.1 = 10% of training.")

cmd = f'{nohup} python bluebert/bluebert/run_bluebert.py --do_train={train} --do_eval={doeval} --do_predict={predict} --task_name="chemprot2" --vocab_file=bluebert/vocab.txt --bert_config_file=bluebert/bert_config.json --init_checkpoint={inputfile} --num_train_epochs={epoche} --data_dir=. --output_dir=output --do_lower_case=true'
os.system(cmd)