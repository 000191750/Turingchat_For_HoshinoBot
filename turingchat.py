import random
import json
import hoshino
from hoshino import Service, aiorequests, priv

sv_help = '''
[回话概率 0.5]设置回话概率（仅管理员且数值在0-0.5之间）
[查看回话概率]查看回话概率
'''.strip()

sv = Service('turingchat', manage_priv=priv.SUPERUSER, enable_on_default=False, visible=True,help_=sv_help, bundle='图灵帮助')

repeatFrequency = 0.1

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

@sv.on_prefix('回话概率')
async def repeat_frequency(bot, ev):
	if not priv.check_priv(ev, priv.SUPERUSER):
		return
	keyword = ev.message.extract_plain_text()
	if keyword and keyword.replace(".",'').isdigit():
		f = float(keyword)
		if f and not (f > 0.5 or f < 0):
			global repeatFrequency
			repeatFrequency = f
			await bot.send(ev, f'概率已设置为{repeatFrequency}')
		else:
			await bot.send(ev, f'{keyword}不是合法的值，请输入一个0-0.5之间的小数')
	else:
		await bot.send(ev, f'{keyword}不是数字，请输入一个0-0.5之间的小数')

@sv.on_fullmatch('查看回话概率')
async def check_frequency(bot, ev):
	await bot.send(ev, f'我有{repeatFrequency}的几率会说话。')

