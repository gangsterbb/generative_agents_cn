
# generative_agents_cn 本项目是对斯坦福大学generative_agents项目的简中翻译，仅用于学习使用(only for learning), 如有错误，烦请Issues提醒
## Generative Agents: Interactive Simulacra of Human Behavior 
## Generative Agents: 人类行为的交互式模拟
<p align="center" width="100%">
<img src="cover.png" alt="Smallville" style="width: 80%; min-width: 300px; display: block; margin: auto;">
</p>

This repository accompanies our research paper titled "[Generative Agents: Interactive Simulacra of Human Behavior](https://arxiv.org/abs/2304.03442)." It contains our core simulation module for  generative agents—computational agents that simulate believable human behaviors—and their game environment. Below, we document the steps for setting up the simulation environment on your local machine and for replaying the simulation as a demo animation.

这个仓库随着我们的论文"[Generative Agents: Interactive Simulacra of Human Behavior](https://arxiv.org/abs/2304.03442)."一起发布。它包括我们的生成代理（模拟可信人类行为的计算代理）及其游戏环境的核心模拟模块。下面将介绍在本地设置模拟环境并将模拟环境播放为演示动画的步骤。

## <img src="https://joonsungpark.s3.amazonaws.com:443/static/assets/characters/profile/Isabella_Rodriguez.png" alt="Generative Isabella">   Setting Up the Environment 设置环境
To set up your environment, you will need to generate a `utils.py` file that contains your OpenAI API key and download the necessary packages.

在这一节中，你需要创建一个名为`utils.py`的文件，在这个文件内写入你的OpenAI API 密钥，并下载必要的包。
### Step 1. Generate Utils File 创建Utils文件
In the `reverie/backend_server` folder (where `reverie.py` is located), create a new file titled `utils.py` and copy and paste the content below into the file:

在`reverie/backend_server`文件夹，也就是`reverie.py`所在的目录下，创建一个`utils.py`文件，并把下面的示例代码复制到文件中：
```
# Copy and paste your OpenAI API Key
# 复制粘贴你的OpenAI API 密钥
openai_api_key = "<Your OpenAI API>"
# Put your name
# 写你的名字
key_owner = "<Name>"

maze_assets_loc = "../../environment/frontend_server/static_dirs/assets"
env_matrix = f"{maze_assets_loc}/the_ville/matrix"
env_visuals = f"{maze_assets_loc}/the_ville/visuals"

fs_storage = "../../environment/frontend_server/storage"
fs_temp_storage = "../../environment/frontend_server/temp_storage"

collision_block_id = "32125"

# Verbose 
# 其他
debug = True
```
Replace `<Your OpenAI API>` with your OpenAI API key, and `<name>` with your name.

用你的Open API 密钥替换 `<Your OpenAI API>`，你的名字替换`<name>`
### Step 2. Install requirements.txt 下载requirements.txt内的包
Install everything listed in the `requirements.txt` file (I strongly recommend first setting up a virtualenv as usual). A note on Python version: we tested our environment on Python 3.9.12. 

下载`requirements.txt`内列举的所有包（我强烈推荐第一步先按往常一样安装一个虚拟环境）。关于Python版本：我们是在Python 3.9.12内进行测试的。
## <img src="https://joonsungpark.s3.amazonaws.com:443/static/assets/characters/profile/Klaus_Mueller.png" alt="Generative Klaus">   Running a Simulation 运行一次模拟
To run a new simulation, you will need to concurrently start two servers: the environment server and the agent simulation server.

为了运行新的模拟，你需要并行启动两个服务：环境服和代理模拟服。
### Step 1. Starting the Environment Server 开启环境服务
Again, the environment is implemented as a Django project, and as such, you will need to start the Django server. To do this, first navigate to `environment/frontend_server` (this is where `manage.py` is located) in your command line. Then run the following command:

同样，该环境是作为Django项目实现的。因此，你需要开启Django服务。为此，先在命令行中跳转到`environment/frontend_server`目录（`manage.py`所在位置）。然后运行下面的命令：

    python manage.py runserver

