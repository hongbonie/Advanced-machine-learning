# -*- coding: UTF-8 -*-
import MySQLdb
import sys
import time
reload(sys)
sys.setdefaultencoding('utf-8')

# 所有登录用户:第一次登陆时间
def get_app_user():
    dct_active_uid = {}
    for i in range(11):
        i += 1
        if i > 1:
            tb_name = "kanzhun_app_action_2017%02d" %(i)
            print tb_name
            # db = MySQLdb.connect(host="47.95.6.195", user="analysis", passwd="v@q$lOPJ4z",
            #                  db="kz", port=7029, charset="utf8")
            db = MySQLdb.connect(host="bi-01", user="kz_bi", passwd="4u!JZ6IRYj@j",
                                 db="kz", port=5029, charset="utf8")
            cursor = db.cursor()
            sql = "SELECT uid,MIN(`date_time`) `date_time` FROM %s WHERE uid > 0 GROUP BY uid;" % (tb_name)
            print sql
            cursor.execute(sql)
            results = cursor.fetchall()
            db.close()
            for item in results:
                uid = long(item[0])
                date10 = str(item[1])
                if uid not in dct_active_uid:
                    dct_active_uid[uid] = date10
    print "dct_active_uid count: ", len(dct_active_uid)
    return dct_active_uid

# 写过的面试
def get_interview_num():
    dct_interview_id = {}
    # db = MySQLdb.connect(host="47.95.6.195", user="analysis", passwd="v@q$lOPJ4z",
    #                      db="kanzhun", port=6006, charset="utf8")
    db = MySQLdb.connect(host="kz_dbserver_kanzhun_dbs_3316", user="kz_bi", passwd="4u!JZ6IRYj@j",
                         db="kanzhun", port=3316, charset="utf8")

    cursor = db.cursor()
    sql = "SELECT `user_id`,`id` FROM `company_interview` WHERE  `user_id`>0 AND `status`=1 "
    print sql
    cursor.execute(sql)
    results = cursor.fetchall()
    db.close()
    for item in results:
        uid = long(item[0])
        ugc_id = long(item[1])
        dct_interview_id[ugc_id] = uid
    print "dct_interview_id count: ", len(dct_interview_id)
    return dct_interview_id

# 写过的点评
def get_review_num():
    dct_review_id = {}
    # db = MySQLdb.connect(host="47.95.6.195", user="analysis", passwd="v@q$lOPJ4z",
    #                      db="kanzhun", port=6006, charset="utf8")
    db = MySQLdb.connect(host="kz_dbserver_kanzhun_dbs_3316", user="kz_bi", passwd="4u!JZ6IRYj@j",
                         db="kanzhun", port=3316, charset="utf8")
    cursor = db.cursor()
    sql = "SELECT `user_id`,`id` FROM `company_review` WHERE  `user_id`>0 AND `status`=1 "
    print sql
    cursor.execute(sql)
    results = cursor.fetchall()
    db.close()
    for item in results:
        uid = long(item[0])
        ugc_id = long(item[1])
        dct_review_id[ugc_id] = uid
    print "dct_review_id count: ", len(dct_review_id)
    return dct_review_id

#ugc被查看次数
def get_interview_view_num():
    dct_interview_view_num = {}
    for i in range(11):
        i += 1
        if i > 1:
            tb_name = "pv_2017%02d" %(i)
            print tb_name
            # db = MySQLdb.connect(host="47.95.6.195", user="analysis", passwd="v@q$lOPJ4z",
            #                  db="kz", port=7029, charset="utf8")
            db = MySQLdb.connect(host="bi-01", user="kz_bi", passwd="4u!JZ6IRYj@j",
                                 db="kz", port=5029, charset="utf8")
            cursor = db.cursor()
            sql = "SELECT pp,COUNT(DISTINCT cid) view_count FROM %s WHERE pk = 'detail-interview' and pp is not null GROUP BY pp" % (tb_name)
            print sql
            cursor.execute(sql)
            results = cursor.fetchall()
            db.close()
            for item in results:
                pp = long(item[0])
                view_count = long(item[1])
                if pp in dct_interview_view_num:
                    vcount = dct_interview_view_num[pp]
                    view_count += vcount
                    dct_interview_view_num[pp] = view_count
                else:
                    dct_interview_view_num[pp] = view_count
    print "dct_interview_view_num count: ", len(dct_interview_view_num)
    return dct_interview_view_num


