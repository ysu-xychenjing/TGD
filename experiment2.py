import json
import time
import random
import math
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from sklearn import metrics
from sklearn.metrics.pairwise import cosine_similarity


plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号


"""
对比模型
基于粒子弹性碰撞的信息扩散模型
"""


def initialize_node(folder, graph):
    """
    初始化影响节点
    :param folder:指定文件夹
    :param graph: 图
    """
    # 获取初始化节点集
    node_list = []
    with open(folder + "/initial_nodes.txt", "r+", encoding="UTF-8") as file_list:
        for file in file_list:
            node_list.append(int(file.strip()))
    act_dict = {}
    # 获取信息转发次数
    rt_num = 0
    # 获取Li中的act
    with open(folder + "/" + folder + ".txt", "r+", encoding="UTF-8") as file_list:
        for file in file_list:
            # 转发次数+1
            rt_num += 1
            content = file.strip().split(",")
            user_B = content[1]
            if act_dict.get(user_B):
                act_dict[user_B] += 1
            else:
                act_dict[user_B] = 1
    # 计算初始能量E0
    E0 = pow(math.e, -(1 / rt_num))
    # 平均网络聚类系数
    g = nx.average_clustering(graph)
    for node in graph:
        # W_k = mi * g * Li, mi是节点度数 g是平均网络聚类系数
        # Li是抵抗力 为 1 / (act + η) act是节点i在过去转发信息数 η是极小的正数 保证分母不为0
        mi = len(graph[node])
        if act_dict.get(node):
            Li = 1 / act_dict[node]
        else:
            Li = 1
        # 定义运动粒子穿过阻尼轨道时所需的能量
        graph.nodes[node]["W_k"] = random.uniform(0.01, 0.3) * mi * g * Li
        # 给初始影响节点赋值速度
        if node in node_list:
            graph.nodes[node]["v"] = math.sqrt((2 * E0) / mi)
        else:
            graph.nodes[node]["v"] = 0
        # 改变node节点动能 状态
        change_status(graph, node)


def update_node(graph, t):
    """
    进行传播过程更新节点信息
    :param graph: 图
    """
    # 输入在线时间概率索引列表
    t_list = [0.18133942346084875, 0.14685646824748005, 0.1324323266938351, 0.11426275176227932,
              0.10228794936176575, 0.09592720428971234, 0.09665325321273999, 0.06431742498786912, 0.06592319798346963]
    for node in graph:
        if graph.nodes[node]["status"] == 'O' and random.uniform(0, 1) < t_list[int(t % len(t_list))]:
            # 计算获得动量
            get_E = 0
            # 计算质量
            m_sum = len(graph[node])
            # 处于传播态的节点才可以进行传播
            for ad_node in graph[node]:
                if graph.nodes[ad_node]["status"] == 'S':
                    # 动量mv
                    get_E += len(graph[ad_node]) * graph.nodes[ad_node]["v"]
                    m_sum += len(graph[ad_node])
            graph.nodes[node]["v"] = get_E / m_sum
            # 改变node节点动能 状态
            change_status(graph, node)


def change_status(graph, node):
    """
    # 改变node节点动能 状态
    :param graph: 图
    :param node: 节点号
    """
    # 节点动能
    graph.nodes[node]["E"] = (graph.nodes[node]["v"] * graph.nodes[node]["v"] * len(graph[node])) / 2
    # 给节点状态赋值 初始有观察态 激活态 和 传播态
    if graph.nodes[node]["v"] != 0:
        if (graph.nodes[node]["v"] * graph.nodes[node]["v"] * len(graph[node])) / 2 > graph.nodes[node]["W_k"]:
            # 传播态
            graph.nodes[node]["status"] = 'S'
        else:
            # 激活态
            graph.nodes[node]["status"] = 'A'
    else:
        # 观察态
        graph.nodes[node]["status"] = 'O'


def count_node(graph):
    """
    计算激活节点
    :param graph:图
    :return: 返回激活节点列表
    """
    act_list = []
    for node in graph:
        if graph.nodes[node]["status"] in ['S', 'A']:
            act_list.append(node)
    return act_list


def mape_value(y_true, y_pred):
    """
    计算mape值
    :param y_true: 真实值
    :param y_pred: 预测值
    :return: MAPE误差
    """
    return np.mean(np.abs((y_pred - y_true) / y_true)) * 100


