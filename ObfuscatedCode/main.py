#!/usr/bin/env python
import os
import codecs
import time
import shutil
import string
import json
import sqlite3
import itchat
from random import Random
from itchat .content import *
ROOTPATH ="./"
LOGPATH ="./log/"
FILEPATH ="./dlfile/"
create_time =""
group_id =""
group_one_id =""
chat_text ="NULL"
group_chat_text ="NULL"
file_type ="TEXT"
file_name ="NULL"
file_dst ="NULL"
kw_type ="NULL"
kw_word ="NULL"
boss =""
gchat_count =0
gchat_kw_count =0
@itchat .msg_register ([TEXT ,MAP ,CARD ,NOTE ,SHARING ,PICTURE ,RECORDING ,ATTACHMENT ,VIDEO ])
def one_chat (O0OO0OOO00OOO0000 ):
    ""
    if O0OO0OOO00OOO0000 ['FromUserName']==O0OO0OOO00OOO0000 ['User']['UserName']:
        O00OO0OOO00OO0O00 =O0OO0OOO00OOO0000 ['User']['NickName']
    else :
        O00OO0OOO00OO0O00 ="本机器人"
    O00000OO0O0O000OO =O0OO0OOO00OOO0000 ['FileName']
    O00OO0O00O0O0O0OO =O0OO0OOO00OOO0000 ['Type']
    O0O00OOO00OOO0OO0 =O0OO0OOO00OOO0000 ['Text']
    if type (O0O00OOO00OOO0OO0 )==type ('string'):
        O0O00OOO00OOO0OO0 =O0O00OOO00OOO0OO0 .replace ('\r','\\r').replace ('\n','\\n')
    else :
        O0O00OOO00OOO0OO0 ="CARD"
    OO0OO0O00OOOO0OO0 =time .strftime ("%Y-%m-%d %H:%M:%S",time .localtime (O0OO0OOO00OOO0000 ['CreateTime']))
    if O00000OO0O0O000OO :
        O0O00OOO00OOO0OO0 ="NULL"
        OOO00OO00O0OOO00O =create_today_folder ()
        try :
            O0OO0OOO00OOO0000 .download (O00000OO0O0O000OO )
            O000OO0O000000O0O =os .path .join (ROOTPATH ,O0OO0OOO00OOO0000 ['FileName'])
            O00O00O00O0000OO0 =random_str (O00OO0OOO00OO0O00 )+'#'+O0OO0OOO00OOO0000 ['FileName']
            OO0O0OO00O000O0OO =OOO00OO00O0OOO00O +O00O00O00O0000OO0
            shutil .move (O000OO0O000000O0O ,OO0O0OO00O000O0OO )
            OO0O00O0O000O0O0O =OO0OO0O00OOOO0OO0 +" dlfile# "+O00OO0OOO00OO0O00 +" "+O00O00O00O0000OO0
            OO0O00O0O000O0O0O =json .dumps (OO0O00O0O000O0O0O ,ensure_ascii =False )
            write_log_one (OO0O00O0O000O0O0O +"\n")
            print (OO0O00O0O000O0O0O )
        except Exception as O0000O0OOO000OO0O :
            print (O0000O0OOO000OO0O )
    else :
        O0O00OOO00OOO0OO0 =O0O00OOO00OOO0OO0 .replace ('\r','\\r').replace ('\n','\\n')
        OO0O00O0O000O0O0O =OO0OO0O00OOOO0OO0 +" one_chat# "+O00OO0OOO00OO0O00 +" : "+O0O00OOO00OOO0OO0
        write_log_one (OO0O00O0O000O0O0O +"\n")
        print (OO0O00O0O000O0O0O )
    O0O000O00OO00O00O ="Default Reply."
    OO0OOO0O00OOO0OO0 ="请不要尝试挑逗机器人，您的言行将被记录."
    return OO0OOO0O00OOO0OO0 or O0O000O00OO00O00O
