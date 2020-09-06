import random
import json
import hoshino
from hoshino import Service, aiorequests, priv

sv_help = '''
[回话概率 0.5]设置回话概率（仅管理员且数值在0-0.5之间）
[查看回话概率]查看回话概率
'''.strip()

sv = Service('turingchat', manage_priv=priv.SUPERUSER, enable_on_default=False, visible=True,help_=sv_help, bundle='图灵')

repeatFrequency = 0.1
#这里设置机器人回复的概率

@sv.on_message('group')
async def tulingchat(bot, ctx):
	text = ctx['message'].extract_plain_text()
	if not text or random.random() > repeatFrequency :
		return
	payload = {
		'reqType':0,
		'perception': {
			'inputText': {
				'text': text,
			}
		},
		'userInfo': {
			'apiKey': '7508cb12fdb54ec7896d193e4ef10ffe',
			#在这里填写你的图灵的apikey
			'userId': ctx['user_id'],
			#'groupId': ctx['group_id']
		}
	}

	sv.logger.debug(payload)
	api = 'http://openapi.tuling123.com/openapi/api/v2'
	rsp = await aiorequests.post(api, json=payload, timeout=10)
	rsp_payload = await rsp.json()
	if rsp_payload['results']:
		for result in rsp_payload['results']:
			if result['resultType'] == 'text':
				await bot.send(ctx, result['values']['text'])

@sv.on_fullmatch('查看回话概率')
async def check_frequency(bot, ctx):
	await bot.send(ctx, f'我有{repeatFrequency}的几率会说话。')

