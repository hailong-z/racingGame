# -*- coding:utf-8 -*-
# @author : hailong@ecut.edu.com
# @Github : https://github.com/hailong-z
# @Time : 2021/3/23 1:42 下午
import configparser

from nonebot import require
from .source import NewGame, GameProcessControl as GPC, CONFIG_PATH_, settings

from nonebot import on_command, on_regex, on_message, permission, on_notice
from nonebot.adapters.cqhttp import Bot, GroupMessageEvent, Event, GroupIncreaseNoticeEvent, GroupDecreaseNoticeEvent
import nonebot
import re
from .model import DB
from .raceProcess import race_process

########################################################
# 赛马开关方便开发调试，先设置成默认开启
raceSwitches = True
isRacing = False
betPool = False
GROUP_ID = '838844825'
SELF_ID = '486319896'
UNIT = "银两"
########################################################


scheduler = require('nonebot_plugin_apscheduler').scheduler


@scheduler.scheduled_job("interval", seconds=5, id="2")
async def race():
    global isRacing, betPool
    bot = nonebot.get_bots().get('486319896')
    champions = []
    if raceSwitches and isRacing:
        dicts = settings.DICT
        for num in dicts.keys():
            result = GPC().game_start(item=num)
            if result[1]:
                champions.append(result[2])
            else:
                pass
        conf = configparser.ConfigParser()
        conf.read(CONFIG_PATH_)
        if len(champions) >= 1:
            isRacing = False

            await bot.call_api("send_msg",
                               message=f"{settings.FENCE_NUM}\n"
                                       f"{GPC.clear_result_num(conf.get('GameRunningProcess', 'horse_one'))}\n"
                                       f"{settings.GUARD_BAR}\n"
                                       f"{GPC.clear_result_num(conf.get('GameRunningProcess', 'horse_two'))}\n"
                                       f"{settings.GUARD_BAR}\n"
                                       f"{GPC.clear_result_num(conf.get('GameRunningProcess', 'horse_three'))}\n"
                                       f"{settings.GUARD_BAR}\n"
                                       f"{GPC.clear_result_num(conf.get('GameRunningProcess', 'horse_four'))}\n"
                                       f"{settings.GUARD_BAR}\n"
                                       f"{GPC.clear_result_num(conf.get('GameRunningProcess', 'horse_five'))}\n"
                                       f"{settings.FENCE_NUM}",
                               **{
                                   "group_id": GROUP_ID
                               })
            earningsDict = {}

            # 找到冠军个数对应的马牌
            horse_id = [re.findall("\d", dicts[mem][0])[0] for mem in champions]
            print(horse_id, champions)
            # 多个冠军
            if len(champions) > 1:
                message = ''
                for item in champions:
                    message += f'\t恭喜{dicts[item][0]}获得冠军🥇\n'
                await bot.call_api("send_msg", message=message,
                                   **{
                                       "group_id": GROUP_ID
                                   })

                # 马牌
                lists = []
                for i in range(len(horse_id)):
                    lists.append(horse_id[i][0])
                GPC.init_process()
                # 检查是否有人押注
                # if betPool:
                #     # 将收益存表中
                #
                #     try:
                #         db = DB()
                #         sql = f"""
                #                     select distinct id from temp_coin where num in {tuple(lists)};#[['2'], ['3'], ['4'], ['5']]
                #                 """
                #         res = db.SEARCH_DATA(sql)
                #         # 拿到id
                #         await bot.call_api("send_msg", **{
                #             "message": str(res),
                #             "group_id": GROUP_ID
                #         })
                #         message = ''  # 冠军马
                #         for item in champions:
                #             message += f'\t恭喜{DICT[item]}获得冠军🥇\n'
                #
                #         for qqNum in res:
                #             await race_process(bot=bot, qqNum=qqNum[0], lists=lists, SELF_ID=SELF_ID, GROUP_ID=GROUP_ID,
                #                                message=message, UNIT=UNIT)
                #
                #     except:
                #         await bot.call_api("send_msg", **{
                #             "message": "error",
                #             "group_id": GROUP_ID
                #         })
                #
                # else:
                #     await bot.call_api("send_msg", **{
                #         "message": "没有人押注",
                #         "group_id": GROUP_ID
                #     })

            else:
                message = f'\t恭喜{dicts[champions[0]][0]}获得冠军🥇'
                await bot.call_api("send_msg", message=message,
                                   **{
                                       "group_id": GROUP_ID
                                   })
                GPC.init_process()
            #
            #     if betPool:
            #         # 去重查找参加比赛的QQ号
            #         try:
            #             db = DB()
            #             sql = f"""select distinct id from temp_coin where num={hourse_id[0]};"""
            #             res = db.SEARCH_DATA(sql)[0]
            #             qqNum = res[0]
            #             message = f'\t恭喜{DICT[champions[0]]}获得冠军🥇\n'
            #             await race_process(bot=bot, qqNum=qqNum, lists=[hourse_id[0]], SELF_ID=SELF_ID,
            #                                GROUP_ID=GROUP_ID, message=message, UNIT=UNIT)
            #         except:
            #             await bot.call_api("send_msg", **{
            #                 "message": f"QQ号获取错误！",
            #                 "group_id": GROUP_ID
            #             })
            #
            #     else:
            #         await bot.call_api("send_msg", **{
            #             "message": f"没有人押注",
            #             "group_id": GROUP_ID
            #         })

            # 完成数据的初始化并且删掉缓库

            # initValues()
            # db = DB()
            # db.UPDATA_DATA("delete from temp_ranking;")
            # db = DB()
            # db.UPDATA_DATA("delete from temp_coin;")
            # betPool = False

        else:
            await bot.call_api("send_msg",
                               message=f"{settings.FENCE_NUM}\n"
                                       f"{GPC.clear_result_num(conf.get('GameRunningProcess', 'horse_one'))}\n"
                                       f"{settings.GUARD_BAR}\n"
                                       f"{GPC.clear_result_num(conf.get('GameRunningProcess', 'horse_two'))}\n"
                                       f"{settings.GUARD_BAR}\n"
                                       f"{GPC.clear_result_num(conf.get('GameRunningProcess', 'horse_three'))}\n"
                                       f"{settings.GUARD_BAR}\n"
                                       f"{GPC.clear_result_num(conf.get('GameRunningProcess', 'horse_four'))}\n"
                                       f"{settings.GUARD_BAR}\n"
                                       f"{GPC.clear_result_num(conf.get('GameRunningProcess', 'horse_five'))}\n"
                                       f"{settings.FENCE_NUM}",
                               **{
                                   "group_id": GROUP_ID
                               })