@itchat .msg_register ([TEXT ,MAP ,NOTE ,SHARING ],isGroupChat =True )
def group_chat (OO0OO00OO00OOO000 ):
    ""
    global gchat_count ,gchat_kw_count
    OO0O00OO00000OOO0 =time .strftime ("%Y-%m-%d %H:%M:%S",time .localtime (OO0OO00OO00OOO000 ['CreateTime']))
    try :
        OO00000OO000O0O0O =OO0OO00OO00OOO000 .user ['NickName']
    except KeyError as O00OOOO0OO00OO0O0 :
        OO00000OO000O0O0O ="本机器人的群组"
        print (O00OOOO0OO00OO0O0 )
    gchat_count +=1
    O0O0O000O00OO0OO0 =OO0OO00OO00OOO000 ['ActualNickName']
    if OO0OO00OO00OOO000 ['Type']=="Map":
        O0OO0OO00OOO0O00O =OO0OO00OO00OOO000 ['Content'].split (':',1 )[0 ]
    else :
        O0OO0OO00OOO0O00O =OO0OO00OO00OOO000 ['Text'].replace ('\r','\\r').replace ('\n','\\n')
    O0O0O000O00OOOO0O =demo (O0OO0OO00OOO0O00O )
    if not O0O0O000O00OOOO0O :
        O0OOOO0OOO000OOO0 ="NULL"
        O0O00O0OOOO0OOOOO ="NULL"
    else :
        O0OOOO0OOO000OOO0 =O0O0O000O00OOOO0O [2 ]
        O0O00O0OOOO0OOOOO =O0OO0OO00OOO0O00O [O0O0O000O00OOOO0O [0 ]:O0O0O000O00OOOO0O [1 ]]
        gchat_kw_count +=1
        # kw_send (O0OO0OO00OOO0O00O ,OO00000OO000O0O0O ,O0O0O000O00OO0OO0 ,boss )
    if O0O0O000O00OO0OO0 :
        O0OO00OO000O00000 =dict (gchat_count =gchat_count ,create_time =OO0O00OO00000OOO0 ,group_id =OO00000OO000O0O0O ,group_one_id =O0O0O000O00OO0OO0 ,group_chat_text =O0OO0OO00OOO0O00O ,file_type =file_type ,file_name =file_name ,file_dst =file_dst ,kw_word =O0O00O0OOOO0OOOOO ,kw_type =O0OOOO0OOO000OOO0 ,gchat_kw_count =gchat_kw_count )
    else :
        O0OO00OO000O00000 =dict (gchat_count =gchat_count ,create_time =OO0O00OO00000OOO0 ,group_id ="本机器人",group_one_id =O0O0O000O00OO0OO0 ,group_chat_text =O0OO0OO00OOO0O00O ,file_type =file_type ,file_name =file_name ,file_dst =file_dst ,kw_word =O0O00O0OOOO0OOOOO ,kw_type =O0OOOO0OOO000OOO0 ,gchat_kw_count =gchat_kw_count )
    O0OO00OO000O00000 =json .dumps (O0OO00OO000O00000 ,ensure_ascii =False )
    write_log_group (O0OO00OO000O00000 +"\n")
    print (O0OO00OO000O00000 )
    try :
        OO0OO0OO00OO00O0O =init ()
        insert_gchat (OO0OO0OO00OO00O0O ,OO0O00OO00000OOO0 ,OO00000OO000O0O0O ,O0O0O000O00OO0OO0 ,O0OO0OO00OOO0O00O ,file_type ,file_name ,file_dst ,O0O00O0OOOO0OOOOO ,O0OOOO0OOO000OOO0 )
        update_var (OO0OO0OO00OO00O0O ,gchat_count ,gchat_kw_count )
        finish (OO0OO0OO00OO00O0O )
    except Exception as O00OOOO0OO00OO0O0 :
        print (O00OOOO0OO00OO0O0 )
