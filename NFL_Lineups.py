from pydfs_lineup_optimizer import Site, Sport, get_optimizer, CSVLineupExporter

from pydfs_lineup_optimizer.stacks import TeamStack, PositionsStack

optimizer = get_optimizer(Site.DRAFTKINGS, Sport.FOOTBALL)
optimizer.load_players_from_csv("NFL.csv")
optimizer.set_min_salary_cap(49000)
#optimizer.add_stack(PositionsStack(['QB', ('WR', 'RB')]))
optimizer.add_stack(TeamStack(3, for_positions=['QB', 'WR' ]))  # stack 3 players with any of specified positions
lineup_generator = optimizer.optimize(20)
i = 1
for lineup in lineup_generator:
    print(lineup)
    print(i)
    i = i + 1
exporter = CSVLineupExporter(optimizer.optimize(20, max_exposure = 50))
exporter.export('resultNFL.csv', None, 'w')