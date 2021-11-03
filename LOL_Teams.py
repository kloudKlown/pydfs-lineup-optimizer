from pydfs_lineup_optimizer import Site, Sport, get_optimizer, CSVLineupExporter
from pydfs_lineup_optimizer.context import OptimizationContext
from pydfs_lineup_optimizer import db_writer
from azure.cosmos import exceptions, CosmosClient, PartitionKey
import json 
import TeamStack

FileName = "LOL.csv"
TotalLineupCount = 20
optimizer = get_optimizer(Site.DRAFTKINGS_CAPTAIN_MODE, Sport.LEAGUE_OF_LEGENDS)
optimizer.load_players_from_csv(FileName)
optimizer.restrict_positions_for_opposing_team(["CPT", "TOP", "MID", "ADC", "JNG","SUP","TEAM"], ["CPT", "TOP", "ADC", "MID", "JNG","SUP","TEAM"])
optimizer.set_min_salary_cap(48000)

cosmosEndpoint = "https://lineupsettings.documents.azure.com:443/"
cosmosKey = "OwqQtbjCrwj9pPqvWtCT8vSGZd5f5gfgM1mMRbhHBNZAVWqwafeO1Cg9fubp9LAsgxK8WxvhdHB1OzkA1ecfIA=="
database_name = 'LineupSettings'
container_name = 'LOL'


client = CosmosClient(cosmosEndpoint, cosmosKey)
database = client.get_database_client(database=database_name)
container = database.get_container_client(container = container_name)


query = "SELECT * FROM c where c.GameDate = '2021-03-18T04:00:00' "
items = list(container.query_items(query = query, enable_cross_partition_query = True))

AllLineups = []
count = 1
def CreateLineups(lineupCount, stack):
    genCount = 0
    print(stack)
    optimizer.set_players_from_one_team(stack)
    lineup_generator = optimizer.optimize(lineupCount)

    for lineup in lineup_generator:
        if (lineup.fantasy_points_projection > 0):        
            print(lineup)
            AllLineups.append(lineup)
            genCount = genCount + 1
    return genCount

for i in items:
    a = json.loads(i["TeamCriteria"])
    for criteria in a["TeamCriteria"]:
        stacks = {}
        Lcount = int(criteria["Lineups"])
        for teamStack in criteria["TeamStack"]:
            stacks[teamStack["Team"]] = int(teamStack["Value"])
        print(stacks)       
        genCount = CreateLineups(Lcount, stacks)
        count = count + genCount    
    print("Generated Lineups = ", count)
    input("") 

#optimizer.set_team_stacking([3, 3])
optimizer = get_optimizer(Site.DRAFTKINGS_CAPTAIN_MODE, Sport.LEAGUE_OF_LEGENDS)
optimizer.load_players_from_csv(FileName)
optimizer.restrict_positions_for_opposing_team(["CPT", "TOP", "MID", "ADC", "JNG","SUP","TEAM"], ["CPT", "TOP", "ADC", "MID", "JNG","SUP","TEAM"])
optimizer.set_min_salary_cap(48000)
lineup_generator = optimizer.optimize(TotalLineupCount-count)

for lineup in lineup_generator:
    print(lineup)
    AllLineups.append(lineup)
    print(count)
    count = count + 1

exporter = CSVLineupExporter(optimizer.optimize(25))
#exporter.export('result_Lol.csv', None, 'w')
db_writer.PrintLineups(AllLineups, FileName)