@itchat .msg_register ([PICTURE ,RECORDING ,ATTACHMENT ,VIDEO ,CARD ],isGroupChat =True )
def group_download_files (OOOO0O00OOO0OOO00 ):
    ""
    global gchat_count ,gchat_kw_count
    O0O00O00OOO0OO000 =create_today_folder ()
    if not OOOO0O00OOO0OOO00 .actualNickName :
        OOOOO000OO00O0O00 ="本机器人"
    else :
        OOOOO000OO00O0O00 =OOOO0O00OOO0OOO00 ['ActualNickName']
    OOOOO000O0000OO0O =OOOO0O00OOO0OOO00 .user ['NickName']
    OO000OO00000OOOO0 =OOOO0O00OOO0OOO00 ['Type']
    OOOOO000O0O000OO0 =time .strftime ("%Y-%m-%d %H:%M:%S",time .localtime (OOOO0O00OOO0OOO00 ['CreateTime']))
    OOO0O00OOO00O000O ={PICTURE :'图片',RECORDING :'语音',ATTACHMENT :'附件',VIDEO :'视频',CARD :'名片',}.get (OOOO0O00OOO0OOO00 ['Type'],'未知内容')
    gchat_count +=1
    try :
        if OO000OO00000OOOO0 =="Card":
            O0O0OOO0OOOOOO00O =OOOO0O00OOO0OOO00 ['Text']['NickName']
            O0O0OO0OO00O0OO00 =random_str (OOOOO000OO00O0O00 )+'#'+O0O0OOO0OOOOOO00O
            OOOO0O0O0O0O0O0OO =O0O00O00OOO0OO000 +O0O0OO0OO00O0OO00
            O0OO00OO0O00OOOO0 =open (OOOO0O0O0O0O0O0OO ,'w')
            O0OO00OO0O00OOOO0 .write (str (OOOO0O00OOO0OOO00 ['Text']))
            O0OO00OO0O00OOOO0 .close ()
        else :
            O0O0OOO0OOOOOO00O =OOOO0O00OOO0OOO00 ['FileName']
            OOOO0O00OOO0OOO00 .download (O0O0OOO0OOOOOO00O )
            O0OOO00O0000O0OOO =os .path .join (ROOTPATH ,O0O0OOO0OOOOOO00O )
            O0O0OO0OO00O0OO00 =random_str (OOOOO000OO00O0O00 )+'#'+O0O0OOO0OOOOOO00O
            OOOO0O0O0O0O0O0OO =O0O00O00OOO0OO000 +O0O0OO0OO00O0OO00
            shutil .move (O0OOO00O0000O0OOO ,OOOO0O0O0O0O0O0OO )
        OOO00000OOO0OO00O =dict (gchat_count =gchat_count ,create_time =OOOOO000O0O000OO0 ,group_id =OOOOO000O0000OO0O ,group_one_id =OOOOO000OO00O0O00 ,group_chat_text =group_chat_text ,file_type =OO000OO00000OOOO0 ,file_name =O0O0OOO0OOOOOO00O ,file_dst =OOOO0O0O0O0O0O0OO ,kw_word =kw_word ,kw_type =kw_type ,gchat_kw_count =gchat_kw_count )
        OOO00000OOO0OO00O =json .dumps (OOO00000OOO0OO00O ,ensure_ascii =False )
        write_log_group (OOO00000OOO0OO00O +"\n")
        print (OOO00000OOO0OO00O )
    except Exception as OOO0O0O000O0O0000 :
        print (OOO0O0O000O0O0000 )
    try :
        OO00OOOOOO0OOO00O =init ()
        insert_gchat (OO00OOOOOO0OOO00O ,OOOOO000O0O000OO0 ,OOOOO000O0000OO0O ,OOOOO000OO00O0O00 ,group_chat_text ,OO000OO00000OOOO0 ,O0O0OOO0OOOOOO00O ,OOOO0O0O0O0O0O0OO ,kw_word ,kw_type )
        update_var (OO00OOOOOO0OOO00O ,gchat_count ,gchat_kw_count )
        finish (OO00OOOOOO0OOO00O )
    except Exception as OOO0O0O000O0O0000 :
        print (OOO0O0O000O0O0000 )
def kw_send (O0000O0OOOO0O0O0O ,OO0O00OOOO0O0OOOO ,O000O0O000O000000 ,OO0O000OOOOOO00OO ):
    ""
    O0000O0OOOO0O0O0O =OO0O00OOOO0O0OOOO +" # "+O000O0O000O000000 +" : \n"+O0000O0OOOO0O0O0O
    try :
        itchat .send (O0000O0OOOO0O0O0O ,toUserName =OO0O000OOOOOO00OO )
    except Exception as O0O00O0OO00OOO0O0 :
        print (O0O00O0OO00OOO0O0 )
def write_log_group (O0OO0OOOO0O000OOO ):
    ""
    OOO0O00OO0OO00OOO =time .strftime ("%Y-%m-%d")+".log"
    if not os .path .exists (LOGPATH ):
        os .makedirs (LOGPATH )
    OOO0OOO0OO0OOO0OO =os .path .join (LOGPATH ,OOO0O00OO0OO00OOO )
    OO0OOOO0O0000OOO0 =codecs .open (OOO0OOO0OO0OOO0OO ,"a","utf-8")
    OO0OOOO0O0000OOO0 .write (O0OO0OOOO0O000OOO )
    OO0OOOO0O0000OOO0 .close ()
def write_log_one (O0O0OO00OO0O0O0O0 ):
    ""
    OO0OO00OOOO0OO0O0 =time .strftime ("%Y-%m-%d")+"-onebyone.log"
    if not os .path .exists (LOGPATH ):
        os .makedirs (LOGPATH )
    OO00OO0O000O0O0OO =os .path .join (LOGPATH ,OO0OO00OOOO0OO0O0 )
    O00O000000O00OOO0 =codecs .open (OO00OO0O000O0O0OO ,"a","utf-8")
    O00O000000O00OOO0 .write (O0O0OO00OO0O0O0O0 )
    O00O000000O00OOO0 .close ()
