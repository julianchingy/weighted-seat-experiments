"""
Functions related to the experiments on election instances.
"""
import random

from numpy.random import randint

import election
from numbers import Number


def getResultsForElection(votes: [int], weights: [Number], seat_assign: [int]) \
        -> [bool, bool, bool, bool, bool, bool, Number, Number, Number]:
    """
    Returns a list containing the experimental results of the seat assignment for the election instance.

    :param votes: [int]
            The number of votes for the parties.
    :param weights: [Number]
            The weights of the seats.
    :param seat_assign: [int]
            A seat assignment indicating, for each seat, the party that the seat was assigned to.
    :return: [bool, bool, bool, bool, bool, bool, Number, Number, Number]
            The experimental results indicating whether the seat assignment satisfies the six axioms,
            and its results for the three distance measures.
    """
    results_list = [providesWLQo(votes, weights, seat_assign), providesWLQ_X(votes, weights, seat_assign),
                    providesWLQ_1(votes, weights, seat_assign), providesWUQo(votes, weights, seat_assign),
                    providesWUQ_X(votes, weights, seat_assign), providesWUQ_1(votes, weights, seat_assign),
                    getAvgDistToWQ(votes, weights, seat_assign), getAvgDistBelowWLQ(votes, weights, seat_assign),
                    getAvgDistAboveWUQ(votes, weights, seat_assign), providesWEF_X(votes, weights, seat_assign),
                    providesWEF_1(votes, weights, seat_assign),providesWLQ_X_r(votes, weights, seat_assign)]

    return results_list


def getResultsAsString(votes: [int], weights: [Number], seat_assign: [int]) -> str:
    """
    Returns a string showing the experimental results of the seat assignment for the election instance,
    and the seat assignments returned by the WSAMs for the election instance.

    :param votes: [int]
            The number of votes for the parties.
    :param weights: [Number]
            The weights of the seats.
    :return: str
            The experimental results for the election instance
    """
    results_string = ""
    results_list = getResultsForElection(votes, weights, seat_assign)

    # Add results for the six proportionality axioms.
    results_string += "Axioms? --> WLQ: " + str(results_list[0]) \
                      + ", WLQ-X: " + str(results_list[1]) \
                      + ", WLQ-1: " + str(results_list[2]) \
                      + ", WUQ: " + str(results_list[3]) \
                      + ", WUQ-X: " + str(results_list[4]) \
                      + ", WUQ-1: " + str(results_list[5]) + "\n"

    # Add the results for the three quantitive measures.
    results_string += "Average distances? --> To Weight Quota: " + str(str(results_list[6])) \
                      + ", Below WLQ: " + str(str(results_list[7])) \
                      + ", Above WUQ: " + str(str(results_list[8]))

    return results_string


def providesWLQo(votes: [int], weights: [Number], seat_assign: [int]) -> bool:
    """
    Returns whether a seat assignment provides obtainable WLQ for the election instance.

    :param votes: [int]
            The number of votes for the parties.
    :param weights: [Number]
            The weights of the seats.
    :param seat_assign: [int]
            A seat assignment indicating, for each seat, the party that the seat was assigned to.
    :return: bool
            A boolean indicating whether the seat assignment provides WLQ for the election instance.
    """
    sat = True
    weight_lower_quotas = election.getWeightLowerQuotas(votes, weights)

    for party in range(len(votes)):
        party_weight = sum([weights[w_i] for w_i in range(len(weights)) if seat_assign[w_i] == party])
        if party_weight < weight_lower_quotas[party]:
            sat = False

    return sat


def providesWLQ_X(votes: [int], weights: [Number], seat_assign: [int]) -> bool:
    """
    Returns whether a seat assignment provides WLQ-X for the election instance.

    :param votes: [int]
            The number of votes for the parties.
    :param weights: [Number]
            The weights of the seats.
    :param seat_assign: [int]
            A seat assignment indicating, for each seat, the party that the seat was assigned to.
    :return: bool
            A boolean indicating whether the seat assignment provides WLQ-X for the election instance.
    """
    sat = True
    weight_quotas = election.getWeightQuotas(votes, weights)

    for party in range(len(votes)):
        party_weight = sum([weights[w_i] for w_i in range(len(weights)) if seat_assign[w_i] == party])
        if party_weight < weight_quotas[party]:
            for w in [weights[w_i] for w_i in range(len(weights)) if seat_assign[w_i] != party]:
                if party_weight + w <= weight_quotas[party]:
                    return False

    return sat

