在AWD攻防赛中通过给定的webshell批量获取flag

为不会现场挖洞写脚本的菜鸡准备

针对简单的单参数传递的一句话和特定的加密一句话

使用metasploit模块标准编写，易于扩展。

目前实现的功能：

 - [X] 批量扫描webshell登录密码，带字典
 - [X] 批量扫描ctf中常用 目录，文件
 - [X] 批量利用websehll执行命令 
 - [X] 批量利用websehll上传新的webshell
 - [ ] 构造payload，批量验证测试
 - [ ] python 很简单，其他功能看懂逻辑功能自己改
 


# 1、使用说明

1. 使用kali或者parrotos，或者安装了metasploit的任意linux机器。
2. 测试metasploit 版本 
3. `git clone https://github.com/dyzsoft/FlagHunter`
4. `cd FlagHunter/` ``
5. 使用 `msfconsole -m .` 加载当前模块
6. 使用 `search flaghunter` 搜索可以使用的模块
```
 #  Name                                          Disclosure Date  Rank       Check  Description
   -  ----                                          ---------------  ----       -----  -----------
   0  auxiliary/flaghunter/caidao_bruteforce_login  2020-03-22       normal     Yes    AWDFlagHunter utils: Caidao bruteforce login
   1  auxiliary/flaghunter/http_scanner             2020-03-22       normal     Yes    AWDFlagHunter utils: http scanner
   2  exploit/flaghunter/my_caidao_php              2017-01-26       excellent  No     Caidao code execute

```

目录结构：

```bash
┌─[user@parrot]─[~/test/FlagHunter]
└──╼ $tree
.
├── auxiliary
│   └── flaghunter
│       ├── caidao_bruteforce_login.py  ## webshell密码 测试模块
│       ├── caidao_pass.txt             ## 密码字典 
│       ├── ctf_webpath.txt             ## ctf常用路径字典
│       └── http_scanner.py             ## ctf常用路径扫描
├── exploits
│   └── flaghunter
│       └── my_caidao_php.py            ##批量利用websehll模块 
├── LICENSE
└── README.md

4 directories, 7 files
```

# 2参考内容

  `https://github.com/Ares-X/AWD-Predator-Framework` 

  `https://github.com/admintony/Prepare-for-AWD`


**使用请遵守国家相关法律**