def create_today_folder ():
    ""
    OO0OO00000000OO00 =FILEPATH +time .strftime ("%Y-%m-%d")+'/'
    if not os .path .exists (OO0OO00000000OO00 ):
        try :
            os .makedirs (OO0OO00000000OO00 )
        except OSError as OOO000OO00OO0O000 :
            print (OOO000OO00OO0O000 )
    return OO0OO00000000OO00
def read_msg ():
    ""
    OOOOOOOOO00OO0O0O =codecs .open ("file_name","r","utf-8",buffering =1 )
    O0OOO0O0O00O0OOOO =OOOOOOOOO00OO0O0O .read ()
    OOOOOOOOO00OO0O0O .close ()
def random_str (key =string .ascii_letters ,randomlength =6 ):
    ""
    OOO0OO0O0O0OOO00O =''
    O0OO0OOOOO0O000O0 =len (key )-1
    O000O0OOO000OOO00 =Random ()
    for OOOO000OO00O0O00O in range (randomlength ):
        OOO0OO0O0O0OOO00O +=key [O000O0OOO000OOO00 .randint (0 ,O0OO0OOOOO0O000O0 )]
    return OOO0OO0O0O0OOO00O
class KeywordProcesser (object ):
    ""
    def __init__ (OOOO0OOOO0O0OO0O0 ,keywords =None ,ignore_space =False ):
        OOOO0OOOO0O0OO0O0 .keyword_trie_dict =dict ()
        OOOO0OOOO0O0OO0O0 .keyword_count =0
        OOOO0OOOO0O0OO0O0 ._keyword_flag ='_type_'
        OOOO0OOOO0O0OO0O0 ._ignore_space =ignore_space
        if isinstance (keywords ,str ):
            OOOO0OOOO0O0OO0O0 .add_keyword_from_file (keywords )
        elif isinstance (keywords ,list ):
            OOOO0OOOO0O0OO0O0 .add_keyword_from_list (keywords )
        elif isinstance (keywords ,dict ):
            OOOO0OOOO0O0OO0O0 .add_keyword_from_dict (keywords )
        else :
            pass
    def add_keyword (O00OO0000O0O0O0OO ,O0OOOOO00O0OO0OOO ,keyword_type =None ):
        ""
        if not keyword_type :
            keyword_type =O0OOOOO00O0OO0OOO
        OOOO0OOOOO0000OO0 =O00OO0000O0O0O0OO .keyword_trie_dict
        for O0O0OOO0OOO0O0O0O in O0OOOOO00O0OO0OOO :
            OOOO0OOOOO0000OO0 =OOOO0OOOOO0000OO0 .setdefault (O0O0OOO0OOO0O0O0O ,{})
        if O00OO0000O0O0O0OO ._keyword_flag not in OOOO0OOOOO0000OO0 :
            O00OO0000O0O0O0OO .keyword_count +=1
            OOOO0OOOOO0000OO0 [O00OO0000O0O0O0OO ._keyword_flag ]=keyword_type
    def add_keyword_from_list (OO0O0O0000OOO0OO0 ,O0O00O0O0OOO0O000 ):
        ""
        for O00000000OO000OOO in O0O00O0O0OOO0O000 :
            OO0O0O0000OOO0OO0 .add_keyword (O00000000OO000OOO )
    def add_keyword_from_dict (OOO00OO0O000OOOOO ,OO00O0OOO000OOO00 ):
        ""
        for O0000O00OO0OO00OO in OO00O0OOO000OOO00 :
            OOO00OO0O000OOOOO .add_keyword (O0000O00OO0OO00OO ,OO00O0OOO000OOO00 [O0000O00OO0OO00OO ])
    def add_keyword_from_file (O000O00O00O000OOO ,O000O0O000O0O00OO ,split ='\t'):
        ""
        import codecs
        O000OO0O0O00OO0O0 =codecs .open (O000O0O000O0O00OO ,'r',encoding ='utf-8')
        O00OO0O0O0O000OOO =O000OO0O0O00OO0O0 .readline ()
        while O00OO0O0O0O000OOO :
            O00OO0O0O0O000OOO =O00OO0O0O0O000OOO .strip ()
            if not O00OO0O0O0O000OOO :
                O00OO0O0O0O000OOO =O000OO0O0O00OO0O0 .readline ()
                continue
            O0O0OO00OO0000OOO =O00OO0O0O0O000OOO .split (split )
            if len (O0O0OO00OO0000OOO )==1 :
                O000O00O00O000OOO .add_keyword (O0O0OO00OO0000OOO [0 ])
            else :
                O000O00O00O000OOO .add_keyword (O0O0OO00OO0000OOO [0 ],O0O0OO00OO0000OOO [1 ])
            O00OO0O0O0O000OOO =O000OO0O0O00OO0O0 .readline ()
        O000OO0O0O00OO0O0 .close ()
    def delete_keyword (OO0OO0OOOO0O00OO0 ,O0OOO00OOO0O0O0OO ):
        ""
        O00OO0O00OOO000O0 =OO0OO0OOOO0O00OO0 .keyword_trie_dict
        O0O000O00000000OO =[]
        for O0O0OOO00000O0O00 in O0OOO00OOO0O0O0OO :
            if O0O0OOO00000O0O00 not in O00OO0O00OOO000O0 :
                return False
            O0O000O00000000OO .append ((O0O0OOO00000O0O00 ,O00OO0O00OOO000O0 ))
            O00OO0O00OOO000O0 =O00OO0O00OOO000O0 [O0O0OOO00000O0O00 ]
        if OO0OO0OOOO0O00OO0 ._keyword_flag not in O00OO0O00OOO000O0 :
            return False
        O0O000O00000000OO .append ((OO0OO0OOOO0O00OO0 ._keyword_flag ,O00OO0O00OOO000O0 ))
        for O0O0OOO00000O0O00 ,OOO0000OOOOO0OOO0 in O0O000O00000000OO [::-1 ]:
            if len (OOO0000OOOOO0OOO0 )==1 :
                OOO0000OOOOO0OOO0 .pop (O0O0OOO00000O0O00 )
            else :
                OOO0000OOOOO0OOO0 .pop (O0O0OOO00000O0O00 )
                break
        OO0OO0OOOO0O00OO0 .keyword_count -=1
        return True
    def delete_keyword_from_list (O0000O00OO0OOO0O0 ,OOOOO0O00O0O00OO0 ):
        ""
        for O0OOO0OO00O00OOOO in OOOOO0O00O0O00OO0 :
            O0000O00OO0OOO0O0 .delete_keyword (O0OOO0OO00O00OOOO )
    def _match_text (OO0O0O0O0O0OOO000 ,OOOOO00O00OOOOOO0 ,O00O0OOO00OOOOOOO ,O00O00OOOOO0000O0 ):
        ""
        OOOOOO000O0O0OO00 =OO0O0O0O0O0OOO000 .keyword_trie_dict
        OOO000OOO0O00O00O ,OOO000O0OO0O00OOO =-1 ,''
        for O0OO0O00000OOO0O0 in range (O00O0OOO00OOOOOOO ,O00O00OOOOO0000O0 ):
            if OOOOO00O00OOOOOO0 [O0OO0O00000OOO0O0 ]==' 'and OO0O0O0O0O0OOO000 ._ignore_space :
                continue
            if OOOOO00O00OOOOOO0 [O0OO0O00000OOO0O0 ]not in OOOOOO000O0O0OO00 :
                if OOO000OOO0O00O00O ==-1 :
                    return O00O0OOO00OOOOOOO +1 ,0 ,''
                else :
                    return OOO000OOO0O00O00O +1 ,OOO000OOO0O00O00O +1 -O00O0OOO00OOOOOOO ,OOO000O0OO0O00OOO
            OOOOOO000O0O0OO00 =OOOOOO000O0O0OO00 [OOOOO00O00OOOOOO0 [O0OO0O00000OOO0O0 ]]
            if OO0O0O0O0O0OOO000 ._keyword_flag in OOOOOO000O0O0OO00 :
                OOO000OOO0O00O00O =O0OO0O00000OOO0O0
                OOO000O0OO0O00OOO =OOOOOO000O0O0OO00 [OO0O0O0O0O0OOO000 ._keyword_flag ]
        if OOO000OOO0O00O00O !=-1 :
            return OOO000OOO0O00O00O +1 ,OOO000OOO0O00O00O +1 -O00O0OOO00OOOOOOO ,OOO000O0OO0O00OOO
        return O00O0OOO00OOOOOOO +1 ,0 ,''
    def extract_keywords (OO0O0O0OO0OOO0O0O ,OO0O00OOOOOOOOO0O ):
        ""
        O00OO00O0OOOOO0OO =[]
        O0OO000O0OOO000OO ,OOOOOOOOOOOOO0OOO =0 ,len (OO0O00OOOOOOOOO0O )
        while O0OO000O0OOO000OO <OOOOOOOOOOOOO0OOO :
            O0OO000O0OOO000OO ,OOO00O0O0O0OOO0O0 ,OO0O00OO00O00000O =OO0O0O0OO0OOO0O0O ._match_text (OO0O00OOOOOOOOO0O ,O0OO000O0OOO000OO ,OOOOOOOOOOOOO0OOO )
            if OO0O00OO00O00000O :
                O00OO00O0OOOOO0OO .append ([O0OO000O0OOO000OO -OOO00O0O0O0OOO0O0 ,O0OO000O0OOO000OO ,OO0O00OO00O00000O ])
        return O00OO00O0OOOOO0OO
    def extract_keywords_from_list (OO00OO0000OOOOO00 ,O0OOO0O0O0O0OO00O ):
        ""
        OO000OOOOO00O0000 =[]
        for O00O000OO000O00OO ,O00O0O0OOOO00O000 in enumerate (O0OOO0O0O0O0OO00O ):
            if OO00OO0000OOOOO00 .contain_keyword (O00O0O0OOOO00O000 ):
                OO000OOOOO00O0000 .append ([O00O0O0OOOO00O000 ,O00O000OO000O00OO ])
        return OO000OOOOO00O0000
    def extract_keywords_from_list_yield (O0O0000OO00000OOO ,O0O0OOOOOOO000O00 ):
        ""
        for OO0O00O0000O0O00O ,OOOOO00OO0000OOO0 in enumerate (O0O0OOOOOOO000O00 ):
            if O0O0000OO00000OOO .contain_keyword (OOOOO00OO0000OOO0 ):
                yield [OOOOO00OO0000OOO0 ,OO0O00O0000O0O00O ]
    def extract_keywords_yield (OO00O0OOO00O00OO0 ,O000OOO0OO0O00O0O ):
        ""
        O0OO0O0OO0OO0O0O0 ,O0OO00000000OO000 =0 ,len (O000OOO0OO0O00O0O )
        while O0OO0O0OO0OO0O0O0 <O0OO00000000OO000 :
            O0OO0O0OO0OO0O0O0 ,O0OO000O0O0OO000O ,O00O00O00OOO0000O =OO00O0OOO00O00OO0 ._match_text (O000OOO0OO0O00O0O ,O0OO0O0OO0OO0O0O0 ,O0OO00000000OO000 )
            if O00O00O00OOO0000O :
                yield ([O0OO0O0OO0OO0O0O0 -O0OO000O0O0OO000O ,O0OO0O0OO0OO0O0O0 ,O00O00O00OOO0000O ])
    def get_keyword_type (O0OOOOO00O000000O ,OOO000OOOO00OO000 ):
        ""
        O00O000O00OOOOO00 =O0OOOOO00O000000O .keyword_trie_dict
        for O0OOOOO0O00000O0O in OOO000OOOO00OO000 :
            if O0OOOOO0O00000O0O not in O00O000O00OOOOO00 :
                return None
            O00O000O00OOOOO00 =O00O000O00OOOOO00 [O0OOOOO0O00000O0O ]
        if O0OOOOO00O000000O ._keyword_flag not in O00O000O00OOOOO00 :
            return None
        return O00O000O00OOOOO00 [O0OOOOO00O000000O ._keyword_flag ]
    def contain_keyword (O0O0000OOO00000OO ,O0OOO0OOO0OO0O00O ):
        ""
        OO000OO00OO00O00O =O0O0000OOO00000OO .keyword_trie_dict
        for O000O00OO0OO0O0OO in O0OOO0OOO0OO0O00O :
            if O000O00OO0OO0O0OO not in OO000OO00OO00O00O :
                return False
            OO000OO00OO00O00O =OO000OO00OO00O00O [O000O00OO0OO0O0OO ]
        if O0O0000OOO00000OO ._keyword_flag not in OO000OO00OO00O00O :
            return False
        return True
    def get_keywords (OO000OO0O0O0OOOOO ,keyword_part ='',current_dict =None ):
        ""
        O0O0OO0O0O0O0O00O =dict ()
        if current_dict is None :
            current_dict =OO000OO0O0O0OOOOO .keyword_trie_dict
        for OO0O0O0O0OOOOOOO0 in current_dict :
            if OO0O0O0O0OOOOOOO0 ==OO000OO0O0O0OOOOO ._keyword_flag :
                O0O0OO0O0O0O0O00O [keyword_part ]=current_dict [OO000OO0O0O0OOOOO ._keyword_flag ]
            else :
                OOOOO00O0000OO0OO =OO000OO0O0O0OOOOO .get_keywords (keyword_part +OO0O0O0O0OOOOOOO0 ,current_dict [OO0O0O0O0OOOOOOO0 ])
                O0O0OO0O0O0O0O00O .update (OOOOO00O0000OO0OO )
        return O0O0OO0O0O0O0O00O
    def remove_keywords_in_words (O0OOO0O0O0OOOO00O ,O0OO00OO0O0O00OOO ):
        ""
        O0OOO0O00OOO00OO0 =[]
        for OO00OOO0OOO0O0OOO in O0OO00OO0O0O00OOO :
            if O0OOO0O0O0OOOO00O .contain_keyword (OO00OOO0OOO0O0OOO ):
                continue
            O0OOO0O00OOO00OO0 .append (OO00OOO0OOO0O0OOO )
        return O0OOO0O00OOO00OO0
    def set_ignore_space (O0O0O0000000OOO0O ,OOOO0OOO000O0OO0O ):
        ""
        O0O0O0000000OOO0O ._ignore_space =OOOO0OOO000O0OO0O
