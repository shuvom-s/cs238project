import rivest_shen as rs
import numpy as np
import pandas as pd
import os
import matplotlib
import matplotlib.pyplot as plt
import glob
import seaborn as sns


# MARGINS IN REAL WORLD DATA
# 1 plot per category of election (not incl. netflix)
# On x axis, type of voting system being compared against GT
# On y axis, normalized margin of that system vs GT

def city_elections_plots():
    #elections = ["vermont", "sf", "sanleandro", "pierce", "oakland", "burlington", "aspen"]
    elections = ["vermont", "sf", "oakland"]
    systems = ["Borda", "plurality", "minimax", "gtd", "Schulze", "IRV"]
    #indents = [28, 23, 31, 27, 28, 31, 26]
    indents = [28, 23, 28]
    # Get normalized margins for all the elections in a single city
    dicts = {}
    for ind in range(len(elections)):
        el = elections[ind]
        margins = {}
        for s in systems:
            margins[s] = []
        city_count = 0
        for fn in glob.glob("data/" + el + "/*.toc"):
            city_count += 1
            # grab number of voters
            #print(fn)
            input = open(fn, "r")
            text = input.read()
            lines = text.split("\n")
            num_alts = lines[0]
            lines = lines[int(num_alts)+1:len(lines)-1]
            first_line = lines[0].split(",")
            count = float(first_line[0])
            #print(count)

            # grab margin from results for each voting system type
            indent = indents[ind]
            margins_df = pd.read_csv("results/real_data/" + el + "/" + fn[indent:indent+2] + "_Nmargins.csv")
            
            for s in systems:
                margins[s].append(np.float(margins_df.loc[2, s])/count)
        
        # margin_matrix = np.zeros((city_count, len(systems)))
        # for election in range(city_count):
        #     for system in range(len(systems)):
        #         margin_matrix[election][system] = margins[systems[system]][election]

        # margin_df = pd.DataFrame(margin_matrix, index=[i for i in range(city_count)], columns=systems)

        #fig, ax = plt.subplots()
        #ax.violinplot([margin_df.Borda, margin_df.plurality, margin_df.minimax, margin_df.gtd, margin_df.Schulze, margin_df.IRV])

        #ax.set_title("Violin Plot of Margins in " + el + " by Voting System")
        
        margin_matrix = [[0 for i in range(2)] for j in range(city_count*len(systems)) ]
        x = 0
        for election in range(city_count):
            for system in range(len(systems)):
                margin_matrix[x][0] = margins[systems[system]][election]
                margin_matrix[x][1] = systems[system]
                x += 1
                #margin_matrix[election][system] = margins[systems[system]][election]
        margin_df = pd.DataFrame(margin_matrix, index = [i for i in range(city_count*len(systems))], columns=["Advantage", "Voting System"])
        
        ax = sns.violinplot(x="Voting System", y="Advantage", data=margin_df)
        ax.set_title("Advantage of GT over Other Voting Systems in " + el)
        ax.set_xlabel("Voting System")
        ax.set_ylabel("Advantage")

        ax = sns.stripplot(x="Voting System", y="Advantage", data=margin_df)
        
        plt.show()

#city_elections_plots()
systems = ["Borda", "plurality", "minimax", "gtd", "Schulze", "IRV"]

# MARGINS IN NON-CONDORCET NETFLIX DATA
def netflix_nc_matrix(dim):
    num_3s = 0 #34077
    num_4s = 0 #37841
    trials = 0
    if (dim == 3):
        num_3s = 34077
        trials = num_3s
    else:
        num_4s = 37841
        trials = num_4s
    margin_matrix = []
    x = 0
    neg = 0
    pos = 0
    for race in range(trials):
        margins_df = pd.read_csv("results/real_data/Netflix" + str(dim) + "/" + str(race) + "_Nmargins.csv")
        for system in range(len(systems)):
            margin_matrix.append([margins_df.loc[2, systems[system]], systems[system]])
            x += 1
            print(x)
    
    # cols = np.array([row[0] for row in margin_matrix])

    # # Filtered matrix
    # arr = cols[:,None]
    # print(arr)
    # median = np.median(arr, axis=0)
    # print(median)
    # diff = np.sum((arr - median)**2, axis=-1)
    # diff = np.sqrt(diff)
    # print(diff)
    # med_abs_deviation = np.median(diff)
    # print(med_abs_deviation)
    # modified_z_score = 0.6745 * diff / med_abs_deviation

    # print(modified_z_score)

    # filtered#_matrix = []
    # for i in range(trials):
    #     if (modified_z_score[i] <= 3.5):
    #         filtered_matrix.append(margin_matrix[i])
    #     #print("filtering" + str(i))

    # return filtered_matrix
    return margin_matrix
 
