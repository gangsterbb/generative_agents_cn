"""
Author: Joon Sung Park (joonspk@stanford.edu)

File: reflect.py
Description: This defines the "Reflect" module for generative agents. 
"""
"""
作者：朴俊成 (joonspk@stanford.edu)

文件：reflect.py
描述：它定义了生成式代理的Reflect模块。
"""
import sys
sys.path.append('../../')

import datetime
import random

from numpy import dot
from numpy.linalg import norm

from global_methods import *
from persona.prompt_template.run_gpt_prompt import *
from persona.prompt_template.gpt_structure import *
from persona.cognitive_modules.retrieve import *

def generate_focal_points(persona, n=3): 
  if debug: print ("GNS FUNCTION: <generate_focal_points>")
  
  nodes = [[i.last_accessed, i]
            for i in persona.a_mem.seq_event + persona.a_mem.seq_thought
            if "idle" not in i.embedding_key]

  nodes = sorted(nodes, key=lambda x: x[0])
  nodes = [i for created, i in nodes]

  statements = ""
  for node in nodes[-1*persona.scratch.importance_ele_n:]: 
    statements += node.embedding_key + "\n"

  return run_gpt_prompt_focal_pt(persona, statements, n)[0]


def generate_insights_and_evidence(persona, nodes, n=5): 
  if debug: print ("GNS FUNCTION: <generate_insights_and_evidence>")

  statements = ""
  for count, node in enumerate(nodes): 
    statements += f'{str(count)}. {node.embedding_key}\n'

  ret = run_gpt_prompt_insight_and_guidance(persona, statements, n)[0]

  print (ret)
  try: 

    for thought, evi_raw in ret.items(): 
      evidence_node_id = [nodes[i].node_id for i in evi_raw]
      ret[thought] = evidence_node_id
    return ret
  except: 
    return {"this is blank": "node_1"} 


def generate_action_event_triple(act_desp, persona): 
  """TODO 

  INPUT: 
    act_desp: the description of the action (e.g., "sleeping")
    persona: The Persona class instance
  OUTPUT: 
    a string of emoji that translates action description.
  EXAMPLE OUTPUT: 
    "🧈🍞"
  """
  """
  输入：
    act_desp：行为的描述(e.g., "sleeping")
    persona：Persona类实例
  输出：
    表示行为描述的表情字符串。
  示例输出：
"🧈🍞"
  """
  if debug: print ("GNS FUNCTION: <generate_action_event_triple>")
  return run_gpt_prompt_event_triple(act_desp, persona)[0]


def generate_poig_score(persona, event_type, description): 
  if debug: print ("GNS FUNCTION: <generate_poig_score>")

  if "is idle" in description: 
    return 1

  if event_type == "event" or event_type == "thought": 
    return run_gpt_prompt_event_poignancy(persona, description)[0]
  elif event_type == "chat": 
    return run_gpt_prompt_chat_poignancy(persona, 
                           persona.scratch.act_description)[0]



def generate_planning_thought_on_convo(persona, all_utt):
  if debug: print ("GNS FUNCTION: <generate_planning_thought_on_convo>")
  return run_gpt_prompt_planning_thought_on_convo(persona, all_utt)[0]


def generate_memo_on_convo(persona, all_utt):
  if debug: print ("GNS FUNCTION: <generate_memo_on_convo>")
  return run_gpt_prompt_memo_on_convo(persona, all_utt)[0]




def run_reflect(persona):
  """
  Run the actual reflection. We generate the focal points, retrieve any 
  relevant nodes, and generate thoughts and insights. 

  INPUT: 
    persona: Current Persona object
  Output: 
    None
  """
  """
  运行真正反思的地方。生成关注点，检索任何相关的节点，并生成想法和见解。
  输入：
    persona：当前Persona对象
  输出：
    无
  """
  # Reflection requires certain focal points. Generate that first. 
  # 反思要求确切的关注点。先生成关注点。
  focal_points = generate_focal_points(persona, 3)
  # Retrieve the relevant Nodes object for each of the focal points. 
  # <retrieved> has keys of focal points, and values of the associated Nodes. 
  
  # 为每个关注点生成相关的节点对象。
  # <retrieved>的键是关注点，值是相关节点。
  retrieved = new_retrieve(persona, focal_points)

  # For each of the focal points, generate thoughts and save it in the 
  # agent's memory. 

  # 对每个关注点，生成想法并保存到代理的记忆中。
  for focal_pt, nodes in retrieved.items(): 
    xx = [i.embedding_key for i in nodes]
    for xxx in xx: print (xxx)

    thoughts = generate_insights_and_evidence(persona, nodes, 5)
    for thought, evidence in thoughts.items(): 
      created = persona.scratch.curr_time
      expiration = persona.scratch.curr_time + datetime.timedelta(days=30)
      s, p, o = generate_action_event_triple(thought, persona)
      keywords = set([s, p, o])
      thought_poignancy = generate_poig_score(persona, "thought", thought)
      thought_embedding_pair = (thought, get_embedding(thought))

      persona.a_mem.add_thought(created, expiration, s, p, o, 
                                thought, keywords, thought_poignancy, 
                                thought_embedding_pair, evidence)