def kw_match_dic ():
    O00OO00OO0OO0000O ={}
    with open ('taboo.txt','r')as O000O0O0O0OOOO000 :
        for OOO00O0OOOO00O0O0 in O000O0O0O0OOOO000 :
            OOO00O0OOOO00O0O0 =OOO00O0OOOO00O0O0 .strip ()
            if OOO00O0OOOO00O0O0 :
                O00OO00OO0OO0000O [OOO00O0OOOO00O0O0 .split (':')[0 ].strip ()]=OOO00O0OOOO00O0O0 .split (':')[1 ].strip ()
    return O00OO00OO0OO0000O
def demo (OOOOO0O0OO00OOOO0 ):
    O0OOO0OOO000O00OO =kw_match_dic ()
    O00OOOO0O0000O0OO =KeywordProcesser ()
    O00OOOO0O0000O0OO .add_keyword_from_dict (O0OOO0OOO000O00OO )
    OO000O00OO0O00OOO =OOOOO0O0OO00OOOO0
    for O00O000O0OOOOOO00 in O00OOOO0O0000O0OO .extract_keywords_yield (OO000O00OO0O00OOO ):
        return O00O000O0OOOOOO00
def create_gchat (OO0O0OOO0OO00O00O ):
    ""
    try :
        O0OO0O0O000OO0000 ='''
            CREATE TABLE IF NOT EXISTS `wc_gchat` (
            `id`  INTEGER PRIMARY KEY AUTOINCREMENT,
            `create_time`  TEXT NOT NULL,
            `group_id`  TEXT NOT NULL,
            `group_one_id`  TEXT NOT NULL,
            `group_chat_text`  TEXT,
            `file_type`  TEXT,
            `file_name`  TEXT,
            `file_dst`  TEXT,
            `kw_word`  TEXT,
            `kw_type`  TEXT
        )
        '''
        OO0O0OOO0OO00O00O .execute (O0OO0O0O000OO0000 )
    except :
        return False
