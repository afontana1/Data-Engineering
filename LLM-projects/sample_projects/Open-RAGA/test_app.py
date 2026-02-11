# import requests
# import json
# import time
# from retrieval.embedder import chat_path
#
# chat_history = []
#
#
#
# payload = {'query':'what is my name','last_3_turn':[
#   {"role": "user", "content": "Hello,my name is akash"},
#   {"role": "assistant", "content": "Hi! How can I help you today?"},
# ]}
#
#
#
# start_time = time.perf_counter()
#
#
# response = requests.post(url='http://localhost:8000/chat',data=json.dumps(payload))
#
# print(response.content)
#
# end_time = time.perf_counter()
#
#
#
# latency_ms = (end_time - start_time) * 1000
# print(f"⏱️ Latency: {latency_ms:.2f} ms")
# print("Response:", response.json())
#
#
import os

# string = """hhehh hhh h hgg ggg ggg ggg  gg gg gg g    ggg g      g ggg              gggg g gggggggg     dhhd hhd dhdhhd dhdhd d       ggggg g gg jjd jjj jj jj jj jj jjj jjdj d    jjdjd jdj"""
#
# print(len(string))
#
#
# from retrieval.embedder import get_embedding_model
#
# print(get_embedding_model('llms/embedding_models/all-mpnet-base-v2'))



list = ['1','2','3','4','5','6','7','8']


print(list[-6:])

