"""
本文件需要的包
"""
import json
import time
import math
import random
import networkx as nx
import matplotlib.pyplot as plt
from sklearn.metrics.pairwise import cosine_similarity

"""
处理 higgs-activity_time.txt
可以生成RT.json higgs.json
# 平均聚类系数： 0.18868658023153387
"""
# content_list = []
# with open("higgs_twitter/higgs-activity_time.txt", "r+", encoding="UTF-8") as file_list:
#     i = 0
#     for file in file_list:
#         content = file.strip().split(' ')
#         content_list.append(content)
#         i += 1
# print("共有", i, "条数据...")
# with open("higgs_twitter/higgs.json", "w+", encoding="UTF-8") as file:
#     for content in content_list:
#         user_A = content[0]  # 用户A 从用户B转发消息
#         user_B = content[1]  # 用户B 影响用户A
#         time_stamp = content[2]  # 时间戳
#         # 转换成 年-月-日 小时：分钟：秒
#         time_Array = time.localtime(int(time_stamp))
#         time_str = time.strftime("%Y-%m-%d %H:%M:%S", time_Array)
#         item = {
#             "user_A": user_A,
#             "user_B": user_B,
#             "time_stamp": time_str
#         }
#         file.write(json.dumps(item, ensure_ascii=False) + "\n")


"""
处理 higgs_social_network.txt
生成higgs_social_network_node.txt
"""
# 节点集 higgs_social_network_node.txt  边集 higgs_social_network.txt
# node_set = set()
# with open("higgs_twitter/higgs_social_network.txt", "r+", encoding="UTF-8") as file_list:
#     for file in file_list:
#         content = file.strip().split(" ")
#         node_set.add(content[0])
#         node_set.add(content[1])
# with open("higgs_twitter/higgs_social_network_node.txt", "w+", encoding="UTF-8") as file:
#     i = 0
#     for node in node_set:
#         i += 1
#         file.write(node + "\n")
# print(i)


"""
处理 RT.json
生成点集 边集
"""
# 处理节点集 共256491个节点
# node_set = set()
# with open("higgs_twitter/RT.json", "r+", encoding="UTF-8") as file_list:
#     i = 0
#     for file in file_list:
#         content = json.loads(file)
#         node_set.add(content["user_A"])
#         node_set.add(content["user_B"])
#         i += 1
#         if i % 1000 == 0:
#             print("处理完" + str(i) + "条信息")
#     print("共有" + str(i) + "条信息")
# with open("higgs_twitter/RT_node_set.txt", "w+", encoding="UTF-8") as file:
#     for node in list(node_set):
#         file.write(node + "\n")


# 处理边集 共329132条边
# 由于是转发 在json文件中是 user_A 转发 user_B 即信息是从user_B 流向 user_A 故边集中是(user_B, user_A)
# edge_set = set()
# with open("higgs_twitter/RT.json", "r+", encoding="UTF-8") as file_list:
#     i = 0
#     for file in file_list:
#         content = json.loads(file)
#         edge_set.add((content["user_B"], content["user_A"]))
#         i += 1
#         if i % 1000 == 0:
#             print("处理完" + str(i) + "条信息")
#     print("共有" + str(i) + "条信息")
# with open("higgs_twitter/RT_edge_set.txt", "w+", encoding="UTF-8") as file:
#     for edge in list(edge_set):
#         file.write(edge[0] + " " + edge[1] + "\n")


"""
三类social_network
生成higgs-activity_time.txt
"""
# social_set = set()
# with open("higgs_twitter/higgs_social_network.txt", "r+", encoding="UTF-8") as file_list:
#     for file in file_list:
#         user_A = int(file.strip().split(" ")[0])
#         user_B = int(file.strip().split(" ")[1])
#         social_set.add((user_A, user_B))
# print("整个网络共", len(social_set), "条")
# s = ["MT", "RE", "RT"]
# s_set = set()
# with open("higgs_twitter/higgs-activity_time.txt", "r+", encoding="UTF-8") as file_list:
#     for file in file_list:
#         if file.strip().split(" ")[3] == s[2]:
#             user_A = int(file.strip().split(" ")[0])
#             user_B = int(file.strip().split(" ")[1])
#             s_set.add((user_A, user_B))
# print("网络共", len(s_set), "条")
# new_set = social_set.intersection(s_set)
# print("两者交集共", len(new_set), "条")
# content_list = []
# with open("higgs_twitter/higgs-activity_time.txt", "r+", encoding="UTF-8") as file_list:
#     for file in file_list:
#         if file.strip().split(" ")[3] == s[2]:
#             user_A = int(file.strip().split(" ")[0])
#             user_B = int(file.strip().split(" ")[1])
#             if (user_A, user_B) in new_set:
#                 content_list.append(file)
# with open("higgs_twitter/" + s[2] + "_social_network.txt", "w+", encoding="UTF-8") as file:
#     for content in content_list:
#         file.write(content)


