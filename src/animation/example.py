"""
File: Example.py
Author: Erik Grabljevec
E-mail: erikgrabljevec5@gmail.com
Doc: Example of how to use Target_animation.py          
"""

from animation.target_animation import Animation


# Set constants
# =============
out_directory = "result.avi"
bg_speed = 4


# Create simple movie.
# ====================
test = Animation()
test.add_target(2, start=[250,0], velocity=[1,1], size=5,
                v=4, color=[0.7, 0.2, 0.1])
test.add_target(2, start=[250,250], velocity=[1,1], size=5, v=6)

test.add_background("images/test.jpg", 2)
test.add_dragonfly([[320, 240, 0.0], [300, 220, 0.5], [250, 200, 1.0]])

test.run(out_directory, 10, 10)