#ugc被查看次数
def get_review_view_num():
    dct_review_view_num = {}
    for i in range(11):
        i += 1
        if i > 1:
            tb_name = "pv_2017%02d" %(i)
            print tb_name
            # db = MySQLdb.connect(host="47.95.6.195", user="analysis", passwd="v@q$lOPJ4z",
            #                  db="kz", port=7029, charset="utf8")
            db = MySQLdb.connect(host="bi-01", user="kz_bi", passwd="4u!JZ6IRYj@j",
                                 db="kz", port=5029, charset="utf8")
            cursor = db.cursor()
            sql = "SELECT pp,COUNT(DISTINCT cid) view_count FROM %s WHERE pk = 'detail-review' and pp is not null GROUP BY pp" % (tb_name)
            print sql
            cursor.execute(sql)
            results = cursor.fetchall()
            db.close()
            for item in results:
                pp = long(item[0])
                view_count = long(item[1])
                if pp in dct_review_view_num:
                    vcount = dct_review_view_num[pp]
                    view_count += vcount
                    dct_review_view_num[pp] = view_count
                else:
                    dct_review_view_num[pp] = view_count
    print "dct_review_view_num count: ", len(dct_review_view_num)
    return dct_review_view_num

def get_results():
    start = time.localtime(time.time())
    print "start time :", start
    #所有app用户第一次登录时间
    dct_login_uid = get_app_user()
    #写过的点评／面试被查看数（有，多条则累加）
    dct_interview_id = get_interview_num()
    dct_interview_view_num = get_interview_view_num()
    dct_review_id = get_review_num()
    dct_review_view_num = get_review_view_num()
    #总被查看次数
    dict_ugc_view_count = {}
    #面经
    for pp in dct_interview_id:
        uid = dct_interview_id[pp]
        v_count = 0
        if pp in dct_interview_view_num:
            v_count = dct_interview_view_num[pp]
        if uid in dict_ugc_view_count:
            l_count = dict_ugc_view_count[uid]
            v_count += l_count
            dict_ugc_view_count[uid] = v_count
        else:
            dict_ugc_view_count[uid] = v_count
    #点评
    for pp in dct_review_id:
        uid = dct_review_id[pp]
        v_count = 0
        if pp in dct_review_view_num:
            v_count = dct_review_view_num[pp]
        if uid in dict_ugc_view_count:
            l_count = dict_ugc_view_count[uid]
            v_count += l_count
            dict_ugc_view_count[uid] = v_count
        else:
            dict_ugc_view_count[uid] = v_count

    #存储数据
    list = []
    for uid in dct_login_uid:
        # print uid
        first_login_time = dct_login_uid[uid]
        view_num = 0
        if uid in dict_ugc_view_count:
            view_num = dict_ugc_view_count[uid]
        data = (uid,first_login_time,view_num)
        list.append(data)
    print "list count: ", len(list)
    #入库
    # db = MySQLdb.connect(host="192.168.1.38", user="kanzhun", passwd="kanzhun",
    #                      db="kanzhun", port=3306, charset="utf8")
    db = MySQLdb.connect(host="kzdb-01", user="kz_bi", passwd="4u!JZ6IRYj@j",
                         db="kanzhun", port=3306, charset="utf8")
    cursor = db.cursor()
    sql = "insert into user_thanks_data (user_id,first_login_time,ugc_view_count) values(%s,%s,%s)"
    cursor.executemany(sql, list)
    db.commit()
    db.close()

    end = time.localtime(time.time())
    print "end time :", end


if __name__ == '__main__':
    get_results()
    print "结果计算完成！"

