from pydfs_lineup_optimizer import Site, Sport, get_optimizer, CSVLineupExporter
from pydfs_lineup_optimizer.stacks import TeamStack, PositionsStack, PlayersGroup, Stack
from pydfs_lineup_optimizer import db_writer

optimizer = get_optimizer(Site.DRAFTKINGS_CAPTAIN_MODE, Sport.CSGO)
FileName = "T2.csv"
optimizer.load_players_from_csv("T2.csv")
optimizer.set_min_salary_cap(47000)
optimizer.restrict_positions_for_opposing_team(["CPT", "FLEX"], ["CPT", "FLEX"])
optimizer.set_team_stacking([2, 2])
#optimizer.set_players_from_one_team({'AAT': 3, 'GY': 2})
optimizeLineups = 25
lineup_generator = optimizer.optimize(optimizeLineups)
i = 1
maxLinups = 20
AllLineups = []
for lineup in lineup_generator:
    print(lineup)
    AllLineups.append(lineup)
    print(i)
    i = i + 1
exporter = CSVLineupExporter(optimizer.optimize(optimizeLineups, max_exposure = 50))
exporter.export('result.csv', None, 'w')

db_writer.PrintLineups(AllLineups[0:maxLinups], FileName)

# optimizer = get_optimizer(Site.DRAFTKINGS_CAPTAIN_MODE, Sport.CSGO)
# optimizer.load_players_from_csv("T2.csv")
# optimizer.set_min_salary_cap(4800)
# optimizer.restrict_positions_for_opposing_team(["CPT", "FLEX"], ["CPT", "FLEX"])
# optimizer.set_team_stacking([3, 2, 1])
# #optimizer.set_players_from_one_team({'AAT': 3, 'GY': 2})
# lineup_generator = optimizer.optimize(15)
# for lineup in lineup_generator:
#     print(lineup)
#     print(i)
#     i = i + 1
# exporter = CSVLineupExporter(optimizer.optimize(15, max_exposure = 50))
# exporter.export('result.csv', None, 'a')

# optimizer = get_optimizer(Site.DRAFTKINGS_CAPTAIN_MODE, Sport.CSGO)
# optimizer.load_players_from_csv("T2.csv")
# optimizer.set_min_salary_cap(48000)
# optimizer.restrict_positions_for_opposing_team(["CPT"], ["FLEX"])
# optimizer.set_team_stacking([3, 2, 1])
# #optimizer.set_players_from_one_team({'AAT': 3, 'GY': 2})
# lineup_generator = optimizer.optimize(10)
# for lineup in lineup_generator:
#     print(lineup)
#     print(i)
#     i = i + 1
# exporter = CSVLineupExporter(optimizer.optimize(10, max_exposure = 50))
# exporter.export('result.csv', None, 'a')
