from pydfs_lineup_optimizer import Site, Sport, get_optimizer, CSVLineupExporter
from pydfs_lineup_optimizer.context import OptimizationContext
from pydfs_lineup_optimizer import db_writer, PlayersGroup, Stack, TeamStack
from azure.cosmos import exceptions, CosmosClient, PartitionKey
import json 

FileName = "MLB.csv"
TotalCount = 100
i = 1
AllLineups = []
optimizer = get_optimizer(Site.DRAFTKINGS, Sport.BASKETBALL)

cosmosEndpoint = "https://cosmosdfq.documents.azure.com:443/"
cosmosKey = "CD8lN6OMKOsWA2FXnyDbkbsTgWBqPO7l8YCIyn8HkX8pOS44Hse7sBxdv0ugJCQwYlCeJ73j9E9ODd49wy5gEg=="
database_name = 'LineupSettings'
container_name = 'NBA'

Lineups = 'Lineups'
Lineups_container = 'Lineups'

client = CosmosClient(cosmosEndpoint, cosmosKey)
database = client.get_database_client(database=database_name)
container = database.get_container_client(container = container_name)


Lineupsclient = CosmosClient(cosmosEndpoint, cosmosKey)
databaseLineups = Lineupsclient.get_database_client(database=Lineups)
containerLineupsContainer = databaseLineups.get_container_client(container = Lineups_container)

QueryDate = '2021-10-30T19:00:00'

query = "SELECT * FROM c where c.GameDate = '" + QueryDate + "'"
items = list(container.query_items(query = query, enable_cross_partition_query = True))

lineupQuery = "SELECT * FROM Lineups c where c.GameDate = '" + QueryDate + "'"
lineupList = list(containerLineupsContainer.query_items(query = lineupQuery, enable_cross_partition_query = True))
gameID = json.loads(lineupList[0]["Lineups"])[0]["GameID"]
optimizer.load_players_from_Json(json.loads(lineupList[0]["Lineups"]))


optimizer.set_min_salary_cap(49500)
optimizer.restrict_positions_for_opposing_team(["C"], ["C"])
lineupDictionary = {}

AllLineups = []
count = 0
def CreateLineups(lineupCount, stack):
    genCount = 0
    print(stack)

    for k, v in stack.items(): 
        optimizer.add_stack(TeamStack(v, [k], ["PG", "SG", "SF", "PF", "C"]))
    lineup_generator = optimizer.optimize(lineupCount)

    for lineup in lineup_generator:
        if (lineup.fantasy_points_projection > 0):
            playerIDs = [x.id for x in lineup.players]            
            playerIDs.sort()            
            playerIDs = ''.join(str(playerIDs))
            if playerIDs in lineupDictionary:
                continue

            print(lineup)
            lineupDictionary[playerIDs] = 1      
            AllLineups.append(lineup)
            genCount = genCount + 1
    optimizer.delete_players_from_one_team()
    return genCount

def CreatePlayerStacks(lineupCount, stack):
    genCount = 0
    optimizer = get_optimizer(Site.DRAFTKINGS, Sport.BASEBALL)
    optimizer.load_players_from_Json(json.loads(lineupList[0]["Lineups"]))
    # optimizer.load_players_from_csv(FileName)
    optimizer.set_min_salary_cap(49500)
    optimizer.restrict_positions_for_opposing_team(["C"], ["C"])

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
    db_writer.PrintLineups(AllLineups, gameID)
    input("Enter to continue") 


### Default
optimizer.set_min_salary_cap(49500)
optimizer.restrict_positions_for_opposing_team(["C"], ["C"])
optimizer.set_team_stacking([2, 2])
tc = (TotalCount-count)
lineup_generator = optimizer.optimize(tc)
lineupScores = {}
lineups = optimizer.load_lineups_from_csv("NBA_Late_Swap.csv")

input(lineups)
for lineup in lineup_generator:
    print(lineup.fantasy_points_projection)
    if (lineup.fantasy_points_projection > 0):        
        playerIDs = [x.id for x in lineup.players]            
        playerIDs.sort()
        playerIDs = ''.join(str(playerIDs))
        if playerIDs in lineupDictionary:
            continue
        lineupDictionary[playerIDs] = 1
        print(lineup)
        AllLineups.append(lineup)
        print(count)
        lineupScores[count] = lineup.actual
        count = count + 1
print(lineupScores)

exporter = CSVLineupExporter(optimizer.optimize(tc))
exporter.export('result_NBA.csv', None, 'w')
db_writer.PrintLineups(AllLineups, gameID)