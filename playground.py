import rivest_shen as rs

rs.compare_methods([("Borda", rs.Borda_winner), ("plurality", rs.plurality_winner)], printing_wanted=False)