"""
RT_social_network.txt
生成点集 边集
"""
# 找出点集
# node_set = set()
# with open("higgs_twitter/RT_social_network.txt", "r+", encoding="UTF-8") as file_list:
#     for file in file_list:
#         user_A = int(file.strip().split(" ")[0])
#         user_B = int(file.strip().split(" ")[1])
#         node_set.add(user_B)
#         node_set.add(user_A)
# print(len(node_set))
# with open("higgs_twitter/RT_node_set.txt", "w+", encoding="UTF-8") as file:
#     for node in node_set:
#         file.write(str(node) + "\n")

# 找出边集
# edge_set = set()
# with open("higgs_twitter/RT_social_network.txt", "r+", encoding="UTF-8") as file_list:
#     for file in file_list:
#         user_A = int(file.strip().split(" ")[0])
#         user_B = int(file.strip().split(" ")[1])
#         edge_set.add((user_B, user_A))
# print(len(edge_set))
# with open("higgs_twitter/RT_edge_set.txt", "w+", encoding="UTF-8") as file:
#     for edge in edge_set:
#         file.write(str(edge[0]) + " " + str(edge[1]) + "\n")

# 解析RT_social_network.txt中的时间戳
# content_list = []
# with open("higgs_twitter/RT_social_network.txt", "r+", encoding="UTF-8") as file_list:
#     i = 0
#     for file in file_list:
#         content = file.strip().split(' ')
#         if content[-1] == "RT":
#             content_list.append(content)
#             i += 1
# print("共有", i, "条数据...")
# with open("higgs_twitter/RT.json", "w+", encoding="UTF-8") as file:
#     for content in content_list:
#         user_A = content[0]  # 用户A 从用户B转发消息
#         user_B = content[1]  # 用户B 影响用户A
#         time_stamp = content[2]  # 时间戳
#         # 转换成 年-月-日 小时：分钟：秒
#         time_Array = time.localtime(int(time_stamp))
#         time_str = time.strftime("%Y-%m-%d %H:%M:%S", time_Array)
#         item = {
#             "user_A": user_A,
#             "user_B": user_B,
#             "time_stamp": time_str
#         }
#         file.write(json.dumps(item, ensure_ascii=False) + "\n")


"""
初始种子节点集
生成RT_initial_nodes.txt
"""
# 按照时间先后
# initial_nodes = set()
# with open("higgs_twitter/RT.json", "r+", encoding="UTF-8") as file_list:
#     i = 0
#     for file in file_list:
#         content = json.loads(file)
#         initial_nodes.add(content["user_B"])
#         i += 1
#         if i == 500:
#             break
# with open("higgs_twitter/RT_initial_nodes.txt", "w+", encoding="UTF-8") as file:
#     for node in list(initial_nodes):
#         file.write(node + "\n")


# 挑选度最大节点
# rt_link_dict = {}
# with open("higgs_twitter/higgs-retweet_network.txt", "r+", encoding="UTF-8") as file_list:
#     i = 0
#     for file in file_list:
#         i += 1
#         content = file.strip().split(" ")
#         user_A = content[1]
#         if rt_link_dict.get(user_A):
#             rt_link_dict[user_A] += 1
#         else:
#             rt_link_dict[user_A] = 1
#         # if i == 10:
#         #     break
# result_list = sorted(rt_link_dict.items(), key=lambda d: d[1], reverse=True)
# with open("higgs_twitter/RT_initial_nodes.txt", "w+", encoding="UTF-8") as file:
#     for result in result_list[:50000]:
#         node = result[0]
#         file.write(node + "\n")


"""
生成RT_time_stamp.json
"""
# 将信息分作八个时段
# date_dict = dict()
# with open("higgs_twitter/RT.json", "r+", encoding="UTF-8") as file_list:
#     for file in file_list:
#         content = json.loads(file)
#         time_stamp = content["time_stamp"].split(" ")[0]
#         if date_dict.get(time_stamp):
#             date_dict[time_stamp].append(int(content["user_A"]))
#         else:
#             date_dict[time_stamp] = [int(content["user_A"])]
# with open("higgs_twitter/RT_time_stamp.json", "w+", encoding="UTF-8") as file:
#     for key in date_dict:
#         item = {
#             "time_stamp": key,
#             "nodes": list(set(date_dict[key]))
#         }
#         file.write(json.dumps(item, ensure_ascii=False) + "\n")


"""
time_stamp.txt
将时间单独提取出来
"""
# time_list = []
# with open("higgs_twitter/RT.json", "r+", encoding="UTF-8") as file_list:
#     for file in file_list:
#         content = json.loads(file)
#         time_list.append(content["time_stamp"])
# with open("higgs_twitter/time_stamp.txt", "w+", encoding="UTF-8") as file:
#     for time in time_list:
#         file.write(time + "\n")


