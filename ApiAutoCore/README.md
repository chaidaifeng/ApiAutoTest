
# 自动化框架：  
### Pytest+Requests+Excel+Git+Jenkins+Allure  
## 本地运行环境
##### python3  
##### pip  
allure-pytest==2.8.36  
allure-python-commons==2.8.36  
configparser==5.0.0  
PyMySQL==0.9.3  
pytest==5.4.3  
pytest-html==2.1.1  
pytest-metadata==1.11.0  
regex==2020.11.13  
requests==2.25.1  
requests-toolbelt==0.9.1  
xlrd==1.2.0  
xlwt==1.3.0  
pyDes==2.0.1  
ruamel.yaml==0.17.10  

##### 备注：   
可以使用pip来安装包
`pip install -r requirements.txt`

## 目录结构V1.0
├── base                      // 工具  
│   ├── api_requests.py  	  // get|post请求封装	  
│   ├── asert_contrast.py     // 断言封装  
│   ├── log.py         		  // 日志封装    
│   ├── pulilc.py             // 常用路径等操作封装    
│   ├── read_excel.py         // 读取excel方法封装  
│   └── read_yml.py          // 读取文件配置数据   
├── config					  // 配置文件  
│	└── config.yml			  // 环境配置   
├── data                      // 文档  
│   ├── apollo  
│   ├── crm   
│   ├── hunter     
│   ├── pinpin  
│	│	└── data_process.yml  // 测试数据   
│	└── 	...  
├── log  					  // 日志文件  
├── page					  // api方法封装  
│   ├── apollo  
│   ├── crm   
│   ├── hunter     
│   ├── pinpin  
│	 ├──	└── page_itention.py     // 用例方法  
│	 └── login.py              // 登录封装   
├── report					  // 测试报告生成路径  
├── testCase				  // 用例脚本  
│   ├── apollo  
│   ├── crm   
│   ├── hunter     
│   ├── pinpin  
│	├──	└── test_company_order_process.py  // 用例脚本编写  
│	├──	└── test_excel_home_case.py  // excel用例脚本编写  
│	└── 	...     
├── testFile				  // excel用例  
│   ├── apollo  
│   ├── crm   
│   ├── hunter     
│   ├── pinpin  
│	├── pinpinHomeTest.xlsx   // excel用例文件  
│	└── ...  
├── conftest.py				  // pytest自定义命令行参数，切换环境   
├── pytest.ini  			  // pytest配置文件  
├── README.md                 // 帮助文档    
├── requirements.txt          // 依赖包    
├── run_all.py				  // 调试执行  
└── 架构设计.xmind   
##
## 目录结构V2.0
###### ApiAutoCore  		  // 平台代码  
├── base                      // 工具  
│   ├── `api_requests.py`  	  // get|post请求封装	  
│   ├── `asert_contrast.py`     // 断言封装  
│   ├── `log.py`         		  // 日志封装    
│   ├── `pulilc.py`             // 常用路径等操作封装    
│   ├── `read_excel.py`         // 读取excel方法封装  
│   └── `read_yml.py`          // 读取文件配置数据   
├── config					  // 配置文件  
│	└── config.yml			  // 环境配置   
├── log  					  // 日志文件  
├── pytest.ini  			  // pytest配置文件  
├── README.md                 // 帮助文档    
├── requirements.txt          // 依赖包    
├── `run_all.py`				  // 调试执行  
└── 架构设计.xmind  
###### ApiAutoTest  			  // 用例脚本  
├── data                      // 文档  
│   ├── apollo  
│   ├── crm   
│   ├── hunter     
│   ├── pinpin  
│	├──	└── data_process.yml  // 测试数据   
│	└── 	...  
├── page					  // api方法封装  
│   ├── apollo  
│   ├── crm   
│   ├── hunter     
│   ├── pinpin  
│	├──	└── `page_itention.py`     // 用例方法  
│	└── login.py              // 登录封装   
├── report					  // 测试报告生成路径  
├── testCase				  // 用例脚本  
│   ├── apollo  
│   ├── crm   
│   ├── hunter     
│   ├── pinpin  
│	├──	└── `test_company_order_process.py`  // 用例脚本编写  
│	├──	└── `test_excel_home_case.py`  // excel用例脚本编写  
│	└── 	...     
├── testFile				  // excel用例  
│   ├── apollo  
│   ├── crm   
│   ├── hunter     
│   ├── pinpin  
│	├── pinpinHomeTest.xlsx   // excel用例文件  
│	└── ...  
└── conftest.py				  // pytest自定义命令行参数，切换环境   
##
### 框架需要包含测试场景  
1.	订单的状态扭转，以及各个状态下对应的操作功能。
2.	用例中需要跨系统操作审核等，如：B端发起意向沟通，CRM需要填写意向沟通报告；b端发起职位委托，需要apollo系统操作审核；apollo订单与B端交互。外部猎头系统与B端职位、订单的交互。
3.	接口无数据关联的用例，如：个人中心-个人信息、公司信息、公司资产等无数据关联的功能模块。
4.	控制切换不同用例执行环境

###	框架做了哪些：
1.	数据文件读取及修改封装，便于用例中调用不同数据文件及修改配置文件的操作。（比如：环境配置、用户信息和切换环境）
2.	各系统登录方法封装，方便用例编写时获取不同系统的token
3.	关于场景用例，主要把模块功能和用例拆分开，方便后续大家调用不同方法来组装用例。

### 框架中编写用例脚本：
1.	page下编写对应模块下的功能方法
2.	testCase下进行编写具体用例
3.	然后针对接口无数据关联的用例，为了方便我们可以统一录入到excel中，进行用例执行；也可以将此类用例编写至testCase中。

### 整体框架运行方式：
1.	通过jenkins操作执行环境和执行分支代码
2.	Jenkins通过Shell命令执行pytest脚本并生成报告数据
3.	Allure工具生成报告模板
4.	Jenkins执行完成后自动发送邮件报告数据
 
### 常见问题
1. 引包base包报错  
项目打开根目录为pinpinAutoTest
2. 环境运行不起来  
项目运行环境选择python3，并且安装了项目依赖包

## 
# 用例脚本编写规范
1. 用例脚本编写时，先封装page方法，再组装测试用例脚本（特殊情况可直接在用例脚本中编写）
2. data数据文件、page方法、用例脚本需要根据模块划分目录
3. 每条用例都需要设置参数化
