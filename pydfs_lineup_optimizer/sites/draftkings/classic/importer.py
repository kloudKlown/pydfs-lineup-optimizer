import re
import csv
from itertools import islice
from datetime import datetime
from pytz import timezone
from typing import Dict, Optional, Tuple
from pydfs_lineup_optimizer.exceptions import LineupOptimizerIncorrectCSV
from pydfs_lineup_optimizer.lineup_importer import CSVImporter
from pydfs_lineup_optimizer.player import Player, LineupPlayer, GameInfo
from pydfs_lineup_optimizer.lineup import Lineup
from pydfs_lineup_optimizer.tz import get_timezone


class DraftKingsCSVImporter(CSVImporter):  # pragma: nocover
    LINEUP_PLAYER_ID_REGEX = r'.+\((?P<id>\d+)\)'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._games = {}  # type: Dict[Tuple[Optional[str], Optional[str]], GameInfo]

    def _parse_game_info(self, row: Dict) -> Optional[GameInfo]:
        raw_game_info = ""
        if ("GameInfo" in row):
            raw_game_info = row.get("GameInfo")
        else:
            raw_game_info = row.get("Game Info")

        if 'In Progress' in raw_game_info or 'Final' in raw_game_info:
            return GameInfo(     # No game info provided, just mark game as started
                home_team='',
                away_team='',
                starts_at='',
                game_started=True)

        if not raw_game_info:
            return None
        try:
            teams, date, time, tz = raw_game_info.rsplit(' ', 3)
            away_team, home_team = teams.split('@')                        
            game_info = self._games.get((home_team, away_team))            
            if game_info:
                return game_info
            starts_at = datetime.strptime(date + time, '%m/%d/%Y%I:%M%p').\
                replace(tzinfo=timezone(get_timezone()))
            game_info = GameInfo(
                home_team=home_team,
                away_team=away_team,
                starts_at=starts_at,
            )
            self._games[(home_team, away_team)] = game_info
            return game_info
        except ValueError:
            return None

    def _row_to_player(self, row: Dict) -> Player:
        try:
            name = row['Name'].split()
            pos = ""
            if ("Roster Position" in row):
                pos = row['Roster Position']
            else:
                pos = row['Position']

            player = Player(
                row['ID'],
                name[0],
                name[1] if len(name) > 1 else '',
                pos.split('/'),
                row['TeamAbbrev'],
                float(row['Salary']),                
                float(row['AvgPointsPerGame']),
                actual = float(row['Actual']),
                game_info = self._parse_game_info(row),
                **self.get_player_extra(row)
            )
            # print(player, player.game_info.game_started)        
        except KeyError:
            raise LineupOptimizerIncorrectCSV
        return player

    def import_players_from_Json(self, lineupsJson: str):
        return [self._row_to_player(row) for row in lineupsJson]

    def import_players(self):
        self._games = {}
        with open(self.filename, 'r') as csv_file:
            start_line = 0  # Find line with 'TeamAbbrev', that's where players data starts
            while True:
                line = csv_file.readline()
                if 'TeamAbbrev' in line:
                    csv_file.seek(0)
                    csv_data = csv.DictReader(islice(csv_file, start_line, None),
                                              skipinitialspace=True)
                    return [self._row_to_player(row) for row in csv_data]
                elif line == '':
                    raise LineupOptimizerIncorrectCSV
                else:
                    start_line += 1

    def import_lineups(self, players):
        with open(self.filename, 'r') as csv_file:
            lines = csv.reader(csv_file)
            try:
                header = next(lines)
                start_column = 4  # First 4 columns has info about tournament
                end_column = header.index('Instructions') - 1
            except (IndexError, ValueError):
                raise LineupOptimizerIncorrectCSV
            position_names = header[start_column:end_column]            
            players_dict = {player.id: player for player in players}            
            lineups = []
            for line in lines:
                if not line[0]:
                    break
                lineup_players = []
                for index, position in zip(range(start_column, end_column), position_names):
                    try:
                        match = re.search(self.LINEUP_PLAYER_ID_REGEX, line[index])
                    except IndexError:
                        raise LineupOptimizerIncorrectCSV
                    if not match:
                        raise LineupOptimizerIncorrectCSV
                    player_id = match.group('id')
                    player_id = int(player_id)
                    # input(match)
                    try:
                        player = players_dict[player_id]
                    except KeyError:
                        raise LineupOptimizerIncorrectCSV('Player not found in players pool')                    
                    lineup_players.append(LineupPlayer(player, position))
                lineups.append(Lineup(lineup_players))
            return lineups
