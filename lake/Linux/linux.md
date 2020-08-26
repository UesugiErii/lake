## ubuntu截图

截取全屏的快捷键是PrintScreen

截取当前窗口的快捷键是Alt+PrintScreen

截取选定区域的快捷键是Shift+PrintScreen

以上三个快捷键可以截取屏幕并保存为图片

若加上Ctrl，则所截取屏幕会直接复制到剪切板，可以直接进行粘贴

## 设置ssh免密码

`ssh-keygen -t rsa`

生成一个私钥和一个.pub的公钥

私钥放到客户端的~/.ssh, 公钥追加到服务端的~/.ssh/authorized_keys

## 设置环境变量

`/etc/profile`, 对所有用户有效

`~/.bash_profile`, 对当前用户有效

使用`source /etc/profile`或`source ~/.bash_profile`立刻生效

直接运行export命令定义变量, 只对当前shell有效(临时的)

## 自动挂载(mount)分区

### 获取UUID

`sudo blkid /dev/sda3`

### 编辑/etc/fstab

下面这行为例子, 不同的地方自行修改

`UUID=904C23B64C23964E /media/aborn/data ntfs defaults        0       2 `

### 测试/etc/fstab

`mount -a`

## 添加虚拟内存

### see if there is a configured swap file

`swapon -s`

### Create swap file

`dd if=/dev/zero of=/swapfile count=2048 bs=1M`

### Activate the swap file

`chmod 600 /swapfile`

`mkswap /swapfile`

### Turn swap on

`swapon /swapfile`

### Enable swap on reboot

`nano /etc/fstab`

`/swapfile   none    swap    sw    0   0`

`mount -a`

## ubuntu中删除deinstall的linux内核

### 查看当前内核版本

`uname -a`

### 查看目前系统中存在的内核版本

`dpkg --get-selections|grep linux`

### 删除举例

`sudo dpkg -P linux-image-4.5.0-4[2-9]-generic`

`sudo dpkg -P linux-image-4.5.0-51-generic`

## 删除仓库及其GPG密钥

### 删除仓库

只需打开`/etc/apt/sources.list`文件并查找仓库名字并将其删除即可

如果已添加 PPA 仓库，请查看`/etc/apt/sources.list.d/`目录并删除相应的条目

最后，使用以下命令更新软件源列表, `sudo apt update`

### 删除仓库密钥

`sudo apt-key list`

`sudo apt-key del 73C62A1B`

`sudo apt update`