######### [Bilibili-Toolkit](https://github.com/Hsury/Bilibili-Toolkit)
#                                                          |
# 将config.toml中的cookie转化为其他两个项目能用的格式            |
#                                                         \|/
######### [bilibili-live-tools](https://github.com/Dawnnnnnn/bilibili-live-tools)

origin = ""
a = origin.split(';')
a = a[2:]
res = []

for i in a:
    if i.startswith('access_token='):
        res.append(i.replace('access_token', 'access_key'))

res.append('cookie = ' + origin)

for i in a:
    if i.startswith('bili_jct'):
        res.append(i.replace('bili_jct', 'csrf'))

for i in a:
    if i.startswith('DedeUserID='):
        res.append(i.replace('DedeUserID', 'uid'))

for i in a:
    if i.startswith('refresh_token'):
        res.append(i)

print('\n'.join(res))

######### [bili2.0](https://github.com/yjqiang/bili2.0)

origin = ""
a = origin.split(';')
a = a[2:]
res = []

for i in a:
    if i.startswith('access_token='):
        temp = i.replace('access_token', 'access_key').split('=')
        temp.insert(1, '=')
        temp.insert(2, '"')
        temp.append('"')
        res.append(''.join(temp))

res.append('cookie = "' + origin + '"')

for i in a:
    if i.startswith('bili_jct'):
        temp = i.replace('bili_jct', 'csrf').split('=')
        temp.insert(1, '=')
        temp.insert(2, '"')
        temp.append('"')
        res.append(''.join(temp))

for i in a:
    if i.startswith('DedeUserID='):
        temp = i.replace('DedeUserID', 'uid').split('=')
        temp.insert(1, '=')
        temp.insert(2, '"')
        temp.append('"')
        res.append(''.join(temp))

for i in a:
    if i.startswith('refresh_token'):
        temp = i.split('=')
        temp.insert(1, '=')
        temp.insert(2, '"')
        temp.append('"')
        res.append(''.join(temp))

print('\n'.join(res))
