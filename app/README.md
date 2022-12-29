# Procedural 2D Island Generation
## Project Description
### What does my application do?
This application utilizes the aspects of the Perlin noise created and developed by Ken Perlin in 1983.
It is inspired by terrain generation in games like Minecraft, Terraria, or basically any open world game. The application takes parameters which can be tweaked and generates a 2-dimensions perlin noise and stores it in 2-dimensions numpy array. Then it translates the values to rgb and displays it as image or plot.

### Why I used the technologies i used?
I used the Perlin noise because of it's quick pseudo-random generation and use of fractals which fascinated me. I found already pre-made implementation of perlin noise in library named "noise" which can make 1,2,3 dimension perlin noise. Later I added my own implementation inspired by the creator of Ken Perlin. Other python noise libraries like SimplexNoise were too slow for my liking, althrough stable and useful. I used numpy for calculating and better array handling because I had to use a lot of arithmetic operations when generating random data.
For displaying the array I found mathplotlib the best.
I also used the PIL library.
For graphical interface I used tkinter library and then the customized version customtkinter for even better looks.

### Challenges and problems.
It was a great challenge for me to bring something new to this big projects and I hope I managed to build something creative, which i believe i did.
It was very tedious to tweak each number so my noise generation works the intended way. All noise generation projects come down to tweaking small numbers, because each implementation of code has it's own interval of parameters that have to be tweaked individually. There is no universal number or parameter to create "nice" noise. In point I had to change numbers in the second decimal places for it to work the way I liked.
## How to Run the Project
In the same directory this README.md file is located you can find the "main.py" file. Run the python3 main.py in terminal and all of the other modules will run up. The graphical interface will appear in which you can tweak individual parameters for your liking and then press the "Generate island!" and wait for the result image. The interface is very intuitive. But if you are for any reason lost the parameters work like this:

## Configurations & How to Use
Octaves - the number of levels of detail you want you perlin noise to have. Adds a new layer of detail to the surface.
Persistence - number that determines how much each octave contributes to the overall shape (adjusts amplitude).
Lacunarity - number that determines how much detail is added or removed at each octave (adjusts frequency).

Mode - There is 7 different island modes. Some favorize forest others lava or deserts. Try it out and see your favourite one.

Width, Height - The resolution of the randomly generated image.  

Save Images - If selected, saves all of the images to the utils/images file. Can save also 3d plots to the utils/graphs file.

Custom Noise - If selected, the program uses the my custom implementation of the perlin noise.

3D Plot - If selected, it will show the moisture and elevation 3d surface plots in a figure.

Generate button - After you are satisfied with the values, press the button and wait.

## Credits and Thanks
I used many interesting science works for this topic,
here are the ones I used:
https://en.wikipedia.org/wiki/Perlin_noise
https://core.ac.uk/download/pdf/34480918.pdf
huttar.net/lars-kathy/graphics/perlin-noise/perlin-noise.html
https://mzucker.github.io/html/perlin-noise-math-faq.html
#### Jáchym Křeček
#### https://gitlab.fit.cvut.cz/BI-PYT/B221/krecejac.git