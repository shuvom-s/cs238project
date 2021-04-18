import rivest_shen as rs
import glob


methods = [("Borda", rs.Borda_winner), ("plurality", rs.plurality_winner), ("gt", rs.gt_winner), \
    ("minimax", rs.minimax_winner), ("gtd", rs.gtd_winner), \
    ("Schulze", rs.Schulze_winner), ("IRV", rs.IRV_winner)]


# datasets = ["burlington", "aspen", "vermont", "sanleandro", "pierce", "oakland"]
# indents = [31, 26, 28, 31, 27, 28]
# for ind in range(len(datasets)):
#     fns = []
#     for fn in glob.glob("data/" + datasets[ind] + "/*converted.toc"):
#         fns.append(fn)
#     rs.evaluate_methods_real(methods, fns, datasets[ind], indents[ind], printing_wanted=False)

fns = []
for fn in glob.glob("netflix_nc/3*/*converted.soc"):
    fns.append(fn)
rs.evaluate_methods_real(methods, fns, "Netflix3_Unnormalized", 0, printing_wanted=False)

fns = []
for fn in glob.glob("netflix_nc/4*/*converted.soc"):
    fns.append(fn)
rs.evaluate_methods_real(methods, fns, "Netflix4_Unnormalized", 0, printing_wanted=False)