"""
time_stamp2.json
将时间划分为7轮 每轮24小时
"""
# time_dic = {}
# with open("higgs_twitter/time_stamp.txt", "r+", encoding="UTF-8") as file_list:
#     for file in file_list:
#         file = file.strip()
#         if "2012-07-01 08:00:00" <= file <= "2012-07-02 07:59:59":
#             if time_dic.get(1):
#                 time_dic[1].append(file)
#             else:
#                 time_dic[1] = [file]
#         elif "2012-07-02 08:00:00" <= file <= "2012-07-03 07:59:59":
#             if time_dic.get(2):
#                 time_dic[2].append(file)
#             else:
#                 time_dic[2] = [file]
#         elif "2012-07-03 08:00:00" <= file <= "2012-07-04 07:59:59":
#             if time_dic.get(3):
#                 time_dic[3].append(file)
#             else:
#                 time_dic[3] = [file]
#         elif "2012-07-04 08:00:00" <= file <= "2012-07-05 07:59:59":
#             if time_dic.get(4):
#                 time_dic[4].append(file)
#             else:
#                 time_dic[4] = [file]
#         elif "2012-07-05 08:00:00" <= file <= "2012-07-06 07:59:59":
#             if time_dic.get(5):
#                 time_dic[5].append(file)
#             else:
#                 time_dic[5] = [file]
#         elif "2012-07-06 08:00:00" <= file <= "2012-07-07 07:59:59":
#             if time_dic.get(6):
#                 time_dic[6].append(file)
#             else:
#                 time_dic[6] = [file]
#         elif "2012-07-07 08:00:00" <= file <= "2012-07-08 07:59:59":
#             if time_dic.get(7):
#                 time_dic[7].append(file)
#             else:
#                 time_dic[7] = [file]
# with open("higgs_twitter/time_stamp2.json", "w+", encoding="UTF-8") as file:
#     for key in time_dic:
#         item = {
#             "key": key,
#             "value": time_dic[key]
#         }
#         file.write(json.dumps(item, ensure_ascii=False) + "\n")


"""
time_stamp3.txt
将每轮的时间做统计 计算在线率
"""
# num_list = []
# with open("higgs_twitter/time_stamp2.json", "r+", encoding="UTF-8") as file_list:
#     for file in file_list:
#         num_dict = {}
#         content = json.loads(file)
#         for value in content["value"]:
#             num = int(value.strip().split(" ")[1][:2])
#             if num_dict.get(num):
#                 num_dict[num] += 1
#             else:
#                 num_dict[num] = 1
#         num_list.append(num_dict)
# with open("higgs_twitter/time_stamp3.json", "w+", encoding="UTF-8") as file:
#     for num in num_list:
#         times = []
#         for key in num:
#             times.append(num[key])
#         item = {
#             "times_list": times
#         }
#         file.write(json.dumps(item, ensure_ascii=False) + "\n")


"""
time_stamp4.json
每天上线概率
"""
# time_list = []
# with open("higgs_twitter/time_stamp3.json", "r+", encoding="UTF-8") as file_list:
#     for file in file_list:
#         content = json.loads(file)
#         time = [time / sum(content["times_list"]) for time in content["times_list"]]
#         time_list.append(time)
# with open("higgs_twitter/time_stamp4.json", "w+", encoding="UTF-8") as file:
#     for time in time_list:
#         item = {
#             "online_pro": time
#         }
#         file.write(json.dumps(item, ensure_ascii=False) + "\n")


"""
time_stamp5.txt
上线概率
"""
# pro_list = []
# with open("higgs_twitter/time_stamp4.json", "r+", encoding="UTF-8") as file_list:
#     for file in file_list:
#         content = json.loads(file)
#         pro_list.append(content["online_pro"])
# temp = [0] * 24
# for pro in pro_list:
#     for num, p in enumerate(pro):
#         temp[num] += p
# with open("higgs_twitter/time_stamp5.json", "w+", encoding="UTF-8") as file:
#     for t in temp:
#         file.write(str(t / 7.0) + "\n")


"""
time_stamp6.txt
划分为每天的时间
"""
# with open("higgs_twitter/time_stamp2.json", "r+", encoding="UTF-8") as file_list:
#     num_list = []
#     for file in file_list:
#         content = json.loads(file)
#         num_list.append(len(content["value"]))
# print(num_list)
# pro_list = [num / sum(num_list) for num in num_list]
# with open("higgs_twitter/time_stamp6.json", "w+", encoding="UTF-8") as file:
#     for pro in pro_list:
#         file.write(str(pro) + "\n")


