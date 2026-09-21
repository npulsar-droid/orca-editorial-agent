import re

with open('app/templates/index.html', 'r') as f:
    content = f.read()

# Body
content = content.replace('class="bg-gray-50 text-gray-800"', 'class="bg-slate-50 text-slate-800 font-sans"')
content = content.replace('class="max-w-4xl mx-auto py-10 px-4"', 'class="max-w-5xl mx-auto py-12 px-6"')
content = content.replace('<h1 class="text-3xl font-bold mb-2">Orca-Editorial Agent</h1>', '<div class="text-center mb-12"><h1 class="text-4xl font-extrabold mb-3 tracking-tight text-transparent bg-clip-text bg-gradient-to-r from-blue-600 to-indigo-600">Orca-Editorial Agent</h1>')
content = content.replace('<p class="text-gray-600 mb-8">コストを68%削り、品質を極める「完全自律型AI編集部」</p>', '<p class="text-slate-500 font-medium text-lg">コストを68%削り、品質を極める「完全自律型AI編集部」</p></div>')

# Top Box
content = content.replace('class="bg-white p-6 rounded-lg shadow-sm border border-gray-200 mb-6"', 'class="bg-white p-8 rounded-2xl shadow-xl border border-slate-100 mb-8"')
content = content.replace('class="text-xl font-semibold whitespace-nowrap"', 'class="text-xl font-bold text-slate-700 whitespace-nowrap"')
content = content.replace('class="flex-1 border p-2 rounded text-sm"', 'class="flex-1 border-2 border-slate-200 focus:border-indigo-500 focus:ring-4 focus:ring-indigo-500/20 p-3 rounded-xl text-sm transition-all outline-none"')

# Selects & Buttons
content = content.replace('class="border p-2 rounded bg-white"', 'class="border-2 border-slate-200 focus:border-indigo-500 focus:ring-4 focus:ring-indigo-500/20 p-3 rounded-xl bg-white transition-all outline-none cursor-pointer"')
content = content.replace('class="border p-2 rounded bg-white text-sm"', 'class="border-2 border-slate-200 focus:border-indigo-500 focus:ring-4 focus:ring-indigo-500/20 p-3 rounded-xl bg-white text-sm transition-all outline-none cursor-pointer"')
content = content.replace('class="bg-blue-600 text-white px-6 py-2 rounded hover:bg-blue-700"', 'class="bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 text-white px-8 py-3 rounded-xl font-semibold shadow-md hover:shadow-lg transition-all duration-200 transform hover:-translate-y-0.5"')
content = content.replace('class="hidden bg-red-600 text-white px-6 py-2 rounded hover:bg-red-700"', 'class="hidden bg-gradient-to-r from-red-500 to-rose-600 hover:from-red-600 hover:to-rose-700 text-white px-8 py-3 rounded-xl font-semibold shadow-md transition-all duration-200"')
content = content.replace('class="bg-gray-100 text-gray-700 px-4 py-2 border rounded hover:bg-gray-200 text-sm"', 'class="bg-slate-100 text-slate-700 px-5 py-2.5 rounded-xl border border-slate-200 hover:bg-slate-200 hover:shadow-sm text-sm font-medium transition-all cursor-pointer"')

# Textarea
content = content.replace('class="w-full border p-2 rounded h-24 text-sm"', 'class="w-full border-2 border-slate-200 focus:border-indigo-500 focus:ring-4 focus:ring-indigo-500/20 rounded-xl p-4 h-32 text-sm transition-all outline-none resize-y"')

# Bottom section
content = content.replace('class="flex flex-col md:flex-row gap-6"', 'class="flex flex-col lg:flex-row gap-8"')
content = content.replace('class="flex-1 flex flex-col bg-white p-6 rounded-lg shadow-sm border border-gray-200"', 'class="flex-1 flex flex-col bg-white p-8 rounded-2xl shadow-xl border border-slate-100"')
content = content.replace('class="text-xl font-semibold"', 'class="text-xl font-bold text-slate-700"')
content = content.replace('class="bg-blue-100 text-blue-700 px-3 py-1 rounded text-sm hover:bg-blue-200 flex items-center gap-1"', 'class="bg-indigo-50 text-indigo-700 px-4 py-2 rounded-lg text-sm font-medium hover:bg-indigo-100 flex items-center gap-1 transition-colors"')
content = content.replace('class="border p-1 rounded text-sm bg-white"', 'class="border-2 border-slate-200 p-2 rounded-lg text-sm bg-white focus:border-indigo-500 outline-none transition-colors"')
content = content.replace('class="bg-green-600 text-white px-3 py-1 rounded text-sm hover:bg-green-700 flex items-center gap-1"', 'class="bg-gradient-to-r from-emerald-500 to-green-600 text-white px-4 py-2 rounded-lg text-sm font-medium hover:from-emerald-600 hover:to-green-700 flex items-center gap-1 shadow-sm transition-all transform hover:-translate-y-0.5"')

# Meta Box
content = content.replace('class="bg-white p-6 rounded-lg shadow-sm border border-gray-200"', 'class="bg-white p-8 rounded-2xl shadow-xl border border-slate-100"')

# Terminal
old_terminal = '<div id="output" class="bg-gray-900 text-green-400 p-4 rounded flex-1 min-h-[16rem] overflow-y-auto whitespace-pre-wrap font-mono text-sm leading-relaxed">スタンバイ...</div>'
new_terminal = '''
                <div class="relative flex-1 flex flex-col rounded-xl overflow-hidden shadow-inner border border-slate-800">
                    <div class="bg-slate-800 px-4 py-2 flex items-center gap-2">
                        <div class="w-3 h-3 rounded-full bg-rose-500"></div>
                        <div class="w-3 h-3 rounded-full bg-amber-500"></div>
                        <div class="w-3 h-3 rounded-full bg-emerald-500"></div>
                        <div class="text-[10px] text-slate-400 font-mono ml-2 uppercase tracking-widest">agent-terminal</div>
                    </div>
                    <div id="output" class="bg-slate-900 text-emerald-400 p-5 flex-1 min-h-[16rem] overflow-y-auto whitespace-pre-wrap font-mono text-sm leading-relaxed shadow-inner">スタンバイ...</div>
                </div>
'''
content = content.replace(old_terminal, new_terminal)

with open('app/templates/index.html', 'w') as f:
    f.write(content)