def create_friends (O0OO0OO0O00OOOO0O ):
    ""
    try :
        O000O00O00OOO00OO ='''
            CREATE TABLE IF NOT EXISTS `wc_friends` (
            `id`  INTEGER PRIMARY KEY AUTOINCREMENT,
            `name`  TEXT NOT NULL,
            `sex`  TEXT,
            `province`  TEXT,
            `city`  TEXT,
            `signature`  TEXT
        )
        '''
        O0OO0OO0O00OOOO0O .execute (O000O00O00OOO00OO )
    except :
        return False
def create_var (OO0OO0000000O0OO0 ):
    ""
    try :
        OO00O00O00O0OOOOO ='''
            CREATE TABLE IF NOT EXISTS `wc_var` (
            `gchat_count`  INTEGER NOT NULL,
            `gchat_kw_count`  INTEGER NOT NULL
        )
        '''
        OO0OO0000000O0OO0 .execute (OO00O00O00O0OOOOO )
    except :
        return False
def insert_gchat (OO0O00O0OOOOOOOO0 ,O00OO0OOOO00O0OOO ,O0O0O0O0000OO0O0O ,O000O0O0O00O0OO0O ,OOO0000000OOO00O0 ,OO0OO000OOOO0O00O ,O00O00O0OOOOO0O0O ,OOO0OOO0O0000O0O0 ,OOO0O0000O00OOOO0 ,OO0O0O0000000OO00 ):
    ""
    O00O00OOO000O000O ='''
    INSERT INTO
        wc_gchat(create_time, group_id, group_one_id, group_chat_text, file_type, file_name, file_dst, kw_word, kw_type)
    VALUES
        (?, ?, ?, ?, ?, ?, ?, ?, ?);
    '''
    OO0O00O0OOOOOOOO0 .execute (O00O00OOO000O000O ,(O00OO0OOOO00O0OOO ,O0O0O0O0000OO0O0O ,O000O0O0O00O0OO0O ,OOO0000000OOO00O0 ,OO0OO000OOOO0O00O ,O00O00O0OOOOO0O0O ,OOO0OOO0O0000O0O0 ,OOO0O0000O00OOOO0 ,OO0O0O0000000OO00 ))