def providesWLQ_X_r(votes: [int], weights: [Number], seat_assign: [int]) -> bool:
    """
    Returns whether a seat assignment provides WLQ-X-r for the election instance.

    :param votes: [int]
            The number of votes for the parties.
    :param weights: [Number]
            The weights of the seats.
    :param seat_assign: [int]
            A seat assignment indicating, for each seat, the party that the seat was assigned to.
    :return: bool
            A boolean indicating whether the seat assignment provides WLQ-X-r for the election instance.
    """
    sat = True
    weight_quotas = election.getWeightQuotas(votes, weights)

    rep_parties = [party for party in range(len(votes)) if
                   sum([weights[w_i] for w_i in range(len(weights)) if seat_assign[w_i] == party]) >= weight_quotas[party]]
    for party in range(len(votes)):
        party_weight = sum([weights[w_i] for w_i in range(len(weights)) if seat_assign[w_i] == party])
        if party_weight < weight_quotas[party]:
            for w in [weights[w_i] for w_i in range(len(weights)) if (seat_assign[w_i] in rep_parties)]:
                if (party_weight + w) <= weight_quotas[party]:
                    return False

    return sat

def providesWLQ_1(votes: [int], weights: [Number], seat_assign: [int]) -> bool:
    """
    Returns whether a seat assignment provides WLQ-1 for the election instance.

    :param votes: [int]
            The number of votes for the parties.
    :param weights: [Number]
            The weights of the seats.
    :param seat_assign: [int]
            A seat assignment indicating, for each seat, the party that the seat was assigned to.
    :return: bool
            A boolean indicating whether the seat assignment provides WLQ-1 for the election instance.
    """
    sat = True
    weight_quotas = election.getWeightQuotas(votes, weights)

    party_below = 0
    for party in range(len(votes)):
        party_weight = sum([weights[w_i] for w_i in range(len(weights)) if seat_assign[w_i] == party])
        if party_weight < weight_quotas[party]:
            party_below += 1
            for w in [weights[w_i] for w_i in range(len(weights)) if seat_assign[w_i] != party]:
                if (party_weight + w) > weight_quotas[party]:
                    party_below -= 1
                    break
        if party_below > 0:
            return False

    return sat


def providesWUQo(votes: [int], weights: [Number], seat_assign: [int]) -> bool:
    """
    Returns whether a seat assignment provides obtainable WUQ for the election instance.

    :param votes: [int]
            The number of votes for the parties.
    :param weights: [Number]
            The weights of the seats.
    :param seat_assign: [int]
            A seat assignment indicating, for each seat, the party that the seat was assigned to.
    :return: bool
            A boolean indicating whether the seat assignment provides WUQ for the election instance.
    """
    sat = True
    weight_upper_quotas = election.getWeightUpperQuotas(votes, weights)

    for party in range(len(votes)):
        party_weight = sum([weights[w_i] for w_i in range(len(weights)) if seat_assign[w_i] == party])
        if party_weight > weight_upper_quotas[party]:
            sat = False

    return sat


def providesWUQ_X(votes: [int], weights: [Number], seat_assign: [int]) -> bool:
    """
    Returns whether a seat assignment provides WUQ-X for the election instance.

    :param votes: [int]
            The number of votes for the parties.
    :param weights: [Number]
            The weights of the seats.
    :param seat_assign: [int]
            A seat assignment indicating, for each seat, the party that the seat was assigned to.
    :return: bool
            A boolean indicating whether the seat assignment provides WUQ-X for the election instance.
    """
    sat = True
    weight_quotas = election.getWeightQuotas(votes, weights)

    for party in range(len(votes)):
        party_weight = sum([weights[w_i] for w_i in range(len(weights)) if seat_assign[w_i] == party])
        if party_weight > weight_quotas[party]:
            for w in [weights[w_i] for w_i in range(len(weights)) if seat_assign[w_i] == party]:
                if party_weight - w >= weight_quotas[party]:
                    return False

    return sat


def providesWEF_X(votes: [int], weights: [Number], seat_assign: [int]) -> bool:
    """
    Returns whether a seat assignment provides WEFX for the election instance.

    :param votes: [int]
            The number of votes for the parties.
    :param weights: [Number]
            The weights of the seats.
    :param seat_assign: [int]
            A seat assignment indicating, for each seat, the party that the seat was assigned to.
    :return: bool
            A boolean indicating whether the seat assignment provides WEFX for the election instance.
    """
    sat = True

    for party_1 in range(len(votes)):
        party1_weight = sum([weights[w_i] for w_i in range(len(weights)) if seat_assign[w_i] == party_1])
        if votes[party_1] == 0:
            continue
        for party_2 in range(len(votes)):
            if votes[party_2] == 0:
                continue
            party2_weight = sum([weights[w_i] for w_i in range(len(weights)) if seat_assign[w_i] == party_2])
            if (party1_weight/votes[party_1]) < (party2_weight/votes[party_2]):
                for w in [weights[w_i] for w_i in range(len(weights)) if seat_assign[w_i] == party_2]:
                    if (party1_weight/votes[party_1]) < ((party2_weight-w)/votes[party_2]):
                        return False

    return sat


