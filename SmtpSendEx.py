#!/bin/env python
# -*- coding: utf-8 -*-

import smtplib
import threading
import re
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from time import sleep
import codecs

conf_list = {'ServerIP': '', 'DomainName': '', 'Password': '', 'UserName': '', 'FromListPath': None,
             'ToCount': '', 'MailContentPath': '', 'ToListPath': '', 'AttechmentPath': None,
             'Vuser': '', 'Duration': '', 'Iteration': '', 'IfSMTPAUTH': '1'}
line_re = re.compile(r'([\w]+)[\s]*=[\s]*([\S]+)')


def catch_conf(catch_file):
    for c in catch_file:
            tmp = line_re.search(c)
            if tmp is not None:
                res = tmp.groups()
                if res[0] in conf_list.keys():
                    conf_list[res[0]] = res[1].strip()


conf = codecs.open('run.conf', 'r', 'utf-8')
catch_conf(conf)

with open(conf_list['MailContentPath'], 'r') as bo:
    BODY = bo.read()

if conf_list['AttechmentPath'] is not None:
    with open(conf_list['AttechmentPath'], 'rb') as fi:
        FILE = fi.read()
else:
    FILE = None

if conf_list['ToListPath'] is not None:
    TO_LIST = []
    tolist = codecs.open(conf_list['ToListPath'], 'rU', 'utf-8')
    for to_line in tolist:
        TO_LIST.append(to_line.strip())

if conf_list['FromListPath'] is not None:
    FROM_LIST = []
    fromlist = codecs.open(conf_list['FromListPath'], 'rU', 'utf-8')
    for from_line in fromlist:
        FROM_LIST.append(from_line.strip())


class SMTPSendEX(threading.Thread):
    def __init__(self, smtp_ip, login_name, password, to_lsit, content_path, count=1):
        threading.Thread.__init__(self)
        self.server_ip = smtp_ip
        self.login_name = login_name
        self.password = password
        self.to_list = to_lsit
        self.body_path = content_path['body_path']
        self.attech_path = content_path['attech_path']
        self.count = count

    def login(self):
        server = smtplib.SMTP()
        try:
            server.connect(self.server_ip, 25)
            if conf_list['IfSMTPAUTH'] == '0':
                pass
            else:
                server.login(self.login_name, self.password)
        except Exception as e:
            print(e)
            print('%s LONGIN Fail' % self.login_name)
        return server

    def one_send_mail(self, smtp_server, body, attach):
        msg = MIMEMultipart()
        msg['From'] = self.login_name
        msg['To'] = ','.join(self.to_list)
        msg['Subject'] = 'pretest'
    #    msg['To'] = to_list
        con = MIMEText(body, 'plain', 'utf-8')
        msg.attach(con)
        if attach is not None:
            att = MIMEApplication(attach)
            att.add_header('Content-Disposition', 'attachment', filename=self.attech_path)
            # MIMEText( attech, 'base64', 'utf-8') att['']
            # att["Content-Type"] = 'application/octet-stream'
            # att["Content-Disposition"] = 'attachment; filename='+file_name
            msg.attach(att)
        try:
            for s_count in range(1, self.count+1):
                # msg['Subject'] = 'pretest_'+str(s_count)
                smtp_server.sendmail(msg['From'], self.to_list, msg.as_string())
                # print("mail_count=%d" % s_count)
                # time.sleep(0.01)
        except Exception as e:
            print(e)
            print('%s SEMD MAIL FAIL TO %s' % (self.login_name, msg['To']))

    # with the attech
    def run(self):
        se = SMTPSendEX.login(self)
        SMTPSendEX.one_send_mail(self, se, BODY, FILE)
        se.quit()


class Scranio:

    ITERATION = 0
    TIME_WAIT = 0

    def __init__(self, thread_count, think_time, iteration):
        self.thread_count = thread_count
        self.TIME_WAIT = think_time
        self.ITERATION = iteration

    def run(self, r_count):
        print('iteration:%d start......' % r_count)
        threads = []
        nloops = range(self.thread_count)
        list_rang = int(conf_list['ToCount'])
        paths = {}
        paths['body_path'] = conf_list['MailContentPath']
        paths['attech_path'] = conf_list['AttechmentPath']
        tmp_i = 0
        for i in nloops:
            lists = []
            # for j in range((i+1)*list_rang)[(i) * list_rang:]:
            if (tmp_i)*list_rang >= len(TO_LIST):
                tmp_i = 0
            for j in TO_LIST[(tmp_i)*list_rang:(tmp_i+1)*list_rang]:
                lists.append(str(j))
            # for j in TO_LIST[:list_rang]:
                # lists.append(conf_list['UserName']+str(j)+'@'+conf_list['DomainName'])
            # user = conf_list['UserName']+str(i)+'@'+conf_list['DomainName']
            if conf_list['FromListPath'] is not None:
                user = FROM_LIST[i]
            else:
                user = conf_list['UserName']
            t = SMTPSendEX(conf_list['ServerIP'], user, conf_list['Password'], lists, paths)
            # t.setDaemon(True)  # father out kill the children
            threads.append(t)
            tmp_i += 1

        for t in threads:
            t.start()

        for t in threads:
            t.join()    # father don't out until the children out

        print('iteration:%d end' % r_count)

    def start(self):
        for i in range(self.ITERATION):
            self.run(i+1)
            if i < self.ITERATION - 1:
                print('wait: %s min......' % self.TIME_WAIT)
                sleep(int(self.TIME_WAIT*60))


def main():
    print('---------------Vuser : %d--start------------' % int(conf_list['Vuser']))
    s = Scranio(int(conf_list['Vuser']), float(conf_list['Duration']), int(conf_list['Iteration']))
    s.start()
    print('---------------Vuser : %d--end-------------' % int(conf_list['Vuser']))


if __name__ == '__main__':
    main()



