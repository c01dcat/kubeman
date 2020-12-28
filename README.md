# kubeman

## 安装 ansible
* 在 `kubeman` 目录下执行  
`pip3 install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/`

## 配置 ssh 和生成 inventory hosts 文件
* 声明 master 节点的 ip  
`declare -a MASTERS=(10.1.0.100)`   
* 声明 node 节点的 ip  
`declare -a NODES=(10.1.0.101 10.1.0.102 10.1.0.103)` 
* 声明集群所有节点的 ip  
`declare -a HOSTS=(${MASTERS[@]} ${NODES[@]})`  
***具体的 ip 地址根据集群实际情况更改***
* 生成 ssh 密钥  
`ssh-keygen -t rsa`
* 将公钥添加到集群各节点上  
`for host in ${HOSTS[@]}; do ssh-copy-id root@$host; done`
* 生成 ansible inventory hosts 文件  
`python3 inventory.py -m ${MASTERS[@]} -n ${NODES[@]}`

***确认 inventory/hosts.yaml 文件中的信息，其中 ansible 的 inventory_hostname (e.g. master1 node1) 将作为该节点的 hostname***

