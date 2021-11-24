# -*- coding:utf-8 -*-
# @author : hailong@ecut.edu.com
# @Github : https://github.com/hailong-z
# @Time : 2021/3/23 1:42 下午
"""
赛马游戏基础版本V1.0.0
    完成基本的自动跑完功能
"""
import re
import string
from ..racingGame import settings
import random
import configparser

"""
🦄 🦌 🐗 🐭 🐴 🥇 🥈 🥉
"""

CONFIG_PATH_ = "NewGame.ini"


class NewGame:
    MIN: 2 = settings.MIN_STEP
    MAX: 5 = settings.MAX_STEP
    GUARD_BAR: 25 = settings.GUARD_BAR
    HORSE_DICT = settings.DICT

    def __init__(self, horse_num: str):
        self.horse_num = horse_num

    def InitialState(self, distance):
        return f"🏁{' ' * distance}{self.HORSE_DICT[self.horse_num][1]}"

    def run(self, distance: int) -> object:
        """
        distance -> reduce -> judge ->return
        :param distance:
        :return:
        """
        step = random.randint(self.MIN, self.MAX)

        distance -= step
        status = f"🏁{' ' * distance}{self.HORSE_DICT[self.horse_num][1]}"

        isChampion = NewGame.ifChampion(distance)
        result = [status + str(distance), isChampion, self.horse_num]
        return NewGame.record_game_process(result)

    @staticmethod
    def record_game_process(result: list) -> list:
        """
        记录每一次的游戏进度
        :param result:
        :return:
        """
        conf = configparser.ConfigParser()
        conf.read(CONFIG_PATH_)
        conf.set("GameRunningProcess", f"{result[2]}", f"{result[0]}")
        with open(CONFIG_PATH_, 'w') as f:
            conf.write(f)
        return result

    @staticmethod
    def ifChampion(distance):
        if distance <= 0:
            return True
        else:
            return False

    @staticmethod
    def champion(cps, msg, coins, unit):
        msgs = f'---------------------------------\n' \
               f'比赛结束\n{cps}' \
               f'---------------------------------\n' \
               f'最大赢家：\n' \
               f'{msg}' \
               f'---------------------------------\n' \
               f'本次获得{coins}{unit}\n' \
               f'---------------------------------\n'
        return msgs


class GameProcessControl:
    DICT = settings.DICT

    @staticmethod
    def clear_result_num(result: str) -> str:
        result = result.strip(string.digits)
        result = result.strip('-')
        return result

    @staticmethod
    def initial_state():
        conf = configparser.ConfigParser()
        conf.read(CONFIG_PATH_)
        item = conf.items("InitialState")
        guard_bar = settings.GUARD_BAR
        fence = settings.FENCE_NUM
        msg = f"{fence}\n" \
              f"{item[0][1]}\n" \
              f"{guard_bar}\n" \
              f"{item[1][1]}\n" \
              f"{guard_bar}\n" \
              f"{item[2][1]}\n" \
              f"{guard_bar}\n" \
              f"{item[3][1]}\n" \
              f"{guard_bar}\n" \
              f"{item[4][1]}\n" \
              f"{fence}\n"
        return msg

    def game_start(self, item):
        """
        start game
        :param item:
        :return:
        """
        conf = configparser.ConfigParser()
        conf.read(CONFIG_PATH_)

        text = conf.get("GameRunningProcess", item)
        distance = int(re.findall(r'\d+', text)[0])
        res = NewGame(horse_num=item)
        return res.run(distance=distance)

    @staticmethod
    def init_process():
        config = configparser.ConfigParser()
        config.add_section("InitialState")
        config.add_section("GameRunningProcess")
        dicts = settings.DICT
        distance = settings.TRACK_LENGTH

        for item in dicts.keys():
            new_game = NewGame(horse_num=item)
            init_state = new_game.InitialState(distance=distance)
            config.set('InitialState', item, init_state)
            config.set('GameRunningProcess', item, init_state + str(distance))
        config.set("Tools")
        with open(CONFIG_PATH_, 'w') as f:
            config.write(f)
        return True


if __name__ == '__main__':
    # res = GameProcessControl.initial_state()
    # print(res)

    DICT = settings.DICT
    for num in DICT.keys():
        # res = NewGame(horse_num=num)

        res = GameProcessControl().game_start(item=num)
        print(res)

    # GameProcessControl.init_process()
# print(res)
'''
初始状态.ini
    1.读取初始状态
    2.建立新状态
    3.新状态覆盖初始状态
    4.返回结果 

'''
