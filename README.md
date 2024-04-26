# Snake-Game
## Basic Overview
This game allows the user to play as a green snake that grows as it eats red apples. The game tracks the user's high score and current score.
## Demo









https://github.com/carsonmdd/Snake-Game/assets/130185711/1a9e10de-f3a1-4cd3-9c99-1da26922dd62










## Features
- The snake can move around the screen with the arrow keys.
- An red apple spawns at random coordinates that do not overlap with the snake's body when the game starts or when the apple is consumed.
- A golden apple has a 20% chance of spawning which allows the snake to grow twice as much as if it ate a red apple.
- The snake's body lights up when it consumes a golden apple.
- The snake grows by four squares when it eats a apple.
- The game ends if the snake runs into its own body or runs into the blue border.
- The game displays the player's current length in the bottom left of the screen.
- The game displays the player's high score in the bottom right of the screen.
- Once the game ends, the game displays the "GAME OVER" text, the user's last length, and a "Play Again" button.
- The "Play Again" button becomes highlighted when hovered over with the cursor.
- Once the player selects the "Play Again" button, the game is restarted and the player's snake is reset. However, the player's high score is retained.
- The game's window is resizable.

## Inspiration
After my introduction to the pygame library in my early classes, I decided to explore deeper and develop a game I've loved for years: the snake game. Using Cool Math Games' game titled "Snake," I challenged myself to replicate their game as closely as possible from scratch. Later, I added an additional powerup feature.
## Reflection
Rather than following a precise plan, this project was more of a learning process. Throughout development, I found myself valuing the separation of concerns principle more and more. I learned a great deal about how to simplify larger problems into more manageable problems to tackle one at a time. Specifically, I would break larger functionalities into simpler functions and develop incrementally.
