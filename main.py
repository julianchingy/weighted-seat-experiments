import itertools
import random

from numpy.random import randint

import election
import experiment
from statistics import median
import rules
import sys


def runBundestagExperiments():
    """
    Run the experiments and write the results to file: 'experiment_results/bundestag_results.txt'

    """
    bundestag_years = range(1, 21)

    # Structure of summaries: [WLQ, WLQ-X, WLQ-1, WUQ, WUQ-X, WUQ-1, avgDistToWQ, avgDistBelowWLQ,
    # avgDistAboveWUQ, WEFX, WEF1. WLQ-X-r]
    bundestag_summary = [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []]
    adams_summary = [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []]
    dhondt_summary = [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []]
    greedy_summary = [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []]

    for elec_num in bundestag_years:
        election_instance = experiment.getElectionFromFile(elec_num)
        votes = election_instance[0]
        votes.sort(reverse=True)
        weights = election_instance[1]
        seat_assign = election_instance[2]

        bundestag_results = experiment.getResultsForElection(votes, weights, seat_assign)
        adams_results = experiment.getResultsForElection(votes, weights, rules.divisorMethod(votes, weights, 0))
        dhondt_results = experiment.getResultsForElection(votes, weights, rules.divisorMethod(votes, weights, 1))
        greedy_results = experiment.getResultsForElection(votes, weights, rules.greedy(votes, weights))

        # Keep track of 9 results across instances for initial outcome and all outcomes from WSAMs
        for i in range(12):
            bundestag_summary[i].append(bundestag_results[i])
            adams_summary[i].append(adams_results[i])
            dhondt_summary[i].append(dhondt_results[i])
            greedy_summary[i].append(greedy_results[i])

    f = open("experiment_results/bundestag_results.txt", "w")
    f.write("Bundestag results for the following seat assignments: Bundestag, Adams, D\'Hondt, Greedy Method.\n\n")

    summaries = [bundestag_summary, adams_summary, dhondt_summary, greedy_summary]

    for summary in summaries:
        summ_name = ''
        if summary == bundestag_summary:
            summ_name = ' BUNDESTAG '
        elif summary == adams_summary:
            summ_name = 'ADAMS'
        elif summary == dhondt_summary:
            summ_name = 'D\'HONDT'
        elif summary == greedy_summary:
            summ_name = 'GREEDY'

        f.write("---------------------------------------" + summ_name + "-----------------------------------------\n")

        # Write to file the the satisfaction rate results for Obtainable Weighted Lower Quota
        f.write("WLQ provided in " + str(
            round((len([x for x in summary[0] if x == True])) * 100 / len(bundestag_years),
                  2)) + "% of the instances.\n")

        # Write to file the the satisfaction rate results for Weighted Lower Quota up to any seat
        f.write("WLQ_X provided in " + str(
            round((len([x for x in summary[1] if x == True])) * 100 / len(bundestag_years),
                  2)) + "% of the instances.\n")

        # Write to file the the satisfaction rate results for Weighted Lower Quota up to one seat
        f.write("WLQ_1 provided in " + str(
            round((len([x for x in summary[2] if x == True])) * 100 / len(bundestag_years),
                  2)) + "% of the instances.\n")

        # Write to file the satisfaction rate results for Obtainable Weighted Upper Quota
        f.write("WUQ provided in " + str(
            round((len([x for x in summary[3] if x == True])) * 100 / len(bundestag_years),
                  2)) + "% of the instances.\n")

        # Write to file the the satisfaction rate results for Weighted Upper Quota up to any seat
        f.write("WUQ_X provided in " + str(
            round((len([x for x in summary[4] if x == True])) * 100 / len(bundestag_years),
                  2)) + "% of the instances.\n")

        # Write to file the the satisfaction rate results for Weighted Upper Quota up to one seat
        f.write("WUQ_1 provided in " + str(
            round((len([x for x in summary[5] if x == True])) * 100 / len(bundestag_years),
                  2)) + "% of the instances.\n")

        # Write to file the results for Average Distance to Weight Quota: average, maximum and median.
        f.write("AvgDistToWQ: " + str(summary[6]))

        f.write("\nMax AvgDistToWQ: " + str(max(summary[6])) + ", Median AvgDistToWQ: "
                + str(round(median(summary[6]), 1)))

        # Write results to file for Average Distance below Obtainable Weighted Lower Quota: average, maximum and median.
        f.write("\nAvgDistBelowWLQ: " + str(summary[7]))
        f.write("\nMax AvgDistBelowWLQ: " + str(max(summary[7]))
                + ", Median AvgDistBelowWLQ: " + str(round(median(summary[7]), 1)))

        # Write results to file for Average Distance above Obtainable Weighted Upper Quota: average, maximum and median.
        f.write("\nAvgDistAboveWUQ: " + str(summary[8]))
        f.write("\nMax AvgDistAboveWUQ: " + str(max(summary[8]))
                + ", Median AvgDistAboveWUQ: " + str(round(median(summary[8]), 1)) + "\n")

        # Write to file the the satisfaction rate results for Weighted Envy-freeness up to any seat
        f.write("WEFX provided in " + str(
            round((len([x for x in summary[9] if x == True])) * 100 / len(bundestag_years),
                  2)) + "% of the instances.\n")

        # Write to file the the satisfaction rate results for Weighted Envy-freeness up to one seat
        f.write("WEF1 provided in " + str(
            round((len([x for x in summary[10] if x == True])) * 100 / len(bundestag_years),
                  2)) + "% of the instances.\n")

        # Write to file the the satisfaction rate results for Weighted Upper Quota up to any seat
        # from a suffciently represented party
        f.write("WLQ-X-r provided in " + str(
            round((len([x for x in summary[11] if x == True])) * 100 / len(bundestag_years),
                  2)) + "% of the instances.\n")
        f.write(
            "\n-----------------------------------------------------------------------------------------\n\n")

    f.close()

    print("Bundestag experiments completed. For the results, navigate to file \'experiment_results/bundestag_results.txt\'.")

