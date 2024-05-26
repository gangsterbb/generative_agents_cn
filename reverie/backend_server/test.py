"""
Author: Joon Sung Park (joonspk@stanford.edu)

File: gpt_structure.py
Description: Wrapper functions for calling OpenAI APIs.
"""
"""
作者：朴俊成 (joonspk@stanford.edu)
文件：gpt_structure.py
描述：为OpenAI API的调用封装函数。
"""
import json
import random
import openai
import time 

from utils import *
openai.api_key = openai_api_key

def ChatGPT_request(prompt): 
  """
  Given a prompt and a dictionary of GPT parameters, make a request to OpenAI
  server and returns the response. 
  ARGS:
    prompt: a str prompt
    gpt_parameter: a python dictionary with the keys indicating the names of  
                   the parameter and the values indicating the parameter 
                   values.   
  RETURNS: 
    a str of GPT-3's response. 
  """
  """
  给定一个提示词和一个GPT参数的字典，发起一个请求到OpenAI并接收返回的值。
  参数：
    prompt: 字符串的prompt
    gpt_paramter: 一个以参数名为键，参数值为值的python字典。
  返回：
    一个GPT-3回复的字符串
  """
  # temp_sleep()
  try: 
    completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo", 
    messages=[{"role": "user", "content": prompt}]
    )
    return completion["choices"][0]["message"]["content"]
  
  except: 
    print ("ChatGPT ERROR")
    return "ChatGPT ERROR"

prompt = """
---
Character 1: Maria Lopez is working on her physics degree and streaming games on Twitch to make some extra money. She visits Hobbs Cafe for studying and eating just about everyday.
Character 2: Klaus Mueller is writing a research paper on the effects of gentrification in low-income communities.

角色1：Maria Lopez 正在攻读物理学位，并在Twitch上直播游戏，以赚取额外的钱。她几乎每天都去Hobbs咖啡馆学习和吃饭。
角色2：Klaus Mueller 正在写一篇关于低收入社区中产阶级化影响的研究论文。

Past Context: 
138 minutes ago, Maria Lopez and Klaus Mueller were already conversing about Maria's research paper mentioned by Klaus This context takes place after that conversation.

以往的上下文：
138分钟之前，Maria Lopez and Klaus Mueller 已经在讨论Klaus提到的Maria的研究论文，这个背景发生在那次谈话之后。

Current Context: Maria Lopez was attending her Physics class (preparing for the next lecture) when Maria Lopez saw Klaus Mueller in the middle of working on his research paper at the library (writing the introduction).
Maria Lopez is thinking of initating a conversation with Klaus Mueller.
Current Location: library in Oak Hill College

当前背景：Maria正在上物理块（为下一节课做准备），这时Maria看到Klaus正在图书馆写他的研究论文（写引言）。Maria想和Klaus谈谈。
当前位置：橡树山学院图书馆


(This is what is in Maria Lopez's head: Maria Lopez should remember to follow up with Klaus Mueller about his thoughts on her research paper. Beyond this, Maria Lopez doesn't necessarily know anything more about Klaus Mueller) 

(This is what is in Klaus Mueller's head: Klaus Mueller should remember to ask Maria Lopez about her research paper, as she found it interesting that he mentioned it. Beyond this, Klaus Mueller doesn't necessarily know anything more about Maria Lopez) 

（这是Maria的想法：Maria应该记得跟进Klaus对她研究论文的看法。除此之外，Maria不一定对Klaus有更多的了解。）
（这是Klaus的想法：Klaus应该记得向Maria询问她的研究论文，因为她觉得Klaus提到这篇论文很有趣。除此之外，Klaus不一定对Maria有更多的了解。）

Here is their conversation. 
下面是他们的对话。

Maria Lopez: "
---
Output the response to the prompt above in json. The output should be a list of list where the inner lists are in the form of ["<Name>", "<Utterance>"]. Output multiple utterances in ther conversation until the conversation comes to a natural conclusion.
Example output json:
{"output": "[["Jane Doe", "Hi!"], ["John Doe", "Hello there!"] ... ]"}

以json格式输出对上述提示词的响应。应该输出一个二维列表，其内部列表的形式为["<Name>", "<Utterance>"]。在他们的对话中输出多个话语，直到对话
自然结束。
输出的json示例：
{"output": "[["Jane Doe", "Hi!"], ["John Doe", "Hello there!"] ... ]"}
"""

print (ChatGPT_request(prompt))












