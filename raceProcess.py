# -*- coding:utf-8 -*-
# @author : hailong@ecut.edu.com
# @Github : https://github.com/hailong-z
# @Time : 2021/3/23 2:37 下午

from .model import DB
from .source import NewGame


async def race_process(bot, lists, qqNum, SELF_ID, GROUP_ID, message, UNIT):
    try:
        if len(lists) > 1:
            db = DB()
            sql_sh = f"""select sum(coins )*2
                             from temp_coin
                             where id = {qqNum} and num in {tuple(lists)};"""

            data = db.SEARCH_DATA(sql_sh)[0][0]
            # 收益添加到数据库
            try:
                sql_up = f"""
                                 update assets
                                 set property = property +(
                                            select sum(coins )*2
                                            from temp_coin
                                            where id = {qqNum} and num in {tuple(lists)}
                                            )
                                 where userid={qqNum};
                              """
                db = DB()
                db.UPDATA_DATA(sql_up)
            except:
                await bot.call_api("send_msg", **{
                    "message": "排行榜添加失败",
                    "group_id": GROUP_ID
                })
        else:
            db = DB()
            sql_sh = f"""select sum(coins )*2
                             from temp_coin
                             where id = {qqNum} and num={lists[0]};"""

            data = db.SEARCH_DATA(sql_sh)[0][0]
            # 收益添加到数据库
            try:
                sql_up = f"""
                                 update assets
                                 set property = property +(
                                            select sum(coins )*2
                                            from temp_coin
                                            where id = {qqNum} and num={lists[0]}
                                            )
                                 where userid={qqNum};
                              """
                db = DB()
                db.UPDATA_DATA(sql_up)
            except:
                await bot.call_api("send_msg", **{
                    "message": "排行榜添加失败",
                    "group_id": GROUP_ID
                })
        # 玩家积分增加
        try:
            db = DB()
            sql_H_E = f"""update assets set hisEarning=hisEarning+{data} where userid={qqNum};"""
            db.UPDATA_DATA(sql_H_E)
        except:
            await bot.call_api("send_msg", **{
                "message": f"玩家{UNIT}结算失败",
                "group_id": GROUP_ID
            })
        # 庄家积分减少
        try:
            db = DB()
            sql_sh_bot = f"""UPDATE assets SET property = property-{data} where userid={SELF_ID};"""
            db.UPDATA_DATA(sql_sh_bot)
        except:
            await bot.call_api("send_msg", **{
                "message": f"庄家{UNIT}结算失败",
                "group_id": GROUP_ID
            })
        # 创建单次的赢家排行添加到临时表中
        try:
            sql_rank_id = f"insert into temp_ranking(id, ranking) values({qqNum}, {data}) "
            db = DB()
            db.INSERT_DATA(sql_rank_id)
        except:
            await bot.call_api("send_msg", **{
                "message": "排行榜榜添加失败",
                "group_id": GROUP_ID
            })
        try:
            db = DB()
            sql = "select id, ranking from temp_ranking where ranking=(select MAX(ranking) from temp_ranking);"
            qq = db.SEARCH_DATA(sql)
            msg = ''
            coins = qq[0][1]

            if len(qq) == 1:
                msg = f"\t[CQ:at,qq={qq[0][0]}]\n"

            else:
                for item in qq:
                    msg += f"\t[CQ:at,qq={item[0]}]\n"

            await bot.call_api("send_msg", **{
                "message": NewGame.champion(cps=message, msg=msg, coins=coins, unit=UNIT),
                "group_id": GROUP_ID
            })
        except:
            await bot.call_api("send_msg", **{
                "message": "获取排行失败。",
                "group_id": GROUP_ID
            })

    except:
        await bot.call_api("send_msg", **{
            "message": "数据查找失败",
            "group_id": GROUP_ID
        })
