import codecs

# import numpy as np
# import pandas as pd


def get_blocks(task_contents):
    indices = get_block_indices(task_contents)

    blocks = []
    for start_idx, end_idx in indices:
        parsed = {}
        for line in task_contents[start_idx:end_idx]:
            try:
                key, value = line.strip().split(": ")
            except ValueError:
                continue
            # Keys we care about should never be duplicated so this is safe
            parsed[key] = value
        blocks.append(parsed)
    return blocks


def get_block_indices(task_contents):
    trials = [i for i, s in enumerate(task) if 'Procedure: TrialsPROC' in s]

    indices = []
    for i, trial_start in enumerate(trials):
        if i == (len(trials) - 1):
            trial_end = len(task_contents)
        else:
            trial_end = trials[i + 1]
        indices.append((trial_start, trial_end))

    return indices


def get_start_time(task_contents):
    onset_times = [s for s in task_contents if 'SyncSlide.OnsetTime:' in s]
    start = onset_times[0].strip().split(": ")[1]
    return float(start)


def parse_eprime_faces(eprime_file):
    """Parse an eprime faces task file into a more consistent format.

    Args:
        eprime_file (str): The path to a single eprime txt file to parse.

    Returns:
        dict: A dictionary containing 'onset', 'duration', 'trial_type',
            'response_time', 'accuracy', 'correct_response',
            'participant_response'. The index n of each list corresponds to
            the value for trial n.
    """
    eprime = codecs.open(eprime_file, "r", encoding="utf-16", errors="strict")
    task_contents = eprime.readlines()

    trial_blocks = get_blocks(task_contents)
    start_time = get_start_time(task_contents)

    data_list = {
        'onset': [],
        'duration': [],
        'trial_type': [],
        'response_time': [],
        'accuracy': [],
        'correct_response': [],
        'participant_response': []
    }
    for block in trial_blocks:
        data_list['onset'].append(
            (float(block['StimSlide.OnsetTime']) - start_time) / 1000
        )

        data_list['trial_type'].append(
            'Shapes' if 'Shape' in str(block) else 'Faces'
        )

        data_list['response_time'].append(float(block['StimSlide.RT']) / 1000)

        data_list['duration'].append(
            float(block['StimSlide.OnsetToOnsetTime']) / 1000
        )

        data_list['accuracy'].append(block['StimSlide.ACC'])
        data_list['correct_response'].append(block['CorrectResponse'])
        data_list['participant_response'].append(
            block.get('StimSlide.RESP') or 'n/a'
        )

    return data_list