def reflection_trigger(persona): 
  """
  Given the current persona, determine whether the persona should run a 
  reflection. 
  
  Our current implementation checks for whether the sum of the new importance
  measure has reached the set (hyper-parameter) threshold.

  INPUT: 
    persona: Current Persona object
  Output: 
    True if we are running a new reflection. 
    False otherwise. 
  """
  """
  给定当前的角色，确定角色是否应该运行反思。

  我们当前的实现检查新的重要性度量的总和是否达到设置（超参数）的阈值。

  输入：
    persona：当前Persona对象
  输出：
    如果正在运行一次新反思则返回True，否则返回False

  """
  print (persona.scratch.name, "persona.scratch.importance_trigger_curr::", persona.scratch.importance_trigger_curr)
  print (persona.scratch.importance_trigger_max)

  if (persona.scratch.importance_trigger_curr <= 0 and 
      [] != persona.a_mem.seq_event + persona.a_mem.seq_thought): 
    return True 
  return False


def reset_reflection_counter(persona): 
  """
  We reset the counters used for the reflection trigger. 

  INPUT: 
    persona: Current Persona object
  Output: 
    None
  """
  """
  重置所有反思触发器使用的计数器。

  输入：
    persona：当前Persona对象
  输出：
    无
  """
  persona_imt_max = persona.scratch.importance_trigger_max
  persona.scratch.importance_trigger_curr = persona_imt_max
  persona.scratch.importance_ele_n = 0


def reflect(persona):
  """
  The main reflection module for the persona. We first check if the trigger 
  conditions are met, and if so, run the reflection and reset any of the 
  relevant counters. 

  INPUT: 
    persona: Current Persona object
  Output: 
    None
  """
  """
  角色的主要反思模块。首先检查是否达到触发条件，如果是的话，运行反思并重置所有相关的计数器。
  
  输入：
    persona：当前Persona对象
  输出：
    无
  """
  if reflection_trigger(persona): 
    run_reflect(persona)
    reset_reflection_counter(persona)



  # print (persona.scratch.name, "al;sdhfjlsad", persona.scratch.chatting_end_time)
  if persona.scratch.chatting_end_time: 
    # print("DEBUG", persona.scratch.curr_time + datetime.timedelta(0,10))
    if persona.scratch.curr_time + datetime.timedelta(0,10) == persona.scratch.chatting_end_time: 
      # print ("KABOOOOOMMMMMMM")
      all_utt = ""
      if persona.scratch.chat: 
        for row in persona.scratch.chat:  
          all_utt += f"{row[0]}: {row[1]}\n"

      # planning_thought = generate_planning_thought_on_convo(persona, all_utt)
      # print ("init planning: aosdhfpaoisdh90m     ::", f"For {persona.scratch.name}'s planning: {planning_thought}")
      # planning_thought = generate_planning_thought_on_convo(target_persona, all_utt)
      # print ("target planning: aosdhfpaodish90m     ::", f"For {target_persona.scratch.name}'s planning: {planning_thought}")

      # memo_thought = generate_memo_on_convo(persona, all_utt)
      # print ("init memo: aosdhfpaoisdh90m     ::", f"For {persona.scratch.name} {memo_thought}")
      # memo_thought = generate_memo_on_convo(target_persona, all_utt)
      # print ("target memo: aosdhfpsaoish90m     ::", f"For {target_persona.scratch.name} {memo_thought}")
      

      # make sure you set the fillings as well

      # print (persona.a_mem.get_last_chat(persona.scratch.chatting_with).node_id)

      evidence = [persona.a_mem.get_last_chat(persona.scratch.chatting_with).node_id]

      planning_thought = generate_planning_thought_on_convo(persona, all_utt)
      planning_thought = f"For {persona.scratch.name}'s planning: {planning_thought}"

      created = persona.scratch.curr_time
      expiration = persona.scratch.curr_time + datetime.timedelta(days=30)
      s, p, o = generate_action_event_triple(planning_thought, persona)
      keywords = set([s, p, o])
      thought_poignancy = generate_poig_score(persona, "thought", planning_thought)
      thought_embedding_pair = (planning_thought, get_embedding(planning_thought))

      persona.a_mem.add_thought(created, expiration, s, p, o, 
                                planning_thought, keywords, thought_poignancy, 
                                thought_embedding_pair, evidence)



      memo_thought = generate_memo_on_convo(persona, all_utt)
      memo_thought = f"{persona.scratch.name} {memo_thought}"

      created = persona.scratch.curr_time
      expiration = persona.scratch.curr_time + datetime.timedelta(days=30)
      s, p, o = generate_action_event_triple(memo_thought, persona)
      keywords = set([s, p, o])
      thought_poignancy = generate_poig_score(persona, "thought", memo_thought)
      thought_embedding_pair = (memo_thought, get_embedding(memo_thought))

      persona.a_mem.add_thought(created, expiration, s, p, o, 
                                memo_thought, keywords, thought_poignancy, 
                                thought_embedding_pair, evidence)



























