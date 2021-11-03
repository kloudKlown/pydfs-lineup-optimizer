from pydfs_lineup_optimizer import Site, Sport, get_optimizer, CSVLineupExporter
from pydfs_lineup_optimizer.context import OptimizationContext
from pydfs_lineup_optimizer import db_writer, PlayersGroup, Stack
from azure.cosmos import exceptions, CosmosClient, PartitionKey
import json 

FileName = "Golf.csv"
TotalCount = 25
i = 1
AllLineups = []


cosmosEndpoint = "https://cosmosdfq.documents.azure.com:443/"
cosmosKey = "CD8lN6OMKOsWA2FXnyDbkbsTgWBqPO7l8YCIyn8HkX8pOS44Hse7sBxdv0ugJCQwYlCeJ73j9E9ODd49wy5gEg=="
database_name = 'LineupSettings'
container_name = 'MLB'


client = CosmosClient(cosmosEndpoint, cosmosKey)
database = client.get_database_client(database=database_name)
container = database.get_container_client(container = container_name)


query = "SELECT * FROM c where c.GameDate = '2021-06-02T19:15:00' "
items = list(container.query_items(query = query, enable_cross_partition_query = True))

AllLineups = []
count = 0
def CreateLineups(lineupCount, stack):
    genCount = 0
    print(stack)
    optimizer = get_optimizer(Site.DRAFTKINGS, Sport.BASEBALL)
    optimizer.load_players_from_csv(FileName)
    optimizer.set_min_salary_cap(49500)
    optimizer.restrict_positions_for_opposing_team(["SP"], ["1B", "2B", "3B", "C", "SS", "OF"])
    optimizer.set_players_from_one_team(stack)
    lineup_generator = optimizer.optimize(lineupCount)

    for lineup in lineup_generator:
        if (lineup.fantasy_points_projection > 0):
            print(lineup)
            AllLineups.append(lineup)
            genCount = genCount + 1
    return genCount

def CreatePlayerStacks(lineupCount, stack):
    genCount = 0
    optimizer = get_optimizer(Site.DRAFTKINGS, Sport.BASEBALL)
    optimizer.load_players_from_csv(FileName)
    optimizer.set_min_salary_cap(49500)
    optimizer.restrict_positions_for_opposing_team(["SP", "P"], ["1B", "2B", "3B", "C", "SS", "OF"])

    playerGroup = PlayersGroup([optimizer.get_player_by_name(name) for name in stack], max_exposure=1)
    optimizer.add_stack(Stack([playerGroup]))
    lineup_generator = optimizer.optimize(lineupCount)

    for lineup in lineup_generator:
        if (lineup.fantasy_points_projection > 0):
            print(lineup)
            AllLineups.append(lineup)
            genCount = genCount + 1
    return genCount    

for i in items:
    print(i["TeamCriteria"])
    a = json.loads(i["TeamCriteria"])
    for criteria in a["TeamCriteria"]:
        stacks = {}     
        TL = int(criteria["Lineups"])
        for teamStack in criteria["TeamStack"]:
            stacks[teamStack["Team"]] = int(teamStack["Value"])
        print(stacks)       
        genCount = CreateLineups(TL, stacks)
        count = count + genCount
    print("Total Count By Teams", count)    
    input("Enter to continue") 

    a = json.loads(i["PlayerCriteria"])
    for criteria in a["PlayerCriteria"]:
        stacks = []
        TL = int(criteria["Lineups"])
        for teamStack in criteria["PlayerStack"]:
            stacks.append(teamStack["PlayerName"])
        print(stacks, TL)       
        genCount = CreatePlayerStacks(TL, stacks)
        count = count + genCount
    print("Total Count By Players", count)
    db_writer.PrintLineups(AllLineups, FileName)
    input("Enter to continue") 


### Default
optimizer = get_optimizer(Site.DRAFTKINGS, Sport.GOLF)
optimizer.load_players_from_csv(FileName)
optimizer.set_min_salary_cap(49500)
# optimizer.set_team_stacking([5])
# optimizer.restrict_positions_for_opposing_team(["P","SP"], ["1B", "2B", "3B", "C", "SS", "OF"])
tc = (TotalCount-count)
lineup_generator = optimizer.optimize(tc)
lineupScores = {}
for lineup in lineup_generator:    
    if (lineup.fantasy_points_projection > 0):
        print(lineup, lineup.fantasy_points_projection)         
        AllLineups.append(lineup)
        print(count)
        lineupScores[count] = lineup.actual
        count = count + 1        
print(lineupScores)

exporter = CSVLineupExporter(optimizer.optimize(tc))
exporter.export('result_GOLF.csv', None, 'w')
db_writer.PrintLineups(AllLineups, FileName)