def insert_friends (O00000OOO0000O0OO ,OO0000O00OOO0OO00 ,O00O000OO00O0OOOO ,O00O0OO0O0OOOO0OO ,O00000000OOO000OO ,OOO0OO0O0OO000OO0 ):
    ""
    OOO000O0O0O000OOO ='''
    INSERT INTO
        wc_friends(name, sex, province, city, signature)
    VALUES
        (?, ?, ?, ?, ?);
    '''
    O00000OOO0000O0OO .execute (OOO000O0O0O000OOO ,(OO0000O00OOO0OO00 ,O00O000OO00O0OOOO ,O00O0OO0O0OOOO0OO ,O00000000OOO000OO ,OOO0OO0O0OO000OO0 ))
def select_var (OO0O0O0O0O0000OO0 ):
    ""
    OOOOOO0OOOO00OOO0 ='''
    SELECT
        `gchat_count`,
        `gchat_kw_count`
    FROM
        `wc_var`;
    '''
    O0O0O0O000O00OO0O =OO0O0O0O0O0000OO0 .execute (OOOOOO0OOOO00OOO0 )
    for O0O0OOO0O0O00O00O in O0O0O0O000O00OO0O :
        O0O000000000OO000 =O0O0OOO0O0O00O00O [0 ]
        OOOOO000OOO0O0O0O =O0O0OOO0O0O00O00O [1 ]
    return (O0O000000000OO000 ,OOOOO000OOO0O0O0O )