#netflix_nc_matrix(3)

def netflix_nc_plots(dim):
    margin_matrix = netflix_nc_matrix(dim)
    #print(margin_matrix)
    margin_df = pd.DataFrame(margin_matrix, index = [i for i in range(len(margin_matrix))], columns=["Advantage", "Voting System"])

    print(margin_df)
    ax = sns.violinplot(x="Voting System", y="Advantage", data=margin_df)
    ax.set_title("Advantage of GT over Voting Systems in Netflix Data, " + str(dim) + " Candidates")
    ax.set_xlabel("Voting System")
    ax.set_ylabel("Advantage")

    # #ax = sns.stripplot(x="Voting System", y="Margin", data=margin_df)
    # ax.set_title("Margin by Voting System in Netflix Data for 4 Candidates")
    # ax.set_xlabel("Voting System")
    # ax.set_ylabel("Margin")

    plt.show()

#netflix_nc_plots(3)


# ONE PLOT FOR 3D HYPERSPHERE FOR VOTERS VS % CONDORCET - ONE LINE PER # CANDIDATES
def plot_hypersphere_condorcet(margins=False):
    xs = [100, 250, 500, 1000, 1500, 2500, 5000, 7500, 10000, 15000]
    ys = [[0 for i in range(len(xs))] for j in range(12)]
    for m in range(3, 11):
        for ind in range(len(xs)):
            x = xs[ind]
            condorcet_df = pd.read_csv("results/distributions/hypersphere/d_3/m_" + str(m) + "/v_" + str(x) + "/condorcet.csv")
            proportion = condorcet_df.loc[0]['n_condorcet']
            proportion = proportion/10000
            ys[m][ind] = proportion

    for m in range(3, 11):
        plt.plot(xs, ys[m], label = str(m) + " candidates")
        plt.xlabel("Number of Voters")
        plt.ylabel("Proportion of Elections with Condorcet Winner")

    plt.title("Proportion of Condorcet Winners by # Voters, # Candidates")
    plt.legend()
    plt.show()

#plot_hypersphere_condorcet()



# ONE PLOT PER VOTING SYSTEM FOR 3D HYPERSPHERE FOR VOTERS VS ADV MARGIN - ONE LINE PER # CANDIDATES
def plot_hypersphere_margin():
    for s in range(len(systems)):
        system = systems[s]
        xs = [100, 250, 500, 1000, 1500, 2500, 5000, 7500, 10000, 15000, 25000]
        ys = [[0 for i in range(len(xs))] for j in range(12)]

        for m in range(3, 11):
            for ind in range(len(xs)):
                x = xs[ind]
                margin_df = pd.read_csv("results/distributions/hypersphere/d_3/m_" + str(m) + "/v_" + str(x) + "/Nmargins.csv")
                margin = margin_df.loc[2][system]
                num_voters = x*10000
                ys[m][ind] = margin/num_voters

        for m in range(3, 11):
            plt.plot(xs, ys[m], label = str(m) + " candidates")
            plt.xlabel("Number of Voters")
            plt.ylabel("Advantage of GT over " + system)

        plt.title("Advantage by # Voters, # Candidates for GT vs. " + system)
        plt.legend()
        plt.show()

#plot_hypersphere_margin()

