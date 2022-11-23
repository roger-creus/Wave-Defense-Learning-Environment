from gym.envs.registration import register 

register(id='WaveDefense-v0',entry_point='WaveDefense.envs:WaveDefense') 
register(id='WaveDefense-v1',entry_point='WaveDefense.envs:WaveDefenseTabular') 
register(id='WaveDefenseNoReward-v0',entry_point='WaveDefense.envs:WaveDefenseNoReward') 