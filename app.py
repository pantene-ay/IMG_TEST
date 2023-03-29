#ライブラリのインポート
from math import e
import streamlit as st
import matplotlib.pyplot as plt
from IPython.display import clear_output
clear_output()
from icrawler.builtin import BingImageCrawler
import random 
from PIL import Image

st.set_page_config(
  page_title="癒しプチアニマル",
  page_icon="🧊",
 )

# タイトル
st.title("癒しプチアニマル")

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
  st.session_state.num_rand=num_rand
  st.session_state.img_ = plt.imread('/content/dataset/'+key+'/00000'+num_rand+'.jpg')

if st.session_state.img_ is not None:
  img_=st.session_state.img_
  st.image(img_, caption='かわいい',use_column_width=False, width=256)
  num=st.session_state.num_rand
  if st.button("癒し度"):
    if st.session_state.img_ is None:
      st.text("画像を表示させてください")
    else:
      ans=("この画像の癒し度は"+"★"*int(num))
      st.text(ans)
      if int(num)==5:
        st.success("Perfect!!")
        st.balloons()
