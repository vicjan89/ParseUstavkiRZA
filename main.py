import os

import config

protections = ("ЛЗШ", "ЗМН", "Контроль УРОВ", "УРОВ",
			   "АПВ", "АВР", "Блокировка АВР", "Защита от замыканий", "ПРД ", "ПРМ ", "Токовая отсечка",
			   "ТО ", "МТЗ ", "сквозных КЗ", " ТЗНП", "|ТЗНП", "Делительная", "Дистанц", "НТЗНП", "Защита от обрыва")
protections_steps = ("1ст", "2ст", "3ст", "4ст", "1 ст", "2 ст", "3 ст", "4 ст", "5 ст", "6 ст")

def parse_header(input_string: str, header_designation: str) -> list:
	headers = []
	start = 0
	end = len(input_string)
	while start <= end:
		index_end = input_string.find(header_designation, start)
		if index_end == -1:
			break
		index_start = input_string.rfind('\n', start, index_end)
		headers.append((index_start+1, index_end))
		start = input_string.find('\n', index_end + 1) + 1
	return headers

def find_prot(input_string: str, prot_name: str, filter: int = 0) -> list:
	run = True
	start = 0
	list_protections = []
	len_prot_name = len(prot_name)
	while run:
		index_start = input_string.find(prot_name, start)
		if index_start == -1:
			run = False
		else:
			from_begin_row = input_string.rfind('\n', start, index_start)
			index_end = index_start + len_prot_name
			if filter == 0 or (index_start - from_begin_row) < filter:
				list_protections.append((index_start, index_end))
			start = index_end
	return list_protections

count_prot = 0
count_steps = 0

for group_name in os.walk(config.path_source, topdown=True, onerror=None, followlinks=False):
	for name in group_name[2]:
		if name == 'Журжево.rst':
			with open(os.path.join(group_name[0], name), 'r', encoding='utf-8') as file:
				str_ustavki = file.read()
				indexes_headers = []
				level3 = parse_header(str_ustavki, '\n""""')
				level2 = parse_header(str_ustavki, '\n~~~~')
				if level3:
					indexes_headers.extend(((i, 3) for i in level3))
					indexes_headers.extend(((i, 2) for i in level2))
				else:
					indexes_headers.extend(((i, 3) for i in level2))
				len_str_ustavki = len(str_ustavki)
				for prot in protections:
					fp = find_prot(str_ustavki, prot, filter=32)
					indexes_headers.extend((i, 4) for i in fp)
				for step in protections_steps:
					fp = find_prot(str_ustavki, step, filter=32)
					indexes_headers.extend((i, 5) for i in fp)
				indexes_headers.sort(key=lambda x: x[0][0])
				len_indexes_headers = len(indexes_headers)
				for num in range(len_indexes_headers):
					item_current = indexes_headers[num]
					if item_current[1] == 4:
						count_prot += 1
					elif item_current[1] == 5:
						count_steps += 1
					print(str(item_current[1]) + ' ' * item_current[1] * 3 + str_ustavki[slice(*item_current[0])])

print(f'Всего РЗА: {count_prot} а ступеней: {count_steps}')



