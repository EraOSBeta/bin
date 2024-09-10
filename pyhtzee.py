# Copyright (C) 2024  EraOS
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import random

UPPER_OPTIONS = {'aces': 1, 'twos': 2, 'threes': 3, 'fours': 4, 'fives': 5, 'sixes': 6}
UPPER_OPTIONS_REVERSE = {1: 'aces', 2: 'twos', 3: 'threes', 4: 'fours', 5: 'fives', 6: 'sixes'}
LOWER_OPTIONS = [
    'chance', 'three_of_a_kind', 'four_of_a_kind', 'full_house', 'small_straight', 'large_straight', 'yahtzee'
]


class Player:
    def __init__(self, name: str) -> None:
        self.name = name

        self.aces = None
        self.twos = None
        self.threes = None
        self.fours = None
        self.fives = None
        self.sixes = None
        self.chance = None
        self.three_of_a_kind = None
        self.four_of_a_kind = None
        self.full_house = None
        self.small_straight = None
        self.large_straight = None
        self.yahtzee = None

        self.upper_sum = 0
        self.upper_bonus = 0
        self.turn = 0

        self.rolls_left = 0
        self.dices = []
        self.selected_dices = []
        self.reset_turn_options()

    def reset_turn_options(self) -> None:
        self.rolls_left = 3
        self.dices = []
        self.selected_dices = [0, 1, 2, 3, 4]

    def count(self) -> dict:
        counting_dict = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}
        for dice in self.dices:
            counting_dict[dice] += 1
        return counting_dict


def print_scores(plist: list[Player]) -> None:
    for player in plist:
        total = 0
        score_str = f'{player.name} | '
        for attr in UPPER_OPTIONS.keys():
            score = getattr(player, attr)
            if score is not None:
                score_str += f'{score} {attr}, '
                total += score
            else:
                score_str += f'empty {attr}, '
        score_str += f'| {player.upper_sum} sum, {player.upper_bonus} bonus | '
        for attr in LOWER_OPTIONS:
            score = getattr(player, attr)
            if score is not None:
                score_str += f'{score} {attr}, '
                total += score
            else:
                score_str += f'empty {attr}, '
        score_str += f'| {total} total'
        print(score_str)
    print('\n')


def run() -> None:
    player_count = int(input('how many players do you want?'))
    players = []
    for i in range(player_count):
        players.append(Player(input(f'enter p{i + 1}\'s name: ')))
    while all(p.turn < 13 for p in players):
        for player in players:
            print_scores(players)
            print(f'{player.name}, it\'s your turn.')
            print(
                'recognized commands: aces, twos, threes, fours, fives, sixes, chance, three_of_a_kind, four_of_a_kind,'
                ' full_house, small_straight, large_straight, yahtzee, toggle_dice_1, toggle_dice_2, toggle_dice_3,'
                ' toggle_dice_4, toggle_dice_5, roll',
            )
            joker = None
            while True:
                command = input()
                if command == 'roll':
                    if joker:
                        print('you can\'t roll with a joker')
                    elif player.rolls_left == 0:
                        print('you don\'t have any rolls left')
                    elif len(player.selected_dices) == 0:
                        print('you don\'t have an active dice')
                    else:
                        player.rolls_left -= 1
                        if len(player.dices) == 0:
                            for _ in range(5):
                                player.dices.append(random.randint(1, 6))
                        else:
                            for i in player.selected_dices:
                                player.dices[i] = random.randint(1, 6)
                        print(
                            f'rolled the dice\ncurrent formation: {player.dices[0]}, {player.dices[1]},'
                            f' {player.dices[2]}, {player.dices[3]}, {player.dices[4]}',
                        )
                        first_dice = player.dices[0]
                        if all(dice == first_dice for dice in player.dices):
                            if player.yahtzee is not None:
                                joker = first_dice
                                print('you already have a yahtzee, this yahtzee will act as a joker')
                                if player.yahtzee > 0:
                                    player.yahtzee += 100
                                    print('non-zero yahtzee bonus added')
                elif len(player.dices) == 0:
                    print('you must roll first')
                elif getattr(player, command, None) is not None:
                    print(f'you have already filled out {command}')
                elif command in UPPER_OPTIONS.keys():
                    recommended_command = None
                    if joker:
                        recommended_command = UPPER_OPTIONS_REVERSE[joker]
                    if (
                        recommended_command
                        and command != recommended_command
                        and any(getattr(player, attr) is None for attr in LOWER_OPTIONS)
                    ):
                        print(
                            f'currently in the upper section, you can only use "{recommended_command}" with this joker'
                        )
                    else:
                        number = UPPER_OPTIONS[command]
                        score = 0
                        for dice in player.dices:
                            if dice == number:
                                score += number
                        setattr(player, command, score)
                        player.upper_sum += score
                        if player.upper_sum > 62:
                            player.upper_bonus = 35
                        break
                elif command in ['toggle_dice_1', 'toggle_dice_2', 'toggle_dice_3', 'toggle_dice_4', 'toggle_dice_5']:
                    dice_to_toggle = int(command[-1]) - 1
                    if dice_to_toggle in player.selected_dices:
                        player.selected_dices.remove(dice_to_toggle)
                        print(f'saved dice {dice_to_toggle + 1}')
                    else:
                        player.selected_dices.append(dice_to_toggle)
                        print(f'dice {dice_to_toggle + 1} will be used in the next roll')
                elif joker and getattr(player, UPPER_OPTIONS_REVERSE[joker]) is None:
                    print('the joker currently demands to be played in the upper section')
                elif command == 'chance':
                    player.chance = 0
                    for dice in player.dices:
                        player.chance += dice
                    break
                elif command == 'three_of_a_kind':
                    numbers = list(player.count().values())
                    player.three_of_a_kind = 0
                    if 3 in numbers or 4 in numbers or 5 in numbers:
                        for dice in player.dices:
                            player.three_of_a_kind += dice
                    break
                elif command == 'four_of_a_kind':
                    numbers = list(player.count().values())
                    player.four_of_a_kind = 0
                    if 4 in numbers or 5 in numbers:
                        for dice in player.dices:
                            player.four_of_a_kind += dice
                    break
                elif command == 'full_house':
                    numbers = list(player.count().values())
                    player.full_house = 0
                    if joker or (3 in numbers and 2 in numbers):
                        player.full_house = 25
                    break
                elif command == 'small_straight':
                    dices = list(player.dices)
                    for dice in [1, 2, 3, 4, 5, 6]:
                        while dices.count(dice) > 1:
                            dices.remove(dice)
                    dices.sort()
                    dices = str(dices)
                    player.small_straight = 0
                    if joker or '1, 2, 3, 4' in dices or '2, 3, 4, 5' in dices or '3, 4, 5, 6' in dices:
                        player.small_straight = 30
                    break
                elif command == 'large_straight':
                    dices = list(player.dices)
                    for dice in [1, 2, 3, 4, 5, 6]:
                        while dices.count(dice) > 1:
                            dices.remove(dice)
                    dices.sort()
                    dices = str(dices)
                    player.large_straight = 0
                    if joker or '1, 2, 3, 4, 5' in dices or '2, 3, 4, 5, 6' in dices:
                        player.large_straight = 40
                    break
                elif command == 'yahtzee':
                    numbers = list(player.count().values())
                    player.yahtzee = 0
                    if 5 in numbers:
                        player.yahtzee = 50
                    break
                else:
                    print('unknown command')
            print('end of turn\n\n')
            player.turn += 1
            player.reset_turn_options()
    print_scores(players)


print('https://en.wikipedia.org/wiki/Yahtzee')
run()
