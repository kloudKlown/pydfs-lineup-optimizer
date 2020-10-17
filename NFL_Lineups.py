from pydfs_lineup_optimizer import Site, Sport, get_optimizer, CSVLineupExporter
from pydfs_lineup_optimizer.stacks import TeamStack, PositionsStack, PlayersGroup, Stack
from pydfs_lineup_optimizer import db_writer
FileName = "NFL.csv"
optimizer = get_optimizer(Site.DRAFTKINGS, Sport.FOOTBALL)
optimizer.load_players_from_csv(FileName)
optimizer.set_min_salary_cap(48500)
#optimizer.add_stack(PositionsStack(['QB', 'WR']))
optimizer.restrict_positions_for_opposing_team(["QB", "WR", "RB", "TE"], ["DST"])
# brees_thomas_group = PlayersGroup([optimizer.get_player_by_name(name) for name in ('Matthew Stafford', 'Kenny Golladay')], max_exposure=0.5)
# optimizer.add_stack(Stack([brees_thomas_group]))
optimizer.set_team_stacking([3, 2, 1])
#optimizer.add_stack(TeamStack(3, for_positions=['QB', 'WR', 'WR']))  # stack 3 players with any of specified positions
lineup_generator = optimizer.optimize(50)
i = 1
AllLineups = []
for lineup in lineup_generator:
    print(lineup)
    AllLineups.append(lineup)
    print(i)
    i = i + 1

# exporter = CSVLineupExporter(optimizer.optimize(20, max_exposure = 50))
# exporter.export('resultNFL.csv', None, 'w')
# db_writer.PrintLineups(AllLineups, FileName)
