"""
Author: Joon Sung Park (joonspk@stanford.edu)

File: retrieve.py
Description: This defines the "Retrieve" module for generative agents. 
"""
"""
作者：朴俊成 (joonspk@stanford.edu)

文件：retrieve.py
描述：它定义了生成式代理的Retrieve模块。
"""
import sys
sys.path.append('../../')

from global_methods import *
from persona.prompt_template.gpt_structure import *

from numpy import dot
from numpy.linalg import norm

def retrieve(persona, perceived): 
  """
  This function takes the events that are perceived by the persona as input
  and returns a set of related events and thoughts that the persona would 
  need to consider as context when planning. 

  INPUT: 
    perceived: a list of event <ConceptNode>s that represent any of the events
    `         that are happening around the persona. What is included in here
              are controlled by the att_bandwidth and retention 
              hyper-parameters.
  OUTPUT: 
    retrieved: a dictionary of dictionary. The first layer specifies an event, 
               while the latter layer specifies the "curr_event", "events", 
               and "thoughts" that are relevant.
  """
  """
  这个函数接收被角色感知的事件作为输入，并返回角色在计划时需要作为上下文考虑的相关事件和
  想法。
  输入：
    perceived：一个代表着发生在角色周围的事件<ConceptNode>s列表。att_bandwidth和retention
              控制着哪些应该被包括在内。
  输出：
    retrieved：一个二维字典。外层代表一个事件，内层代表相关的"curr_event"，"events"和
              "thoughts"
  """
  # We rerieve events and thoughts separately. 
  # 分开检索事件和想法。
  retrieved = dict()
  for event in perceived: 
    retrieved[event.description] = dict()
    retrieved[event.description]["curr_event"] = event
    
    relevant_events = persona.a_mem.retrieve_relevant_events(
                        event.subject, event.predicate, event.object)
    retrieved[event.description]["events"] = list(relevant_events)

    relevant_thoughts = persona.a_mem.retrieve_relevant_thoughts(
                          event.subject, event.predicate, event.object)
    retrieved[event.description]["thoughts"] = list(relevant_thoughts)
    
  return retrieved


def cos_sim(a, b): 
  """
  This function calculates the cosine similarity between two input vectors 
  'a' and 'b'. Cosine similarity is a measure of similarity between two 
  non-zero vectors of an inner product space that measures the cosine 
  of the angle between them.

  INPUT: 
    a: 1-D array object 
    b: 1-D array object 
  OUTPUT: 
    A scalar value representing the cosine similarity between the input 
    vectors 'a' and 'b'.
  
  Example input: 
    a = [0.3, 0.2, 0.5]
    b = [0.2, 0.2, 0.5]
  """
  """
  这个函数计算两个输入的向量'a'和'b'的余弦相似度。余弦相似度是两个非0向量的相似度的
  表示，它计算出两个向量之间的余弦角度。
  输入: 
    a: 1维数组对象
    b: 1维数组对象
  输出：
    一个代表输入向量'a'和'b'的余弦相似度的标量值。
  示例输出：
    a = [0.3, 0.2, 0.5]
    b = [0.2, 0.2, 0.5]
  """
  return dot(a, b)/(norm(a)*norm(b))


def normalize_dict_floats(d, target_min, target_max):
  """
  This function normalizes the float values of a given dictionary 'd' between 
  a target minimum and maximum value. The normalization is done by scaling the
  values to the target range while maintaining the same relative proportions 
  between the original values.

  INPUT: 
    d: Dictionary. The input dictionary whose float values need to be 
       normalized.
    target_min: Integer or float. The minimum value to which the original 
                values should be scaled.
    target_max: Integer or float. The maximum value to which the original 
                values should be scaled.
  OUTPUT: 
    d: A new dictionary with the same keys as the input but with the float
       values normalized between the target_min and target_max.

  Example input: 
    d = {'a':1.2,'b':3.4,'c':5.6,'d':7.8}

    target_min = -5
    target_max = 5
  """
  """
  这个函数将给定字典'd'的浮点值在目标最小值和最大值之间进行标准化。它是通过将值缩放
  到目标范围，同时保持原始值之间相同的相对比例来完成的。
  
  输入：
    d：字典。需要被标准化的输入字典。
    target_min：整数或者浮点数，指原始值应该被缩放成的最小值。
    target_max：整数或者浮点数，指原始值应该被缩放成的最大值。
  输出：
    d：一个拥有着与输入的字典相同的键，但值被标准化为target_min到target_max之间的新字典。
  示例输出：
    d = {'a':1.2,'b':3.4,'c':5.6,'d':7.8}

    target_min = -5
    target_max = 5
  """
  min_val = min(val for val in d.values())
  max_val = max(val for val in d.values())
  range_val = max_val - min_val

  if range_val == 0: 
    for key, val in d.items(): 
      d[key] = (target_max - target_min)/2
  else: 
    for key, val in d.items():
      d[key] = ((val - min_val) * (target_max - target_min) 
                / range_val + target_min)
  return d


