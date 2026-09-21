with open('app/templates/index.html', 'r') as f:
    content = f.read()

content = content.replace('class="grid grid-cols-1 md:grid-cols-3 gap-6"', 'class="flex flex-col lg:flex-row gap-8"')
content = content.replace('class="bg-white p-6 rounded-lg shadow-sm border border-gray-200 flex-1 md:col-span-2 flex flex-col"', 'class="bg-white p-8 rounded-2xl shadow-xl border border-slate-100 flex-1 flex flex-col h-[40rem]"')
content = content.replace('<h3 class="font-semibold">Agent 実行ログ & 結果</h3>', '<h3 class="text-xl font-bold text-slate-700 flex items-center gap-2"><span>🤖</span> Agent 実行ログ & 結果</h3>')
content = content.replace('<select id="download-format" class="border rounded px-2 py-1 text-sm bg-white">', '<select id="download-format" class="border-2 border-slate-200 p-2 rounded-lg text-sm bg-white focus:border-indigo-500 outline-none transition-colors">')
content = content.replace('<div class="bg-white p-6 rounded-lg shadow-sm border border-gray-200">', '<div class="bg-white p-8 rounded-2xl shadow-xl border border-slate-100 w-full lg:w-72 flex-shrink-0">')

with open('app/templates/index.html', 'w') as f:
    f.write(content)
