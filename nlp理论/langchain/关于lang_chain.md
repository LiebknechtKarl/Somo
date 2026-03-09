

#### 周浩然langchain
网站
> https://github.com/NoneJou072/robochain/tree/v-llama2
该2代码有两个分支  main 和 origin/v-llama2，我们需要的是分支v-llama2


```shell
 mkdir gpt_ws && cd gpt_ws
git clone https://github.com/NoneJou072/robochain.git
(optional) mv robochain src
cd robochain/
git checkout origin/v-llama2  # 切换分支

# 运行 gpt_ws/robochain/gpt_client/gpt_client/examples/client_tcp_retrieval_gpt.py
# 要用pycharm运行，终端可能报错
```


```shell
# gpt_ws/robochain/gpt_client/gpt_client/commons/config.json 作以下改动
{
    "OPENAI_API_KEY": "sk-juVyGOJNRRVhrpfL527a237eA7D64bF0A431B68bD61565C1",
    "PINECONE_API_KEY": "sk-juVyGOJNRRVhrpfL527a237eA7D64bF0A431B68bD61565C1",
    "OPENAI_API_BASE": "https://di.xiamoai.top/v1"
}
```




```shell
# 大主机运行langchain
cd /media/ros/1T/djw/chatGLM/langchain-ChatGLM-master
conda activate chatGLM
python webui.py            # 加载完毕才可以执行下面代码      对话大语言模型
```


#### langchain 和chatglm

教程网站

``` shell
https://zhuanlan.zhihu.com/p/643531454
```

项目部署
下载源码

```shell
git clone https://github.com/imClumsyPanda/langchain-ChatGLM.git
```

安装依赖

```shell
cd langchain-ChatGLM
pip install -r requirements.txt
```



```shell
# 安装 git lfs
git lfs install 
# 下载 LLM 模型
git clone https://huggingface.co/THUDM/chatglm2-6b $PWD/chatglm2-6b
# 下载 Embedding 模型
git clone https://huggingface.co/GanymedeNil/text2vec-large-chinese $PWD/text2vec
# 模型需要更新时，可打开模型所在文件夹后拉取最新模型文件/代码
git pull
```

#### 基于 P-Tuning 微调 ChatGLM2-6B

```shell
# error
[W socket.cpp:601] [c10d] The IPv6 network addresses of (ros, 41711) cannot be retrieved (gai error: -2 - Name or service not known).
```
解决办法

```
https://blog.csdn.net/lin_xiao_yi/article/details/132490694 
```


```shell
#解决方案：手动添加本地网络
vim /etc/hosts
#添上本地网络
127.0.0.1  ros
```


#### 一个跑成功的代码   20231105


```python
#开梯子，开全局代理，  同级新建文件 word/text1.txt
import  openai
import  os
os.environ["OPENAI_API_KEY"] = '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'
import langchain
from langchain.llms import OpenAI
llm = OpenAI(model_name="text-davinci-003", max_tokens=1024)
llm = langchain.llms.OpenAI(model_name="text-davinci-003", max_tokens=1024)

print(llm("怎么评价人工智能"))
###############################
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.text_splitter import CharacterTextSplitter
from langchain import OpenAI, VectorDBQA
from langchain.document_loaders import DirectoryLoader
from langchain.chains import RetrievalQA
llm = OpenAI(model_name="text-davinci-003", max_tokens=1024)

# 加载文件夹中的所有txt类型的文件
# loader = DirectoryLoader('/content/sample_data/data/', glob='**/*.txt')
loader = DirectoryLoader('word', glob='text1.txt')

# loader = UnstructuredFileLoader("word/text1.txt")
# 将数据转成 document 对象，每个文件会作为一个 document
documents = loader.load()

# 初始化加载器
text_splitter = CharacterTextSplitter(chunk_size=100, chunk_overlap=0)
# 切割加载的 document
split_docs = text_splitter.split_documents(documents)

# 初始化 openai 的 embeddings 对象
embeddings = OpenAIEmbeddings()
# 将 document 通过 openai 的 embeddings 对象计算 embedding 向量信息并临时存入 Chroma 向量数据库，用于后续匹配查询
docsearch = Chroma.from_documents(split_docs, embeddings)

# 创建问答对象
qa = VectorDBQA.from_chain_type(llm=OpenAI(), chain_type="stuff", vectorstore=docsearch, return_source_documents=True)

result = qa({"query": "你是谁？"})
# result = qa({"query": x})
# print(result)

while True :
    # 进行问答
    x=input('请输入问题：')
    # result = qa({"query": "你是谁？"})
    result = qa({"query": x})
    print(result['result'])
```












