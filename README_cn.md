
# generative_agents_cn 本项目是对斯坦福大学generative_agents项目的简中翻译，仅用于学习使用(only for learning), 如有错误，烦请Issues提醒
## Generative Agents:人类行为的交互式仿真
<p align="center" width="100%">
<img src="cover.png" alt="Smallville" style="width: 80%; min-width: 300px; display: block; margin: auto;">
</p>

****
这个仓库随着我们的论文"[Generative Agents: Interactive Simulacra of Human Behavior](https://arxiv.org/abs/2304.03442)."一起发布。它包括我们的生成代理（模拟可信人类行为的计算代理）及其游戏环境的核心仿真模块。下面将介绍在本地设置仿真环境并将仿真环境播放为演示动画的步骤。

## <img src="https://joonsungpark.s3.amazonaws.com:443/static/assets/characters/profile/Isabella_Rodriguez.png" alt="Generative Isabella">   设置环境

在这一节中，你需要创建一个名为`utils.py`的文件，在这个文件内写入你的OpenAI API 密钥，并下载必要的包。
### Step 1.创建Utils文件

在`reverie/backend_server`文件夹，也就是`reverie.py`所在的目录下，创建一个`utils.py`文件，并把下面的示例代码复制到文件中：
```
# 复制粘贴你的OpenAI API 密钥
openai_api_key = "<Your OpenAI API>"
# 写你的名字
key_owner = "<Name>"

maze_assets_loc = "../../environment/frontend_server/static_dirs/assets"
env_matrix = f"{maze_assets_loc}/the_ville/matrix"
env_visuals = f"{maze_assets_loc}/the_ville/visuals"

fs_storage = "../../environment/frontend_server/storage"
fs_temp_storage = "../../environment/frontend_server/temp_storage"

collision_block_id = "32125"

# 其他
debug = True
```
用你的Open API 密钥替换 `<Your OpenAI API>`，你的名字替换`<name>`
### Step 2.下载requirements.txt内的包
下载`requirements.txt`内列举的所有包（我强烈推荐第一步先按往常一样安装一个虚拟环境）。关于Python版本：我们是在Python 3.9.12内进行测试的。
## <img src="https://joonsungpark.s3.amazonaws.com:443/static/assets/characters/profile/Klaus_Mueller.png" alt="Generative Klaus">    运行一次仿真

为了运行新的仿真，你需要并行启动两个服务：环境服和代理仿真服。
### Step 1.开启环境服务

同样，该环境是作为Django项目实现的。因此，你需要开启Django服务。为此，先在命令行中跳转到`environment/frontend_server`目录（`manage.py`所在位置）。然后运行下面的命令：

    python manage.py runserver


