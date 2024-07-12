import argparse

import png

def get_argument_parser():
    parser = argparse.ArgumentParser(description="IMIT (image editor)")

    parser.add_argument("-f", "--file",
                        help="Imagename which is to be edit", type=str, required=True)
    
    parser.add_argument("-r", "--relative_resize",
                        help="Relative resize image", type=int, nargs="+")
    
    parser.add_argument("-R", "--resize",
                        help="Resize image", type=int, nargs="+")
    
    parser.add_argument("-i", "--info",
                        help="Get image's info", action="store_true")

    return parser

def main():
    parser = get_argument_parser()

    args = parser.parse_args()

    image = png.PNG_img(args.file)

    if args.info:
        print(f"File name: {image.file_name}")
        print(f"File height: {image.file_height}")
        print(f"File widht: {image.file_width}")

    if args.relative_resize:
        image.rresize(args.relative_resize[0], args.relative_resize[1])
    
    if args.resize:
        image.resize(args.resize[0], args.resize[1])

if __name__ == '__main__':
    main()