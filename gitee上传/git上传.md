打开要上传目录


```shell
git init

# 提交全部：

git add .


git commit -m "随便写，这是备注"

git remote add origin "远程仓库地址"
```



![输入图片说明](Screenshot%20from%202023-09-16%2011-19-51.png)


将本地仓库push至远程仓库

```shell
git push -u origin master
```




### error 

```shell
 ! [rejected]        master -> master (fetch first)
error: failed to push some refs to 'git@gitee.com:zhugashvili/iflyteks-old-microphone.git'
```

解决办法：
将线上、线下代码进行合并：

```shell
git checkout 分支名    # 切换分支
```

```shell
git pull --rebase origin master
# 我这里是master分支，还可以是其他分支。

#然后再进行push即可：
git push origin master
```

```shell
git branch -a     # 查看分支
```



```shell
官网  # https://help.gitee.com/enterprise/code-manage/Git%20%E7%9F%A5%E8%AF%86%E5%A4%A7%E5%85%A8/Git%E4%BB%93%E5%BA%93%E5%9F%BA%E7%A1%80%E6%93%8D%E4%BD%9C#article-header1
上传# https://blog.csdn.net/baidu_39212797/article/details/109405988
切换分支# https://www.cnblogs.com/cppeterpan/p/7289266.html

```

```shell
git init
git add .
git commit -m "0327"
git remote add origin "git@gitee.com:usst-imi/voice_dialogue.git"
git branch voice_new_0326
git checkout voice_new_0326
git push -u origin voice_new_0326

# sudo systemctl restart systemd-resolved

git pull --rebase origin voice_new_0326
git push origin voice_new_0326
```




