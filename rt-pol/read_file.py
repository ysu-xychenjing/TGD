"""
本文件需要的包
"""
import json
import time
import datetime
import math
import random
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from sklearn.metrics.pairwise import cosine_similarity
from math import sqrt
from sklearn import metrics

plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号


# 计算mape值
def mape(y_true, y_pred):
    return np.mean(np.abs((y_pred - y_true) / y_true)) * 100


# 划分时间
def divide_time_stamp(time_start, time_end, n):
    # 时间数组
    start_Array = time.strptime(time_start, "%Y-%m-%d %H:%M:%S")
    end_Array = time.strptime(time_end, "%Y-%m-%d %H:%M:%S")
    # 时间戳
    start_stamp = int(time.mktime(start_Array))
    end_stamp = int(time.mktime(end_Array))
    # 将时间划分为n个阶段
    time_list = [int(node) for node in np.linspace(start_stamp, end_stamp, n + 1)]
    time_str_list = []
    for t in time_list:
        time_Array = time.localtime(t)
        time_str = time.strftime("%Y-%m-%d %H:%M:%S", time_Array)
        time_str_list.append(time_str)
    return time_str_list


"""
rt-pol.txt文件
生成rt_node.txt    rt_edge.txt    rt_pol.json
"""
# node_set = set()
# edge_set = set()
# content_list = []
# with open("rt-pol/rt-pol.txt", "r+", encoding="UTF-8") as file_list:
#     # i = 0
#     for file in file_list:
#         content = file.strip().split(",")
#         content_list.append(content)
#         node_set.add(content[0])
#         node_set.add(content[1])
#         edge_set.add((content[0], content[1]))
#         # i += 1
#         # if i == 10:
#         #     break
# print("数据集中共有", len(node_set), "个节点")
# print("数据集中共有", len(edge_set), "条边")
# print("数据集中共有", len(content_list), "条信息")
# # 生成节点集
# print("开始生成点集...")
# with open("rt-pol/rt_node.txt", "w+", encoding="UTF-8") as file:
#     for node in list(node_set):
#         file.write(node + "\n")
# print("生成完毕！")
# # 生成边集
# print("开始生成边集...")
# with open("rt-pol/rt_edge.txt", "w+", encoding="UTF-8") as file:
#     for edge in list(edge_set):
#         file.write(edge[0] + " " + edge[1] + "\n")
# print("生成完毕！")
# # 将txt文件转换为json文件并将时间戳转换为时间值
# print("开始生成json文件...")
# with open("rt-pol/rt_pol.json", "w+", encoding="UTF-8") as file:
#     for content in content_list:
#         user_A = content[0]
#         user_B = content[1]
#         # 时间戳
#         time_stamp = content[2]
#         # 转换成 年-月-日 小时：分钟：秒
#         time_Array = time.localtime(int(time_stamp))
#         time_str = time.strftime("%Y-%m-%d %H:%M:%S", time_Array)
#         item = {
#             "user_A": user_A,
#             "user_B": user_B,
#             "time": time_str
#         }
#         file.write(json.dumps(item, ensure_ascii=False) + "\n")
# print("生成完毕！")


"""
利用rt_pol.json生成时间轴文件rt_time.txt
"""
# time_list = []
# with open("rt-pol/rt_pol.json", "r+", encoding="UTF-8") as file_list:
#     # i = 0
#     for file in file_list:
#         content = json.loads(file)
#         # time = content["time"]
#         # time_set.add(time.strip().split(" ")[0])
#         time_list.append(content["time"].strip())
#         # i += 1
#         # if i == 10:
#         #     break
# time_list = sorted(list(time_list))
# print(len(time_list), time_list[0], time_list[-1])
# time_dict = {}  # 将时间做成字典 {"天"："转发数量"}
# for time in time_list:
#     if time_dict.get(time.split(" ")[0]):
#         time_dict[time.split(" ")[0]].append(time)
#     else:
#         time_dict[time.split(" ")[0]] = [time]
# print(len(time_dict))
# plot_list = []
# for key in time_dict:
#     plot_list.append(len(time_dict[key]))
# plt.plot(plot_list, "ro-")
# plt.show()


