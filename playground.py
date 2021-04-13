import rivest_shen as rs

methods = [("gt", rs.gt_winner), ("IRV", rs.IRV_winner)]

rs.compare_methods(methods, printing_wanted=False)

#rs.runoff("gt", rs.gt_winner, "IRV", rs.IRV_winner, printing_wanted=False)