def top_highest_x_values(d, x):
  """
  This function takes a dictionary 'd' and an integer 'x' as input, and 
  returns a new dictionary containing the top 'x' key-value pairs from the 
  input dictionary 'd' with the highest values.

  INPUT: 
    d: Dictionary. The input dictionary from which the top 'x' key-value pairs 
       with the highest values are to be extracted.
    x: Integer. The number of top key-value pairs with the highest values to
       be extracted from the input dictionary.
  OUTPUT: 
    A new dictionary containing the top 'x' key-value pairs from the input 
    dictionary 'd' with the highest values.
  
  Example input: 
    d = {'a':1.2,'b':3.4,'c':5.6,'d':7.8}
    x = 3
  """
  """
  这个函数接收一个字典'd'和一个整数'x'，并返回一个新字典，其中包含输入字典'd'中最高值的
  前'x'键值对。

  输入：
    d：字典。从中提取具有最高值的顶部"x"键值对。
    x：整数。
  输出：
    一个新字典，包含输入字典'd'中最高值的前'x'键值对。
  示例输出：
    d = {'a':1.2,'b':3.4,'c':5.6,'d':7.8}
    x = 3
  """
  top_v = dict(sorted(d.items(), 
                      key=lambda item: item[1], 
                      reverse=True)[:x])
  return top_v


def extract_recency(persona, nodes):
  """
  Gets the current Persona object and a list of nodes that are in a 
  chronological order, and outputs a dictionary that has the recency score
  calculated.

  INPUT: 
    persona: Current persona whose memory we are retrieving. 
    nodes: A list of Node object in a chronological order. 
  OUTPUT: 
    recency_out: A dictionary whose keys are the node.node_id and whose values
                 are the float that represents the recency score. 
  """
  """
  获取当前Persona对象和一个按时间顺序排列的节点列表，然后输出一个字典，该字典存储着
  最近计算出来的得分。

  输入：
    persona：正在检索记忆的角色。
    nodes：按时间顺序排列的节点对象列表。
  输出：
    recencyy_out：一个键为node.node_id，值为代表最近分数的浮点数的字典。
  """
  recency_vals = [persona.scratch.recency_decay ** i 
                  for i in range(1, len(nodes) + 1)]
  
  recency_out = dict()
  for count, node in enumerate(nodes): 
    recency_out[node.node_id] = recency_vals[count]

  return recency_out


def extract_importance(persona, nodes):
  """
  Gets the current Persona object and a list of nodes that are in a 
  chronological order, and outputs a dictionary that has the importance score
  calculated.

  INPUT: 
    persona: Current persona whose memory we are retrieving. 
    nodes: A list of Node object in a chronological order. 
  OUTPUT: 
    importance_out: A dictionary whose keys are the node.node_id and whose 
                    values are the float that represents the importance score.
  """
  """
  获取当前Persona对象和一个按时间顺序排列的节点列表，并输出一个被计算出来的重要性分数
  字典。

  输入：
    persona：正在检索记忆的当前角色。
    nodes：按时间顺序排列的节点对象列表
  输出：
    importance_out：一个键为node.node_id，值为代表重要性分数浮点数的字典。
  """
  importance_out = dict()
  for count, node in enumerate(nodes): 
    importance_out[node.node_id] = node.poignancy

  return importance_out


def extract_relevance(persona, nodes, focal_pt): 
  """
  Gets the current Persona object, a list of nodes that are in a 
  chronological order, and the focal_pt string and outputs a dictionary 
  that has the relevance score calculated.

  INPUT: 
    persona: Current persona whose memory we are retrieving. 
    nodes: A list of Node object in a chronological order. 
    focal_pt: A string describing the current thought of revent of focus.  
  OUTPUT: 
    relevance_out: A dictionary whose keys are the node.node_id and whose values
                 are the float that represents the relevance score. 
  """
  """
  接收当前角色对象、按时间顺序排列的节点列表和focal_pt字符串，然后输出一个包含被计算出来的
  相关性分数字典。
  输入：
    persona：正在检索记忆的当前角色
    nodes：按时间顺序排列的节点对象列表。
    focal_pt：一个描述当前注意力想法和事件的字符串
  输出：
    relevance_out：一个字典，键为node.node_id，值为代表相关性分数的浮点数。
  """
  focal_embedding = get_embedding(focal_pt)

  relevance_out = dict()
  for count, node in enumerate(nodes): 
    node_embedding = persona.a_mem.embeddings[node.embedding_key]
    relevance_out[node.node_id] = cos_sim(node_embedding, focal_embedding)

  return relevance_out


