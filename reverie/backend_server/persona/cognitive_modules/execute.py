"""
Author: Joon Sung Park (joonspk@stanford.edu)

File: execute.py
Description: This defines the "Act" module for generative agents. 
"""
"""
作者: 朴俊成(joonspk@stanford.edu)

文件: execute.py
描述: 定义生成式代理的行为模式。
"""
import sys
import random
sys.path.append('../../')

from global_methods import *
from path_finder import *
from utils import *

def execute(persona, maze, personas, plan): 
  """
  Given a plan (action's string address), we execute the plan (actually 
  outputs the tile coordinate path and the next coordinate for the 
  persona). 

  INPUT:
    persona: Current <Persona> instance.  
    maze: An instance of current <Maze>.
    personas: A dictionary of all personas in the world. 
    plan: This is a string address of the action we need to execute. 
       It comes in the form of "{world}:{sector}:{arena}:{game_objects}". 
       It is important that you access this without doing negative 
       indexing (e.g., [-1]) because the latter address elements may not be 
       present in some cases. 
       e.g., "dolores double studio:double studio:bedroom 1:bed"
    
  OUTPUT: 
    execution
  """
  """
  给定一个计划（动作的字符串地址），执行该计划（实际上是输出人物的地图块坐标路径和
  下一个坐标）。

  输入：
    persona：当前<Persona>实例。
    maze：当前<Maze>实例。
    personas: 存储小镇中所有角色的字典。
    plan：存储需要执行的动作字符串地址。它的格式是： "{world}:{sector}:{arena}:
    {game_objects}". 注意在操作时不能输入负数索引(e.g., [-1])因为在一些情况下
    后面的地址元素可能没有被初始化。
  输出：
  """
  if "<random>" in plan and persona.scratch.planned_path == []: 
    persona.scratch.act_path_set = False

  # <act_path_set> is set to True if the path is set for the current action. 
  # It is False otherwise, and means we need to construct a new path. 
  # 当路径被设置为当前动作时，<act_path_set> 赋值为True，否则赋值为False，此时代表
  # 需要构造一个新路径
  if not persona.scratch.act_path_set: 
    # <target_tiles> is a list of tile coordinates where the persona may go 
    # to execute the current action. The goal is to pick one of them.
    # <target_tiles>是一个角色为了执行当前行动可能到达的地图块坐标列表。作用是用于
    # 选择其中一个坐标执行。
    target_tiles = None

    print ('aldhfoaf/????')
    print (plan)

    if "<persona>" in plan: 
      # Executing persona-persona interaction.
      # 执行角色到角色的交互
      target_p_tile = (personas[plan.split("<persona>")[-1].strip()]
                       .scratch.curr_tile)
      potential_path = path_finder(maze.collision_maze, 
                                   persona.scratch.curr_tile, 
                                   target_p_tile, 
                                   collision_block_id)
      if len(potential_path) <= 2: 
        target_tiles = [potential_path[0]]
      else: 
        potential_1 = path_finder(maze.collision_maze, 
                                persona.scratch.curr_tile, 
                                potential_path[int(len(potential_path)/2)], 
                                collision_block_id)
        potential_2 = path_finder(maze.collision_maze, 
                                persona.scratch.curr_tile, 
                                potential_path[int(len(potential_path)/2)+1], 
                                collision_block_id)
        if len(potential_1) <= len(potential_2): 
          target_tiles = [potential_path[int(len(potential_path)/2)]]
        else: 
          target_tiles = [potential_path[int(len(potential_path)/2+1)]]
    
    elif "<waiting>" in plan: 
      # Executing interaction where the persona has decided to wait before
      # executing their action.

      # 执行交互，在这个情景中，角色决定在执行动作之前等待。
      x = int(plan.split()[1])
      y = int(plan.split()[2])
      target_tiles = [[x, y]]

    elif "<random>" in plan: 
      # Executing a random location action.
      # 执行一个随机位置的行动。
      plan = ":".join(plan.split(":")[:-1])
      target_tiles = maze.address_tiles[plan]
      target_tiles = random.sample(list(target_tiles), 1)

    else: 
      # This is our default execution. We simply take the persona to the
      # location where the current action is taking place. 
      # Retrieve the target addresses. Again, plan is an action address in its
      # string form. <maze.address_tiles> takes this and returns candidate 
      # coordinates. 

      # 这是默认的执行方式。它只是将角色带到当前动作发生的位置。获取目标地址，同样，
      # plan是一个字符串形式的动作地址。<maze.address_tiles>接受这个地址并返回候选
      # 坐标。
      if plan not in maze.address_tiles: 
        maze.address_tiles["Johnson Park:park:park garden"] #ERRORRRRRRR
      else: 
        target_tiles = maze.address_tiles[plan]

    # There are sometimes more than one tile returned from this (e.g., a table
    # may stretch many coordinates). So, we sample a few here. And from that 
    # random sample, we will take the closest ones. 

    # 有时这里不止返回一个地图块（例如，一个表可能延伸很多坐标）。所以，这里采样一部分。
    # 并且从那些随机样本从获取最近的一个。
    if len(target_tiles) < 4: 
      target_tiles = random.sample(list(target_tiles), len(target_tiles))
    else:
      target_tiles = random.sample(list(target_tiles), 4)
    # If possible, we want personas to occupy different tiles when they are 
    # headed to the same location on the maze. It is ok if they end up on the 
    # same time, but we try to lower that probability. 
    # We take care of that overlap here.  

    # 如果可能的话，我们希望角色在前往迷宫上的同一位置时占据不同的方格。如果他们最后
    # 在同一个方格上，那也没关系，但我们尽量降低这种可能性。在这里处理重叠情况。
    persona_name_set = set(personas.keys())
    new_target_tiles = []
    for i in target_tiles: 
      curr_event_set = maze.access_tile(i)["events"]
      pass_curr_tile = False
      for j in curr_event_set: 
        if j[0] in persona_name_set: 
          pass_curr_tile = True
      if not pass_curr_tile: 
        new_target_tiles += [i]
    if len(new_target_tiles) == 0: 
      new_target_tiles = target_tiles
    target_tiles = new_target_tiles

    # Now that we've identified the target tile, we find the shortest path to
    # one of the target tiles. 

    # 到这里程序已经识别了目标的地图块，并且找到去往其中一个目标地图块的最短路径。
    curr_tile = persona.scratch.curr_tile
    collision_maze = maze.collision_maze
    closest_target_tile = None
    path = None
    for i in target_tiles: 
      # path_finder takes a collision_mze and the curr_tile coordinate as 
      # an input, and returns a list of coordinate tuples that becomes the
      # path. 
      # e.g., [(0, 1), (1, 1), (1, 2), (1, 3), (1, 4)...]

      # path_finder函数接收collision_mze和curr_tile坐标作为输入，并且返回变成
      # 路径的坐标元组列表。
      # e.g., [(0, 1), (1, 1), (1, 2), (1, 3), (1, 4)...]
      curr_path = path_finder(maze.collision_maze, 
                              curr_tile, 
                              i, 
                              collision_block_id)
      if not closest_target_tile: 
        closest_target_tile = i
        path = curr_path
      elif len(curr_path) < len(path): 
        closest_target_tile = i
        path = curr_path

    # Actually setting the <planned_path> and <act_path_set>. We cut the 
    # first element in the planned_path because it includes the curr_tile. 

    # 真正设置<planned_path>和<act_path_set>的地方。这里删除了在planned_path的
    # 第一个元素是因为它包括了当前的tile
    persona.scratch.planned_path = path[1:]
    persona.scratch.act_path_set = True
  
  # Setting up the next immediate step. We stay at our curr_tile if there is
  # no <planned_path> left, but otherwise, we go to the next tile in the path.

  # 设置下一直接步骤。如果没有剩下<planned_path>，则留在原tile，否则会前往路径的下一
  # 个地图块。
  ret = persona.scratch.curr_tile
  if persona.scratch.planned_path: 
    ret = persona.scratch.planned_path[0]
    persona.scratch.planned_path = persona.scratch.planned_path[1:]

  description = f"{persona.scratch.act_description}"
  description += f" @ {persona.scratch.act_address}"

  execution = ret, persona.scratch.act_pronunciatio, description
  return execution















