from pydfs_lineup_optimizer import Site, Sport, get_optimizer, CSVLineupExporter
from pydfs_lineup_optimizer.context import OptimizationContext

FileName = "LOL.csv"
optimizer = get_optimizer(Site.DRAFTKINGS_CAPTAIN_MODE, Sport.LEAGUE_OF_LEGENDS)
optimizer.load_players_from_csv(FileName)
optimizer.set_min_salary_cap(45000)
#optimizer.restrict_positions_for_opposing_team(["CPT", "TOP", "MID", "ADC", "JNG","SUP","TEAM"], ["CPT", "TOP", "ADC", "MID", "JNG","SUP","TEAM"])
optimizer.set_team_stacking([3, 3])
optimizer.set_deviation(10, 25)
lineup_generator = optimizer.optimize(5)
i = 1
AllLineups = []
for lineup in lineup_generator:
    print(lineup)
    AllLineups.append(lineup)
    print(i)
    i = i + 1

exporter = CSVLineupExporter(optimizer.optimize(5))
exporter.export('result_Lol.csv', None, 'w')
# optimizer.optimize_lineups(AllLineups)
# players = [player for player in optimizer.players if player.max_exposure is None or player.max_exposure > 0]
# context = OptimizationContext(
#     total_lineups=len(AllLineups),
#     players=players,
#     existed_lineups=AllLineups,
# )
# optimizer.last_context = context
# optimizer.print_statistic()

# from pydfs_lineup_optimizer import Site, Sport, get_optimizer, CSVLineupExporter
# optimizer = get_optimizer(Site.DRAFTKINGS_CAPTAIN_MODE, Sport.LEAGUE_OF_LEGENDS)
# optimizer.load_players_from_csv("LOL.csv")
# optimizer.set_min_salary_cap(47000)
# #optimizer.restrict_positions_for_opposing_team(["CPT", "TOP", "MID", "ADC", "JNG","SUP","TEAM"], ["CPT", "TOP", "ADC", "MID", "JNG","SUP","TEAM"])
# optimizer.set_team_stacking([3, 3, 1])
# optimizer.set_deviation(15, 25)
# lineup_generator = optimizer.optimize(15)
# for lineup in lineup_generator:
#     print(lineup)
#     print(i)
#     i = i + 1

# exporter = CSVLineupExporter(optimizer.optimize(15))
# exporter.export('result_Lol.csv', None, 'a')