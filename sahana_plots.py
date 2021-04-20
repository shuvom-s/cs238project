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
    elections = ["vermont", "sf", "sanleandro", "pierce", "oakland", "burlington", "aspen"]
    systems = ["Borda", "plurality", "minimax", "gtd", "Schulze", "IRV"]
    indents = [28, 23, 31, 27, 28, 31, 26]
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
        margin_df = pd.DataFrame(margin_matrix, index = [i for i in range(city_count*len(systems))], columns=["Margin", "Voting System"])
        
        ax = sns.violinplot(x="Voting System", y="Margin", data=margin_df)
        ax.set_title("Margin by Voting System in " + el)
        ax.set_xlabel("Voting System")
        ax.set_ylabel("Margin")

        ax = sns.stripplot(x="Voting System", y="Margin", data=margin_df)
        
        plt.show()

systems = ["Borda", "plurality", "minimax", "gtd", "Schulze", "IRV"]

# MARGINS IN NON-CONDORCET NETFLIX DATA
def netflix_nc_plots():
    num_3s = 0 #34077
    num_4s = 37841
    margin_matrix = [[0 for i in range(2)] for j in range((num_3s+num_4s)*len(systems))]
    x = 0
    neg = 0
    pos = 0
    for race in range(num_4s):
        margins_df = pd.read_csv("results/real_data/Netflix4/" + str(race) + "_Nmargins.csv")
        for system in range(len(systems)):
            margin_matrix[x][0] = margins_df.loc[2, systems[system]]
            margin_matrix[x][1] = systems[system]
            if (margin_matrix[x][0] < 0):
                neg += 1
                #print(margin_matrix[x][0], race)
            elif (margin_matrix[x][0] > 0):
                pos += 1
            x += 1
    print("4 Candidates Normalized: \n")
    print("Neg: " + str(neg))
    print("Pos: " + str(pos))


    # for race in range(num_4s):
    #     margins_df = pd.read_csv("results/real_data/Netflix4/" + str(race) + "_Nmargins.csv")
    #     for system in range(len(systems)):
    #         margin_matrix[x][0] = margins_df.loc[2, systems[system]]
    #         margin_matrix[x][1] = systems[system]
    #         x += 1
    #         print(x)

    # margin_df = pd.DataFrame(margin_matrix, index = [i for i in range((num_3s+num_4s)*len(systems))], columns=["Margin", "Voting System"])

    # ax = sns.violinplot(x="Voting System", y="Margin", data=margin_df)
    # # ax.set_title("Margin by Voting System in Netflix Data for 3 Candidates")
    # # ax.set_xlabel("Voting System")
    # # ax.set_ylabel("Margin")

    # #ax = sns.stripplot(x="Voting System", y="Margin", data=margin_df)
    # ax.set_title("Margin by Voting System in Netflix Data for 4 Candidates")
    # ax.set_xlabel("Voting System")
    # ax.set_ylabel("Margin")

    # plt.show()

# netflix_nc_plots()

# ONE PLOT FOR 3D HYPERSPHERE FOR VOTERS VS % CONDORCET - ONE LINE PER # CANDIDATES
def plot_hypersphere_condorcet():
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

plot_hypersphere_condorcet()



# ONE PLOT PER VOTING SYSTEM FOR 3D HYPERSPHERE FOR VOTERS VS ADV MARGIN - ONE LINE PER # CANDIDATES
def plot_hypersphere_margin():
    for s in range(len(systems)):
        system = systems[s]
        xs = [100, 250, 500, 1000, 1500, 2500, 5000, 7500, 10000, 15000]
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
            plt.ylabel("Margin " + system)

        plt.title("Margin by # Voters, # Candidates for GT vs. " + system)
        plt.legend()
        plt.show()

# plot_hypersphere_margin