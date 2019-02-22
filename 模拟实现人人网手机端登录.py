import requests
import js2py

# 创建session对象
session = requests.session()

# 创建请求头
session.headers = {
	'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Mobile Safari/537.36',
}

# 准备rkey的url
rkey_url = 'http://activity.renren.com/livecell/rKey'

# 发送rkey请求,获取rkey数据
response = session.get(rkey_url)

# 将获取的json数据装换为字典
rkey_dict_data = response.json()

# 准备js运行环境依赖的n数据
n = rkey_dict_data['data']

# 使用js2py生成加密后的密码
# 生成js的运行环境
context = js2py.EvalJs()

# 准备要执行的js语句
js_str = '''  t.password = t.password.split("").reverse().join(""),
              setMaxDigits(130);
              var o = new RSAKeyPair(n.e,"",n.n),
              r = encryptedString(o, t.password);
		'''

# 添加环境依赖的t
context.t = {'password': 'rrw19940110'}

# 添加环境依赖的数据n
context.n = n

# 添加环境依赖的js
context.execute(session.get('http://s.xnimg.cn/a85738/wap/mobile/wechatLive/js/BigInt.js').content.decode())
context.execute(session.get('http://s.xnimg.cn/a85738/wap/mobile/wechatLive/js/RSA.js').content.decode())
context.execute(session.get('http://s.xnimg.cn/a85738/wap/mobile/wechatLive/js/Barrett.js').content.decode())

# 执行目标js，获取
context.execute(js_str)

# 获取加密后的密码
password = context.r

# 登录人人网的url
login_url = 'http://activity.renren.com/livecell/ajax/clog'

# 准备请求的数据
data = {
	'phoneNum': '18681510771',
	'password': password,
	'c1': '-100',
	'rKey': n['rkey']
}

# 发送登录请求
responsen = session.post(login_url, data=data)

# 展示登录界面的数据
print(response.content.decode())
