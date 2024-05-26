"""
Author: Joon Sung Park (joonspk@stanford.edu)

File: perceive.py
Description: This defines the "Perceive" module for generative agents. 
"""
"""
作者: 朴俊成(joonspk@stanford.edu)

文件: perceive.py
描述: 这个文件定义了生成式代理的Perceive模块。
"""
import sys
sys.path.append('../../')

from operator import itemgetter
from global_methods import *
from persona.prompt_template.gpt_structure import *
from persona.prompt_template.run_gpt_prompt import *

def generate_poig_score(persona, event_type, description): 
  if "is idle" in description: 
    return 1

  if event_type == "event": 
    return run_gpt_prompt_event_poignancy(persona, description)[0]
  elif event_type == "chat": 
    return run_gpt_prompt_chat_poignancy(persona, 
                           persona.scratch.act_description)[0]

def perceive(persona, maze): 
  """
  Perceives events around the persona and saves it to the memory, both events 
  and spaces. 

  We first perceive the events nearby the persona, as determined by its 
  <vision_r>. If there are a lot of events happening within that radius, we 
  take the <att_bandwidth> of the closest events. Finally, we check whether
  any of them are new, as determined by <retention>. If they are new, then we
  save those and return the <ConceptNode> instances for those events. 

  INPUT: 
    persona: An instance of <Persona> that represents the current persona. 
    maze: An instance of <Maze> that represents the current maze in which the 
          persona is acting in. 
  OUTPUT: 
    ret_events: a list of <ConceptNode> that are perceived and new. 
  """
  """
  感知角色周围的事件并保存到记忆中去，包括事件记忆和空间记忆。
  首先感知角色周围的事件，由<vision_r>决定。如果在此半径范围内有很多时间发生，则
  按照<att_bandwidth>选择最近的事件。最后，检查有没有事件属于新事件，由<retention>
  决定。如果它们是新的，则保存那些事件并且返回那些事件的<ConceptNode>实例。

  输入：
    persona：代表当前persona的<Persona>实例
  输出：
    ret_events：被感知并且是新的<ConceptNode>列表
  """
  # PERCEIVE SPACE
  # We get the nearby tiles given our current tile and the persona's vision
  # radius. 

  # 感知空间
  # 给定的当前地图块和角色的可视范围，返回周围的地图块。
  nearby_tiles = maze.get_nearby_tiles(persona.scratch.curr_tile, 
                                       persona.scratch.vision_r)

  # We then store the perceived space. Note that the s_mem of the persona is
  # in the form of a tree constructed using dictionaries. 

  # 存储感知空间。注意角色的s_mem是将字典构造为树的格式。
  for i in nearby_tiles: 
    i = maze.access_tile(i)
    if i["world"]: 
      if (i["world"] not in persona.s_mem.tree): 
        persona.s_mem.tree[i["world"]] = {}
    if i["sector"]: 
      if (i["sector"] not in persona.s_mem.tree[i["world"]]): 
        persona.s_mem.tree[i["world"]][i["sector"]] = {}
    if i["arena"]: 
      if (i["arena"] not in persona.s_mem.tree[i["world"]]
                                              [i["sector"]]): 
        persona.s_mem.tree[i["world"]][i["sector"]][i["arena"]] = []
    if i["game_object"]: 
      if (i["game_object"] not in persona.s_mem.tree[i["world"]]
                                                    [i["sector"]]
                                                    [i["arena"]]): 
        persona.s_mem.tree[i["world"]][i["sector"]][i["arena"]] += [
                                                             i["game_object"]]

  # PERCEIVE EVENTS. 
  # We will perceive events that take place in the same arena as the
  # persona's current arena. 

  # 感知事件。
  # 感知与角色当前所在场地相同的事件。
  curr_arena_path = maze.get_tile_path(persona.scratch.curr_tile, "arena")
  # We do not perceive the same event twice (this can happen if an object is
  # extended across multiple tiles).

  # 不会多次感知相同的事件（如果一个对象跨越多个方格的情况下可能发生）。
  percept_events_set = set()
  # We will order our percept based on the distance, with the closest ones
  # getting priorities. 

  # 程序将根据距离来排序感知，最近的一个获得最高优先级。
  percept_events_list = []
  # First, we put all events that are occuring in the nearby tiles into the
  # percept_events_list

  # 首先，把周围地图块正在发生的所有事件放入percept_events_list
  for tile in nearby_tiles: 
    tile_details = maze.access_tile(tile)
    if tile_details["events"]: 
      if maze.get_tile_path(tile, "arena") == curr_arena_path:  
        # This calculates the distance between the persona's current tile, 
        # and the target tile.

        # 这里计算了角色所在地图块到目标地图块的距离。
        dist = math.dist([tile[0], tile[1]], 
                         [persona.scratch.curr_tile[0], 
                          persona.scratch.curr_tile[1]])
        # Add any relevant events to our temp set/list with the distant info. 
        # 将任何相关事件和远程信息添加到临时集合/列表中。
        for event in tile_details["events"]: 
          if event not in percept_events_set: 
            percept_events_list += [[dist, event]]
            percept_events_set.add(event)

  # We sort, and perceive only persona.scratch.att_bandwidth of the closest
  # events. If the bandwidth is larger, then it means the persona can perceive
  # more elements within a small area. 

  # 分类并感知最近事件的persona.scratch.att_bandwidth。如果带宽更大，表示角色可以
  # 在小场地内感知更多的元素。
  percept_events_list = sorted(percept_events_list, key=itemgetter(0))
  perceived_events = []
  for dist, event in percept_events_list[:persona.scratch.att_bandwidth]: 
    perceived_events += [event]

  # Storing events. 
  # <ret_events> is a list of <ConceptNode> instances from the persona's 
  # associative memory. 

  # 保存事件。
  # <ret_events>是一个角色联想记忆的<ConceptNode>实例列表。
  ret_events = []
  for p_event in perceived_events: 
    s, p, o, desc = p_event
    if not p: 
      # If the object is not present, then we default the event to "idle".
      # 如果对象没有被初始化，给定默认事件"idle"。
      p = "is"
      o = "idle"
      desc = "idle"
    desc = f"{s.split(':')[-1]} is {desc}"
    p_event = (s, p, o)

    # We retrieve the latest persona.scratch.retention events. If there is  
    # something new that is happening (that is, p_event not in latest_events),
    # then we add that event to the a_mem and return it. 

    # 获取最新的persona.scratch.retention事件。如果有新事件发生（即p_event不在
    # latest_events中），则将该事件添加到a_mem中并返回。
    latest_events = persona.a_mem.get_summarized_latest_events(
                                    persona.scratch.retention)
    if p_event not in latest_events:
      # We start by managing keywords. 

      # 通过管理关键词开启事件。
      keywords = set()
      sub = p_event[0]
      obj = p_event[2]
      if ":" in p_event[0]: 
        sub = p_event[0].split(":")[-1]
      if ":" in p_event[2]: 
        obj = p_event[2].split(":")[-1]
      keywords.update([sub, obj])

      # Get event embedding
      # 获取事件嵌入
      desc_embedding_in = desc
      if "(" in desc: 
        desc_embedding_in = (desc_embedding_in.split("(")[1]
                                              .split(")")[0]
                                              .strip())
      if desc_embedding_in in persona.a_mem.embeddings: 
        event_embedding = persona.a_mem.embeddings[desc_embedding_in]
      else: 
        event_embedding = get_embedding(desc_embedding_in)
      event_embedding_pair = (desc_embedding_in, event_embedding)
      
      # Get event poignancy. 
      # 获取事件的犀利行。
      event_poignancy = generate_poig_score(persona, 
                                            "event", 
                                            desc_embedding_in)

      # If we observe the persona's self chat, we include that in the memory
      # of the persona here.

      # 如果观察到角色的自聊天，将它包含到角色记忆中。
      chat_node_ids = []
      if p_event[0] == f"{persona.name}" and p_event[1] == "chat with": 
        curr_event = persona.scratch.act_event
        if persona.scratch.act_description in persona.a_mem.embeddings: 
          chat_embedding = persona.a_mem.embeddings[
                             persona.scratch.act_description]
        else: 
          chat_embedding = get_embedding(persona.scratch
                                                .act_description)
        chat_embedding_pair = (persona.scratch.act_description, 
                               chat_embedding)
        chat_poignancy = generate_poig_score(persona, "chat", 
                                             persona.scratch.act_description)
        chat_node = persona.a_mem.add_chat(persona.scratch.curr_time, None,
                      curr_event[0], curr_event[1], curr_event[2], 
                      persona.scratch.act_description, keywords, 
                      chat_poignancy, chat_embedding_pair, 
                      persona.scratch.chat)
        chat_node_ids = [chat_node.node_id]

      # Finally, we add the current event to the agent's memory. 
      # 最后，把当前事件加入到代理的记忆中。
      ret_events += [persona.a_mem.add_event(persona.scratch.curr_time, None,
                           s, p, o, desc, keywords, event_poignancy, 
                           event_embedding_pair, chat_node_ids)]
      persona.scratch.importance_trigger_curr -= event_poignancy
      persona.scratch.importance_ele_n += 1

  return ret_events




  











