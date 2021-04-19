import rivest_shen as rs
import numpy as np
import pandas as pd
import os


def convert_to_dataframe(result_dict, method_names):
    """
    Convert result_dict, a dictionary of results (e.g. margins dictionary) to
    a dataframe, using method_names as the row and column names.
    """
    result_matrix = np.zeros((len(method_names), len(method_names)))

    for key in result_dict:
        i = method_names.index(key[0])
        j = method_names.index(key[1])
        result_matrix[i, j] = result_dict[key]
    df = pd.DataFrame(result_matrix, index=method_names, columns=method_names)
    return df


def unpack_and_save_results(results, methods, distribution, m=5):
    """
    results: tuple of results; results[0]: num condorcet, results[1]: num unique strat,
    results[2]: agreement matrix, results[3]: margin matrix
    methods: all methods that were run
    distribution: specific ballot profile distribution 

    Unpacks a dictionary of results from rivest_shen code, converts to dataframe format,
    and saves results.  For example, the dictionary {('A', 'A'): 0, ('A', 'B'): 100, ...}
    might look like
        A     B
    A   0     100
    B   -100  0
    once saved.
    """
    n_condorcet, n_opt_strat_unique, Nagree, Nmargins = results[0], results[1], results[2], results[3]
    methods_names_only = [method[0] for method in methods]

    # make dataframes
    df_agree = convert_to_dataframe(Nagree, methods_names_only)
    df_margins = convert_to_dataframe(Nmargins, methods_names_only)
    df_condorcet = pd.DataFrame(columns = ['n_condorcet', 'n_opt_strat_unique'])
    df_condorcet.loc[len(df_condorcet)] = [n_condorcet, n_opt_strat_unique]

    # make directory if it doesn't exist
    save_path = "results/distributions/" + str(distribution[0]) + "/"
    if distribution[0] == "geometric" or distribution[0] == "hypersphere":
        save_path += "d_" + str(distribution[1]) + "/"
    if distribution[0] == "polya_eggenberger":
        save_path += "alpha_" + str(distribution[1]) + "/"
    if distribution[0] == "UUP":
        save_path += "enum_" + str(distribution[1]) + "/"
        
    save_path += "m_" + str(m) + "/" 
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    save_agree = save_path + "Nagree.csv"
    save_margins = save_path + "Nmargins.csv"
    save_condorcet = save_path + "condorcet.csv"

    # save dataframes
    df_agree.to_csv(save_agree)
    df_margins.to_csv(save_margins)
    df_condorcet.to_csv(save_condorcet)

    if distribution[0] == "UUP":
        df_prob_vector = pd.DataFrame(distribution[2])
        save_prob_vector = save_path + "prob_vector.csv"
        df_prob_vector.to_csv(save_prob_vector)



# methods = [("Borda", rs.Borda_winner), ("plurality", rs.plurality_winner), ("gt", rs.gt_winner), \
#    ("minimax", rs.minimax_winner), ("gtd", rs.gtd_winner), \
#    ("Schulze", rs.Schulze_winner), ("IRV", rs.IRV_winner)]

#ballot_distributions = [("geometric", 2), ("geometric", 3), ("geometric", 4), \
#    ("hypersphere", 2), ("hypersphere", 3), ("hypersphere", 4), \
#    ("uniform", ),]
ballot_distributions = [("polya_eggenberger", 1), ("polya_eggenberger", 2), \
    ("polya_eggenberger", 5), ("polya_eggenberger", 10)]

for ballot_distribution in ballot_distributions:
    for m in [3,4,6]:
        results = rs.compare_methods(methods, ballot_distribution, printing_wanted=True, m=m)
        unpack_and_save_results(results, methods, ballot_distribution, m=m)
#     #enum+=1
# #results = rs.compare_methods(methods, ("uniform",), printing_wanted=True)
enum = 0
# '''
# for p1 in np.arange(0.0, 1.0, 0.25):
#     for p2 in np.arange(0, 1-p1, 0.20):
#         for p3 in np.arange(0, 1-(p1+p2), 0.15):
#             for p4 in np.arange(0, 1-(p1+p2+p3), 0.10):
#                 for p5 in np.arange(0, 1-(p1+p2+p3+p4), 0.05):
#                     p6 = 1-(p1+p2+p3+p4+p5)
#                     prob_vector = [p1,p2,p3,p4,p5,p6]
#                     if np.count_nonzero(prob_vector) > 4:'''
#prob_vector = [1/6 for i in range(6)]
                        

# #rs.runoff("gt", rs.gt_winner, "IRV", rs.IRV_winner, printing_wanted=False)