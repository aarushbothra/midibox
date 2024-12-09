import ezdxf
import svgwrite
import argparse

def dxf_to_svg(dxf_file, svg_file):
    # Read DXF file
    dwg = ezdxf.readfile(dxf_file)
    
    # Get the modelspace where entities are drawn
    msp = dwg.modelspace()
    
    # Create a new SVG drawing
    svg = svgwrite.Drawing(svg_file, profile='tiny')

    # Iterate over entities in the modelspace
    for entity in msp:
        # Convert LINE entities to SVG
        if entity.dxftype() == 'LINE':
            start = entity.dxf.start
            end = entity.dxf.end
            svg.add(svg.line((start.x, start.y), (end.x, end.y), stroke=svgwrite.rgb(0, 0, 0, '%')))
        
        # Convert CIRCLE entities to SVG
        elif entity.dxftype() == 'CIRCLE':
            center = entity.dxf.center
            radius = entity.dxf.radius
            svg.add(svg.circle(center=(center.x, center.y), r=radius, stroke=svgwrite.rgb(0, 0, 0, '%'), fill='none'))
        
        # Convert TEXT entities to SVG
        elif entity.dxftype() == 'TEXT':
            text = entity.dxf.text
            insert = entity.dxf.insert  # Insertion point of the text
            height = entity.dxf.height  # Text height
            svg.add(svg.text(text, insert=(insert.x, insert.y), font_size=height, fill='black'))
        
        # Convert MTEXT (multi-line text) entities to SVG
        elif entity.dxftype() == 'MTEXT':
            text = entity.text  # This gets the full text (multiline text)
            insert = entity.dxf.insert  # Insertion point of the text
            height = entity.dxf.char_height  # Text height
            svg.add(svg.text(text, insert=(insert.x, insert.y), font_size=height, fill='black'))

    # Save the SVG file
    svg.save()

def main():
    # Set up argument parsing
    parser = argparse.ArgumentParser(description='Convert DXF to SVG.')
    parser.add_argument('dxf_file', type=str, help='The input DXF file')
    parser.add_argument('svg_file', type=str, help='The output SVG file')
    
    # Parse arguments
    args = parser.parse_args()
    
    # Convert DXF to SVG
    dxf_to_svg(args.dxf_file, args.svg_file)

if __name__ == '__main__':
    main()