Then, on your favorite browser, go to [http://localhost:8000/](http://localhost:8000/). If you see a message that says, "Your environment server is up and running," your server is running properly. Ensure that the environment server continues to run while you are running the simulation, so keep this command-line tab open! (Note: I recommend using either Chrome or Safari. Firefox might produce some frontend glitches, although it should not interfere with the actual simulation.)

然后，使用你最喜欢的浏览器，访问[http://localhost:8000/](http://localhost:8000/)。如果你看到一条消息：“Your environment server is up and running,”代表你的服务运行正常。为了确保环境服在运行模拟期间持续运行，你需要保持此命令行选项卡保持打开。（注意：我建议使用Chrome或者Safari。Firfox可能会出现一些前端故障，尽管它不会影响实际的模拟。）
### Step 2. Starting the Simulation Server 开启模拟服务
Open up another command line (the one you used in Step 1 should still be running the environment server, so leave that as it is). Navigate to `reverie/backend_server` and run `reverie.py`.

开启新的命令行终端（在Step1使用的终端必须持续运行环境服务，不要使用那个终端）。跳转到 `reverie/backend_server` 然后运行 `reverie.py` 。

    python reverie.py
This will start the simulation server. A command-line prompt will appear, asking the following: "Enter the name of the forked simulation: ". To start a 3-agent simulation with Isabella Rodriguez, Maria Lopez, and Klaus Mueller, type the following:

模拟服务将被启动，会出现一行提示："Enter the name of the forked simulation: "。为了启动3个代理模拟（Isabella Rodriguez, Maria Lopez, and Klaus Mueller），请输入以下内容

    base_the_ville_isabella_maria_klaus
The prompt will then ask, "Enter the name of the new simulation: ". Type any name to denote your current simulation (e.g., just "test-simulation" will do for now).

会出现提示: "Enter the name of the new simulation: "，输入任意名字来表示你当前的模拟（例如，输入"test-simulation"也能运行）

    test-simulation
Keep the simulator server running. At this stage, it will display the following prompt: "Enter option: "

保持模拟服务运行。在这个阶段，它会出现以下提示: "Enter option: "
### Step 3. Running and Saving the Simulation 运行并保存模拟
On your browser, navigate to [http://localhost:8000/simulator_home](http://localhost:8000/simulator_home). You should see the map of Smallville, along with a list of active agents on the map. You can move around the map using your keyboard arrows. Please keep this tab open. To run the simulation, type the following command in your simulation server in response to the prompt, "Enter option":

在浏览器中跳转到[http://localhost:8000/simulator_home](http://localhost:8000/simulator_home)。你会看到一张Smallville的地图，并且在地图上有一些活动中的代理人物。你可以键盘箭头用来移动地图。请保持这个终端打开，为了开启这个模拟，在你的模拟服务中根据提示 "Enter option" 输入以下命令：

    run <step-count>
Note that you will want to replace `<step-count>` above with an integer indicating the number of game steps you want to simulate. For instance, if you want to simulate 100 game steps, you should input `run 100`. One game step represents 10 seconds in the game.

注意，你要将上面的`<step-count>`替换为一个整数，指示你要模拟的游戏步骤数。例如，如果你想摸你100个游戏步骤，你应该输入 `run 100`。一个游戏步骤代表游戏里的10秒钟。


Your simulation should be running, and you will see the agents moving on the map in your browser. Once the simulation finishes running, the "Enter option" prompt will re-appear. At this point, you can simulate more steps by re-entering the run command with your desired game steps, exit the simulation without saving by typing `exit`, or save and exit by typing `fin`.

The saved simulation can be accessed the next time you run the simulation server by providing the name of your simulation as the forked simulation. This will allow you to restart your simulation from the point where you left off.

### Step 4. Replaying a Simulation
You can replay a simulation that you have already run simply by having your environment server running and navigating to the following address in your browser: `http://localhost:8000/replay/<simulation-name>/<starting-time-step>`. Please make sure to replace `<simulation-name>` with the name of the simulation you want to replay, and `<starting-time-step>` with the integer time-step from which you wish to start the replay.

For instance, by visiting the following link, you will initiate a pre-simulated example, starting at time-step 1:  
[http://localhost:8000/replay/July1_the_ville_isabella_maria_klaus-step-3-20/1/](http://localhost:8000/replay/July1_the_ville_isabella_maria_klaus-step-3-20/1/)

### Step 5. Demoing a Simulation
You may have noticed that all character sprites in the replay look identical. We would like to clarify that the replay function is primarily intended for debugging purposes and does not prioritize optimizing the size of the simulation folder or the visuals. To properly demonstrate a simulation with appropriate character sprites, you will need to compress the simulation first. To do this, open the `compress_sim_storage.py` file located in the `reverie` directory using a text editor. Then, execute the `compress` function with the name of the target simulation as its input. By doing so, the simulation file will be compressed, making it ready for demonstration.

To start the demo, go to the following address on your browser: `http://localhost:8000/demo/<simulation-name>/<starting-time-step>/<simulation-speed>`. Note that `<simulation-name>` and `<starting-time-step>` denote the same things as mentioned above. `<simulation-speed>` can be set to control the demo speed, where 1 is the slowest, and 5 is the fastest. For instance, visiting the following link will start a pre-simulated example, beginning at time-step 1, with a medium demo speed:  
[http://localhost:8000/demo/July1_the_ville_isabella_maria_klaus-step-3-20/1/3/](http://localhost:8000/demo/July1_the_ville_isabella_maria_klaus-step-3-20/1/3/)

### Tips
We've noticed that OpenAI's API can hang when it reaches the hourly rate limit. When this happens, you may need to restart your simulation. For now, we recommend saving your simulation often as you progress to ensure that you lose as little of the simulation as possible when you do need to stop and rerun it. Running these simulations, at least as of early 2023, could be somewhat costly, especially when there are many agents in the environment.

## <img src="https://joonsungpark.s3.amazonaws.com:443/static/assets/characters/profile/Maria_Lopez.png" alt="Generative Maria">   Simulation Storage Location
All simulations that you save will be located in `environment/frontend_server/storage`, and all compressed demos will be located in `environment/frontend_server/compressed_storage`. 

## <img src="https://joonsungpark.s3.amazonaws.com:443/static/assets/characters/profile/Sam_Moore.png" alt="Generative Sam">   Customization

There are two ways to optionally customize your simulations. 

### Author and Load Agent History
First is to initialize agents with unique history at the start of the simulation. To do this, you would want to 1) start your simulation using one of the base simulations, and 2) author and load agent history. More specifically, here are the steps:

#### Step 1. Starting Up a Base Simulation 
There are two base simulations included in the repository: `base_the_ville_n25` with 25 agents, and `base_the_ville_isabella_maria_klaus` with 3 agents. Load one of the base simulations by following the steps until step 2 above. 

#### Step 2. Loading a History File 
Then, when prompted with "Enter option: ", you should load the agent history by responding with the following command:

    call -- load history the_ville/<history_file_name>.csv
Note that you will need to replace `<history_file_name>` with the name of an existing history file. There are two history files included in the repo as examples: `agent_history_init_n25.csv` for `base_the_ville_n25` and `agent_history_init_n3.csv` for `base_the_ville_isabella_maria_klaus`. These files include semicolon-separated lists of memory records for each of the agents—loading them will insert the memory records into the agents' memory stream.

#### Step 3. Further Customization 
To customize the initialization by authoring your own history file, place your file in the following folder: `environment/frontend_server/static_dirs/assets/the_ville`. The column format for your custom history file will have to match the example history files included. Therefore, we recommend starting the process by copying and pasting the ones that are already in the repository.

### Create New Base Simulations
For a more involved customization, you will need to author your own base simulation files. The most straightforward approach would be to copy and paste an existing base simulation folder, renaming and editing it according to your requirements. This process will be simpler if you decide to keep the agent names unchanged. However, if you wish to change their names or increase the number of agents that the Smallville map can accommodate, you might need to directly edit the map using the [Tiled](https://www.mapeditor.org/) map editor.


## <img src="https://joonsungpark.s3.amazonaws.com:443/static/assets/characters/profile/Eddy_Lin.png" alt="Generative Eddy">   Authors and Citation 

**Authors:** Joon Sung Park, Joseph C. O'Brien, Carrie J. Cai, Meredith Ringel Morris, Percy Liang, Michael S. Bernstein

Please cite our paper if you use the code or data in this repository. 
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

## <img src="https://joonsungpark.s3.amazonaws.com:443/static/assets/characters/profile/Wolfgang_Schulz.png" alt="Generative Wolfgang">   Acknowledgements

We encourage you to support the following three amazing artists who have designed the game assets for this project, especially if you are planning to use the assets included here for your own project: 
* Background art: [PixyMoon (@_PixyMoon\_)](https://twitter.com/_PixyMoon_)
* Furniture/interior design: [LimeZu (@lime_px)](https://twitter.com/lime_px)
* Character design: [ぴぽ (@pipohi)](https://twitter.com/pipohi)

In addition, we thank Lindsay Popowski, Philip Guo, Michael Terry, and the Center for Advanced Study in the Behavioral Sciences (CASBS) community for their insights, discussions, and support. Lastly, all locations featured in Smallville are inspired by real-world locations that Joon has frequented as an undergraduate and graduate student---he thanks everyone there for feeding and supporting him all these years.