def calculate_error(predictValue, folder):
    """
    计算误差
    :param predictValue: 预测值列表
    """
    realValue = []
    node_set = set()
    with open(folder + "/content_dict.json", "r+", encoding="UTF-8") as file_list:
        for file in file_list:
            content = json.loads(file)
            cur_set = set()
            for value in content["value"]:
                con = json.loads(value)
                if con["user_A"] not in node_set:
                    node_set.add(con["user_A"])
                    cur_set.add(con["user_A"])
                if con["user_B"] not in node_set:
                    node_set.add(con["user_B"])
                    cur_set.add(con["user_B"])
            realValue.append(len(cur_set))
    num1 = 0
    plot_list1 = []
    plot_list2 = predictValue
    for i in range(len(realValue)):
        num1 += realValue[i]
        plot_list1.append(num1)
    # 准确值
    accuracy = []
    for i in range(len(plot_list1)):
        accuracy.append(1 - abs(plot_list1[i] - plot_list2[i]) / plot_list1[i])
    print("准确率：", format(sum(accuracy) / len(accuracy) * 100, ".2f"), "%")
    plot_list1 = np.array(plot_list1)
    plot_list2 = np.array(plot_list2)
    print("余弦相似度：", cosine_similarity([plot_list1], [plot_list2])[0][0])
    mse = metrics.mean_squared_error(plot_list1, plot_list2)  # 均方误差MSE
    rmse = np.sqrt(mse)  # 均方根误差
    mae = metrics.mean_absolute_error(plot_list1, plot_list2)  # 平均绝对误差
    print("RMSE = ", format(rmse, ".2f"))
    print("MAE = ", format(mae, ".2f"))
    # 拟合优度
    r2_score = metrics.r2_score(plot_list1, plot_list2)
    print("R2_score = ", format(r2_score, ".4f"))
    mape = mape_value(plot_list1, plot_list2)
    print("MAPE = ", format(mape, ".2f"), "%")
    x = [i for i in range(36)]
    plt.plot(x, plot_list1, "b-", label="Real Value")
    plt.plot(x, plot_list2, "r-", label="Predict Value")
    plt.fill_between(x, plot_list1, plot_list2, facecolor='yellow', alpha=0.6)
    plt.xlabel("Time")
    plt.ylabel("Number of diffusion")
    plt.legend(loc=0)
    plt.savefig("Particle-model.png", dpi=600, bbox_inches='tight')
    plt.show()


if __name__ == "__main__":
    print("开始读取节点信息...")
    # 文件夹
    folder = "rt_bahrain"
    # 节点集 nodes_list
    nodes_list = []
    with open(folder + "/rt_node.txt", "r+", encoding="UTF-8") as file_list:
        for file in file_list:
            nodes_list.append(int(file.strip()))
    print("读取完成！")
    print("开始读取边信息...")
    # 边集 edges_list
    edges_list = []
    with open(folder + "/rt_edge.txt", "r+", encoding="UTF-8") as file_list:
        for file in file_list:
            edges_list.append((int(file.strip().split(" ")[0]), int(file.strip().split(" ")[1])))
    print("读取完成！")
    print("开始导入图...")
    graph = nx.Graph()
    graph.add_nodes_from(nodes_list)
    graph.add_edges_from(edges_list)
    print("导入完成！")
    print("开始模拟信息传播...")
    # 初始化网络
    initialize_node(folder, graph)
    act_list = count_node(graph)
    # 记录每一阶段新的节点数
    new_node_list = []
    print("初始激活节点：", len(act_list))
    # 前一轮激活节点
    before_node = act_list
    plot_list = []
    for i in range(36):
        update_node(graph, i)
        act_list = count_node(graph)
        # 计算更新节点
        new_node = list(set(act_list) - set(before_node))
        new_node_list.append(new_node)
        before_node = act_list
        plot_list.append(len(act_list))
        print("第", i + 1, "轮传播结束,总共激活节点,", len(act_list), "个")
    # 存储节点
    with open(folder + "/experiment2.json", "w+", encoding="UTF-8") as file:
        for new_node in new_node_list:
            item = {
                "nodes": new_node
            }
            file.write(json.dumps(item, ensure_ascii=False) + "\n")
    calculate_error(plot_list, folder)







