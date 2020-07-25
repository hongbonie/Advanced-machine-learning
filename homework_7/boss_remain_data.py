# -*- coding: UTF-8 -*-
import MySQLdb
import datetime
import logging
import time
import sys
import codecs
import urllib
import urllib2
import os
reload(sys)
sys.setdefaultencoding('utf-8')


# 注册成功用户数
def get_new_register_phone_list(cal_start_t,cal_end_t):
    new_register_phone_dic = {}
    db = MySQLdb.connect(host="kz_dbserver_user_dbs_3326", user="kz_bi", passwd="4u!JZ6IRYj@j",
                         db="user", port=3326, charset="utf8")
    cursor = db.cursor()
    sql = "SELECT a.account,a.add_time,a.user_id,b.channel  FROM login_info a,user_basic b  WHERE a.type=2 AND a.user_id=b.user_id AND b.channel>2 AND a.add_time " \
          "between '%s' and '%s' and LENGTH(0+a.account) = LENGTH(a.account);" % (cal_start_t,cal_end_t)
    print sql
    cursor.execute(sql)
    results = cursor.fetchall()
    db.close()
    for item in results:
        account = long(item[0])
        add_time = str(item[1])
        user_id = long(item[2])
        channel = long(item[3])
        if channel == 3:
            appid = 1001
        elif channel == 4:
            appid = 2001
        else:
            appid = 0
        new_register_phone_dic[account] = [add_time,user_id,appid]
    print "new_register_phone_dic count: ", len(new_register_phone_dic)
    return new_register_phone_dic

# 发送用户数据
def get_boss_phone_dict(cal_start_t,cal_end_t):
    db = MySQLdb.connect(host="kz_dbserver_user_dbs_3326", user="kz_bi", passwd="4u!JZ6IRYj@j",
                         db="user", port=3326, charset="utf8")
    cursor = db.cursor()
    sql = "SELECT  phone_number,update_time,boss_uid FROM boss_zhipin_push_log WHERE update_time between '%s' and '%s';" % (cal_start_t,cal_end_t)
    cursor.execute(sql)
    print sql
    results = cursor.fetchall()
    db.close()
    dct_boss_phones = {}
    # 发送数据
    for item in results:
        phone_number = long(item[0])
        update_time = str(item[1])
        boss_uid = long(item[2])
        dct_boss_phones[phone_number]= [update_time,boss_uid]
    print "dct_boss_phones count: ", len(dct_boss_phones)
    return dct_boss_phones

# 活跃数据
def get_user_active_dict(cal_start_t,cal_end_t,s_month,e_month):
    tb_name_1 = "kanzhun_app_action_" + str(s_month)
    tb_name_2 = "kanzhun_app_action_" + str(e_month)
    db = MySQLdb.connect(host="common_dbserver_bi_dbm_5029", user="kz_bi", passwd="4u!JZ6IRYj@j",
                         db="kz", port=5029, charset="utf8")
    cursor = db.cursor()
    sql = "SELECT DISTINCT uid,DATE_FORMAT(date_time,'%Y-%m-%d') date8,appid FROM " + tb_name_1 + " WHERE uid >0 AND date_time>= '"  + cal_start_t + "'"
    if e_month == s_month :
        sql += " and date_time <= '" + cal_end_t  + "';"
    else:
        sql += " union SELECT DISTINCT uid,DATE_FORMAT(date_time,'%Y-%m-%d') date8,appid FROM " + tb_name_2 + " WHERE uid >0 AND date_time <= '" + cal_end_t  + "';"
    print sql
    cursor.execute(sql)
    results = cursor.fetchall()
    db.close()
    dct_boss_active_uid = {}
    for item in results:
        uid = long(item[0])
        date8 = str(item[1])
        appid = long(item[2])
        key = str(uid) + "," + date8
        dct_boss_active_uid[key] = appid
    print "dct_boss_active_uid count: ", len(dct_boss_active_uid)
    return dct_boss_active_uid



