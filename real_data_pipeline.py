import rivest_shen as rs
import glob

# generate list of netflix files
fns = []
for fn in glob.glob("**/*converted.soc"):
    fns.append(fn)

methods = [("Borda", rs.Borda_winner), ("plurality", rs.plurality_winner), ("gt", rs.gt_winner), \
    ("minimax", rs.minimax_winner), ("gtd", rs.gtd_winner), \
    ("Schulze", rs.Schulze_winner), ("IRV", rs.IRV_winner)]

rs.evaluate_methods_real(methods, fns, printing_wanted=False)