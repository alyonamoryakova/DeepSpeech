# -*- coding:utf-8 -*-

import DeepSpeech
import tensorflow as tf

import sys
import re

import time

from util import text as text_utils

global inputs, outputs
inputs = None
outputs = None

def init():
    DeepSpeech.initialize_globals()

def init_session():  
    global inputs
    global outputs 

    print('Use Language Model: %s' % str(DeepSpeech.FLAGS.infer_use_lm))

    session = tf.Session(config=DeepSpeech.session_config)

    if inputs == None:
        inputs, outputs = DeepSpeech.create_inference_graph(batch_size=1, use_new_decoder=DeepSpeech.FLAGS.infer_use_lm)
    # Create a saver using variables from the above newly created graph
    saver = tf.train.Saver(tf.global_variables())
    # Restore variables from training checkpoint
    # TODO: This restores the most recent checkpoint, but if we use validation to counterract
    #       over-fitting, we may want to restore an earlier checkpoint.
    checkpoint = tf.train.get_checkpoint_state(DeepSpeech.FLAGS.checkpoint_dir)
    if not checkpoint:
        print('Checkpoint directory ({}) does not contain a valid checkpoint state.'.format(DeepSpeech.FLAGS.checkpoint_dir))
        sys.exit(1)

    checkpoint_path = checkpoint.model_checkpoint_path
    saver.restore(session, checkpoint_path)

    return session, inputs, outputs


def infer(wav_path, session_tuple):
    session, inputs, outputs = session_tuple

    init_session()

    mfcc = DeepSpeech.audiofile_to_input_vector(wav_path, DeepSpeech.n_input, DeepSpeech.n_context)
    output = session.run(outputs['outputs'], feed_dict={
        inputs['input']: [mfcc],
        inputs['input_lengths']: [len(mfcc)],
    })

    text = DeepSpeech.ndarray_to_text(output[0][0], DeepSpeech.alphabet)

    return text

if __name__ == "__main__":
    infer(sys.argv[1], init_session())