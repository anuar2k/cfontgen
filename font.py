from PIL import Image
import os

def generateFont(filename, name, w, h):
    image = Image.open(filename)

    if (image.size[0] % w != 0 or image.size[1] % h != 0):
        raise ValueError('wrong w/h of chars')

    pixels = image.load()

    f = open(os.path.splitext(filename)[0] + '.h', 'w', encoding='utf-8')
    f.write(f'#define {name}_COLS {w}\n')
    f.write(f'#define {name}_ROWS {image.size[1] // h}\n')

    cnt = 0
    f.write('\n')
    for charStartX in range(0, image.size[0], w):
        rows = []
        for charStartY in range(0, image.size[1], h):
            line = []
            for x in range(charStartX, charStartX + w):
                byte = ''
                for y in range(charStartY, charStartY + h):
                    byte = byte + ('1' if pixels[x, y] == (0,0,0) else '0')
                byte = '0b' + byte[::-1]
                line.append(byte)
            rows.append('{' + ', '.join(line) + '};')

        for idx in range(0, image.size[1] // h):
            f.write(f'char {name}_{cnt}_{idx}[] = {rows[idx]}\n')

        cnt = cnt + 1
    
    numbers = []

    f.write('\n')
    for char in range(image.size[0] // w):
        rows = []
        for row in range(image.size[1] // h):
            rows.append(f'{name}_{char}_{row}')
        rows = '{' + ', '.join(rows) + '};'
        f.write(f'char* {name}_{char}[] = {rows}\n')
        numbers.append(f'{name}_{char}')
    
    numbers = '{' + ', '.join(numbers) + '};'
    f.write('\n')
    f.write(f'char** {name}[] = {numbers}\n')

generateFont('font1.bmp', 'BIGNUM', 10, 8)
generateFont('font2.bmp', 'MIDNUM', 6, 8)
