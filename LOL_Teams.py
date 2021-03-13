from pydfs_lineup_optimizer import Site, Sport, get_optimizer, CSVLineupExporter
from pydfs_lineup_optimizer.context import OptimizationContext
from pydfs_lineup_optimizer import db_writer

FileName = "LOL.csv"
optimizer = get_optimizer(Site.DRAFTKINGS_CAPTAIN_MODE, Sport.LEAGUE_OF_LEGENDS)
optimizer.load_players_from_csv(FileName)
optimizer.set_min_salary_cap(48000)
optimizer.restrict_positions_for_opposing_team(["CPT", "TOP", "MID", "ADC", "JNG","SUP","TEAM"], ["CPT", "TOP", "ADC", "MID", "JNG","SUP","TEAM"])
optimizer.set_team_stacking([3, 3])
#optimizer.set_deviation(10, 25)
lineup_generator = optimizer.optimize(25)
i = 1
AllLineups = []
for lineup in lineup_generator:
    print(lineup)
    AllLineups.append(lineup)
    print(i)
    i = i + 1

exporter = CSVLineupExporter(optimizer.optimize(25))
#exporter.export('result_Lol.csv', None, 'w')
db_writer.PrintLineups(AllLineups, FileName)