def get_results():
    #发送数，前推一个月+2周
    now = datetime.datetime.now()  # 当前时间
    t_start_m = now + datetime.timedelta(-44)  # 开始日期
    t_end = now + datetime.timedelta(-1)  # 结束日期
    cal_end = t_end.strftime('%Y-%m-%d')  # 格式化时间输出
    cal_start_m = t_start_m.strftime('%Y-%m-%d')  # 格式化时间输出
    cal_end_t = str(cal_end) + " 23:59:59"
    cal_start_m = str(cal_start_m) + " 12:00:00"
    dct_boss_push_phone = get_boss_phone_dict(cal_start_m, cal_end_t)  # 推送
    print cal_start_m, cal_end_t

    #注册和活跃数，前推2周
    t_start = now + datetime.timedelta(-14)  # 开始日期
    s_month = t_start.strftime('%Y%m')
    e_month = t_end.strftime('%Y%m')
    cal_start = t_start.strftime('%Y-%m-%d')  # 格式化时间输出
    cal_start_t = str(cal_start) + " 00:00:00"
    print s_month, e_month, cal_start, cal_start_t
    # 查询数据
    dct_new_register_phone = get_new_register_phone_list(cal_start_t, cal_end_t)  # 注册
    dct_boss_active_uid = get_user_active_dict(cal_start_t, cal_end_t, s_month, e_month)  # 留存

    # 最近一周开始时间
    w_start = now + datetime.timedelta(-7)  # 开始日期
    w_start_s = w_start.strftime('%Y-%m-%d') + " 00:00:00"
    w_start_t = time.strptime(w_start_s, '%Y-%m-%d %H:%M:%S')
    w_time = time.mktime(w_start_t)
    print w_start_s,w_time

    # boss注册数据文件
    f_regit = open("/data/kz_bi/data_analysis/result/boss_regit_user.csv", 'w')
    f_regit.write(codecs.BOM_UTF8)
    r_line = "boss_uid,phone_number,regit_time\n"
    f_regit.write(r_line)
    # boss发送数据文件
    f_push = open("/data/kz_bi/data_analysis/result/boss_push_user.csv", 'w')
    f_push.write(codecs.BOM_UTF8)
    p_line = "boss_uid,phone_number,push_time\n"
    f_push.write(p_line)
    # 用户：注册时间
    dct_new_register_uid = {}
    # 日期+平台：注册数
    dct_register_day = {}
    for phone_number in dct_boss_push_phone:
        p_item = dct_boss_push_phone[phone_number]
        update_time = str(p_item[0])
        boss_uid = long(p_item[1])

        # 时间格式化
        utime = time.strptime(update_time, '%Y-%m-%d %H:%M:%S')
        s_utime = time.mktime(utime)
        # print "s_utime:",s_utime,w_time

        # 写发送文件
        if s_utime >= w_time:
            p_line = str(boss_uid) + "," + str(phone_number) + "," + update_time + "\n"
            f_push.write(p_line)
        #注册数据
        if phone_number in dct_new_register_phone:
            reg_item = dct_new_register_phone[phone_number]
            add_time = str(reg_item[0])
            user_id = long(reg_item[1])
            appid = long(reg_item[2])

            # 时间格式化
            atime = time.strptime(add_time, '%Y-%m-%d %H:%M:%S')
            s_atime = time.mktime(atime)
            ds = (s_atime - s_utime)/(24 * 60 * 60)
            if s_atime >= s_utime and ds <= 30 :
                # 写注册文件
                if s_atime >= w_time:
                    r_line = str(boss_uid) + "," + str(phone_number) + "," + add_time + "\n"
                    f_regit.write(r_line)
                # 用户注册时间
                dct_new_register_uid[user_id] = add_time
                add_time_10 = add_time[0:10]
                key = str(user_id) + "," + add_time_10
                dct_boss_active_uid[key] = appid
                # 每日分平台注册数
                day_channel = add_time_10 + "," + str(appid)
                if day_channel in dct_register_day:
                    ucount = dct_register_day[day_channel]
                    ucount += 1
                    dct_register_day[day_channel] = ucount
                else:
                    dct_register_day[day_channel] = 1
    reg_count = len(dct_new_register_uid)
    f_regit.close()
    f_push.close()
    print "dct_new_register_uid count: ", reg_count
    print "dct_register_day count: ", len(dct_register_day)

    #用户活跃天数
    dict_uid_remain_days = {}  # 用户 ：活跃天数
    dict_uid_remain_1 = {}  # 1日留存用户 ：注册时间 + 平台
    dict_uid_remain_3 = {}  # 3日留存用户  ：注册时间+ 平台
    dict_uid_remain_7 = {}  # 7日留存用户  ：注册时间+ 平台
    for key in dct_boss_active_uid:
        item = str(key).split(",")
        uid = long(item[0])
        date8 = str(item[1])
        appid = dct_boss_active_uid[key]
        #活跃时间
        act_time = time.strptime(date8, '%Y-%m-%d')
        date2 = datetime.datetime(act_time[0], act_time[1], act_time[2])
        if uid in dct_new_register_uid:
            # 注册时间
            add_time = dct_new_register_uid[uid]
            reg_time = time.strptime(add_time[0:10], '%Y-%m-%d')
            date1 = datetime.datetime(reg_time[0], reg_time[1], reg_time[2])
            days = (date2 - date1).days
            # 用户活跃天数
            if days < 8:
                if uid in dict_uid_remain_days:
                    day_count = dict_uid_remain_days[uid]
                    day_count += 1
                    dict_uid_remain_days[uid] = day_count
                else:
                    day_count = 1
                    dict_uid_remain_days[uid] = day_count
            # 1,3,7天留存
            day_channel = add_time[0:10] + "," + str(appid)
            if days == 1:
                dict_uid_remain_1[uid] = day_channel
            elif days == 3:
                dict_uid_remain_3[uid] = day_channel
            elif days == 7:
                dict_uid_remain_7[uid] = day_channel

    print "dict_uid_remain_1 count: ", len(dict_uid_remain_1)
    print "dict_uid_remain_3 count: ", len(dict_uid_remain_3)
    print "dict_uid_remain_7 count: ", len(dict_uid_remain_7)
    print "dict_uid_remain_days count: ", len(dict_uid_remain_days)

    dct_new_register_uid[user_id] = add_time
    dict_day_regit = {}  # 日期：注册用户数
    dict_day_count = {}  # 日期+活跃天数：注册用户数
    for uid in dct_new_register_uid:
        regtime = dct_new_register_uid[uid]
        regtime = regtime[0:10]
        #每日注册数
        if regtime in dict_day_regit:
            d_ucount = dict_day_regit[regtime]
            d_ucount += 1
        else:
            d_ucount = 1
        dict_day_regit[regtime] = d_ucount
        #每日用户活跃天数
        if uid in dict_uid_remain_days:
            day_count = dict_uid_remain_days[uid]
            if day_count >= 7:
                day_count = 7
            a_key = regtime + "," + str(day_count)
            if a_key in dict_day_count:
                a_ucount = dict_day_count[a_key]
                a_ucount += 1
            else:
                a_ucount = 1
            dict_day_count[a_key] = a_ucount
    print "dict_day_regit count: ", len(dict_day_regit)
    print "dict_day_count count: ", len(dict_day_count)

    # 活跃天数分布
    # 写文件:活跃天数计算结果
    # 活跃天数和留存数据结果
    fr = open("/data/kz_bi/data_analysis/result/boss_user_active_days.csv", 'w')
    fr.write(codecs.BOM_UTF8)
    line = "日期,注册用户数,1天,占比,2天,占比,3天,占比,4天,占比,5天,占比,6天,占比,7天,占比\n"
    fr.write(line.encode('utf-8'))
    # 排序
    sorted(dict_day_regit.keys())
    for regtime in dict_day_regit:
        d_ucount = dict_day_regit[regtime]
        line = regtime + "," + str(d_ucount) + ","
        for i in range(7):
            a_key = regtime + "," + str(i+1)
            a_ucount = 0
            if a_key in dict_day_count:
                a_ucount = dict_day_count[a_key]
            act_boss_rate = round((a_ucount / float(d_ucount)) * 100, 2)
            if i < 6:
                line  += str(a_ucount) + "," + str(act_boss_rate) +"%,"
            else:
                line += str(a_ucount) + "," + str(act_boss_rate) + "%\n"
        fr.write(line)

    # 次日留存
    line = "日期,平台,总注册用户数,1日留存,3日留存,7日留存\n"
    fr.write(line)
    dict_remain_day = {}# 日期+平台+留存天数 ：用户数
    for uid in dict_uid_remain_1:
        day_channel_1 = dict_uid_remain_1[uid]
        day_channel = day_channel_1 + "," + '1'
        if day_channel in dict_remain_day:
            ucount_1 = dict_remain_day[day_channel]
            ucount_1 += 1
            dict_remain_day[day_channel] = ucount_1
        else:
            dict_remain_day[day_channel] = 1
    print "dict_remain_day count: ", len(dict_remain_day)

    # 3日留存
    for uid in dict_uid_remain_3:# 日期+平台 ：用户数
        day_channel_3 = dict_uid_remain_3[uid]
        day_channel = day_channel_3 + "," + '3'
        if day_channel in dict_remain_day:
            ucount_3 = dict_remain_day[day_channel]
            ucount_3 += 1
            dict_remain_day[day_channel] = ucount_3
        else:
            dict_remain_day[day_channel] = 1
    print "dict_remain_day count: ", len(dict_remain_day)

    # 7日留存
    for uid in dict_uid_remain_7:
        day_channel_7 = dict_uid_remain_7[uid]
        day_channel = day_channel_7 + "," + '7'
        if day_channel in dict_remain_day:
            ucount_7 = dict_remain_day[day_channel]
            ucount_7 += 1
            dict_remain_day[day_channel] = ucount_7
        else:
            dict_remain_day[day_channel] = 1
    print "dict_remain_day count: ", len(dict_remain_day)

    # 计算1,3，7日留存
    days = ['1', '3', '7']
    #排序
    # dct_register_day = sorted(dct_register_day.iteritems(), key=lambda d: d[1], reverse=True)
    sorted(dct_register_day.keys())
    for t in dct_register_day:
        ucount = dct_register_day[t]
        if '1001' in t:
            l = t.replace('1001','Android')
        else:
            l = t.replace('2001', 'ios')
        line = str(l) + "," + str(ucount) +","
        for d in days:
            r_key = t + ',' + str(d)
            if r_key in dict_remain_day:
                rcount = dict_remain_day[r_key]
                if ucount > 0:
                    remain_rate = round((rcount / float(ucount)) * 100, 4)
                    line += str(remain_rate) +"%,"
        line += '\n'
        fr.write(line)


if __name__ == '__main__':
    get_results()
    print "结果计算完成！"
    os.system('curl -F "file=@/data/kz_bi/data_analysis/result/boss_user_active_days.csv" -F "user=mengjing" -F "media=mail" -F "subject=boss&dz" -F "message=boss&dz" "http://alarm.bosszhipin.com/mail/user/attach"')
    os.system('curl -F "file=@/data/kz_bi/data_analysis/result/boss_push_user.csv" -F "user=mengjing" -F "media=mail" -F "subject=boss&dz" -F "message=boss&dz" "http://alarm.bosszhipin.com/mail/user/attach"')
    os.system('curl -F "file=@/data/kz_bi/data_analysis/result/boss_regit_user.csv" -F "user=mengjing" -F "media=mail" -F "subject=boss&dz" -F "message=boss&dz" "http://alarm.bosszhipin.com/mail/user/attach"')
    print "文件发送成功！"
