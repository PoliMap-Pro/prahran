from votekit.ballot import Ballot
from votekit.pref_profile import PreferenceProfile
from votekit.elections import IRV
import votekit

def run_election(grn_primary, lib_primary, ajp_primary, pref_flows):
    primaries = {"GRN": grn_primary,
                "LIB": lib_primary,
                "AJP": ajp_primary,
                }
    print(primaries)
    print(pref_flows)

    # primaries['GRN'] += alp_primary * alp_swing/100
    primaries['IND'] = 100 - sum(primaries.values())
    votes = 50000
    ballots = []
    for party, prim in primaries.items():
        pv = int(votes * .01 * prim)
        if party in ['GRN', 'LIB']:
            ballots.append(
                Ballot(
                    ranking = [{party}] + [{x} for x in primaries.keys() if x != party],
                    weight = int(votes * prim * .01)
                )
            )
        else:
            first = {party}
            ballots.append(
                Ballot(
                    ranking = [{party}, {"GRN"}] + [{x} for x in primaries.keys() if x not in [party, "GRN"]],
                    weight = int(votes * prim * .0001 * pref_flows[party])
                )
            )
            ballots.append(
                Ballot(
                    ranking = [{party}, {"LIB"}] + [{x} for x in primaries.keys() if x not in [party, "LIB"]],
                    weight = int(votes * prim * .0001 * (100 - pref_flows[party]))
                )
            ) 

    profile = PreferenceProfile(ballots = ballots, candidates = list(primaries.keys()))
    election = IRV(profile = profile)

    irv = election

    final_round = irv.length - 1
    final_profile = irv.get_profile(final_round)
    final_scores = votekit.utils.first_place_votes(final_profile)
    top_two = sorted(final_scores, key=final_scores.get, reverse=True)[:2]
    two_party_profile = votekit.utils.remove_cand([c for c in final_profile.candidates if c not in top_two], final_profile)
    two_party_scores = votekit.utils.first_place_votes(two_party_profile)
    total_votes = sum(two_party_scores.values())
    percentages = {cand: 100*float(votes / total_votes) for cand, votes in two_party_scores.items()}
    return percentages 
    # # Get final round results
    # last_round = election.get_step(election.length)[0]
    # total_votes = last_round.total_ballot_wt

    # # Calculate and return percentages for final candidates
    # results = {
    #     cand: (last_round.weights[cand] / total_votes) * 100 
    #     for cand in last_round.weights
    # }

    # return results