然后，使用你最喜欢的浏览器，访问[http://localhost:8000/](http://localhost:8000/)。如果你看到一条消息：“Your environment server is up and running,”代表你的服务运行正常。为了确保环境服在运行仿真期间持续运行，你需要保持此命令行选项卡保持打开。（注意：我建议使用Chrome或者Safari。Firfox可能会出现一些前端故障，尽管它不会影响实际的仿真。）
### Step 2.开启仿真服务
开启新的命令行终端（在Step1使用的终端必须持续运行环境服务，不要使用那个终端）。跳转到 `reverie/backend_server` 然后运行 `reverie.py` 。

    python reverie.py
仿真服务将被启动，会出现一行提示："Enter the name of the forked simulation: "。为了启动3个代理仿真（Isabella Rodriguez, Maria Lopez, and Klaus Mueller），请输入以下内容

    base_the_ville_isabella_maria_klaus

会出现提示: "Enter the name of the new simulation: "，输入任意名字来表示你当前的仿真（例如，输入"test-simulation"也能运行）

    test-simulation

保持仿真服务运行。在这个阶段，它会出现以下提示: "Enter option: "
### Step 3.运行并保存仿真
在浏览器中跳转到[http://localhost:8000/simulator_home](http://localhost:8000/simulator_home)。你会看到一张Smallville的地图，并且在地图上有一些活动中的代理人物。你可以键盘箭头用来移动地图。请保持这个终端打开，为了开启这个仿真，在你的仿真服务中根据提示 "Enter option" 输入以下命令：

    run <step-count>

注意，你要将上面的`<step-count>`替换为一个整数，指示你要模拟的游戏步骤数。例如，如果你想摸你100个游戏步骤，你应该输入 `run 100`。一个游戏步骤代表游戏里的10秒钟。

你的仿真此时应该在运行，您将在浏览器中看到代理在地图上移动。仿真完成运行后，“Enter option”提示将重新出现。此时，您可以通过使用所需的游戏步骤重新输入运行命令来模拟更多步骤，通过键入“exit”退出仿真而不保存，或者通过键入“fin”保存并退出。

下次运行仿真服务时，你可以通过将仿真的名称提供为分叉仿真来访问保存的仿真。这将允许你从停止时的节点重启仿真。

### Step 4.重放仿真

通过运行环境服务器并打开浏览器的以下地址，你就可以回放已经运行的仿真: `http://localhost:8000/replay/<simulation-name>/<starting-time-step>`。请将`<simulation-name>`替换为你想要回放的仿真名称，并将`<starting-time-step>`替换为你希望重放的整数时间步长。

例如，通过访问下面的地址，你将在时间步骤1开始启动一个预先模拟的示例：

[http://localhost:8000/replay/July1_the_ville_isabella_maria_klaus-step-3-20/1/](http://localhost:8000/replay/July1_the_ville_isabella_maria_klaus-step-3-20/1/)


### Step 5.仿真演示

你可能已经注意到，回放中的所有角色看起来都是相同的。我们想说明，回放功能主要用于调试，不会优先优化仿真文件夹或视觉效果的大小。若要使用适当的角色正确演示仿真，需要首先压缩仿真。要执行此操作，请使用文本编辑器打开位于“reverie”目录中的“compress_sim_storage.py”文件。然后，以目标仿真的名称作为输入，进行压缩。这样做以后，仿真文件将被压缩，以便进行演示。

To start the demo, go to the following address on your browser: `http://localhost:8000/demo/<simulation-name>/<starting-time-step>/<simulation-speed>`. Note that `<simulation-name>` and `<starting-time-step>` denote the same things as mentioned above. `<simulation-speed>` can be set to control the demo speed, where 1 is the slowest, and 5 is the fastest. For instance, visiting the following link will start a pre-simulated example, beginning at time-step 1, with a medium demo speed:  
[http://localhost:8000/demo/July1_the_ville_isabella_maria_klaus-step-3-20/1/3/](http://localhost:8000/demo/July1_the_ville_isabella_maria_klaus-step-3-20/1/3/)

### Tips

我们发现，当OpenAI的API调用达到每小时的费率限制时，它可能会被挂起。此时，你可能需要重新启动仿真。所以我们建议你在进行模拟时经常保存仿真，以确保在需要停止并重新运行仿真时尽可能少地丢失仿真。尤其是当环境中有许多代理时， 从2023年初开始运行这些仿真可能需要一定的开销。

## <img src="https://joonsungpark.s3.amazonaws.com:443/static/assets/characters/profile/Maria_Lopez.png" alt="Generative Maria">  仿真存储的位置
你保存的所有仿真会被放在`environment/frontend_server/storage`文件夹，所有压缩的demo会被放在`environment/frontend_server/compressed_storage`文件夹。

## <img src="https://joonsungpark.s3.amazonaws.com:443/static/assets/characters/profile/Sam_Moore.png" alt="Generative Sam"> 自定义

下面介绍两种可以选择性地自定义仿真的方式。

### 作者和加载代理历史记录

首先是在仿真的开始阶段去初始化带有唯一历史记录的代理。要做到这点，你需要（1）使用一个基础仿真去开启仿真，（2）作者和加载代理历史，下面是更细致的步骤：

#### Step 1.开启一个基础仿真

在仓库中有两个基础仿真：`base_the_ville_n25`有25个代理，`base_the_ville_isabella_maria_klaus`有3个代理。通过接下来的步骤加载其中一个基础仿真。

#### Step 2.加载一个历史文件
然后，当终端提示：”Enter option: “，你要通过下面的命令来加载代理历史：

    call -- load history the_ville/<history_file_name>.csv

你需要把 `<history_file_name>` 替换成一个存在的历史文件。在仓库里面有两个历史文件作为例子：给`base_the_ville_n25`的`agent_history_init_n25.csv`以及给`base_the_ville_isabella_maria_klaus`的`agent_history_init_n3.csv`。


#### Step 3.更多自定义选项

要通过编写自己的历史文件来自定义初始化，请将文件放在以下文件夹中：`environment/frontend_server/static_dirs/assets/the_ville`。自定义历史记录文件的列格式必须与包含的示例历史记录文件相匹配。因此，我们建议通过复制和粘贴存储库中已经存在的文件来启动该过程。

### 创建新的基础仿真

对于更复杂的自定义，你需要自己编写一个基础仿真。最直接的方法是复制一个已经存在的基础仿真文件夹，并根据你的要求重命名和修改它。但是，如果你想要修改他们的名字或者增加
斯坦福小镇地图能容纳的代理数量，你需要用[Tiled](https://www.mapeditor.org/)地图编辑器来更改地图。

## <img src="https://joonsungpark.s3.amazonaws.com:443/static/assets/characters/profile/Eddy_Lin.png" alt="Generative Eddy"> 作者和引用

**Authors:** Joon Sung Park, Joseph C. O'Brien, Carrie J. Cai, Meredith Ringel Morris, Percy Liang, Michael S. Bernstein

如果你使用了这个仓库的代码或数据，请按以下格式引用我们的论文。

```
@inproceedings{Park2023GenerativeAgents,  
author = {Park, Joon Sung and O'Brien, Joseph C. and Cai, Carrie J. and Morris, Meredith Ringel and Liang, Percy and Bernstein, Michael S.},  
title = {Generative Agents: Interactive Simulacra of Human Behavior},  
year = {2023},  
publisher = {Association for Computing Machinery},  
address = {New York, NY, USA},  
booktitle = {In the 36th Annual ACM Symposium on User Interface Software and Technology (UIST '23)},  
keywords = {Human-AI interaction, agents, generative AI, large language models},  
location = {San Francisco, CA, USA},  
series = {UIST '23}
}
```

## <img src="https://joonsungpark.s3.amazonaws.com:443/static/assets/characters/profile/Wolfgang_Schulz.png" alt="Generative Wolfgang">   鸣谢

我们希望你们能关注下面三位出色的画家，尤其是当你想在你的项目中使用这些素材时，他们为这个项目画了游戏素材。

* Background art: [PixyMoon (@_PixyMoon\_)](https://twitter.com/_PixyMoon_)
* Furniture/interior design: [LimeZu (@lime_px)](https://twitter.com/lime_px)
* Character design: [ぴぽ (@pipohi)](https://twitter.com/pipohi)


此外，我们感谢Lindsay Popowski、Philip Guo、Michael Terry和行为科学高级研究中心（CASBS）社区的见解、讨论和支持。最后，Smallville的所有景点都受到了Joon在读本科生和研究生时经常光顾的现实世界景点的启发——他感谢那里的每一个人这些年来为他提供食物和支持。