import pymysql as DBAdapter
import numpy as np
import pandas as pd
import sys, os, math
from threading import Thread
import datetime
from math import pi,sqrt,sin,cos,atan2
import base64
import ftplib
from ftplib import FTP
from contextlib import closing
import time

__PATH__ = os.path.realpath("")

def listdir(d = '/nb', server = "ftp.drivehq.com", usr = "tecnosam", pwd = "I$AAc1023"):
    with closing(FTP(server)) as ftp:
        try:
            ftp.login(usr, pwd)
            ftp.cwd( d )
            files = []
            ftp.dir(files.append)
            return files
        except ftplib.all_errors as e:
            raise e
def listfiles(d = '/nb', server = "ftp.drivehq.com", usr = "tecnosam", pwd = "I$AAc1023"):
    with closing(FTP(server)) as ftp:
        try:
            ftp.login(usr, pwd)
            ftp.cwd( d )
            files = list ( ftp.nlst ( d ) )
            return files
        except ftplib.all_errors as e:
            raise e
def mkdir(dn, server = 'ftp.drivehq.com', usr = 'tecnosam', pwd = 'I$AAc1023'):
    with closing(FTP(server)) as ftp:
        try:
            ftp.login(usr, pwd)
            ftp.mkd(dn)
        except ftplib.all_errors as e:
            raise e
def save_file(f, d = '/music', server = 'ftp.drivehq.com', usr = 'tecnosam', pwd = 'I$AAc1023'):
    with closing(ftplib.FTP(server)) as ftp:
        filename = f.name
        try:
            ftp.login(usr, pwd)
            with f as fp:
                ftp.cwd( d )
                res = ftp.storbinary("STOR " + filename, fp)
                if not res.startswith('226 Transfer complete'):
                    return False
            fp.close()
        except ftplib.all_errors as e:
            raise e
    return True
def open_file(f, d = '/nb', server = 'ftp.drivehq.com', usr = 'tecnosam', pwd = 'I$AAc1023'):
    jj = os.listdir(os.path.realpath(""))
    if (f in jj):
        return True
    with closing(ftplib.FTP(server)) as ftp:
        filename = f
        try:
            ftp.login(usr, pwd)
            with open(f, "wb") as fp:
                ftp.cwd( d )
                res = ftp.retrbinary("RETR " + filename, fp.write)
                if not res.startswith('226 Transfer complete'):
                    return res
            fp.close()
        except ftplib.all_errors as e:
            raise e
    return True
def delete_all(d = '/nb', server = 'ftp.drivehq.com', usr = 'tecnosam', pwd = 'I$AAc1023'):
    with closing(ftplib.FTP(server)) as ftp:

        try:
            ftp.login(usr, pwd)

            ftp.cwd( '.' )

            files = list( ftp.nlst( d ) )
            for f in files:
                ftp.delete( f )
        except ftplib.all_errors as e:
            raise e
def delete(f, server = 'ftp.drivehq.com', usr = 'tecnosam', pwd = 'I$AAc1023'):
    with closing(ftplib.FTP(server)) as ftp:

        try:
            ftp.login(usr, pwd)

            ftp.cwd( '.' )

            ftp.delete( f )
        except ftplib.all_errors as e:
            raise e



def download_all(d = '/music', server = 'ftp.drivehq.com', usr = 'tecnosam', pwd = 'I$AAc1023'):
    os.chdir("static%s" % d)
    jj = os.listdir(os.path.realpath(""))
    with closing(ftplib.FTP(server)) as ftp:
        try:
            ftp.login(usr, pwd)
            for f in listfiles(d):
                filename = f
                if (f in jj):
                    continue
                with open(f, "wb") as fp:
                    ftp.cwd( d )
                    res = ftp.retrbinary("RETR " + filename, fp.write)
                    if not res.startswith('226 Transfer complete'):
                        continue
            fp.close()
        except ftplib.all_errors as e:
            raise e
    return True

def BuildStandardDateTime():
	obj = datetime.datetime.now()
	return "%d-%d-%d %s:%s:%s" % (obj.day, obj.month, obj.year, obj.hour, obj.minute, obj.second)
def BuildStandardTime():
	obj = datetime.datetime.now()
	return "%s:%s:%s" % (obj.hour, obj.minute, obj.second)
def BuildStandardDate():
    obj = time.ctime(time.time()).split(" ")
    return "%s %s %s" % (obj[3], obj[1], obj[-1])

def con(host='remotemysql.com', db='h707135xob'):
	return DBAdapter.connect(host, "h707135xob", "CP3juC9owr", db)

