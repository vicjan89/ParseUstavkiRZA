import os

import config

protections = ("ЛЗШ", "1ст", "2ст", "3ст", "ЗМН", "Контроль УРОВ", "АВР", "Блокировка АВР", "Защита от замыканий",
			   "ТО ", "МТЗ ", "сквозных КЗ", "ТЗНП", "Делительная")
def parse_header(input_string, header_designation, level):
	headers = []
	start = 0
	end = len(input_string)
	while start <= end:
		index_end = input_string.find(header_designation, start)
		if index_end == -1:
			break
		index_start = input_string.rfind('\n', start, index_end)
		headers.append((index_start+1, level, input_string[index_start+1: index_end]))
		start = input_string.find('\n', index_end + 1) + 1
	return headers

for group_name in os.walk(config.path_source, topdown=True, onerror=None, followlinks=False):
	for name in group_name[2]:
		if name[-3:] == 'rst':
			with open(os.path.join(group_name[0], name), 'r', encoding='utf-8') as file:
				str_ustavki = file.read()
				items = []
				items.extend(parse_header(str_ustavki, '\n====', 1))
				items.extend(parse_header(str_ustavki, '\n~~~~', 2))
				items.extend(parse_header(str_ustavki, '\n""""', 3))
				items.sort(key=lambda x: x[0])
				items_level_3 = [i for i in items if i[1] == 3]
				items_level_3.append((-1, 3, ''))
				for index in range(len(items_level_3)-1):
					for prot in protections:
						if prot in str_ustavki[items_level_3[index][0]:items_level_3[index + 1][0]]:
							items.append((items_level_3[index][0] +1 , 4, prot))
				items.sort(key=lambda x: x[0])
				for i in items:
					print(i[1] * 2 * ' ' + i[2])
				input()

