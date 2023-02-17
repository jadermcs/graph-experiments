# git pull

# Make folders
mkdir -p data/matrices/
mkdir -p data/results/

# Iterate over languages
declare -a languages=(english german latin swedish)
for language in "${languages[@]}"
do

    # Make folders
    mkdir -p data/matrices/$language/
    mkdir -p data/results/$language/


    ### Baseline 1: Normalized Frequency Difference (FD) ###

    # # Get normalized (-n) frequencies for both corpora
    # python src/freq.py -n data/$language/corpus1/lemma data/$language/targets.txt data/results/$language/freq_corpus1.csv
    # python src/freq.py -n data/$language/corpus2/lemma data/$language/targets.txt data/results/$language/freq_corpus2.csv

    # # Subtract frequencies and store absolute (-a) difference
    # python src/diff.py -a data/$language/targets.txt data/results/$language/freq_corpus1.csv data/results/$language/freq_corpus2.csv data/results/$language/fd.csv

    # # Classify results into two classes according to threshold
    # python src/class.py data/results/$language/fd.csv data/results/$language/fd_classes.csv 0.0003


    # ### Baseline 2: Count Vectors with Column Intersection and Cosine Distance (CNT+CI+CD) ###

    # # Get co-occurrence matrices for both corpora
    # python src/cnt.py data/$language/corpus1/lemma data/matrices/$language/cnt_matrix1 1
    # python src/cnt.py data/$language/corpus2/lemma data/matrices/$language/cnt_matrix2 1

    # # Align matrices with Column Intersection
    # python src/ci.py data/matrices/$language/cnt_matrix1 data/matrices/$language/cnt_matrix2 data/matrices/$language/cnt_matrix1_aligned data/matrices/$language/cnt_matrix2_aligned

    # # Load matrices and calculate Cosine Distance
    # python src/cd.py data/$language/targets.txt data/matrices/$language/cnt_matrix1_aligned data/matrices/$language/cnt_matrix2_aligned data/results/$language/cnt_ci_cd.csv

    # # Classify results into two classes according to threshold
    # python src/class.py data/results/$language/cnt_ci_cd.csv data/results/$language/cnt_ci_cd_classes.csv 0.4

    ### Model shingles ###

    # Get normalized (-n) frequencies for both corpora
    python src/shing.py data/$language/corpus1/lemma data/$language/targets.txt data/results/$language/shing1.csv
    python src/shing.py data/$language/corpus2/lemma data/$language/targets.txt data/results/$language/shing2.csv

    # Subtract frequencies and store absolute (-a) difference
    python src/comp.py data/results/$language/shing1.csv data/results/$language/shing2.csv data/results/$language/comp.csv

    # Classify results into two classes according to threshold
    python src/class.py data/results/$language/comp.csv data/results/$language/sh_classes.csv 0.5


    ### Make answer files for submission ###

    # # Baseline 1
    # mkdir -p data/answer/freq/task2/ && cp data/results/$language/fd.csv data/answer/freq/task2/$language.txt
    # mkdir -p data/answer/freq/task1/ && cp data/results/$language/fd_classes.csv data/answer/freq/task1/$language.txt

    # # Baseline 2
    # mkdir -p data/answer/cicd/task2/ && cp data/results/$language/cnt_ci_cd.csv data/answer/cicd/task2/$language.txt
    # mkdir -p data/answer/cicd/task1/ && cp data/results/$language/cnt_ci_cd_classes.csv data/answer/cicd/task1/$language.txt

    # Model
    mkdir -p data/answer/shing/task2/ && cp data/results/$language/comp.csv data/answer/shing/task2/$language.txt
    mkdir -p data/answer/shing/task1/ && cp data/results/$language/sh_classes.csv data/answer/shing/task1/$language.txt

    echo Evaluation...
    python src/evaluation.py data
    echo Done.

done
