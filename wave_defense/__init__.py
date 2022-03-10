from gym.envs.registration import register 

register(id='WaveDefense-v0',entry_point='wave_defense.envs:WaveDefense') 
register(id='WaveDefense-v1',entry_point='wave_defense.envs:WaveDefenseTabular') 