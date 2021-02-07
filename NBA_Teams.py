from pydfs_lineup_optimizer import Site, Sport, get_optimizer, CSVLineupExporter
from pydfs_lineup_optimizer.context import OptimizationContext
from pydfs_lineup_optimizer import db_writer

FileName = "NBA.csv"
optimizer = get_optimizer(Site.DRAFTKINGS, Sport.BASKETBALL)
optimizer.load_players_from_csv(FileName)
optimizer.set_min_salary_cap(49300)
#optimizer.restrict_positions_for_opposing_team(["PG", "SG", "PF", "SF", "C"], ["PG", "SG", "PF", "SF", "C"])
#optimizer.set_team_stacking([2])
lineup_generator = optimizer.optimize(50)
i = 1
AllLineups = []
for lineup in lineup_generator:
    print(lineup, lineup.fantasy_points_projection)    
    if (lineup.fantasy_points_projection > 0):
        AllLineups.append(lineup)
        print(i)
        i = i + 1

#exporter.export('result_NBA.csv', None, 'w')
exporter = CSVLineupExporter(optimizer.optimize(50))
#db_writer.PrintLineups(AllLineups, FileName)
