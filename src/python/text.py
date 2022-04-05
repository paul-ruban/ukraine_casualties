from tqdm import tqdm
from typing import List, Set
import more_itertools as mit

import torch
from transformers import AutoTokenizer, AutoModelForTokenClassification

from .utils import (
    get_device
)


PERSON_LABELS = {"B-PER", "I-PER"}


def extract_named_entities(
    samples: List[str],
    model: AutoModelForTokenClassification, 
    tokenizer: AutoTokenizer,
    batch_size: int = 128,
    progress_bar: bool = True
) -> List[str]:
    """ Extracts named entities from a list of text.
    
    Args:
        samples: A list of text samples to extract named entities from.
        model: The model to use for extracting named entities.
        tokenizer: The tokenizer to use for extracting named entities.
        batch_size: The batch size to use for extracting named entities.
        progress_bar: Whether to show a progress bar.
        
    Returns:
        A list of named entities extracted from the text.
    """
    
    device = get_device()
    model = model.to(device)

    # TODO think about how to handle this
    batches = [samples[i:i+batch_size] for i in range(0, len(samples), batch_size)]

    all_labels = []

    for batch in tqdm(batches, disable=not progress_bar):
        inputs = tokenizer(
            batch,
            padding=True,
            return_special_tokens_mask=True,
            return_tensors="pt"
        ).to(device)
        with torch.no_grad():
            outputs = model(
                input_ids=inputs["input_ids"], 
                attention_mask=inputs["attention_mask"]
            )
            predictions = torch.argmax(outputs.logits, dim=-1)

        predictions = remove_predictions_for_special_tokens(
            predictions=predictions,
            special_tokens_mask=inputs["special_tokens_mask"]
        )

        labels = convert_predictions_to_labels(
            predictions=predictions,
            id2label=model.config.id2label
        )
        
        all_labels.extend(labels)

    return all_labels


def remove_predictions_for_special_tokens(
    predictions: torch.tensor,
    special_tokens_mask: torch.tensor
) -> List[List[str]]:
    """ Removes predictions for special tokens.
    
    Args:
        predictions: The predictions.
        special_tokens_mask: The special tokens mask for the predictions.

    Returns:
        A list of lists of predictions without predictions for special tokens.
    """
    predictions = predictions.cpu().numpy()
    batch_size, seq_len = predictions.shape

    return [[predictions[i][j] for j in range(seq_len) if special_tokens_mask[i][j] == 0]
            for i in range(batch_size)]


def convert_predictions_to_labels(
    predictions: List[List[str]],
    id2label: dict,
) -> List[List[str]]:
    """ Converts predictions to labels.
    
    Args:
        predictions: The predictions.
        id2label: The mapping from ids to labels.

    Returns:
        A list of lists of labels.
    """

    return [[id2label.get(p) for p in sample] for sample in predictions]


def extract_names(
    tokens: List[str], 
    labels: List[str],
    tokenizer: AutoTokenizer,
    person_labels: Set[str] = PERSON_LABELS
) -> List[str]:
    """ Extracts names from a list of tokens and labels.
    
    Args:
        tokens: A list of tokens.
        labels: A list of labels.
        tokenizer: The tokenizer to use for extracting names.

    Returns:
        A list of names.
    """
    assert (len(tokens) == len(labels)), "The number of tokens and labels must be the same."
    names = []

    if person_labels.intersection(set(labels)):
        person_label_idx = [i for i, label in enumerate(labels) if label in person_labels]

        people = [list(group) for group in mit.consecutive_groups(person_label_idx)]

        for i, person in enumerate(people):
            # TODO think about how to handle this
            # since last name is not tagged as a person, add at most 10 tokens from the left
            start_idx = max(person[0] - 10, 0 if i == 0 else people[i-1][-1])
            name = tokens[start_idx : person[-1] + 1]
            names.append(tokenizer.convert_tokens_to_string(name))        

    return names


def extract_names_from_batch(
    tokens_list: List[List[str]], 
    labels_list: List[List[str]],
    tokenizer: AutoTokenizer
) -> List[List[str]]:
    """ Extracts names from a list of lists of tokens and labels.

    Args:
        tokens_list: A list of lists of tokens.
        labels_list: A list of lists of labels.
        tokenizer: The tokenizer to use for extracting names.

    Returns:
        A list of lists of names.
    """
    assert (len(tokens_list) == len(labels_list)), "The number of tokens and labels must be the same."
    names_list = []

    for tokens, labels in zip(tokens_list, labels_list):
        names = extract_names(tokens, labels, tokenizer)
        if names:
            names_list.extend(names)

    return names_list