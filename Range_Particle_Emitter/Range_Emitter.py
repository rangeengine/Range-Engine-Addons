###############################################################################
#                      Particles System | RanGE 1.6                           #
###############################################################################
#                      Created by: Range Engine Team                          #
#                     Original Code By: Andreas Esau                          #
#                        Access: rangeengine.tech                             #
###############################################################################
from Range import logic, types
import mathutils, math, random

class Range_Emitter(types.KX_PythonComponent):
    args = ({})
    
    def awake(self, args):
        ...

    def start(self, args):
        self.scene = logic.getCurrentScene()
        
        self.object["particles"] = eval(self.object["particleList"])
        self.object["scale"] = eval(self.object["particleScale"])
        self.object["addmode"] = eval(self.object["particleAddMode"])
        
        # INIT
        self.object["init"] = True
        self.object["killTicker"] = 0
        self.object["emitcounter"] = 0
        self.object["particlelist"] = []   
        self.object["multiplier"] = 2.0
        self.object["ticker"] = 0.0
        self.object["counter"] = 0.0
        self.object["oldcounter"] = self.object["counter"]
        self.object["listlen"] = (len(self.object["particles"])) - 1
        self.object["cullingTime"] = 0
        self.object["emitterVisible"] = False

        # CACHING
        self.object["colorCache"] = []
        self.object["colorCacheProgress"] = -1
        self.object["scaleCache"] = []
        self.object["scaleCacheProgress"] = -1
        self.object["speedCache"] = []
        self.object["speedCacheProgress"] = -1
        
        # Particle Pool
        self.availableParticlesPool = []
        self.tick = 0
        
    def update(self):
        #self.object["ticker"] += 1
        
        ### Kill Emitter
        if self.object["kill"]:
            self.object["killTicker"] += 1
            if self.object["killTicker"] >= self.object["lifetime"] + 10:
                self.object.endObject()
                
                # Delete pool
                for particle in self.availableParticlesPool:
                    particle.endObject()
        
        ### CULLING
        if self.object["culling"]:
            cam = self.scene.active_camera
            if (cam.sphereInsideFrustum(self.object.position, self.object["cullingRadius"]) != cam.OUTSIDE):
                self.object["emitterVisible"] = True
            else: self.object["emitterVisible"] = False
        else: self.object["emitterVisible"] = True
        
        # PARTICLE UPDATE #
        for particle in self.object["particlelist"]:
            if particle["ticker"] % self.object["multiplier"] == 0:
                mult = self.object["multiplier"]
                
                # DeltaTime Mul Fix, only with CACHE disabled
                if (not self.object["with_cache"]):
                    mult = (mult * 60) * logic.deltaTime()
                    
                # print(logic.deltaTime())
                
                # Update
                self.particle_update(particle, self.object["particlelist"], mult)
            particle["ticker"] += 1
        ###################
        
        if self.object["emitteron"] and not self.object["kill"] and self.object["emitterVisible"]:
            self.object["cullingTime"] = 0
            randParticle = random.randint(0, self.object["listlen"])
        
            self.object["counter"] += ((self.object["amount"] / 60) * 60) * logic.deltaTime()
            emitcount = int(self.object["counter"] - self.object["oldcounter"])
            
            if (self.object["emitcounter"] < self.object["emitTime"]) or (self.object["emitTime"] == 0):
                for x in range(0, emitcount):  
                    self.object["random"] = random.uniform(1, self.object["randomscale"])
                    
                    # Get a particle from pool
                    particle = self.availableParticlesPool.pop(0) if self.availableParticlesPool else None
                    
                    # If not have particle in pool, add a new particle
                    if (not particle):
                        particle = self.scene.addObject("ParticleParent", self.object)
                        particle["child"] = self.scene.addObject(self.object["particles"][randParticle], self.object)
                        particle["child"].setParent(particle)
                    else:
                        # Reuse Particle
                        particle.worldPosition = self.object.worldPosition
                        particle.worldOrientation = (0, 0, 0, 0)
                        # If we have one more particle in the pool, we need to update it.
                        if (particle["child"].name != self.object["particles"][randParticle]):
                            particle["child"].endObject()
                            particle["child"] = self.scene.addObject(self.object["particles"][randParticle], self.object)
                            particle["child"].setParent(particle)
                        particle["child"].localPosition = (0, 0, 0)
                        particle["child"].localOrientation = (0, 0, 0, 0)
                    
                    vect = mathutils.Vector((random.uniform(-self.object["rangeEmitX"], self.object["rangeEmitX"]), 
                                             random.uniform(-self.object["rangeEmitY"], self.object["rangeEmitY"]), 
                                             random.uniform(-self.object["rangeEmitZ"], self.object["rangeEmitZ"])))
                    vect = particle.localOrientation * vect

                    particle.localPosition += vect
                                       
                    self.object["particlelist"].append(particle)
                    particle["scale"] = self.object["scale"][randParticle]
                    particle["localEmit"] = self.object["localEmit"]
                    particle["coneX"] = (self.object["coneX"]) / 2
                    particle["coneY"] = (self.object["coneY"]) / 2
                    particle["coneZ"] = (self.object["coneZ"]) / 2
                    euler = particle.localOrientation.to_euler()
                    particle["randRotX"] = random.uniform(euler[0] - particle["coneX"], euler[0] + particle["coneX"])
                    particle["randRotY"] = random.uniform(euler[1] - particle["coneY"], euler[1] + particle["coneY"])
                    particle["randRotZ"] = random.uniform(euler[2] - particle["coneZ"], euler[2] + particle["coneZ"])
                    
                    particle["lifeticker"] = 0.0
                    particle["scaleticker"] = 0.0
                    particle["colorticker"] = 0.0
                    particle["fadeinticker"] = 0.0
                    particle["fadeoutticker"] = 0.0
                    particle["speedticker"] = 0.0
                    particle["speed"] = [0, 0, 0]
                    particle["ticker"] = random.randint(0, int((self.object["multiplier"]) - 1))
                    particle["speedfade_start"] = self.object["speedfade_start"]
                    particle["speedfade_end"] = self.object["speedfade_end"]
                    particle["lifetime"] = self.object["lifetime"]
                    
                    particle["startcolor"] = [self.object["start_r"], self.object["start_g"], self.object["start_b"],self.object["alpha"]]
                    particle["endcolor"] = [self.object["end_r"], self.object["end_g"], self.object["end_b"],self.object["alpha"]]
                    particle["alpha"] = self.object["alpha"]
                    particle["tmpColor"] = [0, 0, 0, 0]
                    particle["finColor"] = [0, 0, 0, 0]
                    
                    particle["startspeed"] = (0, 0, self.object["startspeed"])
                    particle["endspeed"] = (0, 0, self.object["endspeed"])
                    particle["randomMovement"] = self.object["randomMovement"]
                    
                    particle["colorfade_start"] = self.object["colorfade_start"]
                    particle["colorfade_end"] = self.object["colorfade_end"]
                    particle["scalefade_start"] = self.object["scalefade_start"]
                    particle["scalefade_end"] = self.object["scalefade_end"]
                    particle["fadein"] = self.object["fadein"]
                    particle["fadeout"] = self.object["fadeout"]
                    
                    particle["startscale"] = (self.object["startscale_x"] * self.object["random"], 
                                              self.object["startscale_y"] * self.object["random"], 
                                              self.object["startscale_z"] * self.object["random"])
                    particle["endscale"] = (self.object["endscale_x"], self.object["endscale_y"], self.object["endscale_z"])
                    
                    particle["child"].color = particle["finColor"]
                    particle["child"].localScale[0] = particle["startscale"][0] * particle["scale"]
                    particle["child"].localScale[1] = particle["startscale"][1] * particle["scale"]
                    particle["child"].localScale[2] = particle["startscale"][2] * particle["scale"]
                    particle["child"].applyRotation((random.uniform(0, 2 * math.pi), 0, 0), True)
                    particle.localOrientation = (particle["randRotX"], particle["randRotY"], particle["randRotZ"])
                    euler = particle.localOrientation.to_euler()
                    particle["RotX"] = euler[0]
                    particle["RotY"] = euler[1]
                    particle["RotZ"] = euler[2]
                    particle["halo"] = self.object["halo"]
                    particle["rotation"] = self.object["rotation"]
                    particle["addmode"] = self.object["addmode"][randParticle]
                    particle.localScale = (1, 1, 1)
                    particle["randomDirection"] = random.choice([-1, 1])
                    self.object["oldcounter"] = self.object["counter"]
            else:
                self.object["kill"] = True
        else:
            self.object["cullingTime"] += 1
         
        self.object["emitcounter"] += self.object["multiplier"]

    def particle_update(self, obj, list, multiplier):
        obj["child"].applyRotation((obj["rotation"] * multiplier * obj["randomDirection"], 0, 0), True)    

        ### Fade between two colors ###
        if obj["lifeticker"] > self.object["colorCacheProgress"] or not self.object["with_cache"]:
            if obj["lifeticker"] < obj["colorfade_start"]:
                obj["tmpColor"] = obj["startcolor"]
            elif (obj["lifeticker"] >= obj["colorfade_start"]) and (obj["lifeticker"] <= obj["colorfade_end"]):
                fadetime = obj["colorfade_end"] - obj["colorfade_start"]
                fadefactor_down = obj["colorticker"] / fadetime
                fadefactor_up = 1 - fadefactor_down
                obj["tmpColor"][0] = (obj["startcolor"][0] * fadefactor_up + obj["endcolor"][0] * fadefactor_down) # * obj["alpha"]
                obj["tmpColor"][1] = (obj["startcolor"][1] * fadefactor_up + obj["endcolor"][1] * fadefactor_down) # * obj["alpha"]
                obj["tmpColor"][2] = (obj["startcolor"][2] * fadefactor_up + obj["endcolor"][2] * fadefactor_down) # * obj["alpha"]
                obj["tmpColor"][3] = obj["startcolor"][3]
                obj["colorticker"] += multiplier
            elif obj["lifeticker"] > obj["colorfade_end"]:
                obj["tmpColor"] = obj["endcolor"]
        
            if obj["lifeticker"] <= obj["fadein"] : 
                fadeinfactor_down = obj["fadeinticker"] / obj["fadein"]
                fadeinfactor_up = 1 - fadeinfactor_down
                if obj["addmode"]:      
                    obj["finColor"][0] = obj["tmpColor"][0] * fadeinfactor_down
                    obj["finColor"][1] = obj["tmpColor"][1] * fadeinfactor_down
                    obj["finColor"][2] = obj["tmpColor"][2] * fadeinfactor_down
                    obj["finColor"][3] = obj["startcolor"][3]
                else:
                    obj["finColor"][0] = obj["tmpColor"][0]
                    obj["finColor"][1] = obj["tmpColor"][1]
                    obj["finColor"][2] = obj["tmpColor"][2]
                    obj["finColor"][3] = obj["tmpColor"][3] * fadeinfactor_down      
                obj["fadeinticker"] += multiplier
            
            elif (obj["lifeticker"] > (obj["lifetime"] - obj["fadeout"])) and (obj["lifeticker"] > obj["fadein"]):
                fadeoutfactor_down = obj["fadeoutticker"] / (obj["fadeout"] - multiplier)
                fadeoutfactor_up = 1 - fadeoutfactor_down
                
                if (fadeoutfactor_up < 0.02): fadeoutfactor_up = 0
                
                if obj["addmode"]:
                    obj["finColor"][0] = obj["tmpColor"][0] * fadeoutfactor_up
                    obj["finColor"][1] = obj["tmpColor"][1] * fadeoutfactor_up
                    obj["finColor"][2] = obj["tmpColor"][2] * fadeoutfactor_up
                    obj["finColor"][3] = 1
                else:
                    obj["finColor"][0] = obj["tmpColor"][0]
                    obj["finColor"][1] = obj["tmpColor"][1]
                    obj["finColor"][2] = obj["tmpColor"][2]
                    obj["finColor"][3] = obj["tmpColor"][3] * fadeoutfactor_up
                
                obj["fadeoutticker"] += multiplier
            else:
                obj["finColor"][0] = obj["tmpColor"][0]
                obj["finColor"][1] = obj["tmpColor"][1]
                obj["finColor"][2] = obj["tmpColor"][2]
                obj["finColor"][3] = obj["tmpColor"][3]
                
            # caching color
            if (self.object["with_cache"]):
                self.object["colorCache"].append(mathutils.Vector(obj["finColor"]))
                self.object["colorCacheProgress"] += multiplier
        else:
            # Use Color Cache
            indexCache = int(obj["lifeticker"] / multiplier)
            obj["finColor"] = self.object["colorCache"][indexCache]
            
        ## Final Color calculation
        obj["child"].color[0] = obj["finColor"][0]
        obj["child"].color[1] = obj["finColor"][1]
        obj["child"].color[2] = obj["finColor"][2]
        obj["child"].color[3] = obj["finColor"][3]

        ## Calculate speed
        if obj["lifeticker"] > self.object["speedCacheProgress"] or not self.object["with_cache"]:
            speedfade = obj["speedfade_end"] - obj["speedfade_start"]
            speedfactor_down = obj["speedticker"] / speedfade
            speedfactor_up = 1 - speedfactor_down
        
            if obj["lifeticker"] <= obj["speedfade_start"]:
                obj["speed"][0] = obj["startspeed"][0]
                obj["speed"][1] = obj["startspeed"][1]
                obj["speed"][2] = obj["startspeed"][2]
            elif obj["lifeticker"] > obj["speedfade_start"] and obj["lifeticker"] < obj["speedfade_end"]:
                obj["speed"][0] = obj["startspeed"][0] * speedfactor_up + obj["endspeed"][0] * speedfactor_down
                obj["speed"][1] = obj["startspeed"][1] * speedfactor_up + obj["endspeed"][1] * speedfactor_down
                obj["speed"][2] = obj["startspeed"][2] * speedfactor_up + obj["endspeed"][2] * speedfactor_down
                obj["speedticker"] += multiplier
            elif obj["lifeticker"] >= obj["speedfade_end"]:
                obj["speed"][0] = obj["endspeed"][0]
                obj["speed"][1] = obj["endspeed"][1]
                obj["speed"][2] = obj["endspeed"][2]
                
            obj["speed"][0] *= multiplier * 0.01
            obj["speed"][1] *= multiplier * 0.01
            obj["speed"][2] *= multiplier * 0.01
            
            # caching speed
            if (self.object["with_cache"]):
                self.object["speedCache"].append(mathutils.Vector(obj["speed"]))
                self.object["speedCacheProgress"] += multiplier
        else:
            # Use Speed Cache
            indexCache = int(obj["lifeticker"] / multiplier)
            obj["speed"] = self.object["speedCache"][indexCache]
            
        #obj.applyMovement((mathutils.Vector(obj["speed"]) * 60) * logic.deltaTime(), obj["localEmit"])
        obj.applyMovement(mathutils.Vector(obj["speed"]), obj["localEmit"])

        ## Calculate scale
        if obj["lifeticker"] > self.object["scaleCacheProgress"] or not self.object["with_cache"]:
            if obj["lifeticker"] <= obj["scalefade_start"]:
                obj["child"].localScale[0] = obj["startscale"][0] * obj["scale"]
                obj["child"].localScale[1] = obj["startscale"][1] * obj["scale"]
                obj["child"].localScale[2] = obj["startscale"][2] * obj["scale"]
            elif obj["lifeticker"] > obj["scalefade_start"] and obj["lifeticker"] < obj["scalefade_end"]:
                scaletime = obj["scalefade_end"] - obj["scalefade_start"]
                scalefactor_down = obj["scaleticker"] / scaletime
                scalefactor_up = 1 - scalefactor_down
                
                obj["child"].localScale[0] = (obj["startscale"][0]* scalefactor_up + obj["endscale"][0] * scalefactor_down)* obj["scale"]
                obj["child"].localScale[1] = (obj["startscale"][1]* scalefactor_up + obj["endscale"][1] * scalefactor_down)* obj["scale"]
                obj["child"].localScale[2] = (obj["startscale"][2]* scalefactor_up + obj["endscale"][2] * scalefactor_down)* obj["scale"]
                obj["scaleticker"] += multiplier
            elif obj["lifeticker"] >= obj["scalefade_end"]:
                obj["child"].localScale[0] = obj["endscale"][0] * obj["scale"]
                obj["child"].localScale[1] = obj["endscale"][1] * obj["scale"]
                obj["child"].localScale[2] = obj["endscale"][2] * obj["scale"]
            
            if obj["child"].localScale[0] < 0:
                obj["child"].localScale[0] = 0
            if obj["child"].localScale[1] < 0:
                obj["child"].localScale[1] = 0
            if obj["child"].localScale[2] < 0:
                obj["child"].localScale[2] = 0
                 
            # caching scale
            if (self.object["with_cache"]):
                self.object["scaleCache"].append(mathutils.Vector(obj["child"].localScale))
                self.object["scaleCacheProgress"] += multiplier
        else:
            # Use Scale Cache
            indexCache = int(obj["lifeticker"] / multiplier)
            obj["child"].localScale = self.object["scaleCache"][indexCache]
            
        ### Random movement
        if obj["lifeticker"] % (30 * 60) * logic.deltaTime() == 0:
            obj["randRotX"] = random.uniform((obj["RotX"] - obj["randomMovement"]), (obj["RotX"] + obj["randomMovement"]))
            obj["randRotY"] = random.uniform((obj["RotY"] - obj["randomMovement"]), (obj["RotY"] + obj["randomMovement"]))
            obj["randRotZ"] = random.uniform((obj["RotZ"] - obj["randomMovement"]), (obj["RotZ"] + obj["randomMovement"]))

        obj["RotX"] = obj["RotX"] * 0.9 + obj["randRotX"] * 0.1
        obj["RotY"] = obj["RotY"] * 0.9 + obj["randRotY"] * 0.1
        obj["RotZ"] = obj["RotZ"] * 0.9 + obj["randRotZ"] * 0.1

        obj.localOrientation = (obj["RotX"], obj["RotY"], obj["RotZ"])       

        ### Lifeticker
        obj["lifeticker"] += multiplier
        # print(obj["lifeticker"], obj["lifetime"])
        
        ### Kill particle after lifetime  
        if (obj["lifeticker"] > obj["lifetime"]) and obj["lifetime"] != 0:
            list.remove(obj)
            self.availableParticlesPool.append(obj)
            # print("End", obj["lifeticker"])
            # obj["child"].endObject()
            # obj.endObject()
