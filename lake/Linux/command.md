与linux有关的一些命令

## screen

### 新建

`screen -S test`

### 列出当前所有的session

`screen -ls`

### 返回

`screen -r test`

### 快捷键

ctrl+ad, 离开当前session

ctrl+ak, 杀死当前session

### 解决screen状态为Attached连上不的问题

`screen -D  -r ＜session-id>`

解释：-D -r 先踢掉前一用户，再登陆

## chown和chgrp

`chown [-R] 账号名称 文件或目录`

`chgrp [-R] 用户组名称 文件或目录`

## sftp

`sftp root@ip`

`get ~/test/index.php  ~/test/`

`put ~/test/Linux.pdf ~/test/`

## du

输出当前目录下各个子目录所使用的空间

`du -h  --max-depth=1`

## 解压缩

### tar

解包：`tar xvf FileName.tar`

打包：`tar cvf FileName.tar DirName`

### .gz

解压1：`gunzip FileName.gz`

解压2：`gzip -d FileName.gz`

压缩：`gzip FileName`

### .tar.gz 和 .tgz

解压：`tar zxvf FileName.tar.gz`

压缩：`tar zcvf FileName.tar.gz DirName`

### .bz

解压1：`bzip2 -d FileName.bz`

解压2：`bunzip2 FileName.bz`

压缩：未知

### .tar.bz

解压：tar jxvf FileName.tar.bz

压缩：未知

### .bz2

解压1：`bzip2 -d FileName.bz2`

解压2：`bunzip2 FileName.bz2`

压缩： `bzip2 -z FileName`

### .tar.bz2

解压：`tar jxvf FileName.tar.bz2`

压缩：`tar jcvf FileName.tar.bz2 DirName`

### .Z

解压：`uncompress FileName.Z`

压缩：`compress FileName`

### .tar.Z

解压：`tar Zxvf FileName.tar.Z`

压缩：`tar Zcvf FileName.tar.Z DirName`

### .zip

解压：`unzip FileName.zip`

压缩：`zip FileName.zip DirName`

### .rar

解压：`rar x FileName.rar`

压缩：`rar a FileName.rar DirName`

### .tar.xz

解压：`tar -xvJf FileName.tar.xz`

压缩：

先创建xxx.tar文件, `tar -cvf xxx.tar xxx`

再创建xxx.tar.xz文件, `xz -z xxx.tar`

## apt-key

`apt-key list          #列出已保存在系统中key`

`apt-key add keyname   #把下载的key添加到本地trusted数据库中`

`apt-key del keyname   #从本地trusted数据库删除key`

`apt-key update        #更新本地trusted数据库，删除过期没用的key`

## snap

### 列出

`snap list`

### 安装

`sudo snap install <snap软件包名>`

### 更新

`sudo snap refresh <snap软件包名>`

`sudo snap refresh all`

### 删除旧的core

`sudo snap remove core --revision xxx`

## sha256sum

`sha256sum filename`

`sha256sum -c <(grep filename filename.sha256sum)`




















