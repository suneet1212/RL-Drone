# RL-Drone

important links:
* https://coppeliarobotics.com/helpFiles/
* https://www.coppeliarobotics.com/helpFiles/en/mainScript.htm
* http://fid.cl/courses/ai-robotics/vrep-tut/pythonBubbleRob.pdf
* https://www.coppeliarobotics.com/helpFiles/en/remoteApiModusOperandi.htm
* https://www.coppeliarobotics.com/helpFiles/en/remoteApiConstants.htm
* https://forum.coppeliarobotics.com/viewtopic.php?f=9&t=6794#p27017

<br>To start simulation:

``` python
self.clientID=sim.simxStart("127.0.0.1",19997,True,True,5000,5) # start a connection
sim.simxSynchronous(self.clientID,True) 
```

For each step:

```python
sim.simxSynchronousTrigger(self.clientID)
```