
#ライブラリのインポート
from math import e
import streamlit as st
import matplotlib.pyplot as plt
from icrawler.builtin import BingImageCrawler
import random 

import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import torchvision
import torchvision.transforms as transforms
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMACES = True
import japanize_matplotlib
from IPython.display import clear_output
clear_output()

#コンフィグ
st.set_page_config(
  page_title="癒しプチアニマル",
  page_icon="🧊",
 )

# タイトル
st.title("癒しプチアニマル")

#ニューラルネットワークの定義
class CNN_ORIGINAL(nn.Module):
    def __init__(self):
        super(CNN_ORIGINAL, self).__init__()
        self.conv1 = nn.Conv2d(3, 8, 3)
        self.conv2 = nn.Conv2d(8, 8, 3)
        self.conv3 = nn.Conv2d(8, 3, 3)
        self.fc = nn.Linear(108, 2)

    def forward(self, x):
        h = self.conv1(x)
        h = F.max_pool2d(h, 2)
        h = F.relu(h)

        h = self.conv2(h)
        h = F.max_pool2d(h, 2)
        h = F.relu(h)

        h = self.conv3(h)
        h = F.max_pool2d(h, 2)
        h = F.relu(h)

        h = h.view(-1, 108)

        y = self.fc(h)
        return y

#インスタンスの宣言
cnn_original = CNN_ORIGINAL()
cnn_original.load_state_dict(torch.load("cnn_original.pth"))

#外部入力
key = st.text_input("好きな動物の名前を入力してください", "猫")
if 'img_' not in st.session_state:
  st.session_state['img_'] = None

#ボタンを押して処理  
main_b= st.button('GO')
if main_b:
  crawler = BingImageCrawler(storage={"root_dir": "dataset/"+key})
  crawler.crawl(keyword=key, max_num=5)
  clear_output()

  num_rand=str(random.randint(1,5))
  st.session_state.img_ = plt.imread('/content/dataset/'+key+'/00000'+num_rand+'.jpg')
  st.session_state.num_rand = num_rand
if st.session_state.img_ is not None:
  img_=st.session_state.img_

  # 画像の読み込みと加工
  st.image(img_, caption='かわいい',use_column_width=False, width=256)
  transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Resize((64, 64)),
        transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
  ])

  inputs = transform(img_).reshape(1,3,64,64)

  if st.button("この画像は犬？猫？"):
    outputs = cnn_original(inputs)
    label = outputs.argmax(dim=1).item()
    ans = ""
    if label==0:
        ans = "犬！"
    elif label==1:
        ans = "猫！"
    st.markdown(ans)

  if st.button("癒し度"):
    num=int(st.session_state.num_rand)
    ans=("この画像の癒し度は"+"★"*num)
    st.text(ans)
    if num==5:
      st.success("Perfect!!")
      st.balloons()
