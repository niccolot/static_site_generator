# Static site generator

Python package to turn a markdown file into a static html page.

## How to use

* Put static content like images or `.css` files in the `static` folder
* Put your `.md` files to be turned into static web pages in the `content` folder
* Execute the program by running the `main.sh` file (first it might be necessary to run `chmod +x main.sh test.sh` in order to run the main and tests script) to see the result on localhost
* There is already some example contents in the `content` and `static` folders already to be used

```bash
git clone https://github.com/niccolot/static_site_generator
cd static_site_generator
chmod +x main.sh test.sh
./test.sh
./main.sh
```

Here some example screenshot of the static site

![](imgs/first_page.png)
![](imgs/second_page.png)

