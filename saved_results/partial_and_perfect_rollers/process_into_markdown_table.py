ordered_tilings = ['3^6', '4^4', '6^3', '3^4x6', '3^3x4^2', '3^2x4x3x4', '3x4x6x4', '3x6x3x6', '3x12^2', '4x6x12', '4x8^2', '(3^6;3^4x6)1', '(3^6;3^4x6)2', '(3^6;3^3x4^2)1', '(3^6;3^3x4^2)2', '3^6;3^2x4x3x4', '3^6;3^2x4x12', '3^6;3^2x6^2', '3^4x6;3^2x6^2', '(3^3x4^2;3^2x4x3x4)1', '(3^3x4^2;3^2x4x3x4)2', '3^3x4^2;3x4x6x4', '(3^3x4^2;4^4)1', '(3^3x4^2;4^4)2', '3^2x4x3x4;3x4x6x4', '3^2x6^2;3x6x3x6', '3x4x3x12;3x12^2', '3x4^2x6;3x4x6x4', '(3x4^2x6;3x6x3x6)1', '3x4^2x6;3x6x3x6)_2', '3x4x6x4;4x6x12']

categories = dict()
current_category = ""

tiling_urls = []

with open("tiling_urls.txt","r") as f:
    lines = f.read().strip().split("\n")
    # print(lines)
    for line in lines:
        # if(line!=line.strip()):
        #     print("Err")
        if line.startswith("http"):
            tiling_urls.append(line.strip())
            categories[current_category].append(line.strip())
        else:
            current_category=line.strip()
            categories[line.strip()]=list()
    # print(categories)

with open("rollers_position_urls.txt","r") as f:
    roller_entries_url = [line.strip() for line in f.read().strip().split("\n")]

# print(roller_entries_url)

ordered_lines_data = {tiling:([],[]) for tiling in ordered_tilings}

with open("rollers.txt","r") as f:
    lines = f.read().strip().split("\n")
    for index,line in enumerate(lines):
        tiling, poly, c,f,o, faces = line.split(" ")
        partial = faces!="None"
        ordered_lines_data[tiling][partial].append((poly,roller_entries_url[index]))

output = "#|Tiling|Perfect rollers|Partial rollers|\n"
output+= "-|------|---------------|---------------|\n"

for category, tilings in categories.items():
    output += "||"+category + "\n"
    for tiling_url in tilings:
        index = tiling_urls.index(tiling_url)
        tiling_name = ordered_tilings[index]
        tiling = "[%s](%s)"%(tiling_name,tiling_url)
        perfect, partial = ordered_lines_data[tiling_name]
        perfects = ", ".join(["[%s](%s)"%(p,url) for p,url in perfect]) or "None"
        partials = ", ".join(["[%s](%s)"%(p,url) for p,url in partial]) or "None"
        output+= "%i|%s|%s|%s|\n"%(index,tiling,perfects,partials)
print(output)