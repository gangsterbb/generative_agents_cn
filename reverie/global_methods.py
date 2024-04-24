"""
Author: Joon Sung Park (joonspk@stanford.edu)

File: global_methods.py
Description: Contains functions used throughout my projects.
"""
"""
作者：朴俊成 (joonspk@stanford.edu)
文件：global_methods.py
描述：本文件的函数在我整个项目都有用到（译注：即全局方法函数）
"""
import random
import string
import csv
import time
import datetime as dt
import pathlib
import os
import sys
import numpy
import math
import shutil, errno

from os import listdir

def create_folder_if_not_there(curr_path): 
  """
  Checks if a folder in the curr_path exists. If it does not exist, creates
  the folder. 
  Note that if the curr_path designates a file location, it will operate on 
  the folder that contains the file. But the function also works even if the 
  path designates to just a folder. 
  Args:
    curr_list: list to write. The list comes in the following form:
               [['key1', 'val1-1', 'val1-2'...],
                ['key2', 'val2-1', 'val2-2'...],]
    outfile: name of the csv file to write    
  RETURNS: 
    True: if a new folder is created
    False: if a new folder is not created
  """
  """
  检查文件夹是否在当前路径内，如果不存在，则创建此文件夹。
  注意，如果curr_path指定了文件的位置，它将在包含文件的文件夹下操作
  如果这个路径仅指定了文件夹，这个函数也能正常运行
  参数：
  curr_list：要写入的列表。该列表采用以下形式：
               [['key1', 'val1-1', 'val1-2'...],
                ['key2', 'val2-1', 'val2-2'...],]
  outfile：要写入的 csv 文件的名称  
  返回值：
    True：如果新文件夹被创建
    False：如果新文件夹没有被创建
  """
  outfolder_name = curr_path.split("/")
  if len(outfolder_name) != 1: 
    # This checks if the curr path is a file or a folder. 
    # 检查当前路径是文件还是文件夹
    if "." in outfolder_name[-1]: 
      outfolder_name = outfolder_name[:-1]

    outfolder_name = "/".join(outfolder_name)
    if not os.path.exists(outfolder_name):
      os.makedirs(outfolder_name)
      return True

  return False 


def write_list_of_list_to_csv(curr_list_of_list, outfile):
  """
  Writes a list of list to csv. 
  Unlike write_list_to_csv_line, it writes the entire csv in one shot. 
  ARGS:
    curr_list_of_list: list to write. The list comes in the following form:
               [['key1', 'val1-1', 'val1-2'...],
                ['key2', 'val2-1', 'val2-2'...],]
    outfile: name of the csv file to write    
  RETURNS: 
    None
  """
  """
  将一个二维列表写入csv文件中。
  与write_list_to_csv_line不同，这个函数一次性写入了整个csv
  参数：
    curr_list_of_list：要写入的列表，该列表采用以下的格式：
               [['key1', 'val1-1', 'val1-2'...],
                ['key2', 'val2-1', 'val2-2'...],]
    outfile：要写入的csv文件名
  返回值：
    无
  """
  create_folder_if_not_there(outfile)
  with open(outfile, "w") as f:
    writer = csv.writer(f)
    writer.writerows(curr_list_of_list)


def write_list_to_csv_line(line_list, outfile): 
  """
  Writes one line to a csv file.
  Unlike write_list_of_list_to_csv, this opens an existing outfile and then 
  appends a line to that file. 
  This also works if the file does not exist already. 
  ARGS:
    curr_list: list to write. The list comes in the following form:
               ['key1', 'val1-1', 'val1-2'...]
               Importantly, this is NOT a list of list. 
    outfile: name of the csv file to write   
  RETURNS: 
    None
  """
  """
  将一行数据写入一个csv文件
  与write_list_of_list_to_csv不同，此函数打开了一个已有的outfile文件并且在文件中
  追加了一行数据。
  如果文件不存在仍然能正常运行
  参数：
      curr_list: 要写入的列表数据，该列表采用以下形式：
               ['key1', 'val1-1', 'val1-2'...]
               注意，这不是一个二维列表。 
    outfile: 待写入的csv文件名
  返回值：
    无
  """
  create_folder_if_not_there(outfile)

  # Opening the file first so we can write incrementally as we progress
  # 先打开文件，才可以逐步进行增量写入
  curr_file = open(outfile, 'a',)
  csvfile_1 = csv.writer(curr_file)
  csvfile_1.writerow(line_list)
  curr_file.close()