def providesWEF_1(votes: [int], weights: [Number], seat_assign: [int]) -> bool:
    """
    Returns whether a seat assignment provides WEF1 for the election instance.

    :param votes: [int]
            The number of votes for the parties.
    :param weights: [Number]
            The weights of the seats.
    :param seat_assign: [int]
            A seat assignment indicating, for each seat, the party that the seat was assigned to.
    :return: bool
            A boolean indicating whether the seat assignment provides WEF1 for the election instance.
    """
    sat = True

    party_envy = 0
    for party_1 in range(len(votes)):
        if votes[party_1] == 0:
            continue
        party1_weight = sum([weights[w_i] for w_i in range(len(weights)) if seat_assign[w_i] == party_1])
        for party_2 in range(len(votes)):
            if votes[party_2] == 0:
                continue
            party2_weight = sum([weights[w_i] for w_i in range(len(weights)) if seat_assign[w_i] == party_2])
            if (party1_weight/votes[party_1]) < (party2_weight/votes[party_2]):
                party_envy += 1
                for w in [weights[w_i] for w_i in range(len(weights)) if seat_assign[w_i] == party_2]:
                    if (party1_weight/votes[party_1]) >= ((party2_weight-w)/votes[party_2]):
                        party_envy -= 1
                        break
        if party_envy > 0:
            return False

    return sat



def providesWUQ_1(votes: [int], weights: [Number], seat_assign: [int]) -> bool:
    """
    Returns whether a seat assignment provides WUQ-1 for the election instance.

    :param votes: [int]
            The number of votes for the parties.
    :param weights: [Number]
            The weights of the seats.
    :param seat_assign: [int]
            A seat assignment indicating, for each seat, the party that the seat was assigned to.
    :return: bool
            A boolean indicating whether the seat assignment provides WUQ-1 for the election instance.
    """
    sat = True
    weight_quotas = election.getWeightQuotas(votes, weights)

    party_above = 0
    for party in range(len(votes)):
        party_weight = sum([weights[w_i] for w_i in range(len(weights)) if seat_assign[w_i] == party])
        if party_weight > weight_quotas[party]:
            party_above += 1
            for w in [weights[w_i] for w_i in range(len(weights)) if seat_assign[w_i] == party]:
                if (party_weight - w) <= weight_quotas[party]:
                    party_above -= 1
                    break

    if party_above > 0:
        sat = False

    return sat


def getAvgDistToWQ(votes: [int], weights: [Number], seat_assign: [int]) -> Number:
    """
    Returns a number, for an election instance's seat assignment, indicating the average distance
        (in terms of representation) that parties are from their weight quota.

    :param votes: [int]
            The number of votes for the parties.
    :param weights: [Number]
            The weights of the seats.
    :param seat_assign: [int]
            A seat assignment indicating, for each seat, the party that the seat was assigned to.
    :return: Number
            The average distance (in terms of representation) that parties are from their weight quota.
    """
    total_dist = 0
    weight_quotas = election.getWeightQuotas(votes, weights)

    for party in range(len(votes)):
        party_weight = sum([weights[w_i] for w_i in range(len(weights)) if seat_assign[w_i] == party])
        total_dist += abs(weight_quotas[party] - party_weight)

    return round(total_dist / len(votes), 1)


def getAvgDistBelowWLQ(votes: [int], weights: [Number], seat_assign: [int]) -> Number:
    """
    Returns a number , for an election instance's seat assignment, indicating
    the average distance (in terms of representation) that parties are below
    their weighted lower quota (for those parties below it).

    :param votes: [int]
            The number of votes for the parties.
    :param weights: [Number]
            The weights of the seats.
    :param seat_assign: [int]
            A seat assignment indicating, for each seat, the party that the seat was assigned to.
    :return: Number
            The average distance (in terms of representation) that parties are below their weighted lower quota.
    """
    total_dist = 0
    weighted_lower_quotas = election.getWeightLowerQuotas(votes, weights)

    # A variable used to count the number of parties below their weighted lower quota.
    party_count = 0

    for party in range(len(votes)):
        party_weight = sum([weights[w_i] for w_i in range(len(weights)) if seat_assign[w_i] == party])
        if party_weight < weighted_lower_quotas[party]:
            party_count += 1
            total_dist += weighted_lower_quotas[party] - party_weight

    if party_count == 0:
        return 0
    else:
        return round(total_dist / party_count, 1)


