# wave-function-collapse
Foray into wave function collapse

Very simple wfc attempt to generate terrain. The math currently isn't really set up correctly, but it works pretty good so I've put that aside in favor of messing with exploration algorithms.  

The most fun of these exploration algorithms so far (and what the code currently does) is drawing! Simply click and drag (start from the center). The brush generates a box around the mouse click (currently top left to bottom right) and handles conflicts (when a space has conflicting adjacencies eg. dense trees next to water which is not permitted in the current probabilities mappings) with the cliff terrain.  

Here's an example:
![Example generation](./wfc_example.png)  

Other algorithms are commented out. I intend on cleaning this up.  