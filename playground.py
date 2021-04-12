import rivest_shen as rs

methods = [("Borda", rs.Borda_winner), ("plurality", rs.plurality_winner), ("gt", rs.gt_winner), \
    ("minimax", rs.minimax_winner), ("gtd", rs.gtd_winner), \
    ("Schulze", rs.Schulze_winner), ("IRV", rs.IRV_winner)]

rs.compare_methods(methods, printing_wanted=False)

#rs.runoff("gt", rs.gt_winner, "Borda", rs.Borda_winner, printing_wanted=False)