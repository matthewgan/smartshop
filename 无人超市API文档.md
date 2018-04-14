# 智慧零售API文档_V0.1
##1. 概述
##2. 数据结构
####2.1 用户/`customer`
通过小程序端微信认证登录注册的用户

| 字段 | 允许空值 | 类型 | 长度 | 描述 |
| --- | --- | --- | --- | --- |
| customer_id* | NO | int | 10 | 用户数据库id，自增长int |
| uuid | NO | char | 30 | 用户唯一识别符，回传小程序端存储，访问识别 |
| openId | NO | char | 30 | 微信用户唯一识别符 |
| user_nickName | NO | char |  | 用户昵称，获取自微信端 |
| user_avataUrl  | YES | char |  | 用户头像地址，获取自微信端 |
| user_gender | NO | int | 1 | 用户的性别，值为1时是男性，值为2时是女性，值为0时是未知 |
| user_city | YES | char |  | 用户城市，获取自微信端 |
| user_province | YES | char |  | 用户省份，获取自微信端 |
| user_country | YES | char |  | 用户国家，获取自微信端 |
| user_language | YES | char |  | 用户语言，获取自微信端 |
| user_level | YES | char |  | 用户会员等级 |
| user_point | YES | char |  | 用户会员积分 |
| user_face | YES | int |  | 用户面部数据id |

####2.2 商铺/`shop`
店面数据库


| 字段 | 允许空值 | 类型 | 长度 | 描述 |
| --- | --- | --- | --- | --- |
| shop_id* | NO | int | 10 | 商铺数据库id，自增长int |
| shop_name | NO | char |  | 商铺名称 |
| shop_longitude | NO | long | 10 | 商铺地理位置，经度 |
| shop_latitude | NO | long | 10 | 商铺地理位置，纬度 |
| shop_size | NO | long | 5 | 商铺面积 |
| shop_owner | NO  | char |  | 商铺所有者 |
| shop_capbility | NO | int | 5 | 商铺SKU数量 |
| shop_status | NO | int | 1 | 1为正常营业，0为暂停营业，2为补货中 |

####2.3 商品基本信息/`product_info`

| 字段 | 允许空值 | 类型 | 长度 | 描述 |
| --- | --- | --- | --- | --- |
| product_id* | NO | int | 10 | 商品唯一编码 |
| product_name | NO | char | 30 | 商品名称 |
| product_imageUrl | NO | char | 300 | 商品图片url |
| product_description | NO | char | 300 | 商品文字描述 |
| product_categoryId | NO | int | 2 | 商品类别id |
| quantityPerUnit | NO | long | 5 | 商品重量
| unitSelled | NO | int | 5 | 总计售出的数量 |

####2.4 商品销售信息/`product_SUK`

| 字段 | 允许空值 | 类型 | 长度 | 描述 |
| --- | --- | --- | --- | --- |
| SKU_id* | NO | int | 10 | 商品SKU唯一编码 |
| product_id | NO | int | 10 | 商品唯一编码 |
| shop_id | NO | int | 10 | 商铺数据外链，商品所在商铺 |
| product_buyPrice | NO | long | 6 | 商品进货价 |
| product_sellPrice | NO | long | 6 | 商品零售价 |
| product_discount | NO | long | 6 | 商品折扣价 |
| unitInStore | NO | int | 3 | 商品库存数量 |
####2.5 货架/`rack`


| 字段 | 允许空值 | 类型 | 长度 | 描述 |
| --- | --- | --- | --- | --- |
| rack_id* | NO | int | 10 | 货架唯一识别id |
| rack_size | NO | long | 10 | 货架大小 |
| rack_level | NO | int | 2 | 货架层数 |
| rack_capbiity  | NO | int | 5 | 货架商品数量 |
| unitOnOrder | NO | int | 3 | 商品下单补货数量 |
| product_ids | NO | array |  | 货架包含的商品 id 列表 |

####2.6 订单/`order`


