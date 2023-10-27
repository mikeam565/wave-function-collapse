# wave-function-collapse
Foray into wave function collapse

Very simple wfc attempt to generate terrain. The math currently isn't really set up correctly, but it works pretty good so I've put that aside in favor of messing with exploration algorithms.  

The most fun of these exploration algorithms so far (and what the code currently does) is drawing! Simply click and drag (start from the center). The brush generates a box around the mouse click (currently top left to bottom right) and handles conflicts (when a space has conflicting adjacencies eg. dense trees next to water which is not permitted in the current probabilities mappings) with the cliff terrain.  

Here's an example:
![Example generation](./wfc_example.png)  

Other algorithms are commented out. I intend on cleaning this up.  

I also intend on implementing keeping track of each unpopulated tile's possible terrain options, and algorithmically populating the ones with the lowest possible options. This should allow terrain to be generated consistently from any starting tile without resorting to cliffs to handle conflicts. You can see that this would be the case in action with user draw: if you draw where there aren't a lot of options for the terrain to be generated (where water and land meet, especially if there's trees close by), you will avoid cliffs from being generated.  