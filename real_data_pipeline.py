import rivest_shen as rs
import glob


# generate list of netflix files
# fns = []
# for fn in glob.glob("**/*converted.soc"):
#     fns.append(fn)

# generate list of converted sf files
fns = []
for fn in glob.glob("SFData/RivestShen/*.toc"):
    fns.append(fn)

#print(fns)

methods = [("Borda", rs.Borda_winner), ("plurality", rs.plurality_winner), ("gt", rs.gt_winner), \
    ("minimax", rs.minimax_winner), ("gtd", rs.gtd_winner), \
    ("Schulze", rs.Schulze_winner), ("IRV", rs.IRV_winner)]

rs.evaluate_methods_real(methods, fns, "sf", printing_wanted=False)
#print(rs.extract_alts("SFData/RivestShen/ED-00021-00000001-converted.toc"))
#print(rs.extract_profile("SFData/RivestShen/ED-00021-00000001-converted.toc"))