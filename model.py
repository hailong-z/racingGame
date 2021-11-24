# -*- coding:utf-8 -*-
# @author : hailong@ecut.edu.com
# @Github : https://github.com/hailong-z
# @Time : 2021/3/23 1:42 下午
import pymysql


class DB:
    def __init__(self):
        self.conn = pymysql.connect(
            host="localhost",
            user="root",
            password="Zhl199702",
            db="racingGame",
            charset="utf8"
        )

    def cur(self):
        return self.conn.cursor()

    def INSERT_DATA(self, SQL) -> str or Exception:
        """
        数据插入

        :param SQL: sql语句
        :return:
        """
        try:
            self.__init__()
            with self.conn.cursor() as cur:
                cur.execute(SQL)
                self.conn.commit()
                return True
        except Exception as e:
            self.conn.rollback()
            return False
        finally:
            self.conn.close()

    def UPDATA_DATA(self, SQL) -> str or Exception:
        """
        数据更新

        :param SQL: sql语句
        :return:
        """
        try:
            self.__init__()
            with self.conn.cursor() as cur:
                cur.execute(SQL)
                self.conn.commit()
                return True
        except Exception as e:
            self.conn.rollback()
            return False
        finally:
            self.conn.close()

    def SEARCH_DATA(self, SQL) -> tuple or Exception:
        """
        查找数据

        :param sql:
        :return:
        """
        try:
            self.__init__()
            with self.conn.cursor() as cur:
                cur.execute(SQL)
                data = cur.fetchall()
                return data
        except Exception as e:
            self.conn.rollback()
            return e
        finally:
            self.conn.close()

    def CONNECT(self):
        return self.__init__()