startGame = on_command(cmd="开始")


@startGame.handle()
async def start(bot: Bot, event: GroupMessageEvent):
    global raceSwitches, isRacing
    if str(event.group_id) == GROUP_ID:
        if raceSwitches and not isRacing:
            isRacing = True
            if isRacing:
                await bot.send(event=event,
                               message=f"所有的动物已经准备就绪，买定离手！")  #
        elif isRacing:
            await bot.send(event=event,
                           message="赛马正在进行中...")
        else:
            await bot.send(event=event,
                           message="赛马未开启，请管理输入开启赛马！")


switchesUserOn = on_command("开启")


@switchesUserOn.handle()
async def swithesOn(bot: Bot, event: GroupMessageEvent):
    if str(event.group_id) == GROUP_ID:
        global raceSwitches, isRacing
        if isRacing:
            await switchesUserOn.finish("游戏进行中")
        else:
            raceSwitches = True
            if raceSwitches:
                await switchesUserOn.finish("赛马已开启！")


switchesUserOff = on_command("关闭")


@switchesUserOff.handle()
async def swithesOff(bot: Bot, event: GroupMessageEvent):
    if str(event.group_id) == GROUP_ID:
        global raceSwitches, isRacing
        raceSwitches = False
        isRacing = False
        await switchesUserOff.finish("赛马已关闭！")


# getCoin = on_message()


