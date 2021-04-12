import rivest_shen as rs

#rs.compare_methods([("Borda", rs.Borda_winner), ("plurality", rs.plurality_winner), ("gtd", rs.gt_optimal_mixed_strategy)], printing_wanted=False)

rs.runoff("gt", rs.gt_winner, "Borda", rs.Borda_winner)