"""
利用rt_bahrain.json查看时间分布情况
第一个时间为 2010-09-14 12:00:21
最后一个时间为 2010-11-02 06:41:59
即文件摘取时间为 2010-09-14 12:00:00--2010-11-02 07:00:00
"""
# time_list = []
# with open("rt_pol.json", "r+", encoding="UTF-8") as file_list:
#     for file in file_list:
#         content = json.loads(file)
#         time_list.append(content["time"].strip())
# time_list = sorted(list(time_list))
# print(len(time_list), time_list[0], time_list[-1])
# time_dict = {}  # 将时间做成字典 {"天"："转发数量"}
# for time in time_list:
#     if time_dict.get(time.split(" ")[0]):
#         time_dict[time.split(" ")[0]].append(time)
#     else:
#         time_dict[time.split(" ")[0]] = [time]
# print(len(time_dict))


"""
生成content_dict.json
将内容划分为多个阶段
"""
# content_dict = {}
# node_set = set()
# # 时间字符串 年-月-日 小时:分钟:秒
# time_start = "2010-09-14 12:00:00"
# time_end = "2010-11-02 07:00:00"
# time_str_list = divide_time_stamp(time_start, time_end, 50)
# space_list = []
# for i in range(len(time_str_list) - 1):
#     space_list.append([time_str_list[i], time_str_list[i + 1]])
# content_dict = {}
# node_set = set()
# with open("rt_pol.json", "r+", encoding="UTF-8") as file_list:
#     for file in file_list:
#         content = json.loads(file)
#         for num, space in enumerate(space_list):
#             if space[0] <= content["time"] < space[1]:
#                 if content_dict.get(num):
#                     content_dict[num].append(file)
#                 else:
#                     content_dict[num] = [file]
#                 break
# with open("content_dict.json", "w+", encoding="UTF-8") as file:
#     for key in content_dict:
#         item = {
#             "key": key,
#             "value": content_dict[key]
#         }
#         file.write(json.dumps(item, ensure_ascii=False) + "\n")


"""
从content_dict.json中的每个阶段 看每个阶段影响的节点数
"""
# # 存储每轮节点
# num_list = []
# node_set = set()
# num = 0
# l = []
# with open("content_dict.json", "r+", encoding="UTF-8") as file_list:
#     # 当前轮的节点数
#     cur_list = []
#     for file in file_list:
#         # 每条是一个json语句
#         content = json.loads(file)
#         for value in content["value"]:
#             # 每一个json语句中存储的也是json语句 解析第二次
#             con = json.loads(value)
#             num += 1
#             if con["user_A"] not in node_set:
#                 node_set.add(con["user_A"])
#                 cur_list.append(con["user_A"])
#             if con["user_B"] not in node_set:
#                 node_set.add(con["user_B"])
#                 cur_list.append(con["user_B"])
#         num_list.append(cur_list)
#         cur_list = []
# print([len(num) for num in num_list])


"""
初始种子节点集
生成initial_nodes.txt
"""
# initial_nodes = set()
# with open("content_dict.json", "r+", encoding="UTF-8") as file_list:
#     for file in file_list:
#         content = json.loads(file)
#         if content["key"] == 0:
#             for value in content["value"]:
#                 con = json.loads(value)
#                 initial_nodes.add(con["user_A"])
#             break
# print(len(initial_nodes))
# with open("initial_nodes.txt", "w+", encoding="UTF-8") as file:
#     for node in list(initial_nodes)[:300]:
#         file.write(node + "\n")


# 挑选度最大节点
# rt_link_dict = {}
# with open("rt-pol.txt", "r+", encoding="UTF-8") as file_list:
#     for file in file_list:
#         content = file.strip().split(",")
#         user_A = content[0]
#         if rt_link_dict.get(user_A):
#             rt_link_dict[user_A] += 1
#         else:
#             rt_link_dict[user_A] = 1
# result_list = sorted(rt_link_dict.items(), key=lambda d: d[1], reverse=True)
# print(result_list)
# with open("initial_nodes.txt", "w+", encoding="UTF-8") as file:
#     for result in result_list[:75]:
#         node = result[0]
#         file.write(node + "\n")