def new_retrieve(persona, focal_points, n_count=30): 
  """
  Given the current persona and focal points (focal points are events or 
  thoughts for which we are retrieving), we retrieve a set of nodes for each
  of the focal points and return a dictionary. 

  INPUT: 
    persona: The current persona object whose memory we are retrieving. 
    focal_points: A list of focal points (string description of the events or
                  thoughts that is the focus of current retrieval).
  OUTPUT: 
    retrieved: A dictionary whose keys are a string focal point, and whose 
               values are a list of Node object in the agent's associative 
               memory.

  Example input:
    persona = <persona> object 
    focal_points = ["How are you?", "Jane is swimming in the pond"]
  """
  """
  给定当前角色和关注点（关注点是正在检索的事件或者想法），对每个关注点检索一个节点集合
  并返回一个字典。

  输入：
    persona：正在检索记忆的当前角色对象。
    focal_points：关注点列表（当前检索关注的事件或者想法的字符串描述）
  输出：
    retrieved：一个字典，键为字符串关注点，值为代理联想记忆的节点对象列表。
  示例输出：
    persona = <persona> object 
    focal_points = ["How are you?", "Jane is swimming in the pond"]
  """
  # <retrieved> is the main dictionary that we are returning
  # <retrieved>是正在返回的主要字典。
  retrieved = dict() 
  for focal_pt in focal_points: 
    # Getting all nodes from the agent's memory (both thoughts and events) and
    # sorting them by the datetime of creation.
    # You could also imagine getting he raw conversation, but for now. 

    # 从代理的记忆（包括想法和事件）中获取所有节点，然后将他们按照创建日期进行分类。
    # 你也可以想象得到他的原始对话。
    nodes = [[i.last_accessed, i]
              for i in persona.a_mem.seq_event + persona.a_mem.seq_thought
              if "idle" not in i.embedding_key]
    nodes = sorted(nodes, key=lambda x: x[0])
    nodes = [i for created, i in nodes]

    # Calculating the component dictionaries and normalizing them.
    # 计算组件字典并将他们标准化。
    recency_out = extract_recency(persona, nodes)
    recency_out = normalize_dict_floats(recency_out, 0, 1)
    importance_out = extract_importance(persona, nodes)
    importance_out = normalize_dict_floats(importance_out, 0, 1)  
    relevance_out = extract_relevance(persona, nodes, focal_pt)
    relevance_out = normalize_dict_floats(relevance_out, 0, 1)

    # Computing the final scores that combines the component values. 
    # Note to self: test out different weights. [1, 1, 1] tends to work
    # decently, but in the future, these weights should likely be learned, 
    # perhaps through an RL-like process.

    # 通过合并组件值计算最终分数。写给自己的标注：测试不同的权重。[1, 1, 1]倾向于
    # 合适地工作，但是在未来，这些权重也应该被计算在内，可能通过一个RL-like过程。
    # gw = [1, 1, 1]
    # gw = [1, 2, 1]
    gw = [0.5, 3, 2]
    master_out = dict()
    for key in recency_out.keys(): 
      master_out[key] = (persona.scratch.recency_w*recency_out[key]*gw[0] 
                     + persona.scratch.relevance_w*relevance_out[key]*gw[1] 
                     + persona.scratch.importance_w*importance_out[key]*gw[2])

    master_out = top_highest_x_values(master_out, len(master_out.keys()))
    for key, val in master_out.items(): 
      print (persona.a_mem.id_to_node[key].embedding_key, val)
      print (persona.scratch.recency_w*recency_out[key]*1, 
             persona.scratch.relevance_w*relevance_out[key]*1, 
             persona.scratch.importance_w*importance_out[key]*1)

    # Extracting the highest x values.
    # <master_out> has the key of node.id and value of float. Once we get the 
    # highest x values, we want to translate the node.id into nodes and return
    # the list of nodes.

    # 导出最高的x值。
    # <master_out>具有键为node.id以及浮点数值。一旦拿到了最高的x值，我们想要将node.id
    # 翻译到节点中然后返回节点列表。
    master_out = top_highest_x_values(master_out, n_count)
    master_nodes = [persona.a_mem.id_to_node[key] 
                    for key in list(master_out.keys())]

    for n in master_nodes: 
      n.last_accessed = persona.scratch.curr_time
      
    retrieved[focal_pt] = master_nodes

  return retrieved













