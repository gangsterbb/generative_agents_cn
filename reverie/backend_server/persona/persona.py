"""
Author: Joon Sung Park (joonspk@stanford.edu)

File: persona.py
Description: Defines the Persona class that powers the agents in Reverie. 

Note (May 1, 2023) -- this is effectively GenerativeAgent class. Persona was
the term we used internally back in 2022, taking from our Social Simulacra 
paper.
"""
"""
作者：朴俊成 (joonspk@stanford.edu)
文件：persona.py
描述：定义Persona类，用于驱动Reverie中的代理

小记 (May 1, 2023) -- 这是实际上的GenerativeAgent类。Persona是我们在2022年内部使用
的术语，来自我们的Social Simulacra论文
"""
import math
import sys
import datetime
import random
sys.path.append('../')

from global_methods import *

from persona.memory_structures.spatial_memory import *
from persona.memory_structures.associative_memory import *
from persona.memory_structures.scratch import *

from persona.cognitive_modules.perceive import *
from persona.cognitive_modules.retrieve import *
from persona.cognitive_modules.plan import *
from persona.cognitive_modules.reflect import *
from persona.cognitive_modules.execute import *
from persona.cognitive_modules.converse import *

class Persona: 
  def __init__(self, name, folder_mem_saved=False):
    # PERSONA BASE STATE 
    # <name> is the full name of the persona. This is a unique identifier for
    # the persona within Reverie. 
    
    # PERSONA 基本状态
    # <name>是指persona的全名。这是Reverie中角色的唯一标识符。
    self.name = name

    # PERSONA MEMORY 
    # If there is already memory in folder_mem_saved, we load that. Otherwise,
    # we create new memory instances. 
    # <s_mem> is the persona's spatial memory. 

    # PERSONA 记忆
    # 如果在folder_mem_saved中有记忆，将优先加载此记忆，否则就创建新的记忆实例。
    # <s_mem>是角色的空间记忆。
    f_s_mem_saved = f"{folder_mem_saved}/bootstrap_memory/spatial_memory.json"
    self.s_mem = MemoryTree(f_s_mem_saved)
    # <s_mem> is the persona's associative memory. 
    # <s_mem>是角色的联想记忆。
    f_a_mem_saved = f"{folder_mem_saved}/bootstrap_memory/associative_memory"
    self.a_mem = AssociativeMemory(f_a_mem_saved)
    # <scratch> is the persona's scratch (short term memory) space. 
    # <scratch> 是角色的短时记忆空间。
    scratch_saved = f"{folder_mem_saved}/bootstrap_memory/scratch.json"
    self.scratch = Scratch(scratch_saved)


  def save(self, save_folder): 
    """
    Save persona's current state (i.e., memory). 

    INPUT: 
      save_folder: The folder where we wil be saving our persona's state. 
    OUTPUT: 
      None
    """
    """
    保存角色当前的状态(i.e., 记忆)

    输入: 
      save_folder:保存角色状态的文件夹名称
    输出: 
      无
    """
    # Spatial memory contains a tree in a json format. 
    # e.g., {"double studio": 
    #         {"double studio": 
    #           {"bedroom 2": 
    #             ["painting", "easel", "closet", "bed"]}}}

    # 空间记忆包含一个json格式的树。
    # e.g., {"double studio": 
    #         {"double studio": 
    #           {"bedroom 2": 
    #             ["painting", "easel", "closet", "bed"]}}}
    f_s_mem = f"{save_folder}/spatial_memory.json"
    self.s_mem.save(f_s_mem)
    
    # Associative memory contains a csv with the following rows: 
    # [event.type, event.created, event.expiration, s, p, o]
    # e.g., event,2022-10-23 00:00:00,,Isabella Rodriguez,is,idle

    # 关联记忆包含是指有着如下行数据的csv：
    # [event.type, event.created, event.expiration, s, p, o]
    # e.g., event,2022-10-23 00:00:00,,Isabella Rodriguez,is,idle

    f_a_mem = f"{save_folder}/associative_memory"
    self.a_mem.save(f_a_mem)

    # Scratch contains non-permanent data associated with the persona. When 
    # it is saved, it takes a json form. When we load it, we move the values
    # to Python variables. 

    # 划痕存储与角色关联的非持久性数据，并以json格式保存。在加载的时候把它的值保存到python变量中。
    f_scratch = f"{save_folder}/scratch.json"
    self.scratch.save(f_scratch)


  def perceive(self, maze):
    """
    This function takes the current maze, and returns events that are 
    happening around the persona. Importantly, perceive is guided by 
    two key hyper-parameter for the  persona: 1) att_bandwidth, and 
    2) retention. 

    First, <att_bandwidth> determines the number of nearby events that the 
    persona can perceive. Say there are 10 events that are within the vision
    radius for the persona -- perceiving all 10 might be too much. So, the 
    persona perceives the closest att_bandwidth number of events in case there
    are too many events. 

    Second, the persona does not want to perceive and think about the same 
    event at each time step. That's where <retention> comes in -- there is 
    temporal order to what the persona remembers. So if the persona's memory
    contains the current surrounding events that happened within the most 
    recent retention, there is no need to perceive that again. xx

    INPUT: 
      maze: Current <Maze> instance of the world. 
    OUTPUT: 
      a list of <ConceptNode> that are perceived and new. 
        See associative_memory.py -- but to get you a sense of what it 
        receives as its input: "s, p, o, desc, persona.scratch.curr_time"
    """
    """
    这个函数接收当前的迷宫，然后返回角色周边发生的事件。要注意的是，角色感知被两个
    重要的超参数控制：（1）att_bandwith和（2）retention。

    首先，<att_bandwith>决定着角色能够感知的周围事件数量。假设有10个发生在角色可
    视半径内的事件-感知全部10个事件可能太多了。所以，角色感知最接近<att_bandwith>
    的事件数量以免有太多的事件要处理。

    其次，角色不希望在一个时间步骤内感知和考虑相同的事件。这就是<retention>的作用了
    人物角色的记忆是有时间顺序的。所以如果角色的记忆包含了最近一次记忆中发生的当前周
    围事件，那么就没有必要再去感知它了。
    输入：
      maze：小镇当前的<Maze>实例。
    输出：
      一个被感知的新<ConceptNode>列表。
      查看 associative_memory.py -- 为了让你了解它接收到的输入：
      "s, p, o, desc, persona.scratch.curr_time"
    """
    return perceive(self, maze)


  def retrieve(self, perceived):
    """
    This function takes the events that are perceived by the persona as input
    and returns a set of related events and thoughts that the persona would 
    need to consider as context when planning. 

    INPUT: 
      perceive: a list of <ConceptNode> that are perceived and new.  
    OUTPUT: 
      retrieved: dictionary of dictionary. The first layer specifies an event,
                 while the latter layer specifies the "curr_event", "events", 
                 and "thoughts" that are relevant.
    """
    """
    这个函数以被角色感知的事件作为输入，并把角色在计划时需要考虑作为上下文的想法事件和
    想法集合返回。

    输入：
      perceive: 一个被感知且是新的<ConceptNode>列表
    输出：
      retrieved: 字典的字典。第一层表示一个事件，第二层表示相关的当前事件、事件和想法。
    """
    return retrieve(self, perceived)


  def plan(self, maze, personas, new_day, retrieved):
    """
    Main cognitive function of the chain. It takes the retrieved memory and 
    perception, as well as the maze and the first day state to conduct both 
    the long term and short term planning for the persona. 

    INPUT: 
      maze: Current <Maze> instance of the world. 
      personas: A dictionary that contains all persona names as keys, and the 
                Persona instance as values. 
      new_day: This can take one of the three values. 
        1) <Boolean> False -- It is not a "new day" cycle (if it is, we would
           need to call the long term planning sequence for the persona). 
        2) <String> "First day" -- It is literally the start of a simulation,
           so not only is it a new day, but also it is the first day. 
        2) <String> "New day" -- It is a new day. 
      retrieved: dictionary of dictionary. The first layer specifies an event,
                 while the latter layer specifies the "curr_event", "events", 
                 and "thoughts" that are relevant.
    OUTPUT 
      The target action address of the persona (persona.scratch.act_address).
    """
    """
    链条的主认知函数。它接收恢复记忆、感知、迷宫和第一天的状态来构建角色的长短期计划。

    输入：
      maze：小镇当前的<Maze>类实例。
      personas：一个字典，以所有角色名作为键，Persona实例作为值。
      new_day：可以接收以下三种值。
      1) <Boolean> False -- 表示它不是新一天的循环 (如果它是，则需要调用角色的
         长期计划序列). 
      2) <String> "First day" -- 它就是变量名的含义，仿真的开始，所以它不仅是
         新的一天，也是第一天。 
      3) <String> "New day" -- 它是新的一天
    输出：
      角色的目标行动地址（persona.scratch.act_address）。
    """
    return plan(self, maze, personas, new_day, retrieved)


  def execute(self, maze, personas, plan):
    """
    This function takes the agent's current plan and outputs a concrete 
    execution (what object to use, and what tile to travel to). 

    INPUT: 
      maze: Current <Maze> instance of the world. 
      personas: A dictionary that contains all persona names as keys, and the 
                Persona instance as values. 
      plan: The target action address of the persona  
            (persona.scratch.act_address).
    OUTPUT: 
      execution: A triple set that contains the following components: 
        <next_tile> is a x,y coordinate. e.g., (58, 9)
        <pronunciatio> is an emoji.
        <description> is a string description of the movement. e.g., 
        writing her next novel (editing her novel) 
        @ double studio:double studio:common room:sofa
    """
    """
    这个函数接收代理当前的计划，然后输出一个具体的执行过程(使用什么对象，并移
    动到哪个位置)

    输入：
      maze：当前世界的<Maze>类示例
      personas：一个字典，以所有角色的名字为键，Persona类实例为值。
      plan：角色的目标行为地址（persona.scratch.act_address）
    输出:
      execution：一个元组集合，存储了以下的内容：
      <next_tile>是一个x，y坐标。例如，(58, 9)
      <pronunciatio>是一个表情。
      <description>是动作的一个字符串描述。例如，写下她的下一篇小说（
      编辑她的小说）
      @ double studio:double studio:common room:sofa
    """
    return execute(self, maze, personas, plan)


  def reflect(self):
    """
    Reviews the persona's memory and create new thoughts based on it. 

    INPUT: 
      None
    OUTPUT: 
      None
    """
    """
    回忆角色的记忆然后基于回忆创建新想法。

    输入：
      无
    输出：
      无
    """
    reflect(self)


  def move(self, maze, personas, curr_tile, curr_time):
    """
    This is the main cognitive function where our main sequence is called. 

    INPUT: 
      maze: The Maze class of the current world. 
      personas: A dictionary that contains all persona names as keys, and the 
                Persona instance as values. 
      curr_tile: A tuple that designates the persona's current tile location 
                 in (row, col) form. e.g., (58, 39)
      curr_time: datetime instance that indicates the game's current time. 
    OUTPUT: 
      execution: A triple set that contains the following components: 
        <next_tile> is a x,y coordinate. e.g., (58, 9)
        <pronunciatio> is an emoji.
        <description> is a string description of the movement. e.g., 
        writing her next novel (editing her novel) 
        @ double studio:double studio:common room:sofa
    """
    """
    这个函数是主要序列被调用的主要感知函数。

    输入：
      maze：当前世界的Maze类。
      personas：一个字典，以所有角色的名字为键，Persona类实例为值。
      curr_tile：一个元组，表示角色的当前地图位置坐标。例如：(58, 39)
      curr_time：表示游戏当前时间的日期时间实例
    输出：
      execution：一个元组集合，存储了以下的内容：
      <next_tile>是一个x，y坐标。例如，(58, 9)
      <pronunciatio>是一个表情。
      <description>是动作的一个字符串描述。例如，写下她的下一篇小说（
      编辑她的小说）
      @ double studio:double studio:common room:sofa
    """
    # Updating persona's scratch memory with <curr_tile>. 
    # 用<curr_tile>更新角色的临时记忆。
    self.scratch.curr_tile = curr_tile

    # We figure out whether the persona started a new day, and if it is a new
    # day, whether it is the very first day of the simulation. This is 
    # important because we set up the persona's long term plan at the start of
    # a new day. 

    # 判断角色是否开启新的一天，如果是新的一天，则再判断是否为仿真开启的第一天。这很重要
    # 因为我们在第一天时生成角色的长期计划。
    new_day = False
    if not self.scratch.curr_time: 
      new_day = "First day"
    elif (self.scratch.curr_time.strftime('%A %B %d')
          != curr_time.strftime('%A %B %d')):
      new_day = "New day"
    self.scratch.curr_time = curr_time

    # Main cognitive sequence begins here. 
    # 主要的感知序列在这里开始。
    perceived = self.perceive(maze)
    retrieved = self.retrieve(perceived)
    plan = self.plan(maze, personas, new_day, retrieved)
    self.reflect()

    # <execution> is a triple set that contains the following components: 
    # <next_tile> is a x,y coordinate. e.g., (58, 9)
    # <pronunciatio> is an emoji. e.g., "\ud83d\udca4"
    # <description> is a string description of the movement. e.g., 
    #   writing her next novel (editing her novel) 
    #   @ double studio:double studio:common room:sofa

    # execution：一个元组集合，存储了以下的内容：
    # <next_tile>是一个x，y坐标。例如，(58, 9)
    # <pronunciatio>是一个表情。
    # <description>是动作的一个字符串描述。例如，写下她的下一篇小说（
    # 编辑她的小说）
    # @ double studio:double studio:common room:sofa
    return self.execute(maze, personas, plan)


  def open_convo_session(self, convo_mode): 
    open_convo_session(self, convo_mode)
    




