"""
分阶段查看模型节点质量，即阶段性节点预测准确率
"""
# nodes_dict1 = {}
# with open("heat_node.json", "r+", encoding="UTF-8") as file_list:
#     i = 0
#     for file in file_list:
#         content = json.loads(file)
#         nodes_dict1[i] = content["nodes"]
#         i += 1
# 存储每轮节点
# nodes_dict2 = {}
# node_set = set()
# num = 0
# l = []
# with open("content_dict.json", "r+", encoding="UTF-8") as file_list:
#     # 当前轮的节点数
#     cur_list = []
#     for file in file_list:
#         # 每条是一个json语句
#         content = json.loads(file)
#         key = content["key"]
#         nodes = content["value"]
#         for value in content["value"]:
#             # 每一个json语句中存储的也是json语句 解析第二次
#             con = json.loads(value)
#             num += 1
#             if con["user_A"] not in node_set:
#                 node_set.add(con["user_A"])
#                 cur_list.append(con["user_A"])
#             if con["user_B"] not in node_set:
#                 node_set.add(con["user_B"])
#                 cur_list.append(con["user_B"])


"""
真实值可能具有周期上线规律 利用余弦相似度查看
"""
# realValue = []
# node_set = set()
# with open("content_dict.json", "r+", encoding="UTF-8") as file_list:
#     for file in file_list:
#         content = json.loads(file)
#         cur_set = set()
#         for value in content["value"]:
#             con = json.loads(value)
#             if con["user_A"] not in node_set:
#                 node_set.add(con["user_A"])
#                 cur_set.add(con["user_A"])
#             if con["user_B"] not in node_set:
#                 node_set.add(con["user_B"])
#                 cur_set.add(con["user_B"])
#         realValue.append(len(cur_set))
# space_list = [int(n) for n in np.linspace(0, len(realValue), 3)]
# value_list = []
# for i in range(len(space_list) - 1):
#     value_list.append(realValue[space_list[i]: space_list[i + 1]])
# pro_list = []
# for i in range(len(value_list)):
#     pro_list.append([v/sum(value_list[i]) for v in value_list[i]])
# result = []
# for i in range(len(pro_list[0])):
#     num = 0
#     for j in range(len(pro_list)):
#         num += pro_list[j][i]
#     result.append(num / len(pro_list))
# print(result)
# print(sum(result))


"""
总数误差计算
"""


"""
查看三种模型与实际情况的曲线
"""


def get_figure():
    node_list1 = []
    num1 = 0
    with open("heat_node.json", "r+", encoding="UTF-8") as file_list:
        for file in file_list:
            content = json.loads(file)
            num1 += len(content["nodes"])
            node_list1.append(num1)
    node_list2 = []
    num2 = 0
    with open("experiment1.json", "r+", encoding="UTF-8") as file_list:
        for file in file_list:
            content = json.loads(file)
            num2 += len(content["nodes"])
            node_list2.append(num2)
    node_list3 = []
    num3 = 0
    with open("experiment2.json", "r+", encoding="UTF-8") as file_list:
        for file in file_list:
            content = json.loads(file)
            num3 += len(content["nodes"])
            node_list3.append(num3)
    realValue = []
    node_set = set()
    num4 = 0
    with open("content_dict.json", "r+", encoding="UTF-8") as file_list:
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
            num4 += len(cur_set)
            realValue.append(num4)
    plt.plot(node_list1, label="HT-model")
    plt.plot(node_list2, label="SI-model")
    plt.plot(node_list3, label="particle-model")
    plt.plot(realValue, label="real value")
    plt.xlabel("时间(单位：轮)")
    plt.ylabel("传播数量(单位：个)")
    plt.legend(loc=0)
    plt.savefig("rt-pol.png")
    plt.show()


