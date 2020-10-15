[如何安装docker](https://docs.docker.com/engine/install/ubuntu/)

[docker设置代理](https://www.serverlab.ca/tutorials/containers/docker/how-to-set-the-proxy-for-docker-on-ubuntu/)

[docker简明教程](https://jiajially.gitbooks.io/dockerguide/content/index.html)

## 镜像

### 列出本地镜像

`sudo docker images -a`

### 拉取镜像

`sudo docker pull 镜像名[:tag]`

### 删除镜像

`sudo docker rmi 镜像id`

## 容器

### 查看所有容器

`sudo docker ps -a`

### 启动容器

启动某个已停止容器

`sudo docker start 容器ID或容器名`

交互式启动

`sudo docker run -it --name=test 镜像名[:tag] /bin/bash`

启动守护式容器

`sudo docker run -d --name=test 镜像名[:tag]`

端口映射

-p ip:hostPort:containerPort

选择GPU

\-\-gpus all

例如

`sudo docker run --gpus all -it --name=tf -v /home/zx:/home/zx tensorflow/tensorflow:latest-gpu-py3  /bin/bash`

### 进入正在运行的容器

`sudo docker exec -it 容器ID或容器名 /bin/bash`

`sudo docker attach 容器ID或容器名`

### 停止容器

`sudo docker stop 容器ID或容器名`

### 强制停止容器

`sudo docker kill 容器ID或容器名`

### 退出容器

容器停止退出 exit

容器不停止退出 ctrl+P+Q

### 删除容器

`sudo docker rm 容器ID或容器名`

### 从容器拷贝文件到主机

`sudo docker cp 容器ID或容器名:容器内路径 目的主机路径`

## docker commit

commit可以提交容器副本使之成为一个新的镜像

`sudo docker commit -a="作者名" -m="注释" 容器ID或容器名 名称/名称:tag`

举例

`sudo docker commit -a="zzyy" -m="del tomcat docs" d52495cea537 atguigu/tomcat02:1.2`

## 数据卷

### 直接命令添加

`sudo docker run -it --name=test -v /宿主机目录:/容器内目录 镜像名 /bin/bash`

### dockerfile添加

`VOLUME ["/dataVolumeContainer1","/dataVolumeContainer2"]`

主机对应位置可以用以下命令查看

`sudo docker inspect 容器ID`

### 备注

Docker挂载主机目录Docker访问出现cannot open directory .: Permission denied

解决办法：在挂载目录后多加一个--privileged=true参数即可

## Dockerfile

用一个例子来说明

### 目录内容

找一个单独文件夹构建镜像，此目录下有Dockerfile，c.txt, jdk-8u171-linux-x64.tar.gz, apache-tomcat-9.0.8.tar.gz

### Dockerfile文件内容

```
FROM         centos
MAINTAINER    zzyy<zzyybs@126.com>
#把宿主机当前上下文的c.txt拷贝到容器/usr/local/路径下
COPY c.txt /usr/local/cincontainer.txt
#把java与tomcat添加到容器中
ADD jdk-8u171-linux-x64.tar.gz /usr/local/
ADD apache-tomcat-9.0.8.tar.gz /usr/local/
#安装vim编辑器
RUN yum -y install vim
#设置工作访问时候的WORKDIR路径，登录落脚点
ENV MYPATH /usr/local
WORKDIR $MYPATH
#配置java与tomcat环境变量
ENV JAVA_HOME /usr/local/jdk1.8.0_171
ENV CLASSPATH $JAVA_HOME/lib/dt.jar:$JAVA_HOME/lib/tools.jar
ENV CATALINA_HOME /usr/local/apache-tomcat-9.0.8
ENV CATALINA_BASE /usr/local/apache-tomcat-9.0.8
ENV PATH $PATH:$JAVA_HOME/bin:$CATALINA_HOME/lib:$CATALINA_HOME/bin
#容器运行时监听的端口
EXPOSE  8080
#启动时运行tomcat
# ENTRYPOINT ["/usr/local/apache-tomcat-9.0.8/bin/startup.sh" ]
# CMD ["/usr/local/apache-tomcat-9.0.8/bin/catalina.sh","run"]
CMD /usr/local/apache-tomcat-9.0.8/bin/startup.sh && tail -F /usr/local/apache-tomcat-9.0.8/bin/logs/catalina.out
```

### 构建

-t: 镜像的名字及标签，.表示当前目录

`docker build -t runoob/zzyytomcat9:[tag] .`

## 杂七杂八

### 查看本机IP

`hostname -I`