"""
RT_time_stamp.json
每轮节点数
"""
# date_dict = {}
# with open("higgs_twitter/RT.json", "r+", encoding="UTF-8") as file_list:
#     for file in file_list:
#         content = json.loads(file)
#         time = content["time_stamp"]
#         node = content["user_A"]
#         file = file.strip()
#         if "2012-07-01 08:00:00" <= time <= "2012-07-02 07:59:59":
#             if date_dict.get(1):
#                 date_dict[1].append(int(node))
#             else:
#                 date_dict[1] = [int(node)]
#         elif "2012-07-02 08:00:00" <= time <= "2012-07-03 07:59:59":
#             if date_dict.get(2):
#                 date_dict[2].append(int(node))
#             else:
#                 date_dict[2] = [int(node)]
#         elif "2012-07-03 08:00:00" <= time <= "2012-07-04 07:59:59":
#             if date_dict.get(3):
#                 date_dict[3].append(int(node))
#             else:
#                 date_dict[3] = [int(node)]
#         elif "2012-07-04 08:00:00" <= time <= "2012-07-05 07:59:59":
#             if date_dict.get(4):
#                 date_dict[4].append(int(node))
#             else:
#                 date_dict[4] = [int(node)]
#         elif "2012-07-05 08:00:00" <= time <= "2012-07-06 07:59:59":
#             if date_dict.get(5):
#                 date_dict[5].append(int(node))
#             else:
#                 date_dict[5] = [int(node)]
#         elif "2012-07-06 08:00:00" <= time <= "2012-07-07 07:59:59":
#             if date_dict.get(6):
#                 date_dict[6].append(int(node))
#             else:
#                 date_dict[6] = [int(node)]
#         elif "2012-07-07 08:00:00" <= time <= "2012-07-08 07:59:59":
#             if date_dict.get(7):
#                 date_dict[7].append(int(node))
#             else:
#                 date_dict[7] = [int(node)]
# with open("higgs_twitter/RT_time_stamp.json", "w+", encoding="UTF-8") as file:
#     for key in date_dict:
#         item = {
#             "time_stamp": key,
#             "nodes": date_dict[key]
#         }
#         file.write(json.dumps(item, ensure_ascii=False) + "\n")


"""
处理higgs-retweet_network.txt
转发网络 user_A user_B 转发次数
"""
# time_dict = {}
# with open("higgs_twitter/higgs-retweet_network.txt", "r+", encoding="UTF-8") as file_list:
#     for file in file_list:
#         content = file.strip().split(" ")
#         if time_dict.get(content[-1]):
#             time_dict[content[-1]] += 1
#         else:
#             time_dict[content[-1]] = 1
# print(time_dict)


"""
给度值前100的节点随机加边
节点间可能存在空隙,可能是多个社区,合并它,在前100个节点中随机加边
"""
# node1 = []
# with open("higgs_twitter/network.txt", "r+", encoding="UTF-8") as file_list:
#     for file in file_list:
#         node1.append(file.strip())
# node2 = []
# with open("higgs_twitter/higgs-retweet_network.txt", "r+", encoding="UTF-8") as file_list:
#     i = 0
#     for file in file_list:
#         i += 1
#         if (i + 1) % 10000 == 0:
#             print(i + 1)
#         content = file.strip().split(" ")
#         user_A = content[1]
#         user_B = content[0]
#         if user_A not in node1:
#             node2.append(user_A)
#         if user_B not in node1:
#             node2.append(user_B)
# edges = set()
# for i in range(10000):
#     user_A = node1[random.randint(0, len(node1) - 1)]
#     user_B = node2[random.randint(0, len(node2) - 1)]
#     edges.add((user_A, user_B))
#
# with open("higgs_twitter/RT_edge_set2.txt", "w+", encoding="UTF-8") as file:
#     for edge in list(edges):
#         file.write(edge[0] + " " + edge[1] + "\n")


"""
平均聚类系数
网络数据大的时候时间有点长
"""
# print("开始读取节点信息...")
# # 节点集 nodes_list
# nodes_list = []
# with open("higgs_twitter/higgs_social_network_node.txt", "r+", encoding="UTF-8") as file_list:
#     for file in file_list:
#         nodes_list.append(int(file.strip()))
# print("读取完成！")
# print("开始读取边信息...")
# # 边集 edges_list
# edges_list = []
# with open("higgs_twitter/higgs_social_network.txt", "r+", encoding="UTF-8") as file_list:
#     for file in file_list:
#         edges_list.append((int(file.strip().split(" ")[0]), int(file.strip().split(" ")[1])))
# print("读取完成！")
# print("开始导入图...")
# graph = nx.Graph()
# graph.add_nodes_from(nodes_list)
# graph.add_edges_from(edges_list)
# print("平均聚类系数：", nx.average_clustering(graph))