def delete (O00OO0OOOO0000OO0 ,OOOO00000O0O0O00O ):
    ""
    OOOO0O0OO0OO0O000 ='''
    DELETE FROM
        wc_gchat_txt
    WHERE
        id=?
    '''
    O00OO0OOOO0000OO0 .execute (OOOO0O0OO0OO0O000 ,(OOOO00000O0O0O00O ,))
def update_var (OO0O000O0OOO000O0 ,OOOOO0OOO00O0OO0O ,OO0OOOO0OO00O0O0O ):
    ""
    O0OO00O0O0OO0OO0O ='''
    UPDATE
        `wc_var`
    SET
        `gchat_count`=?,
        `gchat_kw_count`=?
    '''
    OO0O000O0OOO000O0 .execute (O0OO00O0O0OO0OO0O ,(OOOOO0OOO00O0OO0O ,OO0OOOO0OO00O0O0O ))
def init ():
    OOOO00O0000O0000O =ROOTPATH +"db.sqlite3"
    O0O0OO000OOOOO0O0 =sqlite3 .connect (OOOO00O0000O0000O )
    O0O0OO000OOOOO0O0 .text_factory =str
    return O0O0OO000OOOOO0O0
def finish (O00O00O00OO00OOOO ):
    O00O00O00OO00OOOO .commit ()
    O00O00O00OO00OOOO .close ()
def init_sqlite ():
    OO00OOO00OO0000OO =init ()
    create_gchat (OO00OOO00OO0000OO )
    create_var (OO00OOO00OO0000OO )
    OOOO0O00OOOO0O00O ="INSERT INTO wc_var(gchat_count, gchat_kw_count) VALUES (0, 0);"
    OO00OOO00OO0000OO .execute (OOOO0O00OOOO0O00O )
    create_friends (OO00OOO00OO0000OO )
    finish (OO00OOO00OO0000OO )
def main ():
    ""
    global gchat_count ,gchat_kw_count ,boss
    try :
        OO000OOOO0OO00OO0 =init ()
        (gchat_count ,gchat_kw_count )=select_var (OO000OOOO0OO00OO0 )
        finish (OO000OOOO0OO00OO0 )
    except Exception as O0OO0O0OOO0O00000 :
        print (O0OO0O0OOO0O00000 )
    itchat .auto_login (enableCmdQR =2 )
    try :
        boss =itchat .search_friends (name ="●﹏●")[0 ]['UserName']
        itchat .run ()
    except KeyboardInterrupt as O0OO0O0OOO0O00000 :
        print ("itchat Error ..."+O0OO0O0OOO0O00000 )
        itchat .logout ()
if __name__ =="__main__":
    # init_sqlite()
    main ()
