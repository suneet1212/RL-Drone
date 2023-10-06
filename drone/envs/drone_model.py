# #python
# import coppeliasim_python.sim as sim
# sim.simxGetObjects()

# class Drone():
#     def __init__(self) -> None:
#         self.particlesAreVisible=True
#         self.simulateParticles=True
#         self.fakeShadow=True
        
#         self.particleCountPerSecond=430
#         self.particleSize=0.005
#         self.particleDensity=8500
#         self.particleScatteringAngle=30
#         self.particleLifeTime=0.5
#         self.maxParticleCount=50

#         # -- Detatch the manipulation sphere:
#         self.targetObj=sim.getObject('./target')
#         sim.setObjectParent(self.targetObj,-1,True)

#         # -- This control algo was quickly written and is dirty and not optimal. It just serves as a SIMPLE example
#         self.d=sim.getObject('./base')

#         self.propellerHandles={}
#         self.jointHandles={}
#         self.particleObjects={-1,-1,-1,-1}
#         ttype=sim.particle_roughspheres+sim.particle_cyclic+sim.particle_respondable1to4+sim.particle_respondable5to8+sim.particle_ignoresgravity
#         if not self.particlesAreVisible:
#             ttype=ttype+sim.particle_invisible

#         for i in range(1,4,1):
#             self.propellerHandles[i]=sim.simxGetObjects('./propeller['..(i-1)..']/respondable')
#             self.jointHandles[i]=sim.getObject('./propeller['..(i-1)..']/joint')
#             if self.simulateParticles:
#                 self.particleObjects[i]=sim.addParticleObject(ttype,self.particleSize,self.particleDensity,{2,1,0.2,3,0.4},self.particleLifeTime,self.maxParticleCount,{0.3,0.7,1})

#         self.heli=sim.getObject('.')

#         self.pParam=2
#         self.iParam=0
#         self.dParam=0
#         self.vParam=-2

#         self.cumul=0
#         self.lastE=0
#         self.pAlphaE=0
#         self.pBetaE=0
#         self.psp2=0
#         self.psp1=0

#         self.prevEuler=0


#         if (self.fakeShadow):
#             self.shadowCont=sim.addDrawingObject(sim.drawing_discpts+sim.drawing_cyclic+sim.drawing_25percenttransparency+sim.drawing_50percenttransparency+sim.drawing_itemsizes,0.2,0,-1,1)

#     def cleanup(self):
#         sim.removeDrawingObject(self.shadowCont)
#         for i=1,#particleObjects,1 do
#             sim.removeParticleObject(self.particleObjects[i])
#         end
#     end 