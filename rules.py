"""
The Weighted Seat Assignment Methods (WSAMs)
"""
import election
from numbers import Number


def getSeatAssignments(votes: [int], weights: [Number]) -> str:
    """
    Returns a string showing the seat assignments returned by the WSAMs for the election instance.

    :param votes: [int]
            The number of votes for the parties.
    :param weights: [Number]
            The weights of the seats.
    :return: str
            The seat assignments returned by the WSAMs for the election instance.
    """
    seat_assignments = "Seat assignment returned by:\n" + "Adams --> " + str(divisorMethod(votes, weights, 0)) \
                       + "\nD\'Hondt --> " + str(divisorMethod(votes, weights, 1)) \
                       + "\nSaint Lague --> " + str(divisorMethod(votes, weights, 0.5)) \
                       + "\nGreedy Method --> " + str(greedy(votes, weights))

    return seat_assignments


def divisorMethod(votes: [int], weights: [Number], divisor: Number) -> [int]:
    """
    Returns, for the election instance, the seat assignment constructed by the specified divisor method.
    Ties broken in favour of party appearing earlier in vote vector.

    :param votes: [int]
            The number of votes for the parties.
    :param weights: [Number]
            The weights of the seats.
    :param divisor: Number
            Initialises the divisor method to use, either 0 or 1 for Adams or D'Hondt, respectively.
    :return: seat_assign: [int]
            A seat assignment indicating, for each seat, the party that the seat was assigned to.
    """
    # Check if divisor is valid (either 0,1 or 0.5)
    if divisor not in [0, 1, 0.5]:
        raise ValueError("Divisor must be 0, 1 or 0.5.")

    # Sort weights into non-increasing order.
    weights.sort(reverse=True)

    seat_assign = [-1] * len(weights)

    for w_i in range(len(weights)):
        max_ratio = 0
        win_party = -1
        for party in range(len(votes)):
            party_current_rep = sum([weights[w_i] for w_i in range(len(weights)) if seat_assign[w_i] == party])
            # check if Adams method is applied for party with current representation of 0.
            if divisor + party_current_rep == 0:
                party_ratio = float('inf')
            else:
                party_ratio = votes[party] / (party_current_rep + (weights[w_i] * divisor))

            if party_ratio > max_ratio:
                max_ratio = party_ratio
                win_party = party

        seat_assign[w_i] = win_party

    return seat_assign


def greedy(votes: [int], weights: [Number]) -> [int]:
    """
    Returns, for the election instance, the seat assignment constructed by the Greedy method.
    Ties broken in favour of party appearing earlier in vote vector.

    :param votes: [int]
            The number of votes for the parties.
    :param weights: [Number]
            The weights of the seats.
    :return: seat_assign: [int]
            A seat assignment indicating, for each seat, the party that the seat was assigned to.
    """
    # Sort weights into non-increasing order.
    weights.sort(reverse=True)

    seat_assign = [-1] * len(weights)
    weight_quotas = election.getWeightQuotas(votes, weights)

    for w_i in range(len(weights)):
        max_party_ratio = 0
        win_party = -1
        for party in range(len(votes)):
            party_current_rep = sum([weights[w_i] for w_i in range(len(weights)) if seat_assign[w_i] == party])
            party_ratio = weight_quotas[party] - party_current_rep
            if party_ratio > max_party_ratio:
                max_party_ratio = party_ratio
                win_party = party
        seat_assign[w_i] = win_party

    return seat_assign