def getAvgDistAboveWUQ(votes: [int], weights: [Number], seat_assign: [int]) -> Number:
    """
    Returns a number, for an election instance's seat assignment, indicating
    the average distance (in terms of representation) that parties are above
    their weighted upper quota (for those parties above it).

    :param votes: [int]
            The number of votes for the parties.
    :param weights: [Number]
            The weights of the seats.
    :param seat_assign: [int]
            A seat assignment indicating, for each seat, the party that the seat was assigned to.
    :return: Number
            The average distance (in terms of representation) that parties are above their weighted upper quota.
    """
    total_dist = 0
    weighted_upper_quotas = election.getWeightUpperQuotas(votes, weights)
    # A variable used to count the number of parties below their weighted upper quota.
    party_count = 0

    for party in range(len(votes)):
        party_weight = sum([weights[w_i] for w_i in range(len(weights)) if seat_assign[w_i] == party])
        if party_weight > weighted_upper_quotas[party]:
            party_count += 1
            total_dist += party_weight - weighted_upper_quotas[party]

    if party_count == 0:
        return 0
    else:
        return round(total_dist / party_count, 1)


def getElectionFromFile(elec_num: int) -> [[int], [Number], [int]]:
    """
    Returns, from a file, the votes, weights and seat assignment associated with the specified election instance.

    :param elec_num: int
            An integer specifying which election instance to obtain details for.
    :return: [[int], [Number], [int]]
            A list containing a list of votes, a list of weights and a list representing a seat assignment.
    """
    election_instance = [getVotesFromFile(elec_num), getWeightsFromFile(elec_num), getSeatAssignFromFile(elec_num)]
    return election_instance


def getVotesFromFile(elec_num: int) -> [int]:
    """
    Returns, from a file, the votes associated with specified election instance.

    :param elec_num: int
            An integer specifying which election instance to obtain details for.
    :return: [int]
            The number of votes for the parties.
    """
    votes = []
    for file_name in ["bundestag_committees/" + str(elec_num) + "/german_parliament_" + str(elec_num) + ".txt"]:
        with open(file_name, "r") as f:
            for line in f.readlines():
                line = line.strip()
                if len(line) > 1:
                    if not line.startswith('#'):
                        votes.append(int(line.split(":")[-1]))

    return votes


def getWeightsFromFile(elec_num: int) -> [Number]:
    """
    Returns, from a file, the weights associated with the specified election instance.

    :param elec_num: int
            An integer specifying which election instance to obtain details for.
    :return: [int]
            The weights of the seats.
    """
    weights = []

    for file_name in ["bundestag_committees/" + str(elec_num) + "/bundestag_" + str(elec_num) + ".txt"]:
        with open(file_name, "r") as f:
            for line in f.readlines():
                line = line.strip()
                if len(line) > 1:
                    if not line.startswith('#'):
                        weights.append(int(line.split(":")[0]))

    # Sort weights into non-increasing order.
    weights.sort(reverse=True)

    return weights


def getSeatAssignFromFile(elec_num: int) -> [int]:
    """
    Returns, from a file, the seat assignment associated with the specified election instance.

    :param elec_num: int
            An integer specifying which election instance to obtain details for.
    :return: [int]
            A seat assignment indicating, for each seat, the party that the seat was assigned to.
    """
    seat_assign = []

    for file_name in ["bundestag_committees/" + str(elec_num) + "/bundestag_" + str(elec_num) + ".txt"]:
        with open(file_name, "r") as f:
            for line in f.readlines():
                line = line.strip()
                if len(line) > 1:
                    if not line.startswith('#'):
                        seat_assign.append(int(line.split(":")[-1]) - 1)

    return seat_assign


def generateElection(num_votes: int, vote_range: [int],num_weights:int, weight_range: [Number]) -> [[int],[Number]]:
    election_instance = [[],[]]

    election_instance[0] = list(random.sample(vote_range, num_votes))
    election_instance[1] = list(random.sample(weight_range, num_weights))

    return election_instance

def generateAllElections(num_elections: int, num_votes: int, vote_range: [int],num_weights:int, weight_range: [Number]):
    elections = []
    for i in range(num_elections):
        elections.append(generateElection(num_votes,vote_range,num_weights,weight_range))

    return elections