"""
查看初始节点对于模型的影响
"""
# node_list1 = []
# num1 = 0
# with open("heat_node.json", "r+", encoding="UTF-8") as file_list:
#     for file in file_list:
#         content = json.loads(file)
#         num1 += len(content["nodes"])
#         node_list1.append(num1)
# node_list2 = []
# num2 = 0
# with open("heat_node2.json", "r+", encoding="UTF-8") as file_list:
#     for file in file_list:
#         content = json.loads(file)
#         num2 += len(content["nodes"])
#         node_list2.append(num2)
# node_list3 = []
# num3 = 0
# with open("heat_node3.json", "r+", encoding="UTF-8") as file_list:
#     for file in file_list:
#         content = json.loads(file)
#         num3 += len(content["nodes"])
#         node_list3.append(num3)
# node_list4 = []
# num4 = 0
# with open("heat_node4.json", "r+", encoding="UTF-8") as file_list:
#     for file in file_list:
#         content = json.loads(file)
#         num4 += len(content["nodes"])
#         node_list4.append(num4)
# node_list5 = []
# num5 = 0
# with open("heat_node5.json", "r+", encoding="UTF-8") as file_list:
#     for file in file_list:
#         content = json.loads(file)
#         num5 += len(content["nodes"])
#         node_list5.append(num5)
# # 前十条数据
# plt.plot(node_list1[:10], 'b+-', label="初始节点为300")
# plt.plot(node_list3[:10], 'ro-', label="初始节点为100")
# plt.plot(node_list5[:10], 'yv-', label="初始节点为25")
# # 最后十条数据
# # plt.plot(node_list1[38:], 'b+-', label="初始节点为300")
# # plt.plot(node_list3[38:], 'ro-', label="初始节点为100")
# # plt.plot(node_list5[38:], 'yv-', label="初始节点为25")
# # 总节点
# # plt.plot(node_list1, 'b+-', label="初始节点为300")
# # plt.plot(node_list3, 'r--', label="初始节点为100")
# # plt.plot(node_list5, 'yv-', label="初始节点为25")
# plt.legend(loc=0)
# plt.xlabel("时间(单位：轮)")
# plt.ylabel("传播数量(单位：个)")
# plt.savefig("initial1.png", dpi=600, bbox_inches='tight')
# plt.show()


if __name__ == '__main__':
    predictValue = []
    with open("heat_node.json", "r+", encoding="UTF-8") as file_list:
        for file in file_list:
            content = json.loads(file)
            predictValue.append(len(content["nodes"]))
    realValue = []
    node_set = set()
    with open("content_dict.json", "r+", encoding="UTF-8") as file_list:
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
    num2 = 300
    plot_list2 = []
    for i in range(len(realValue)):
        num1 += realValue[i]
        plot_list1.append(num1)
    for i in range(len(predictValue)):
        num2 += predictValue[i]
        plot_list2.append(num2)
    accuracy = []
    for i in range(len(plot_list1)):
        accuracy.append(1 - abs(plot_list1[i] - plot_list2[i]) / plot_list1[i])
    print("准确率：", format(sum(accuracy) / len(accuracy) * 100, ".2f"), "%")
    plot_list1 = np.array(plot_list1)
    plot_list2 = np.array(plot_list2)
    print("余弦相似度：", cosine_similarity([plot_list1], [plot_list2]))
    mse = metrics.mean_squared_error(plot_list1, plot_list2)  # 均方误差MSE
    rmse = np.sqrt(mse)  # 均方根误差
    mae = metrics.mean_absolute_error(plot_list1, plot_list2)  # 平均绝对误差
    print("RMSE = ", format(rmse, ".2f"))
    print("MAE = ", format(mae, ".2f"))
    r2_score = metrics.r2_score(plot_list1, plot_list2)
    print("R2_score = ", format(r2_score, ".4f"))
    mape = mape(plot_list1, plot_list2)
    print("MAPE = ", format(mape, ".2f"), "%")
    x = [i for i in range(50)]
    plt.plot(x, plot_list1, "b-", label="Real Value")
    plt.plot(x, plot_list2, "r-", label="Predict Value")
    plt.fill_between(x, plot_list1, plot_list2, facecolor='yellow', alpha=0.6)
    plt.xlabel("Time")
    plt.ylabel("Number of diffusion")
    plt.legend(loc=0)
    plt.savefig("rt-pol2.png", dpi=600, bbox_inches='tight')
    plt.show()
