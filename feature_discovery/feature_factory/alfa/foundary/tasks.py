from celery import task
import MySQLdb as sql
from  models import Code
import time
from django.core.mail import send_mail
from string import Template

import hoover
handler = hoover.LogglyHttpHandler(token='74416ffd-70d4-4260-b065-a6ad3317eace')
import logging
log = logging.getLogger('MyApp')
log.addHandler(handler)
log.setLevel(logging.INFO)


@task()
def run_script(pk):
    s=Code.objects.get(pk=pk)

    email_message=Template('Feature factory submission result:\n\n$errors\n\nThe code: {0} \n\nThe idea: {1} \n\nThanks for participating.'.format(s.code, s.idea.idea))

    try:
        passwd = 'kalyan' 
        db = 'small_mock'  
        mockdb = sql.connect('mysql.csail.mit.edu','server',passwd,db)
        c = mockdb.cursor()
        start=time.clock()
        c.execute(s.code)
        sql_rows = c.fetchall()
        end=time.clock()
        c.close()
        mockdb.close()
        s.sub_result="Small mock done! It took {0} seconds. \n".format(str(int(end-start)))    

        try:
            passwd = 'kalyan' 
            db = 'large_mock'  
            mockdb = sql.connect('mysql.csail.mit.edu','server',passwd,db)
            c = mockdb.cursor()
            start=time.clock()
            c.execute(s.code)
            sql_rows = c.fetchall()
            end=time.clock()
            c.close()
            mockdb.close()
            s.sub_result="Large mock done! It took {0} seconds. \n".format(str(int(end-start)))
            s.elapsed=int(end-start)
            s.is_correct=True
            s.save()
            send_mail('Feature factory submission result: CORRECT', email_message.substitute(errors=s.sub_result), 'do_not_reply@moocdbfeaturediscovery.csail.mit.edu', [str(s.email)])

        except Exception, e:
            s.is_correct=False
            s.sub_result+="Error running large mock: " + str(e) + "\n"
            s.save()
            send_mail('Feature factory submission result: ERROR',  email_message.substitute(errors=s.sub_result) , 'do_not_reply@moocdbfeaturediscovery.csail.mit.edu', [str(s.email)])


    except Exception, e:
        s.is_correct=False
        s.sub_result="Error running small mock: " + str(e) + "\n"
        s.save()
        send_mail('Feature factory submission result: ERROR', email_message.substitute(errors=s.sub_result) , 'do_not_reply@moocdbfeaturediscovery.csail.mit.edu', [str(s.email)])

    return "done"