def read_file_to_list(curr_file, header=False, strip_trail=True): 
  """
  Reads in a csv file to a list of list. If header is True, it returns a 
  tuple with (header row, all rows)
  ARGS:
    curr_file: path to the current csv file. 
  RETURNS: 
    List of list where the component lists are the rows of the file. 
  """
  """
  将一个csv文件读入二维列表。如果 header=True，此函数返回一个(标题行,所有行数据)的元组(译注：即带有标题信息)
  参数：
    curr_file: 当前csv文件的路径
  返回值：
    一个二维列表，其中每个子列表都是csv文件的一行数据
  """
  if not header: 
    analysis_list = []
    with open(curr_file) as f_analysis_file: 
      data_reader = csv.reader(f_analysis_file, delimiter=",")
      for count, row in enumerate(data_reader): 
        if strip_trail: 
          row = [i.strip() for i in row]
        analysis_list += [row]
    return analysis_list
  else: 
    analysis_list = []
    with open(curr_file) as f_analysis_file: 
      data_reader = csv.reader(f_analysis_file, delimiter=",")
      for count, row in enumerate(data_reader): 
        if strip_trail: 
          row = [i.strip() for i in row]
        analysis_list += [row]
    return analysis_list[0], analysis_list[1:]


def read_file_to_set(curr_file, col=0): 
  """
  Reads in a "single column" of a csv file to a set. 
  ARGS:
    curr_file: path to the current csv file. 
  RETURNS: 
    Set with all items in a single column of a csv file. 
  """
  """
  将csv文件的一列数据读取到一个set集合中
  参数：
    curr_file: 当前csv文件的路径
  返回值：
    一个包含csv文件单列中所有单元的set集合
  """
  analysis_set = set()
  with open(curr_file) as f_analysis_file: 
    data_reader = csv.reader(f_analysis_file, delimiter=",")
    for count, row in enumerate(data_reader): 
      analysis_set.add(row[col])
  return analysis_set


def get_row_len(curr_file): 
  """
  Get the number of rows in a csv file 
  ARGS:
    curr_file: path to the current csv file. 
  RETURNS: 
    The number of rows
    False if the file does not exist
  """
  """
  获取一个csv文件的行数
  参数：
    curr_file: 当前csv文件的路径
  返回值：
    行数
    如果文件不存在，返回False
  """
  try: 
    analysis_set = set()
    with open(curr_file) as f_analysis_file: 
      data_reader = csv.reader(f_analysis_file, delimiter=",")
      for count, row in enumerate(data_reader): 
        analysis_set.add(row[0])
    return len(analysis_set)
  except: 
    return False


def check_if_file_exists(curr_file): 
  """
  Checks if a file exists
  ARGS:
    curr_file: path to the current csv file. 
  RETURNS: 
    True if the file exists
    False if the file does not exist
  """
  """
  检查文件是否存在
  参数：
    curr_file: 当前csv文件的路径
  返回值：
    True: 文件存在
    False: 文件不存在
  """
  try: 
    with open(curr_file) as f_analysis_file: pass
    return True
  except: 
    return False


def find_filenames(path_to_dir, suffix=".csv"):
  """
  Given a directory, find all files that ends with the provided suffix and 
  returns their paths.  
  ARGS:
    path_to_dir: Path to the current directory 
    suffix: The target suffix.
  RETURNS: 
    A list of paths to all files in the directory. 
  """
  """
  给定一个文件夹，找出所有以给定suffix为后缀的文件并返回它们的路径
  参数：
    path_to_dir: 给定的文件夹路径
    suffix: 目标文件名后缀
  返回值：
    一个符合条件的所有文件路径的列表
  """
  filenames = listdir(path_to_dir)
  return [ path_to_dir+"/"+filename 
           for filename in filenames if filename.endswith( suffix ) ]


def average(list_of_val): 
  """
  Finds the average of the numbers in a list.
  ARGS:
    list_of_val: a list of numeric values  
  RETURNS: 
    The average of the values
  """
  """
  计算一个列表的平均值
  参数：
    list_of_val: 数值列表
  返回值：
    平均值
  """
  return sum(list_of_val)/float(len(list_of_val))


def std(list_of_val): 
  """
  Finds the std of the numbers in a list.
  ARGS:
    list_of_val: a list of numeric values  
  RETURNS: 
    The std of the values
  """
  std = numpy.std(list_of_val)
  return std


def copyanything(src, dst):
  """
  Copy over everything in the src folder to dst folder. 
  ARGS:
    src: address of the source folder  
    dst: address of the destination folder  
  RETURNS: 
    None
  """
  """
  把src文件夹所有东西拷贝至dst文件夹
  参数：
    src: 源文件夹路径 
    dst: 目标文件夹路径
  返回值：
  """
  try:
    shutil.copytree(src, dst)
  except OSError as exc: # python >2.5
    if exc.errno in (errno.ENOTDIR, errno.EINVAL):
      shutil.copy(src, dst)
    else: raise


if __name__ == '__main__':
  pass
















