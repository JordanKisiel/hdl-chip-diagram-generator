from PIL import Image, ImageDraw, ImageFont

width = 600
height = 400

out = Image.new("RGB", (width, height), (255, 255, 255))

chip_font = ImageFont.truetype("FreeMono.ttf", 30)
chip_io_font = ImageFont.truetype("FreeMono.ttf", 20)
part_font= ImageFont.truetype("FreeMono.ttf", 20)
part_io_font= ImageFont.truetype("FreeMono.ttf", 15)

draw_context = ImageDraw.Draw(out)

# chip title
draw_context.text(((width / 2) - 30, 10), "Foo", (0, 0, 0), chip_font, align="center")
# chip outline
# the round corners look pretty jagged, is there any way to alias the drawing?
draw_context.rounded_rectangle([(100, 60), (width - 100, height - 30)], 
                               15, 
                               outline=(0, 0, 0), 
                               width=2)
# primitive chip title
draw_context.text(((width / 2) - 20, 200), "Not", (0, 0, 0), part_font, align="center")
# primitive chip outline
draw_context.rounded_rectangle([(200, 150), (width - 200, height - 120)], 
                               10, 
                               outline=(0, 0, 0), 
                               width=2)
# Foo Chip in1
draw_context.text((40, 125), "in1", (0, 0, 0), chip_io_font, align="center")
draw_context.line([(20, 150), (100, 150)], (0, 0, 0), 2)
# Foo Chip in2
draw_context.text((40, 250), "in2", (0, 0, 0), chip_io_font, align="center")
draw_context.line([(20, 275), (100, 275)], (0, 0, 0), 2)
# Foo Chip out
draw_context.text((width - 75, 195), "out", (0, 0, 0), chip_io_font, align="center")
draw_context.line([(width - 100, height / 2 + 20), (width - 20, height / 2 + 20)], (0, 0, 0), 2)
# Not Part a
draw_context.text((175, 175), "a", (0, 0, 0), part_io_font, align="center")
draw_context.line([(160, 190), (200, 190)], (0, 0, 0), 2)
# Not Part b 
draw_context.text((175, 220), "b", (0, 0, 0), part_io_font, align="center")
draw_context.line([(160, 235), (200, 235)], (0, 0, 0), 2)
# Not Part out
draw_context.text((405, 205), "out", (0, 0, 0), part_io_font, align="center")
draw_context.line([(width - 200, height / 2 + 20), (width - 160, height / 2 + 20)], (0, 0, 0), 2)
# out = out connection 
draw_context.line([(width - 160, height / 2 + 20), (width - 100, height / 2 + 20)], (0, 0, 0), 2)
# in1 = a connection (first segment)
draw_context.line([(100, 150), (140, 150)], (0, 0, 0), 2)
# in1 = a connection (second segment)
draw_context.line([(140, 150), (140, 190)], (0, 0, 0), 2)
# in1 = a connection (third segment)
draw_context.line([(140, 190), (160, 190)], (0, 0, 0), 2)
# in2 = b connection (first segment)
draw_context.line([(100, 275), (140, 275)], (0, 0, 0), 2)
# in2 = b connection (second segment)
draw_context.line([(140, 275), (140, 235)], (0, 0, 0), 2)
# in2 = b connection (third segment)
draw_context.line([(140, 235), (160, 235)], (0, 0, 0), 2)
out.save("test.png")
