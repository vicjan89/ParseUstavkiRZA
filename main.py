import os

def parse_header(input_string, header_designation):
	headers = []
	start = 0
	end = len(input_string)
	while start <= end:
		index_end = input_string.find(header_designation, start)
		if index_end == -1:
			break
		index_start = input_string.rfind('\n', start, index_end)
		headers.append(input_string[index_start+1: index_end])
		start = input_string.find('\n', index_end + 1) + 1
	return headers

for group_name in os.walk(r'C:\Users\rzi1\InfoRZA\docs\source\Уставки', topdown=True, onerror=None, followlinks=False):
	for name in group_name[2]:
		if name[-3:] == 'rst':
			with open(os.path.join(group_name[0], name), 'r', encoding='utf-8') as file:
				str_ustavki = file.read()
				print(parse_header(str_ustavki, '\n""""'))