# @getCoin.handle()
# async def putCoins(bot: Bot, event: GroupMessageEvent):
#     global betPool
#     if str(event.group_id) == GROUP_ID:
#         messages = event.message
#         user_id = event.user_id
#         if re.match("押\d号\d+", str(messages)):
#             result = re.findall(r"\d+", str(messages))
#             horse_Num = result[0]
#             if int(horse_Num) in range(1, 6):
#                 coinsPut = int(result[1])
#                 database = DB()
#                 # 插入临时表
#                 sql = f"INSERT INTO temp_coin(id, num, coins) values({user_id}, {hourseNum}, {coinsPut});"
#                 if database.INSERT_DATA(sql):
#                     # 从本金中减去押金
#                     database.CONNECT()
#                     # 查询当前余额
#                     sql = f"select property from assets where userid ={user_id};"
#                     cash = int(database.SEARCH_DATA(sql)[0][0])
#                     if cash > 0:
#                         if cash - coinsPut > 0:
#                             sql = f"update assets SET property = property-{coinsPut} where userid = {user_id};"
#                             sql_robot = f"update assets SET property = property+{coinsPut} where userid ={SELF_ID};"
#                             if database.UPDATA_DATA(sql):
#                                 db = DB()
#                                 db.UPDATA_DATA(sql_robot)
#                                 betPool = True
#                                 await getCoin.finish(message=str(f"押{hourseNum}号，金额:{coinsPut}{UNIT}，成功押注！"),
#                                                      **{"at_sender": True})
#                             else:
#                                 await getCoin.finish(message="押注失败啊！", **{"at_sender": True})
#                         else:
#                             await bot.send(event=event, message=f"{UNIT}不够，你这点{UNIT}，怎么够玩啊？", **{"at_sender": True})
#                     else:
#                         await bot.send(event=event, message=f"没{UNIT}啦，去讨点{UNIT}再来玩吧！", **{"at_sender": True})
#                 else:
#                     await bot.send(event=event, message="下注失败！", **{"at_sender": True})
#
#
# initCoins = on_command("#@初始化", permission=permission.SUPERUSER)
#
#
# @initCoins.handle()
# async def initCoins(bot: Bot, event: GroupMessageEvent):
#     if str(event.group_id) == GROUP_ID:
#         res = await bot.call_api("get_group_member_list", **{
#             "group_id": GROUP_ID
#         })
#         # await bot.send(event=event, message=str(res))
#         # 清理所有表格
#         db = DB()
#         db.UPDATA_DATA("delete from assets;")
#         db = DB()
#         db.UPDATA_DATA("delete from temp_coin;")
#         # 分配资产
#         db = DB()
#         db.UPDATA_DATA(f"insert into assets(userid, property) values({SELF_ID}, 1000000000);")
#         for user in res:
#             if str(user['user_id']) != SELF_ID:
#                 # await bot.send(event=event, message=str(user['user_id'])+str(type(user['user_id'])))
#                 # 用户加钱
#                 db = DB()
#                 db.INSERT_DATA(f"insert into assets(userid, property) values({str(user['user_id'])}, 100000);")
#                 # 庄家减钱
#                 db = DB()
#                 db.UPDATA_DATA(f"update assets set property = property-100000 where userid={SELF_ID};")
#         await bot.send(event=event, message="初始化完成！")
#
#
# assets = on_command("资产")
#
#
# @assets.handle()
# async def assetss(bot: Bot, event: GroupMessageEvent):
#     if str(event.group_id) == GROUP_ID:
#         userID = event.user_id
#         db = DB()
#         sql = f"select property from assets where userid ={str(userID)};"
#         res = db.SEARCH_DATA(sql)
#         await bot.send(event=event, message="总资产：" + str(res[0][0]) + f"{UNIT}", **{"at_sender": True})
#
#
# memberInNotice = on_notice()
#
#
# @memberInNotice.handle()
# async def memberInNotices(bot: Bot, event: GroupIncreaseNoticeEvent):
#     if str(event.group_id) == GROUP_ID:
#         usersList = await bot.call_api("get_group_member_list", **{
#             "group_id": GROUP_ID
#         })
#         user_id = event.user_id
#
#         # 用户加钱
#         db = DB()
#         db.INSERT_DATA(f"insert into assets(userid, property) values({str(user_id)}, 100000);")
#         # 庄家减钱
#         db = DB()
#         sql = f"update assets set property = property-100000 where userid={SELF_ID}"
#         if db.UPDATA_DATA(sql):
#             await bot.send(event=event, message=f"欢迎进群，您的编号{10000 + len(usersList)}，已为您自动充值100000{UNIT}，回复资产即可查询！",
#                            **{
#                                "at_sender": True
#                            }
#                            )
#         else:
#             await bot.send(event=event, message=f"欢迎进群，您的编号{10000 + len(usersList)}，自动充值失败，请联系管理员，回复资产即可查询当前资产！",
#                            **{
#                                "at_sender": True
#                            }
#                            )
#
#
# memberDeNotice = on_notice()
#
#
# @memberDeNotice.handle()
# async def memberDeNotices(bot: Bot, event: GroupDecreaseNoticeEvent):
#     if str(event.group_id) == GROUP_ID:
#         deUserId = event.user_id
#         userInfo = event.dict()
#         # 没收退群资产
#         db = DB()
#         sql = f" update assets set property = property+(select property from(select * from  assets where userid={deUserId})as a) where userid = {SELF_ID};"
#         db.UPDATA_DATA(sql)
#
#         # 删除退群人的资产账户
#         db = DB()
#         sql = f"delete from assets where userid= {deUserId}"
#         if db.UPDATA_DATA(sql):
#             await bot.send(event=event, message=f"{str(deUserId)}退出了赛马场，资产已收回。")
#         else:
#             await bot.send(event=event, message=f"{str(deUserId)}退出了赛马场，资产尚未收回。")
#
#
# checkBet = on_command("检查")
#
#
# @checkBet.handle()
# async def checkPets(bot: Bot, event: GroupMessageEvent):
#     db = DB()
#     lists = ['1', '2', '3', '4', '5']
#     sql = f"""
#                 select distinct id from temp_coin where num in {tuple(lists)};#[['2'], ['3'], ['4'], ['5']]
#             """
#     res = db.SEARCH_DATA(sql)
#     await checkBet.finish(str(res))
#
#
# assetsCheck = on_command("全部")
#
#
# @assetsCheck.handle()
# async def assets(bot: Bot, event: GroupMessageEvent):
#     db = DB()
#     sql = "select *from assets;"
#     res = db.SEARCH_DATA(sql)
#     await bot.call_api("send_msg", **{
#         "message": str(res),
#         "group_id": GROUP_ID
#     }
#                        )
