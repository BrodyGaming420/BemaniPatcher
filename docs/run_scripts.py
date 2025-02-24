from pathlib import Path
import subprocess
import sys
import time

# copy multiple DLLs to here with the datecode appended

# x64 ddr example: `gamemdx-2022020200x64.dll`
# everything else: `soundvoltex-2022021400.dll` etc

games = [
    {
        'script': 'ddr',
        'title': 'DDR A3',
        'dll': 'gamemdx',
        'html': 'ddra3.html',
    },
    {
        'script': 'gitadora',
        'title': 'GITADORA HIGH-VOLTAGE',
        'dll': 'game',
        'html': 'gitadorahv.html',
    },
    {
        'script': 'iidx',
        'title': 'IIDX RESIDENT',
        'dll': 'bm2dx',
        'html': 'resident.html',
    },
    {
        'script': 'jubeat',
        'title': 'jubeat Ave.',
        'dll': 'jubeat',
        'html': 'jubeatave.html',
    },
    {
        'script': 'popn',
        'title': 'pop\'n music UniLab',
        'dll': 'popn22',
        'html': 'popn27unilab.html',
    },
    {
        'script': 'sdvx',
        'title': 'SDVX EXCEED GEAR',
        'dll': 'soundvoltex',
        'html': 'sdvx6.html',
    },
]

start = time.time()

for g in games:
    header = (
f'''<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <title>{g.get("title")} DLL Modder</title>
    <link rel="stylesheet" href="css/style.css" />
    <script type="text/javascript" src="js/dllpatcher.js"></script>
    <script type="text/javascript">
        window.addEventListener("load", function () {{
            new PatchContainer([
''')

    footer = (
f'''
            ]);
        }});
    </script>
  </head>
  <body>
    <h1>{g.get("title")} DLL Modder</h1>
  </body>
</html>
''')

    with open(g.get("html"), 'w', newline='\n') as outfile:
        outfile.write(header.rstrip())
        for dll in Path('.').glob(f'{g.get("dll")}-*.dll'):
            print(dll, g.get("html"))
            try:
                name, d = str(dll.stem).split('-')
            except ValueError:
                print(f'Requires the format to match example: {g.get("dll")}-2022010100.dll')
                continue
            d = "-".join([d[:4], d[4:6], d[6:8], d[8:]])
            if str(dll.stem).endswith('x64'):
                d = d[:-3]
            datecode = d[:-3] if d[-3:] == '-00' else d
            orig = g.get("dll")+dll.suffix
            Path(dll).rename(Path(orig))
            if not str(dll.stem).endswith('x64'):
                outfile.write(f'\n                new Patcher("{orig}", "{datecode}", [\n')
                output = subprocess.run([sys.executable, f'{g.get("script")}.py'], capture_output=True, text=True)
            else:
                outfile.write(f'\n                new Patcher("{orig}", "{datecode} (x64)", [\n')
                output = subprocess.run([sys.executable, f'{g.get("script")}_x64.py'], capture_output=True, text=True)
            output = output.stdout.replace('\n', '\n                    ').rstrip()
            outfile.write("                    "+output)
            outfile.write('\n                ]),')
            Path(orig).rename(Path(dll))
        outfile.write(footer)
    if Path(g.get("html")).stat().st_size < 1000:
        Path(g.get("html")).unlink()

end = time.time()

print()
print("Elapsed time:", end - start)
