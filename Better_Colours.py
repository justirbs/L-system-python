def hex_to_rgb(h): 
    s = '0123456789abcdef' 
    return [s.index(h[1]) * 16 + s.index(h[2]), s.index(h[3]) * 16 + s.index(h[4]), s.index(h[5]) * 16 + s.index(h[6])] 
   
def get_colors(): 
    colors = [] 
    with open("color.conf", "r") as f: 
        for line in f: 
            if line[0] == "#": 
                colors.append(hex_to_rgb(line.strip())) 

    return colors 

def create_blended_colors(blend_factor, args): 
    colors = args + [args[0]] 
    all_colors = [] 
    for i in range(len(colors)-1): 
        c1, c2 = colors[i], colors[i+1] 
        d_red   = (c2[0] - c1[0]) / blend_factor 
        d_green = (c2[1] - c1[1]) / blend_factor 
        d_blue  = (c2[2] - c1[2]) / blend_factor 
        for s in range(blend_factor): 
            all_colors.append([int(c1[0] + d_red * s), int(c1[1] + d_green * s), int(c1[2] + d_blue * s)]) 

    return all_colors
