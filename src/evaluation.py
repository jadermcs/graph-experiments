#!/usr/bin/env python
import sys
import os
import os.path
import numpy as np
from scipy.stats import spearmanr
from sklearn.metrics import accuracy_score
import codecs


# as per the metadata file, input and output directories are the arguments
[_, input_dir] = sys.argv

tasks = ['task1', 'task2']
languages = ['german', 'english', 'latin', 'swedish']
columns_task1 = ['ACC_ALL', 'ACC_GERMAN', 'ACC_ENGLISH', 'ACC_LATIN', 'ACC_SWEDISH']
columns_task2 = ['SPR_ALL', 'SPR_GERMAN', 'SPR_ENGLISH', 'SPR_LATIN', 'SPR_SWEDISH']
language2column_task1 = {('task1','all'):'ACC_ALL',('task1','german'):'ACC_GERMAN',('task1','english'):'ACC_ENGLISH',('task1','latin'):'ACC_LATIN',('task1','swedish'):'ACC_SWEDISH'}
language2column_task2 = {('task2','all'):'SPR_ALL',('task2','german'):'SPR_GERMAN',('task2','english'):'SPR_ENGLISH',('task2','latin'):'SPR_LATIN',('task2','swedish'):'SPR_SWEDISH'}

methods = os.path.join(input_dir, 'answer')
for method in os.listdir(methods):
    # Task 1
    accuracies = {}
    for language in languages:
        # Load submission file
        submission_file_name = language + '.txt'
        submission_dir = os.path.join(input_dir, 'answer/{}/task1'.format(method))
        submission_path = os.path.join(submission_dir, submission_file_name)
        if not os.path.exists(submission_path):
            message = "Error: Expected submission file '{0}', found files {1}"
            sys.exit(message.format(submission_file_name, os.listdir(submission_dir)))
        with codecs.open(submission_path, 'r', 'utf-8') as submission_file:
            # for l in submission_file:
            submission = {line.strip().split('\t')[0]:int(line.strip().split('\t')[1]) for line in submission_file}

        # Load truth file
        truth_file_name = 'truth/binary.txt'
        truth_dir = os.path.join(input_dir, language)
        truth_path = os.path.join(truth_dir, truth_file_name)
        with codecs.open(truth_path, 'r', 'utf-8') as truth_file:
            truth = {line.strip().split('\t')[0]:int(line.strip().split('\t')[1]) for line in truth_file}

        # Check submission format
        if set(submission.keys())!=set(truth.keys()) or len(submission.keys())!=len(truth.keys()):
            message = "Error in '{0}': Submitted targets do not match gold targets."
            sys.exit(message.format(truth_path))

        if any((not (i==0 or i==1) for i in truth.values())):
            message = "Error in '{0}': Submitted values contain values that are not equal to 0, 1."
            sys.exit(message.format(truth_path))

        # Get submitted values and true values
        submission_values = [submission[target] for target in truth.keys()]
        truth_values = [truth[target] for target in truth.keys()]

        # Make results
        acc = accuracy_score(truth_values, submission_values)
        accuracies[language] = acc


    # Task 2
    spearmans = {}
    for language in languages:
        # Load submission file
        submission_file_name = language + '.txt'
        submission_dir = os.path.join(input_dir, 'answer/{}/task2'.format(method))
        submission_path = os.path.join(submission_dir, submission_file_name)
        if not os.path.exists(submission_path):
            message = "Error: Expected submission file '{0}', found files {1}"
            sys.exit(message.format(submission_file_name, os.listdir(submission_dir)))
        with codecs.open(submission_path, 'r', 'utf-8') as submission_file:
            submission = {line.strip().split('\t')[0]:float(line.strip().split('\t')[1]) for line in submission_file}

        # Load truth file
        truth_file_name = 'truth/graded.txt'
        truth_dir = os.path.join(input_dir, language)
        truth_path = os.path.join(truth_dir, truth_file_name)
        with codecs.open(truth_path, 'r', 'utf-8') as truth_file:
            truth = {line.strip().split('\t')[0]:float(line.strip().split('\t')[1]) for line in truth_file}

        # Check submission format
        if set(submission.keys())!=set(truth.keys()) or len(submission.keys())!=len(truth.keys()):
            message = "Error in '{0}': Submitted targets do not match gold targets."
            sys.exit(message.format(truth_path))

        # Get submitted values and true values
        submission_values = [submission[target] for target in truth.keys()]
        truth_values = [truth[target] for target in truth.keys()]

        # Make results
        rho, p = spearmanr(submission_values, truth_values, nan_policy='raise')
        spearmans[language] = rho


    # Make average results
    average_accuracy = np.mean([accuracies[language] for language in accuracies])
    accuracies['all'] = average_accuracy
    average_spearman = np.mean([spearmans[language] for language in spearmans])
    spearmans['all'] = average_spearman

    # Write output scores
    with open(os.path.join(input_dir, 'scores.txt'), 'w') as output_file:
        output_file.write("{}\n".format(method))
        # Task 1
        for language in accuracies:
            column = language2column_task1[('task1',language)]
            score = accuracies[language]
            output_file.write("{0}:{1}\n".format(column,score))
        # Task 2
        for language in spearmans:
            column = language2column_task2[('task2',language)]
            score = spearmans[language]
            output_file.write("{0}:{1}\n".format(column,score))

