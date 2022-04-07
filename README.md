# sycgram

## 安装与更新

```shell
# 如果选择的是安装，则安装成功后，可先使用Ctrl+P，然后使用Ctrl+Q挂到后台运行
bash <(curl -fsL "https://raw.githubusercontent.com/iwumingz/sycgram/main/install.sh")
```



## 迁移备份

1. 停止容器
2. 打包`/opt/sycgram`文件夹到新环境相同位置
3. 在新环境使用sycgram管理脚本，选择：更新



## 自定义指令及指令前缀

- 请根据需要修改`/opt/sycgram/data/command.yml`内容即可
- 每次更新都会自动将原来的`command.yml`备份命名为`command.yml.bk`
- 每次更新的新指令的格式用法只会在`command.yml`末尾补充



## 注意事项

- 脚本仅适用于Ubuntu/Debian
- 按个人需求随缘更，仅用于学习用途
- 如果号码等输入错误了，重新安装即可