# For Borda, IRV, plurality, for m = 3 and 10 (so six graphs), plot
# margin, margin coming from Condorcet, and margin coming from non-Condorcet
def adv_analysis():
    xs = [100, 250, 500, 1000, 1500, 2500, 5000, 7500, 10000, 15000]
    graphs = ["Borda, 3 Cand", "Borda, 10 Cand", "IRV, 3 Cand", "IRV, 10 Cand", "Plurality, 3 Cand", "Plurality, 10 Cand"]
    ys_labels = ["Avg Adv from Condorcet Paradoxes", "Avg Adv from Condorcet Winners", "Total Advantage"]
    cand = [3, 10]
    methods = ["Borda", "IRV", "plurality"]
    for c in cand: 
        for m in methods:
            ys = [[0 for i in range(len(xs))] for j in range(len(ys_labels))]
            for ind in range(len(xs)):
                x = xs[ind]
                Nmargin = pd.read_csv("results/distributions/hypersphere/condorcet/d_3/m_" + str(c) + "/v_" + str(x) + "/Nmargins.csv")
                Nmargin_condorcet_winner = pd.read_csv("results/distributions/hypersphere/condorcet/d_3/m_" + str(c) + "/v_" + str(x) + "/Nmargins_condorcet.csv")
                condorcet_df = pd.read_csv("results/distributions/hypersphere/condorcet/d_3/m_" + str(c) + "/v_" + str(x) + "/condorcet.csv")
                
                num_cond_winner = condorcet_df.loc[0]['n_condorcet']
                condorcet_winner_adv = Nmargin_condorcet_winner.loc[2][m]
                total_adv = Nmargin.loc[2][m]
                condorcet_paradox_adv  = total_adv - condorcet_winner_adv

                condorcet_winner_adv = condorcet_winner_adv/(num_cond_winner * x) 
                total_adv = total_adv / (1000 * x) 
                condorcet_paradox_adv = condorcet_paradox_adv / ((1000 - num_cond_winner)*x)
            
                ys[0][ind] = condorcet_paradox_adv
                ys[1][ind] = condorcet_winner_adv
                ys[2][ind] = total_adv

            for line in range(len(ys_labels)):
                plt.plot(xs, ys[line], label = ys_labels[line])
                plt.xlabel("Number of Voters")
                plt.ylabel("Advantage")

            plt.title("Average Advantage by Type of Election (Condorcet), " + m + ", " + str(c) + " Cand")
            plt.legend()
            plt.show()

adv_analysis()

# For Borda, IRV, plurality, for m = 3 and 10 (all on one graph; six lines), plot
# probability the method picks a Condorcet winner given there is one
def prob_picks_Condorcet():
    xs = [100, 250, 500, 1000, 1500, 2500, 5000, 7500, 10000, 15000]
    ys_labels = ["Borda, 3 Cand", "Borda, 10 Cand", "IRV, 3 Cand", "IRV, 10 Cand", "Plurality, 3 Cand", "Plurality, 10 Cand"]
    ys = [[0 for i in range(len(xs))] for j in range(len(ys_labels))]
    cand = [3, 10]
    methods = ["Borda", "IRV", "plurality"]
    for c in cand: 
        for ind in range(len(xs)):
            x = xs[ind]
            condorcet_df = pd.read_csv("results/distributions/hypersphere/condorcet/d_3/m_" + str(c) + "/v_" + str(x) + "/condorcet.csv")
            num_cond = condorcet_df.loc[0]['n_condorcet']
            print("cand: " + str(c) + " voters: " + str(x) + " condorcet num: " + str(num_cond))

            Nagreecond_df = pd.read_csv("results/distributions/hypersphere/condorcet/d_3/m_" + str(c) + "/v_" + str(x) + "/Nagree_condorcet.csv")

            for m in methods:
                agree = Nagreecond_df.loc[2][m]

                proportion = agree/num_cond
                print("method: " + m + " proportion: " + str(proportion))

                ys_ind = methods.index(m)*2
                if (c == 10):
                    ys_ind += 1
                ys[ys_ind][ind] = proportion

    for line in range(len(ys_labels)):
        plt.plot(xs, ys[line], label = ys_labels[line])
        plt.xlabel("Number of Voters")
        plt.ylabel("Probability")

    plt.title("Probability of Non-Condorcet Method Picking Condorcet Winner")
    plt.legend()
    plt.show()

#prob_picks_Condorcet()