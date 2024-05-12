import pandas as pd
from sklearn.model_selection import train_test_split
import logging
import re
import string
import multiprocessing

from simpletransformers.seq2seq import Seq2SeqModel, Seq2SeqArgs

def count_matches(labels, preds):
    print(labels)
    print(preds)
    return sum(
        [
            1 if label == pred else 0
            for label, pred in zip(labels, preds)
        ]
    )

if __name__ == '__main__':
    df = pd.read_csv("Train.csv")[0:35000]  # Change Train Data directory
    test = pd.read_csv("Test.csv")  # Change Test Data Directory

    Fon = df[df.Target_Language == "Fon"]
    Fon_test = test[test.Target_Language == "Fon"]

    logging.basicConfig(level=logging.INFO)
    transformers_logger = logging.getLogger("transformers")
    transformers_logger.setLevel(logging.WARNING)

    train_data = Fon[["French", "Target"]]
    train_data = train_data.rename(columns={"French": "input_text", "Target": "target_text"})
    train_df, eval_df = train_test_split(train_data, test_size=0.2, random_state=42)

    model_args = Seq2SeqArgs()
    model_args.num_train_epochs = 30
    model_args.no_save = True
    model_args.evaluate_generated_text = False
    model_args.evaluate_during_training = False
    model_args.evaluate_during_training_verbose = True
    model_args.rag_embed_batch_size = 32
    model_args.max_length = 120
    model_args.src_lang = "fr"
    model_args.tgt_lang = "fon"
    model_args.overwrite_output_dir = True

    # Initialize model
    model_fon = Seq2SeqModel(
        encoder_decoder_type="marian",
        encoder_decoder_name="Helsinki-NLP/opus-mt-en-mul",
        args=model_args,
        use_cuda=False,
    )

    # Train the model
    model_fon.train_model(
        train_df, eval_data=eval_df, matches=count_matches
    )

    # Add freeze_support for Windows compatibility
    multiprocessing.freeze_support()
