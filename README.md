# Snake Game (Chamber of Secrets)

## Description
### The Harry Potter: Chamber of Secrets takes on the classic Snake game. 
This project is a recreation of the classic snake game, but the storyline encapsulates the Harry Potter world. It includes smooth movement and different game modes. 
### Instructions
Players use either WASD or the arrow keys for movement, as well as P or the Space bar to pause. \
<em>Easy mode</em> -> Harry Potter will be idle, and you will have slower movement. \
<em>Normal mode</em> -> Normal speed with idle Harry Potter as well. \
<em>Hard mode</em> -> Normal speed with a Harry Potter shooting at you. A body hit removes 1 piece. A head hit will remove 5 and result in death if there is only the head remaining.

To access the development mode, press I. This gives insights into the Linear Interpolation math and deque for the snake body. 

## Key Features: 
<strong>Smooth Movement</strong> -> Linear interpolation(LERP) so that the snake segments transition smoothly between the tiles\
<strong>Projectiles</strong> -> Shot class that can collide with the snake to remove body parts \
<strong>Animation</strong> -> Utilize a sprite sheet to allow for animated Harry Potter \
<strong>Developer Mode</strong> -> Overlay that displays hitboxes, LERP math, and debug visuals \
<strong>Deque</strong> -> Used for the Snake body to allow for inserts and removals in constant time \
<strong>State Machine</strong> -> Used Enum values to handle game states \
<strong>Spawn Algorithm</strong> -> Randomized spawn Algorithm to ensure Harry does not spawn under Snake \

## Screenshots:
<img width="400" height="300" alt="image" src="https://github.com/user-attachments/assets/a6b66a8f-24c0-4241-955c-ba6347bb0eba" /> Screen to choose different game modes\
<img width="400" height="300" alt="image" src="https://github.com/user-attachments/assets/7261e366-7fb8-41da-a633-41811ce50491" />
Playing screen with development mode on (Hard mode w/ projecticles)

## Resources: 
<em>Splash Screens</em>: Generated using Google's Gemini (Nano/Banana model) and edited and refined in Adobe Photoshop for use in the game. \
<em>Harry Potter sprite sheet</em> adapted from [Stooben Rooben](https://www.spriters-resource.com/game_boy_gbc/harrypotterthechamberofsecrets/asset/27356/), modified in LibreSprite \ 
<em>Eat Sound</em> from [jaydenclifford0908](https://www.voicy.network/search/warzone-sound-effects) \
<em>Music</em> from [James Berkley](https://soundcloud.com/jamesmberkeley) \ \

AI tools (ChatGPT) were used for the following small game logic pieces:
- next_direction variable to prevent reverse movement on double inputs within a singular move cycle
- Previous body state to remove glitching back and forth upon initial LERP logic



