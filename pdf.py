import string
import streamlit as st
from io import BytesIO

import fitz, os
import zipfile

def add_file_to_zip(file_path, zip_path):
    if not os.path.exists(zip_path):
        with zipfile.ZipFile(zip_path, 'w') as my_zip:
            my_zip.write(file_path, os.path.basename(file_path))
    else:
        with zipfile.ZipFile(zip_path, 'a') as my_zip:
            my_zip.write(file_path, os.path.basename(file_path))

def fun(file, name):
    doc = fitz.open(stream=file)

    for page in doc:
        imageList = page.get_images()
        k = 0
        for imginfo in imageList:
            if k==0:
                doc._deleteObject(imginfo[0]) #删除图片
            else:
                pass
            k = k+1
        
    doc.save(f"{name}.pdf") #重新保存PDF
    
    with open(f"{name}.pdf", "rb") as f:
        data = f.read()
    
    add_file_to_zip(f"{name}.pdf")
    os.remove(f"{name}.pdf")

    return data

st.info("该APP用于移除pdf蒙版!")
code  = ["3478"]
pw = st.text_input("请输入口令", type="password")
if pw in code:
    files = st.file_uploader("上传要处理的pdf", accept_multiple_files=True, type=["pdf"])

    f = []
    name = []
    if files:
        for uploaded_file in files:
            f.append(BytesIO(uploaded_file.read()))
            name.append(uploaded_file.name)
        
    start = st.button("开始处理", use_container_width=True)

    d = []
    if len(f)>0 and start:
        with st.spinner('正在处理...'):
            for i, j in zip(f, name):
                data = fun(i, j.replace(".pdf", ""))
                d.append(data)
            with open("result.zip", "rb") as f:
                d = f.read()
        if len(d)==1:
            download = st.download_button(label=f"下载处理后的文件", data=d, file_name=name[0], mime='pdf', use_container_width=True)
        else:
            download = st.download_button(label=f"下载处理后的文件", data=d, file_name="result.zip", mime='zip', use_container_width=True)
        if download:
            os.remove("result.zip")
    else:
        st.info("点击开始处理即可开始处理！")
else:
    st.info("口令错误, 请联系QQ1726794987")
