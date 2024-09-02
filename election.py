"""
Functions related to an election instance.
"""
import math
from mip import Model, xsum, maximize, minimize, BINARY
from numbers import Number


def getWeightQuotas(votes: [int], weights: [Number]) -> [Number]:
    """
    Returns the weight quotas for the parties.

    :param votes: [int]
            The number of votes for the parties.
    :param weights: [Number]
            The weights of the seats.
    :return: [Number]
            The weight quotas for the parties.
    """
    return [(sum(weights) * (votes[party] / sum(votes))) for party in range(len(votes))]


def getWeightLowerQuotas(votes: [int], weights: [Number]) -> [Number]:
    """
    Returns the weighted lower quotas of the parties.

    :param votes: [int]
            The number of votes for the parties.
    :param weights: [Number]
            The weights of the seats.
    :return: [Number]
            The weighted lower quotas of the parties.
    """
    weighted_lower_quotas = [-1] * len(votes)
    seats = range(len(weights))

    for party in range(len(votes)):
        seat_lower_quota = math.floor(len(weights) * (votes[party] / sum(votes)))

        weight_quota = sum(weights) * (votes[party] / sum(votes))
        # Use MIP solver for Knapsack to compute the weighted lower quotas.
        m = Model("knapsack")
        m.verbose = 0
        x = [m.add_var(var_type=BINARY) for s in seats]
        m.objective = maximize(xsum(weights[s] * x[s] for s in seats))
        m += xsum(weights[s] * x[s] for s in seats) <= weight_quota
        m += xsum(x[s] for s in seats) <= seat_lower_quota
        m.optimize()
        selected = [s for s in seats if x[s].x >= 0.99]
        weighted_lower_quotas[party] = sum(weights[s] for s in selected)

    return weighted_lower_quotas


def getWeightUpperQuotas(votes: [int], weights: [Number]) -> [Number]:
    """
    Returns the weighted upper quotas of the parties.

    :param votes: [int]
            The number of votes for the parties.
    :param weights: [Number]
            The weights of the seats.
    :return: [Number]
            The weighted upper quotas of the parties.
    """
    weighted_upper_quotas = [-1] * len(votes)
    seats = range(len(weights))

    for party in range(len(votes)):

        weight_quota = sum(weights) * (votes[party] / sum(votes))
        # Use MIP solver for Knapsack to compute the weighted upper quotas.
        m = Model("knapsack")
        m.verbose = 0
        x = [m.add_var(var_type=BINARY) for s in seats]
        m.objective = minimize(xsum(weights[s] * x[s] for s in seats))
        m += xsum(weights[s] * x[s] for s in seats) >= weight_quota
        m.optimize()
        selected = [s for s in seats if x[s].x >= 0.99]
        weighted_upper_quotas[party] = sum(weights[s] for s in selected)

    return weighted_upper_quotas