| 字段 | 允许空值 | 类型 | 长度 | 描述 |
| --- | --- | --- | --- | --- |
| order_id* | NO | int | 10 | 货架唯一识别id |
| customer_id | NO | int | 10 | 用户数据库id|
| shop_id | NO | int | 10 | 商铺数据库id |
| order_status | NO | int | 1 | 订单状态 |
| payment_method | NO | char | 10 | 订单支付方式 |
| total_cost  | NO | long | 15 | 订单总金额 |
| address_book_id | NO | int | 20 | 订单关联的地址id |
| remark | YES | char | 200 | 订单备注 |


####2.7 订单详情/`order_detail`


| 字段 | 允许空值 | 类型 | 长度 | 描述 |
| --- | --- | --- | --- | --- |
| detail_id* | NO | int | 10 | id |
| order_id | NO | int | 10 | 用户数据库id|
 |product_name | NO | int | 10 | 商品id |
| SKU_id | NO | int | 10 | 关联的商品sku id |
| quantity | NO | int | 5 | 数量 |
| unit_price  | NO | long | 15 | 单价 |
| sell_price  | NO | long | 15 | 成交价 |

####2.8 脸部图像数据库/`face_data`


| 字段 | 允许空值 | 类型 | 长度 | 描述 |
| --- | --- | --- | --- | --- |
| face_id* | NO | int | 10 | id |
| customer_id | NO | int | 10 | 用户数据库id|
 |faceUrl | NO | array |  | 脸部图像库 |

####2.9 商品类别/`product_category`


| 字段 | 允许空值 | 类型 | 长度 | 描述 |
| --- | --- | --- | --- | --- |
| category_id* | NO | int | 10 | id |
| category_name | NO | char | 20 | 分类名称|

##3. 数据接口
###3.1 微信小程序与后台交互
####3.1.1 新用户首次登陆或删除小程序后首次登陆（不鉴权）
- ***API***

```
url: /api/wxlogin/
method: 'POST'
header: 'Content-type: application/json'
data: {code:[微信获得登陆code]，
       nickName:[微信userInfo信息]
       avataUrl:[微信userInfo信息]
       city:[微信userInfo信息]
       province:[微信userInfo信息]
       country:[微信userInfo信息]
       gender:[微信userInfo信息]
       language:[微信userInfo信息]
       }  
```
> ***服务器端***
1 此API访问不鉴权
2 获取微信端登陆code，与腾讯服务器通信获取用户openId和session_key
3 在数据库中查找对应openId用户
    - 如果查询到，则返回对应用户的uuid及password
    - 如果未查询到，则为新登陆用户，首先在数据库中创建新用户，并将客户端附带的userInfo填入对应值，同时基于生成一串随机字符串作为password存入数据库，随后将uuid和passowrd返回至客户端，同时在Django框架中以uuid为用户名，password为密码拥有api访问权限的用户。


```
服务器返回值
Response:{
    uuid:""
    password:""
}

```

####3.1.2 已经获得uuid和password的用户在未获得token或者token过期后登陆获取token(不鉴权)
- ***API***

```
url: /api/rest_auth/login
method: 'POST'
header: 'Content-type: application/json'
data: {username:[本地缓存uuid]，
       password:[本地缓存password]
       }  
```
> ***服务器端***
1 此API访问不鉴权
2 如uuid及password合法，则返回客户端JWT token

```
服务器返回值
Response:{
    token:""
}

```
####3.1.3 以获得token的小程序从服务器端获取用户会员积分及等级
- ***API***

```
url: /api/wxUser/getCustomerInfo
method: 'POST'
header: 'Authorization':'JWT: [本地缓存token]''Content-type: application/json'
data: {uuid:[本地缓存uuid]，
       }  
```
> ***服务器端***
1 此API访问铜鼓token判断是否为何法访问
2 如token合法，则返回相应请求数据；如token过期或不合法，则返回错误信息。

```
服务器返回值
Success Response:{
    status:"1"
    level:""
    point:""
}
Fail Response:{
    status:"0"
    errorMessage:""

}

```


