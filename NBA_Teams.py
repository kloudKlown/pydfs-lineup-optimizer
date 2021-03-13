from pydfs_lineup_optimizer import Site, Sport, get_optimizer, CSVLineupExporter
from pydfs_lineup_optimizer.context import OptimizationContext
from pydfs_lineup_optimizer import db_writer

FileName = "NBA.csv"
count = 20
optimizer = get_optimizer(Site.DRAFTKINGS, Sport.BASKETBALL)
optimizer.load_players_from_csv(FileName)
optimizer.set_min_salary_cap(49000)
optimizer.set_team_stacking([2,2,2])
lineup_generator = optimizer.optimize(count)
i = 1
AllLineups = []
for lineup in lineup_generator:
    print(lineup, lineup.fantasy_points_projection)    
    if (lineup.fantasy_points_projection > 0):
        AllLineups.append(lineup)
        print(i)
        i = i + 1

exporter = CSVLineupExporter(optimizer.optimize(count))
exporter.export('result_NBA.csv', None, 'w')
db_writer.PrintLineups(AllLineups, FileName)