class ServeData:
    def __init__(self, fetchall = False):
        if (fetchall == True):
            self.reviews = self.fetchRev()
            self.events = self.fetchUpcoming()
            self.gallery = self.fetchGallery()
            self.music = self.fetchMusic()
            self.album = self.fetchAlbum()
            self.blog = self.fetchBlog()
    def fetchRev(self):
        db = con()
        sql = """SELECT * FROM reviews"""
        with db.cursor() as c:
            try:
                c.execute(sql)
                res = c.fetchall()
                return res if len(res) != 0 else ()
            except Exception as e:
                raise e
        return ()
    def fetchUpcoming(self):
        db = con()
        sql = """SELECT * FROM upcoming"""
        with db.cursor() as c:
            try:
                c.execute(sql)
                res = c.fetchall()
                return res if len(res) != 0 else ()
            except Exception as e:
                raise e
        return ()
    def fetchGallery(self):
        db = con()
        sql = """SELECT * FROM gallery"""
        with db.cursor() as c:
            try:
                c.execute(sql)
                res = c.fetchall()
                return res if len(res) != 0 else ()
            except Exception as e:
                raise e
        return ()
    def fetchMusic(self):
        db = con()
        sql = """SELECT * FROM music"""
        with db.cursor() as c:
            try:
                c.execute(sql)
                res = c.fetchall()
                return res[::-1] if len(res) != 0 else ()
            except Exception as e:
                raise e
        return ()
    def get_unique_cat(self):
        gal = []
        for i in self.fetchGallery():
            if (i[2] not in gal):
                gal.append(i[2])
            else:
                continue
        return gal
    def fetchAlbum(self):
        db = con()
        sql = """SELECT * FROM album"""
        with db.cursor() as c:
            try:
                c.execute(sql)
                res = c.fetchall()
                return res if len(res) != 0 else ()
            except Exception as e:
                raise e
        return ()
    def fetchBlog(self):
        db = con()
        sql = """SELECT * FROM blog"""
        with db.cursor() as c:
            try:
                c.execute(sql)
                res = c.fetchall()
                return res if len(res) != 0 else ()
            except Exception as e:
                raise e
        return ()
    def fetchMsg(self):
        db = con()
        sql = """SELECT * FROM message"""
        with db.cursor() as c:
            try:
                c.execute(sql)
                res = c.fetchall()
                return res if len(res) != 0 else ()
            except Exception as e:
                raise e
        return ()

def contact(email, phone, msg, name = "anonymous"):
    db = con()
    sql = """
            INSERT INTO message
            (name, email, phone, msg)
            VALUES
            ('%s', '%s', '%s', '%s')
    """ % (name, email, phone, msg)
    with db.cursor() as c:
        try:
            c.execute(sql)
            db.commit()
            return True
        except Exception as e:
            db.rollback()
            raise e
    db.close()
    return False

def popId(tbl, mid):
    db = con()
    with db.cursor() as c:
        try:
            c.execute( "DELETE FROM `%s` WHERE id=%d" % ( tbl, int(mid) ) )
            db.commit()
            return True
        except Exception as e:
            db.rollback()
            raise e
        db.close()
    return False

class Admin:
    def upload_song(self, name, artist, fname, lyrics = "No Quotable Lyrics", dt = BuildStandardDate()):
        db = con()
        sql = """
                INSERT INTO music (name, artist, dt, lyrics, fname)
                VALUES
                ('%s', '%s', '%s', '%s', '%s')
        """ % (name, artist, dt, lyrics, fname)
        with db.cursor() as c:
            try:
                c.execute(sql)
                db.commit()
                return True
            except Exception as e:
                db.rollback()
                raise e
        db.close()
        return False
    def upload_album(self, name, price):
        obj = BuildStandardDate().split(" ")
        year = obj[-1]
        db = con()
        sql = """
                INSERT INTO album (name, year, price) VALUES ('%s', %d, %d)
        """ % ( name, int(year), int(price) )
        with db.cursor() as c:
            try:
                c.execute(sql)
                db.commit()
                return True
            except Exception as e:
                db.rollback()
                raise e
        db.close()
        return False
    def upload_to_blog(self, cover, title, info):
        obj = BuildStandardDate().split(" ")
        db = con()
        print(obj)
        sql = """
                INSERT INTO blog
                (cover, title, info, day, month, year)
                VALUES
                ('%s', '%s', '%s', %s, '%s', %s)
        """ % ( cover, title, info, obj[0], obj[1], obj[-1] )
        with db.cursor() as c:
            try:
                c.execute(sql)
                db.commit()
                return True
            except Exception as e:
                db.rollback()
                raise e
        db.close()
        return False
    def upload_to_gallery(self, img, category):
        db = con()
        sql = """
                INSERT INTO gallery
                (img, category)
                VALUES
                ('%s', '%s')
        """ % ( img, category )
        with db.cursor() as c:
            try:
                c.execute(sql)
                db.commit()
                return True
            except Exception as e:
                db.rollback()
                raise e
        db.close()
        return False
    def upload_review(self, review, name, bio):
        db = con()
        sql = """
                INSERT INTO reviews
                (review, name, bio)
                VALUES
                ('%s', '%s', '%s')
        """ % ( review, name, bio )
        with db.cursor() as c:
            try:
                c.execute(sql)
                db.commit()
                return True
            except Exception as e:
                db.rollback()
                raise e
        db.close()
        return False
    def upload_event(self, name, info, date):
        obj = pd.to_datetime(date)
        db = con()
        sql = """
                INSERT INTO upcoming
                (name, info, day, month)
                VALUES
                ('%s', '%s', %d, '%s')
        """ % ( name, info, int(obj.day), obj.month_name()[:3] )
        with db.cursor() as c:
            try:
                c.execute(sql)
                db.commit()
                return True
            except Exception as e:
                db.rollback()
                raise e
        db.close()
        return False

# m = Admin()
# print(m.upload_album("Signs and Wonders", 12))
# print(m.upload_event("worship without walls", "come and be blessed", "20th of Jan 2020"))
# print(m.upload_song("in Jesus name remix", "Phada Abraham ft frank edwards"))
