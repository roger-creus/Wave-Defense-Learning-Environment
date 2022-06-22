# Wave-Defense-Learning-Environment

Wave defense is an RL environment based on a custom game inspired from the typical wave defense games. The agent is a static cannon in the center of the map and can only rotate and shoot, while the enemies keep spawning around and willing to destroy the agent. 

For the RL settings, the agent is rewarded depending on the number of enemies on screen (the lower the better) and the distance to these (the closer the worse). At each frame the agent choses wether to rotate left, rotate right, shoot, or do nothing. 

See this video to see the results: https://www.youtube.com/watch?v=VOmj7_nnPJ0&t=1s&ab_channel=RogerCreusCastanyer

# Files

The environment class (based on Open AI Gym) is in **./wave_defense/envs/wave_defense.py** and all the game classes (player, enemy, spawner...) can be found in **./wave_defense/envs/prefabs/**