def runSynthExperiments(exp_num: int):
    """
        Run the experiments and write the results to file: 'experiment_results/results_synth.txt' for set 1
                                                           'experiment_results/results_synth_2.txt' for set 2
                                                           'experiment_results/results_synth_3.txt' for set 3
    """

    num_elections = 1000
    num_votes = 10

    # set 1 results written to "experiment_results/results_synth.txt"
    # set 2 results written to "experiment_results/results_synth_2.txt"
    # set 3 results written to "experiment_results/results_synth_3.txt"

    if exp_num == 1:
        num_weights = 25
        vote_range = range(5, 300)
        weight_range = range(10, 50)
        file_name = "results_synth.txt"
    elif exp_num == 2:
        num_weights = 100
        vote_range = range(5, 1000)
        weight_range = range(1, 1000)
        file_name = "results_synth_2.txt"
    else:
        num_weights = 100
        vote_range = range(5, 1000)
        weight_range = range(1, 101)
        file_name = "results_synth_3.txt"

    elections = experiment.generateAllElections(num_elections, num_votes, vote_range, num_weights, weight_range)

    # Structure of summaries: [WLQ, WLQ-X, WLQ-1, WUQ, WUQ-X, WUQ-1, avgDistToWQ, avgDistBelowWLQ,
    # avgDistAboveWUQ, WEFX, WEF1. WLQ-X-r]
    adams_summary = [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []]
    dhondt_summary = [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []]
    greedy_summary = [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []]

    for election_instance in elections:
        votes = election_instance[0]
        votes.sort(reverse=True)
        weights = election_instance[1]

        adams_results = experiment.getResultsForElection(votes, weights, rules.divisorMethod(votes, weights, 0))
        dhondt_results = experiment.getResultsForElection(votes, weights, rules.divisorMethod(votes, weights, 1))
        greedy_results = experiment.getResultsForElection(votes, weights, rules.greedy(votes, weights))

        # Keep track of 9 results across instances for initial outcome and all outcomes from WSAMs
        for i in range(12):
            adams_summary[i].append(adams_results[i])
            dhondt_summary[i].append(dhondt_results[i])
            greedy_summary[i].append(greedy_results[i])

    f = open("experiment_results/"+file_name, "w")
    f.write("Synthetic results for the following seat assignments: Adams, D\'Hondt, Greedy Method.\n\n")

    f.write("Number of elections: " + str(num_elections) + "| Number of parties: " + str(
        num_votes) + "| Number of seats: " + str(num_weights) + "\n\n")

    summaries = [adams_summary, dhondt_summary, greedy_summary]

    for summary in summaries:
        summ_name = ''
        if summary == adams_summary:
            summ_name = 'ADAMS'
        elif summary == dhondt_summary:
            summ_name = 'D\'HONDT'
        elif summary == greedy_summary:
            summ_name = 'GREEDY'

        f.write("---------------------------------------" + summ_name + "-----------------------------------------\n")

        # Write to file the the satisfaction rate results for Obtainable Weighted Lower Quota
        f.write("WLQo provided in " + str(
            round((len([x for x in summary[0] if x == True])) * 100 / len(elections),
                  2)) + "% of the instances.\n")

        # Write to file the the satisfaction rate results for Weighted Lower Quota up to any seat
        f.write("WLQ_X provided in " + str(
            round((len([x for x in summary[1] if x == True])) * 100 / len(elections),
                  2)) + "% of the instances.\n")

        # Write to file the the satisfaction rate results for Weighted Upper Quota up to any seat
        # from a suffciently represented party
        f.write("WLQ-X-r provided in " + str(
            round((len([x for x in summary[11] if x == True])) * 100 / len(elections),
                  2)) + "% of the instances.\n")

        # Write to file the the satisfaction rate results for Weighted Lower Quota up to one seat
        f.write("WLQ_1 provided in " + str(
            round((len([x for x in summary[2] if x == True])) * 100 / len(elections),
                  2)) + "% of the instances.\n")

        # Write to file the satisfaction rate results for Obtainable Weighted Upper Quota
        f.write("WUQo provided in " + str(
            round((len([x for x in summary[3] if x == True])) * 100 / len(elections),
                  2)) + "% of the instances.\n")

        # Write to file the the satisfaction rate results for Weighted Upper Quota up to any seat
        f.write("WUQ_X provided in " + str(
            round((len([x for x in summary[4] if x == True])) * 100 / len(elections),
                  2)) + "% of the instances.\n")

        # Write to file the the satisfaction rate results for Weighted Upper Quota up to one seat
        f.write("WUQ_1 provided in " + str(
            round((len([x for x in summary[5] if x == True])) * 100 / len(elections),
                  2)) + "% of the instances.\n")

        # Write to file the the satisfaction rate results for Weighted Envy-freeness up to any seat
        f.write("WEFX provided in " + str(
            round((len([x for x in summary[9] if x == True])) * 100 / len(elections),
                  2)) + "% of the instances.\n")

        # Write to file the the satisfaction rate results for Weighted Envy-freeness up to one seat
        f.write("WEF1 provided in " + str(
            round((len([x for x in summary[10] if x == True])) * 100 / len(elections),
                  2)) + "% of the instances.\n")

        # Write to file the results for Average Distance to Weight Quota: average, maximum and median.
        f.write("AvgDistToWQ: " + str(summary[6]))

        f.write("\nMax AvgDistToWQ: " + str(max(summary[6])) + ", Median AvgDistToWQ: "
                + str(round(median(summary[6]), 1)))

        # Write results to file for Average Distance below Obtainable Weighted Lower Quota: average, maximum and median.
        f.write("\nAvgDistBelowWLQ: " + str(summary[7]))
        f.write("\nMax AvgDistBelowWLQ: " + str(max(summary[7]))
                + ", Median AvgDistBelowWLQ: " + str(round(median(summary[7]), 1)))

        # Write results to file for Average Distance above Obtainable Weighted Upper Quota: average, maximum and median.
        f.write("\nAvgDistAboveWUQ: " + str(summary[8]))
        f.write("\nMax AvgDistAboveWUQ: " + str(max(summary[8]))
                + ", Median AvgDistAboveWUQ: " + str(round(median(summary[8]), 1)) + "\n")
        f.write(
            "\n-----------------------------------------------------------------------------------------\n\n")

    f.close()

    print(
        "Synthetic experiments completed. For the results, navigate to file \'experiment_results/"+file_name+"\'.")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    if len(sys.argv) > 1 and int(sys.argv[1]) == 1:
            runSynthExperiments(1)
            runSynthExperiments(2)
            runSynthExperiments(3)
    elif len(sys.argv) > 1 and int(sys.argv[1]) == 0:
            runBundestagExperiments()
    else:
        print("Argument error: enter 0 as an argument to run Bundestga experiments or enter 1 as an argument to run synthetic experiments.")



# See PyCharm help at https://www.jetbrains.com/help/pycharm/
