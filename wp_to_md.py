#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import MySQLdb
import os
import re
from shutil import copyfile
from os.path import basename
from bs4 import BeautifulSoup

reload(sys)
sys.setdefaultencoding('utf8')

db = MySQLdb.connect(host="localhost", # your host, usually localhost
                    user="root",       # your username
                    passwd="56805696", # your passwd
                    db="tmpdb",        # name of the data base
                    charset="utf8",    # set charset
                    use_unicode=True)

cur = db.cursor()

# The wordpress's posts in'wp_posts' table, so we just get it.
sql_string = """select post_title, post_name, post_date, 
post_content,ID from wp_posts 
where post_status = 'publish' and post_type = 'post'"""

cur.execute(sql_string)

for row in cur.fetchall():
    title = row[0]      # post's title
    post_date = row[2]  # post's publish date
    folder_name = post_date.strftime("%Y%m%d%H%M%S")    #we use each post's publish data as markdown file's dicrecotry name
    folder_name = 'blogs/' + folder_name    # put all exported posts in 'blogs' dicrecotry
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    f = open(folder_name+'/item.md','w')    # we set all posts name as item.md
    f.write('---\n')    # write markdown file header information
    f.write('title: '+title+'\n')
    f.write('date: '+post_date.strftime("%m/%d/%Y %H:%M:%S")+'\n')
    f.write('---\n')
    post_content = row[3]
    lst = post_content.splitlines() # split post content as a list
    for str in lst:
        caption = ''
        if str.startswith('[caption'): # get image's caption information
            caption = re.search('caption="(.*)"]',str).group(1)
        if ('<img ' in str) and ('/wp-content/uploads/' in str):
            start = 'wp-content/'       
            end = '.jpg'
            img_path = str.split(start)[1].split(end)[0] # get image path
            if img_path:
                img_path = img_path + '.jpg'            
            filename = basename(img_path)
            copyfile('wp-content/'+img_path,folder_name+'/'+filename)   # copy image to the same direcotry of markdown file 
            f.write('!['+caption+']('+filename+'"'+caption+'")\n')      # insert image mark into markdown file
        else:
            soup = BeautifulSoup(str)   # if image or cation not in line, then just write text into markdown file
            f.write(soup.get_text()+'\n')
    f.close()
    
db.close()