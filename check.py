#!/usr/bin/env python3
"""提交前檢查 data.json：格式、日期、網址，以及不可出現的個人資料。有問題即以非零結束。"""
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
GROUPS = {'優先參加', '值得參加', '本校常規'}
DATE = re.compile(r'\d{4}-\d{2}-\d{2}')
problems = []
text = (HERE / 'data.json').read_text(encoding='utf-8')
data = json.loads(text)

for key in ['updated', 'checked']:
    if not DATE.fullmatch(str(data.get(key, ''))):
        problems.append(f'{key} 不是 YYYY-MM-DD')
ids = [it.get('id') for it in data.get('items', [])]
if len(ids) != len(set(ids)):
    problems.append('id 重複')
for it in data.get('items', []):
    name = it.get('id', '?')
    for key in ['id', 'name', 'group', 'advice', 'next', 'register', 'usual', 'status', 'links', 'events', 'note', 'school']:
        if key not in it:
            problems.append(f'{name} 缺少 {key}')
    if it.get('group') not in GROUPS:
        problems.append(f'{name} 的 group 不在 {sorted(GROUPS)}')
    for link in it.get('links', []):
        if not str(link.get('url', '')).startswith(('https://', 'http://')) or not link.get('label'):
            problems.append(f'{name} 的連結不完整')
    for e in it.get('events', []):
        if not DATE.fullmatch(str(e.get('date', ''))) or not e.get('label'):
            problems.append(f'{name} 的日期項目不完整：{e}')
        if 'end' in e and (not DATE.fullmatch(str(e['end'])) or e['end'] < e['date']):
            problems.append(f'{name} 的結束日期不對：{e}')
for n in data.get('news', []):
    if not DATE.fullmatch(str(n.get('date', ''))) or not n.get('text') or n.get('id') not in ids:
        problems.append(f'消息不完整或 id 不存在：{n}')
    if n.get('url') and not str(n['url']).startswith(('https://', 'http://')):
        problems.append(f'消息的來源網址不對：{n}')
# 這是公開頁面：不可有電郵、Class_No_Name 形式的學生資料或本機路徑。
if re.search(r'[\w.+-]+@[\w-]+\.\w+', text):
    problems.append('出現電郵地址')
if re.search(r'[^\s、/：:_"]+_\d+_[^\s、/；;"]', text):
    problems.append('出現 Class_No_Name 形式的學生資料')
if '/Users/' in text:
    problems.append('出現本機路徑')
# 老師要求：公開頁面不可出現其他學校的名稱。
for f in ['data.json', 'index.html', 'README.md', 'ROUTINE.md']:
    if '培' + '正' in (HERE / f).read_text(encoding='utf-8'):
        problems.append(f'{f} 出現不可公開的校名')
if 'noindex' not in (HERE / 'index.html').read_text(encoding='utf-8'):
    problems.append('index.html 缺少 noindex')

if problems:
    print('檢查未通過：')
    for p in problems:
        print('  - ' + p)
    sys.exit(1)
print(f"PASS：{len(ids)} 項比賽、{sum(len(it['events']) for it in data['items'])} 個日期、{len(data['news'])} 則消息。")
