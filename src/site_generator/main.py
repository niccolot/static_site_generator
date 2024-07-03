from site_generator import generator


def main():
    generator.copy_static_contents("static", "public")
    generator.generate_pages_recursive("content", "template.html", "public")
    

if __name__ == "__main__":
    main()