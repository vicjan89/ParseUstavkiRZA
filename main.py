import os

import config

protections = ("ЛЗШ", "1ст", "2ст", "3ст", "ЗМН", "Контроль УРОВ", "АВР", "Блокировка АВР", "Защита от замыканий",
			   "ТО ", "МТЗ ", "сквозных КЗ", "ТЗНП", "Делительная")

def parse_header(input_string: str, header_designation: str) -> list:
	headers = []
	start = 0
	end = len(input_string)
	while start <= end:
		index_end = input_string.find(header_designation, start)
		if index_end == -1:
			break
		index_start = input_string.rfind('\n', start, index_end)
		headers.append((index_start+1, input_string[index_start+1: index_end]))
		start = input_string.find('\n', index_end + 1) + 1
	return headers

class GroupItems():

	def __init__(self, string_with_headers: str):
		self.string_with_headers = string_with_headers
		self.name = ''
		self.delimeters = tuple()
		self.index_start = 0
		self.index_end = 0
		self.childs = []

	@property
	def laboriousness(self):
		pass

	def parse(self):
		start = self.index_start
		while start <= self.index_end:
			index_name_end = self.string_with_headers.find(self.delimeters[0], start)
			if index_name_end == -1:
				break
			index_name_start = self.string_with_headers.rfind('\n', start, index_name_end)
			gr = GroupItems(self.string_with_headers)
			gr.name=self.string_with_headers[index_name_start + 1: index_name_end]
			start = self.string_with_headers.find('\n', index_name_end + 1) + 1
			gr.index_start = start
			if len(self.childs):
				self.childs[-1].index_end = index_name_start
			if len(self.delimeters) > 1:
				gr.delimeters = self.delimeters[1:]
				gr.parse()
			self.childs.append(gr)
		if self.childs:
			self.childs[-1].index_end = self.index_end

	def __str__(self):
		out_str = f'Название: {self.name}\n'
		out_str += f'Начало: {self.index_start} Конец: {self.index_end}\n'
		for i in self.childs:
			out_str += str(i)
		return out_str


for group_name in os.walk(config.path_source, topdown=True, onerror=None, followlinks=False):
	for name in group_name[2]:
		if name[-3:] == 'rst':
			with open(os.path.join(group_name[0], name), 'r', encoding='utf-8') as file:
				str_ustavki = file.read()
				energoobjects = GroupItems(str_ustavki)
				energoobjects.name = name[:-3]
				energoobjects.index_start = 0
				energoobjects.index_end = len(str_ustavki)
				if '\n====' not in str_ustavki:
					energoobjects.delimeters = ('\n~~~~',)
				else:
					energoobjects.delimeters = ('\n~~~~', '\n""""')
				energoobjects.parse()
				print(energoobjects)
				input()



				# level_designations = ['\n~~~~', '\n""""']
				# level1_designation = find_levels(str_ustavki, level_designations)
				# level_designations.remove(level1_designation)
				# level2_designation = find_levels(str_ustavki, level_designations)
				# print(name, level1_designation, level2_designation)
				# # items = []
				# items_level_1 = parse_header(str_ustavki, '\n====')
				# if items_level_1:
				# 	items.extend(items_level_1)
				# 	items.extend(parse_header(str_ustavki, '\n~~~~', 2))
				# else:
				# 	items.extend(parse_header(str_ustavki, '\n~~~~', 1))
				# items.extend(parse_header(str_ustavki, '\n""""', 3))
				# items.sort(key=lambda x: x[0])
				# items_level_3 = [i for i in items if i[1] == 3]
				# items_level_3.append((-1, 3, ''))
				# for index in range(len(items_level_3)-1):
				# 	for prot in protections:
				# 		if prot in str_ustavki[items_level_3[index][0]:items_level_3[index + 1][0]]:
				# 			items.append((items_level_3[index][0] +1 , 4, prot))
				# items.sort(key=lambda x: x[0])
				# for i in items:
				# 	print(i[1] * 2 * ' ' + i[2])
				# input()

