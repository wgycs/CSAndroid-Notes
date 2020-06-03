# -*- coding: utf-8 -*-
"""
Created on Mon Nov 19 19:52:40 2018

@author: wangy
"""

#coding:utf-8

import os

"""
"列出文件夹及文件并提供索引
"""
def list_files(startpath):    
    for root, dirs, files in os.walk(startpath):
        level = root.replace(startpath, '').count('\\')
        dir_indent = "    " * (level - 1) + "* "
        file_indent = "    " * (level) + "* "
        
        path = root.replace(startpath, '')
       
        if not level:
           path = '.'
        else:
           path = '.'+root.replace(startpath, '')
            #print('%s ***%s***'%(dir_indent, full_dir))
        #dirs = full_dir.split('/')
        #print(level)
        #print(path)
        print('%s***%s***'%(dir_indent, os.path.basename(path)))
        #print(full_dir)
        #打印文件
        for f in files:
            file_dir = path + '\\' + f
            dir_format = file_dir.replace('\\','/')
            print('%s[%s](%s)'%(file_indent, f, dir_format))
            
            
def print_to_file(str):
    #print to README.md
    print(str)

if __name__ == '__main__':
    
    list_files("./")