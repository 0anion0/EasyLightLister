# coding: utf8 
import c4d,os


PLUGIN_ID           = 1037828
TAG_ID_OCTANE       = 1029526
TAG_ID_ARNOLD       = 1029989
TAG_ID_VRAY         = 1020441

STEP                =  202

LIGHT_LISTER_GRP_LIGHT                  = 0
LIGHT_LISTER_SELECT                     = LIGHT_LISTER_GRP_LIGHT                        + STEP
LIGHT_LISTER_RENDER                     = LIGHT_LISTER_SELECT                           + STEP
LIGHT_LISTER_NAME                       = LIGHT_LISTER_RENDER                           + STEP
LIGHT_LISTER_LIGHT_TYPE                 = LIGHT_LISTER_NAME                             + STEP
LIGHT_LISTER_LIGHT_COLOR                = LIGHT_LISTER_LIGHT_TYPE                       + STEP
LIGHT_LISTER_LIGHT_INTENSITY            = LIGHT_LISTER_LIGHT_COLOR                      + STEP
LIGHT_LISTER_LIGHT_USE_DECAY            = LIGHT_LISTER_LIGHT_INTENSITY                  + STEP
LIGHT_LISTER_LIGHT_DECAY_RADIUS         = LIGHT_LISTER_LIGHT_USE_DECAY                  + STEP
LIGHT_LISTER_LIGHT_USE_VISIBILITY       = LIGHT_LISTER_LIGHT_DECAY_RADIUS               + STEP
LIGHT_LISTER_LIGHT_VISIBILITY_PERCENT   = LIGHT_LISTER_LIGHT_USE_VISIBILITY             + STEP
LIGHT_LISTER_LIGHT_VISIBILITY_RADIUS    = LIGHT_LISTER_LIGHT_VISIBILITY_PERCENT         + STEP
LIGHT_LISTER_SHADOW_USE                 = LIGHT_LISTER_LIGHT_VISIBILITY_RADIUS          + STEP
LIGHT_LISTER_SHADOW_DENSITY             = LIGHT_LISTER_SHADOW_USE                       + STEP
LIGHT_LISTER_SHADOW_COLOR               = LIGHT_LISTER_SHADOW_DENSITY                   + STEP
LIGHT_LISTER_SHADOW_RESOLUTION          = LIGHT_LISTER_SHADOW_COLOR                     + STEP
LIGHT_LISTER_SHADOW_BIAS                = LIGHT_LISTER_SHADOW_RESOLUTION                + STEP
LIGHT_LISTER_SHADOW_ACCURACY            = LIGHT_LISTER_SHADOW_BIAS                      + STEP
LIGHT_LISTER_SHADOW_MIN_SAMPLE          = LIGHT_LISTER_SHADOW_ACCURACY                  + STEP
LIGHT_LISTER_SHADOW_MAX_SAMPLE          = LIGHT_LISTER_SHADOW_MIN_SAMPLE                + STEP

LIGHT_LISTER_SEPARATOR                  = LIGHT_LISTER_SHADOW_MAX_SAMPLE                + STEP

LIGHT_LISTER_GRP_1                      = LIGHT_LISTER_SEPARATOR                        + 1
LIGHT_LISTER_GRP_2                      = LIGHT_LISTER_GRP_1                            + 1
LIGHT_LISTER_GRP_SEPARATOR              = LIGHT_LISTER_GRP_2                            + 1

LIGHT_LISTER_BTN_REFRSH_C4D             = LIGHT_LISTER_GRP_SEPARATOR                    + 1
LIGHT_LISTER_BTN_ALWAYS_REFRESH_C4D     = LIGHT_LISTER_BTN_REFRSH_C4D                    + 1


class lightManager():
    def __init__(self):
        self.allLights = []

    def getLightEngine(self,op):
        for tag in op.GetTags():
            if tag.CheckType(TAG_ID_OCTANE):
                return 1
            elif tag.CheckType(TAG_ID_ARNOLD):
                return 2
            elif tag.CheckType(TAG_ID_VRAY):
                return 3
        return 0         

    def searchLightInHierarchy(self,op,first = True):
        if first:
            self.allLights = []

        while op:
            if op.CheckType(5102):
                self.allLights.append(op)
            self.searchLightInHierarchy(op.GetDown(),False)
            op = op.GetNext()

    def checkIfIsSame(self):
        buffer = self.allLights
        self.searchLightInHierarchy(c4d.documents.GetActiveDocument().GetFirstObject(),True)
        if len(self.allLights) == len(buffer):
            self.allLights = buffer
            return False
        else:
            return True


class mainDialog(c4d.gui.GeDialog):
    def __init__(self):
        self.doc = c4d.documents.GetActiveDocument()
        self.lm = lightManager()

    def Timer(self,msg):
        if self.GetBool(LIGHT_LISTER_BTN_ALWAYS_REFRESH_C4D):
            self.lm.searchLightInHierarchy(self.doc.GetFirstObject())
            self.refreshLightData()
        else:
            if self.lm.checkIfIsSame():
                self.refreshLightData()

    def refreshLightData(self):
        self.LayoutFlushGroup(LIGHT_LISTER_GRP_2)
        self.createLightData()
        self.LayoutChanged(LIGHT_LISTER_GRP_2)

    def createLightData(self):
        if len(self.lm.allLights) > STEP - 2:
            loopToDo = STEP - 3
        else:
            loopToDo = len(self.lm.allLights)

        self.selectGroup(loopToDo)
        #self.renderGroup(loopToDo)
        self.nameGroup(loopToDo)
        self.lightTypeGroup(loopToDo)
        self.lightColorGroup(loopToDo)
        self.lightIntensityGroup(loopToDo)
        self.useDecayGroup(loopToDo)
        self.decayRadiusGroup(loopToDo)      
        self.useVisibilityGroup(loopToDo)              
        self.visibilityPercentGroup(loopToDo)              
        self.visibilityRadiusGroup(loopToDo)              
        self.shadowUseGroup(loopToDo)              
        self.shadowDensityGroup(loopToDo)             
        self.shadowColorGroup(loopToDo)
        self.shadowResolutionGroup(loopToDo)
        self.shadowBiaisGroup(loopToDo)
        self.shadowAccuracyGroup(loopToDo)
        self.minSampleGroup(loopToDo)
        self.maxSampleGroup(loopToDo)

    def CreateLayout(self):
        self.lm.searchLightInHierarchy(self.doc.GetFirstObject())

        self.SetTitle('Easy Light Lister v1')
        self.SetTimer(500)

        self.GroupBeginInMenuLine()
        self.GroupBorderSpace(5, 5, 5, 5) #Left, top, Right, Bottom 
        self.AddCheckbox(LIGHT_LISTER_BTN_ALWAYS_REFRESH_C4D,c4d.BFH_CENTER,150,15,"Auto Refresh")
        self.AddButton(LIGHT_LISTER_BTN_REFRSH_C4D, c4d.BFH_CENTER, 60, 15, "Refresh")
        self.GroupEnd()


        if self.ScrollGroupBegin(LIGHT_LISTER_GRP_1, c4d.BFH_SCALEFIT | c4d.BFV_SCALEFIT, c4d.SCROLLGROUP_VERT, 100, 100):
            self.GroupBorderSpace(5, 10, 3, 10)
            if self.GroupBegin(LIGHT_LISTER_GRP_2, c4d.BFH_SCALEFIT | c4d.BFV_SCALEFIT, 19, 500):
                self.GroupBorderNoTitle(c4d.BORDER_GROUP_IN)
                self.GroupBorderSpace(10, 10, 10, 10)

                self.createLightData()
                self.GroupEnd()
            self.GroupEnd()
        return True 

    def selectOnChange(self,id,msg):
        if id >= LIGHT_LISTER_SELECT and id < LIGHT_LISTER_RENDER:
            currentLightID = id - LIGHT_LISTER_SELECT - 2
            if c4d.gui.GetInputState(c4d.BFM_INPUT_KEYBOARD,c4d.BFM_INPUT_CHANNEL,msg):
                if msg[c4d.BFM_INPUT_QUALIFIER] & c4d.QCTRL:
                    self.doc.SetSelection(self.lm.allLights[currentLightID],c4d.SELECTION_ADD)
                elif msg[c4d.BFM_INPUT_QUALIFIER] & c4d.QALT:
                    self.doc.SetSelection(self.lm.allLights[currentLightID],c4d.SELECTION_SUB)
                else:
                    self.doc.SetSelection(self.lm.allLights[currentLightID],c4d.SELECTION_NEW)
            c4d.EventAdd()

    """
    def renderOnChange(self,id,msg):
        if id >= LIGHT_LISTER_RENDER and id < LIGHT_LISTER_NAME:
            currentLightID = id - LIGHT_LISTER_RENDER - 2
            print "render"
    """

    def nameOnChange(self,id,msg):
        if id >= LIGHT_LISTER_NAME and id < LIGHT_LISTER_LIGHT_TYPE:
            currentLightID = id - LIGHT_LISTER_NAME - 2
            currentData = self.GetString(id)
            self.lm.allLights[currentLightID].SetName(currentData)
            c4d.EventAdd()

    def lightTypeOnChange(self,id,msg):
        if id >= LIGHT_LISTER_LIGHT_TYPE and id < LIGHT_LISTER_LIGHT_COLOR:
            currentLightID = id - LIGHT_LISTER_LIGHT_TYPE - 2
            currentData = self.GetLong(id)
            self.lm.allLights[currentLightID][c4d.LIGHT_TYPE] = currentData
            c4d.EventAdd()  

    def lightColorOnChange(self,id,msg):
        if id >= LIGHT_LISTER_LIGHT_COLOR and id < LIGHT_LISTER_LIGHT_INTENSITY:
            currentLightID = id - LIGHT_LISTER_LIGHT_COLOR - 2
            currentData = self.GetColorField(id)["color"]
            self.lm.allLights[currentLightID][c4d.LIGHT_COLOR] = currentData
            c4d.EventAdd()

    def lightIntensityOnChange(self,id,msg):
        if id >= LIGHT_LISTER_LIGHT_INTENSITY and id < LIGHT_LISTER_LIGHT_USE_DECAY:
            currentLightID = id - LIGHT_LISTER_LIGHT_INTENSITY - 2
            currentData = self.GetReal(id)
            self.lm.allLights[currentLightID][c4d.LIGHT_BRIGHTNESS] = currentData
            c4d.EventAdd()

    def useDecayOnChange(self,id,msg):
        if id >= LIGHT_LISTER_LIGHT_USE_DECAY and id < LIGHT_LISTER_LIGHT_DECAY_RADIUS:
            currentLightID = id - LIGHT_LISTER_LIGHT_USE_DECAY - 2
            currentData = self.GetLong(id)
            self.lm.allLights[currentLightID][c4d.LIGHT_DETAILS_FALLOFF] = currentData
            c4d.EventAdd()

            if self.lm.allLights[currentLightID][c4d.LIGHT_DETAILS_FALLOFF] is 0:
                self.Enable(LIGHT_LISTER_LIGHT_DECAY_RADIUS+currentLightID+2,False)
            else:
                self.Enable(LIGHT_LISTER_LIGHT_DECAY_RADIUS+currentLightID+2,True)

    def decayRadiusOnChange(self,id,msg):
        if id >= LIGHT_LISTER_LIGHT_DECAY_RADIUS and id < LIGHT_LISTER_LIGHT_USE_VISIBILITY:
            currentLightID = id - LIGHT_LISTER_LIGHT_DECAY_RADIUS - 2
            currentData = self.GetReal(id)
            self.lm.allLights[currentLightID][c4d.LIGHT_DETAILS_OUTERDISTANCE] = currentData
            c4d.EventAdd()

    def useVisibilityOnChange(self,id,msg):
        if id >= LIGHT_LISTER_LIGHT_USE_VISIBILITY and id < LIGHT_LISTER_LIGHT_VISIBILITY_PERCENT:
            currentLightID = id - LIGHT_LISTER_LIGHT_USE_VISIBILITY - 2
            currentData = self.GetLong(id)
            self.lm.allLights[currentLightID][c4d.LIGHT_VLTYPE] = currentData
            c4d.EventAdd()

            if self.lm.allLights[currentLightID][c4d.LIGHT_VLTYPE] is 0:
                self.Enable(LIGHT_LISTER_LIGHT_VISIBILITY_PERCENT+currentLightID+2,False)
                self.Enable(LIGHT_LISTER_LIGHT_VISIBILITY_RADIUS+currentLightID+2,False)
            else:
                self.Enable(LIGHT_LISTER_LIGHT_VISIBILITY_PERCENT+currentLightID+2,True)
                self.Enable(LIGHT_LISTER_LIGHT_VISIBILITY_RADIUS+currentLightID+2,True)
     
    def visibilityPercentOnChange(self,id,msg):
        if id >= LIGHT_LISTER_LIGHT_VISIBILITY_PERCENT and id < LIGHT_LISTER_LIGHT_VISIBILITY_RADIUS:
            currentLightID = id - LIGHT_LISTER_LIGHT_VISIBILITY_PERCENT - 2
            currentData = self.GetReal(id)
            self.lm.allLights[currentLightID][c4d.LIGHT_VISIBILITY_BRIGHTNESS] = currentData
            c4d.EventAdd()

    def visibilityRadiusOnChange(self,id,msg):
        if id >= LIGHT_LISTER_LIGHT_VISIBILITY_RADIUS and id < LIGHT_LISTER_SHADOW_USE:
            currentLightID = id - LIGHT_LISTER_LIGHT_VISIBILITY_RADIUS - 2
            currentData = self.GetReal(id)
            self.lm.allLights[currentLightID][c4d.LIGHT_VISIBILITY_OUTERDISTANCE] = currentData
            c4d.EventAdd()

    def shadowUseOnChange(self,id,msg):
        if id >= LIGHT_LISTER_SHADOW_USE and id < LIGHT_LISTER_SHADOW_DENSITY:
            currentLightID = id - LIGHT_LISTER_SHADOW_USE - 2
            currentData = self.GetLong(id)
            self.lm.allLights[currentLightID][c4d.LIGHT_SHADOWTYPE_VIRTUAL] = currentData
            c4d.EventAdd()

            if self.lm.allLights[currentLightID][c4d.LIGHT_SHADOWTYPE_VIRTUAL] is 1:
                self.Enable(LIGHT_LISTER_SHADOW_RESOLUTION+currentLightID+2,True)
                self.Enable(LIGHT_LISTER_SHADOW_BIAS+currentLightID+2,True)
            else:
                self.Enable(LIGHT_LISTER_SHADOW_RESOLUTION+currentLightID+2,False)
                self.Enable(LIGHT_LISTER_SHADOW_BIAS+currentLightID+2,False)

            if self.lm.allLights[currentLightID][c4d.LIGHT_SHADOWTYPE_VIRTUAL] is 3:
                self.Enable(LIGHT_LISTER_SHADOW_ACCURACY+currentLightID+2,True)
                self.Enable(LIGHT_LISTER_SHADOW_MIN_SAMPLE+currentLightID+2,True)
                self.Enable(LIGHT_LISTER_SHADOW_MAX_SAMPLE+currentLightID+2,True)
            else:
                self.Enable(LIGHT_LISTER_SHADOW_ACCURACY+currentLightID+2,False)
                self.Enable(LIGHT_LISTER_SHADOW_MIN_SAMPLE+currentLightID+2,False)
                self.Enable(LIGHT_LISTER_SHADOW_MAX_SAMPLE+currentLightID+2,False)

    def shadowDensityOnChange(self,id,msg):
        if id >= LIGHT_LISTER_SHADOW_DENSITY and id < LIGHT_LISTER_SHADOW_COLOR:
            currentLightID = id - LIGHT_LISTER_SHADOW_DENSITY - 2
            currentData = self.GetReal(id)
            self.lm.allLights[currentLightID][c4d.LIGHT_SHADOW_DENSITY] = currentData
            c4d.EventAdd()

    def shadowColorOnChange(self,id,msg):
        if id >= LIGHT_LISTER_SHADOW_COLOR and id < LIGHT_LISTER_SHADOW_RESOLUTION:
            currentLightID = id - LIGHT_LISTER_SHADOW_COLOR - 2
            currentData = self.GetColorField(id)["color"]
            self.lm.allLights[currentLightID][c4d.LIGHT_SHADOW_COLOR] = currentData
            c4d.EventAdd()

    def shadowResolutionOnChange(self,id,msg):
        if id >= LIGHT_LISTER_SHADOW_RESOLUTION and id < LIGHT_LISTER_SHADOW_BIAS:
            currentLightID = id - LIGHT_LISTER_SHADOW_RESOLUTION - 2
            currentData = self.GetLong(id)
            self.lm.allLights[currentLightID][c4d.LIGHT_SHADOW_MAPSIZE] = currentData
            c4d.EventAdd()
    
    def shadowBiasOnChange(self,id,msg):
        if id >= LIGHT_LISTER_SHADOW_BIAS and id < LIGHT_LISTER_SHADOW_ACCURACY:
            currentLightID = id - LIGHT_LISTER_SHADOW_BIAS - 2
            currentData = self.GetReal(id)
            self.lm.allLights[currentLightID][c4d.LIGHT_SHADOW_ABSOLUTEBIAS] = currentData
            c4d.EventAdd()

    def shadowAccuracyOnChange(self,id,msg):
        if id >= LIGHT_LISTER_SHADOW_ACCURACY and id < LIGHT_LISTER_SHADOW_MIN_SAMPLE:
            currentLightID = id - LIGHT_LISTER_SHADOW_ACCURACY - 2
            currentData = self.GetReal(id)
            self.lm.allLights[currentLightID][c4d.LIGHT_SHADOW_ACCURACY] = currentData
            c4d.EventAdd()

    def shadowMinSampleOnChange(self,id,msg):
        if id >= LIGHT_LISTER_SHADOW_MIN_SAMPLE and id < LIGHT_LISTER_SHADOW_MAX_SAMPLE:
            currentLightID = id - LIGHT_LISTER_SHADOW_MIN_SAMPLE - 2
            currentData = self.GetLong(id)
            self.lm.allLights[currentLightID][c4d.LIGHT_SHADOW_MINSAMPLES] = currentData
            c4d.EventAdd()

    def shadowMaxSampleOnChange(self,id,msg):
        if id >= LIGHT_LISTER_SHADOW_MAX_SAMPLE and id < LIGHT_LISTER_SEPARATOR:
            currentLightID = id - LIGHT_LISTER_SHADOW_MAX_SAMPLE - 2
            currentData = self.GetLong(id)
            self.lm.allLights[currentLightID][c4d.LIGHT_SHADOW_MAXSAMPLES] = currentData
            c4d.EventAdd()


    def Command(self, id, msg):
        self.selectOnChange(id,msg)
        #self.renderOnChange(id,msg)
        self.nameOnChange(id,msg)
        self.lightTypeOnChange(id,msg)
        self.lightColorOnChange(id,msg)
        self.lightIntensityOnChange(id,msg)
        self.useDecayOnChange(id,msg)
        self.decayRadiusOnChange(id,msg)
        self.useVisibilityOnChange(id,msg)
        self.visibilityPercentOnChange(id,msg)
        self.visibilityRadiusOnChange(id,msg)
        self.shadowUseOnChange(id,msg)
        self.shadowDensityOnChange(id,msg)
        self.shadowColorOnChange(id,msg)
        self.shadowResolutionOnChange(id,msg)
        self.shadowBiasOnChange(id,msg)
        self.shadowAccuracyOnChange(id,msg)
        self.shadowMinSampleOnChange(id,msg)
        self.shadowMaxSampleOnChange(id,msg)
        self.shadowAccuracyOnChange(id,msg)

        if id == LIGHT_LISTER_BTN_REFRSH_C4D:
            self.lm.searchLightInHierarchy(self.doc.GetFirstObject())
            self.refreshLightData()

        return True

    #------------------------
    #        SELECT
    #------------------------
    def selectGroup(self,loopToDo):
        if self.GroupBegin(LIGHT_LISTER_SELECT, c4d.BFH_SCALEFIT | c4d.BFV_SCALEFIT, 1, STEP):
            self.AddStaticText(LIGHT_LISTER_SELECT+1,c4d.BFH_SCALEFIT|c4d.BFV_TOP,0,10,"Select",c4d.BORDER_NONE)
            self.AddSeparatorH(0)
            for i in xrange(0,loopToDo):
                self.AddButton(LIGHT_LISTER_SELECT+i+2 ,c4d.BFH_SCALEFIT|c4d.BFV_TOP ,0 ,13 ,"S")                
            self.GroupEnd()

    """
    #------------------------
    #        RENDER
    #------------------------
    def renderGroup(self,loopToDo):
        if self.GroupBegin(LIGHT_LISTER_RENDER, c4d.BFH_SCALEFIT | c4d.BFV_SCALEFIT, 1, STEP):
            self.AddStaticText(LIGHT_LISTER_RENDER+1,c4d.BFH_SCALEFIT|c4d.BFV_TOP,0,10,"Render",c4d.BORDER_NONE)
            self.AddSeparatorH(0)
            for i in xrange(0,loopToDo):
                self.AddComboBox(LIGHT_LISTER_RENDER+i+2,c4d.BFH_SCALEFIT|c4d.BFV_TOP, 0, 13, False)
                self.AddChild(LIGHT_LISTER_RENDER+i+2, 0, "C4D")              
                self.AddChild(LIGHT_LISTER_RENDER+i+2, 1, "Octane")              
                self.AddChild(LIGHT_LISTER_RENDER+i+2, 2, "Arnold")              
                self.AddChild(LIGHT_LISTER_RENDER+i+2, 3, "Vray")
                self.SetLong(LIGHT_LISTER_RENDER+i+2, self.lm.getLightEngine(self.lm.allLights[i]))
            self.GroupEnd()
    """

    #------------------------
    #         NAME
    #------------------------
    def nameGroup(self,loopToDo):
        if self.GroupBegin(LIGHT_LISTER_NAME, c4d.BFH_SCALEFIT | c4d.BFV_SCALEFIT, 1, STEP):
            self.AddStaticText(LIGHT_LISTER_NAME+1,c4d.BFH_SCALEFIT|c4d.BFV_TOP,0,10,"Name",c4d.BORDER_NONE)
            self.AddSeparatorH(0)
            for i in xrange(0,loopToDo):
                self.AddEditText(LIGHT_LISTER_NAME+i+2 ,c4d.BFH_SCALEFIT|c4d.BFV_TOP ,0 ,13)
                self.SetString(LIGHT_LISTER_NAME+i+2, self.lm.allLights[i].GetName())           
            self.GroupEnd()

    #------------------------
    #      LIGHT_TYPE
    #------------------------
    def lightTypeGroup(self,loopToDo):
        if self.GroupBegin(LIGHT_LISTER_LIGHT_TYPE, c4d.BFH_SCALEFIT | c4d.BFV_SCALEFIT, 1, STEP):
            self.AddStaticText(LIGHT_LISTER_LIGHT_TYPE+1,c4d.BFH_SCALEFIT|c4d.BFV_TOP,0,10,"Light Type",c4d.BORDER_NONE)
            self.AddSeparatorH(0)
            for i in xrange(0,loopToDo):
                self.AddComboBox(LIGHT_LISTER_LIGHT_TYPE+i+2,c4d.BFH_SCALEFIT|c4d.BFV_TOP, 0, 13, False)
                self.AddChild(LIGHT_LISTER_LIGHT_TYPE+i+2, 0, "Omni")              
                self.AddChild(LIGHT_LISTER_LIGHT_TYPE+i+2, 1, "Spot")              
                self.AddChild(LIGHT_LISTER_LIGHT_TYPE+i+2, 3, "Infinite")              
                self.AddChild(LIGHT_LISTER_LIGHT_TYPE+i+2, 8, "Area")              
                self.AddChild(LIGHT_LISTER_LIGHT_TYPE+i+2, 2, "Square Spot")              
                self.AddChild(LIGHT_LISTER_LIGHT_TYPE+i+2, 4, "Parallel")              
                self.AddChild(LIGHT_LISTER_LIGHT_TYPE+i+2, 5, "Parallel Spot")              
                self.AddChild(LIGHT_LISTER_LIGHT_TYPE+i+2, 6, "Square Parallel Spot")
                self.SetLong(LIGHT_LISTER_LIGHT_TYPE+i+2, self.lm.allLights[i][c4d.LIGHT_TYPE])            
            self.GroupEnd()

    #------------------------
    #      LIGHT_COLOR
    #------------------------
    def lightColorGroup(self,loopToDo):
        if self.GroupBegin(LIGHT_LISTER_LIGHT_COLOR, c4d.BFH_SCALEFIT | c4d.BFV_SCALEFIT, 1, STEP):
            self.AddStaticText(LIGHT_LISTER_LIGHT_COLOR+1,c4d.BFH_SCALEFIT|c4d.BFV_TOP,0,10,"Color",c4d.BORDER_NONE)
            self.AddSeparatorH(0)
            for i in xrange(0,loopToDo):
                self.AddColorField(LIGHT_LISTER_LIGHT_COLOR+i+2 ,c4d.BFH_SCALEFIT|c4d.BFV_TOP , 0,15)
                self.SetColorField(LIGHT_LISTER_LIGHT_COLOR+i+2,self.lm.allLights[i][c4d.LIGHT_COLOR],1,1,c4d.DR_COLORFIELD_NO_BRIGHTNESS)              
            self.GroupEnd()

    #------------------------
    #     LIGHT_INTENSITY
    #------------------------
    def lightIntensityGroup(self,loopToDo):
        if self.GroupBegin(LIGHT_LISTER_LIGHT_INTENSITY, c4d.BFH_SCALEFIT | c4d.BFV_SCALEFIT, 1, STEP):
            self.AddStaticText(LIGHT_LISTER_LIGHT_INTENSITY+1,c4d.BFH_SCALEFIT|c4d.BFV_TOP,0,10,"Intensity",c4d.BORDER_NONE)
            self.AddSeparatorH(0)
            for i in xrange(0,loopToDo):
                self.AddEditNumberArrows(LIGHT_LISTER_LIGHT_INTENSITY+i+2, c4d.BFH_SCALEFIT|c4d.BFV_TOP ,0 ,16)           
                self.SetPercent(LIGHT_LISTER_LIGHT_INTENSITY+i+2,self.lm.allLights[i][c4d.LIGHT_BRIGHTNESS],0)         
            self.GroupEnd()

    #------------------------
    #       USE_DECAY
    #------------------------
    def useDecayGroup(self,loopToDo):
        if self.GroupBegin(LIGHT_LISTER_LIGHT_USE_DECAY, c4d.BFH_SCALEFIT | c4d.BFV_SCALEFIT, 1, STEP):
            self.AddStaticText(LIGHT_LISTER_LIGHT_USE_DECAY+1,c4d.BFH_SCALEFIT|c4d.BFV_TOP,0,10,"Decay",c4d.BORDER_NONE)
            self.AddSeparatorH(0)
            for i in xrange(0,loopToDo):
                self.AddComboBox(LIGHT_LISTER_LIGHT_USE_DECAY+i+2,c4d.BFH_SCALEFIT|c4d.BFV_TOP, 0, 13, False)
                self.AddChild(LIGHT_LISTER_LIGHT_USE_DECAY+i+2, 0, "None")              
                self.AddChild(LIGHT_LISTER_LIGHT_USE_DECAY+i+2, 10, "Inverse Square Physically")              
                self.AddChild(LIGHT_LISTER_LIGHT_USE_DECAY+i+2, 8, "Linear")              
                self.AddChild(LIGHT_LISTER_LIGHT_USE_DECAY+i+2, 5, "Step")              
                self.AddChild(LIGHT_LISTER_LIGHT_USE_DECAY+i+2, 7, "Inverse Square Clamped")              

                self.SetLong(LIGHT_LISTER_LIGHT_USE_DECAY+i+2, self.lm.allLights[i][c4d.LIGHT_DETAILS_FALLOFF])   
            
            self.GroupEnd()

    #------------------------
    #      DECAY_RADIUS
    #------------------------
    def decayRadiusGroup(self,loopToDo):
        if self.GroupBegin(LIGHT_LISTER_LIGHT_DECAY_RADIUS, c4d.BFH_SCALEFIT | c4d.BFV_SCALEFIT, 1, STEP):
            self.AddStaticText(LIGHT_LISTER_LIGHT_DECAY_RADIUS+1,c4d.BFH_SCALEFIT|c4d.BFV_TOP,0,10,"Decay",c4d.BORDER_NONE)
            self.AddSeparatorH(0)
            for i in xrange(0,loopToDo):
                self.AddEditNumberArrows(LIGHT_LISTER_LIGHT_DECAY_RADIUS+i+2, c4d.BFH_SCALEFIT|c4d.BFV_TOP ,0 ,16)     
                self.SetMeter(LIGHT_LISTER_LIGHT_DECAY_RADIUS+i+2,self.lm.allLights[i][c4d.LIGHT_DETAILS_OUTERDISTANCE],0)
                if self.lm.allLights[i][c4d.LIGHT_DETAILS_FALLOFF] is 0:
                    self.Enable(LIGHT_LISTER_LIGHT_DECAY_RADIUS+i+2,False)
            self.GroupEnd()

    #------------------------
    #     USE_VISIBILITY
    #------------------------
    def useVisibilityGroup(self,loopToDo):
        if self.GroupBegin(LIGHT_LISTER_LIGHT_USE_VISIBILITY, c4d.BFH_SCALEFIT | c4d.BFV_SCALEFIT, 1, STEP):
            self.AddStaticText(LIGHT_LISTER_LIGHT_USE_VISIBILITY+1,c4d.BFH_SCALEFIT|c4d.BFV_TOP,0,10,"Visibility",c4d.BORDER_NONE)
            self.AddSeparatorH(0)
            for i in xrange(0,loopToDo):
                self.AddComboBox(LIGHT_LISTER_LIGHT_USE_VISIBILITY+i+2,c4d.BFH_SCALEFIT|c4d.BFV_TOP, 0, 13, False)
                self.AddChild(LIGHT_LISTER_LIGHT_USE_VISIBILITY+i+2, 0, "None")              
                self.AddChild(LIGHT_LISTER_LIGHT_USE_VISIBILITY+i+2, 1, "Visible")              
                self.AddChild(LIGHT_LISTER_LIGHT_USE_VISIBILITY+i+2, 2, "Volumetric")              
                self.AddChild(LIGHT_LISTER_LIGHT_USE_VISIBILITY+i+2, 3, "Inverse Volumetric")              

                self.SetLong(LIGHT_LISTER_LIGHT_USE_VISIBILITY+i+2, self.lm.allLights[i][c4d.LIGHT_VLTYPE])  
            self.GroupEnd()

    #------------------------
    #   VISIBILITY_PERCENT
    #------------------------
    def visibilityPercentGroup(self,loopToDo):
        if self.GroupBegin(LIGHT_LISTER_LIGHT_VISIBILITY_PERCENT, c4d.BFH_SCALEFIT | c4d.BFV_SCALEFIT, 1, STEP):
            self.AddStaticText(LIGHT_LISTER_LIGHT_VISIBILITY_PERCENT+1,c4d.BFH_SCALEFIT|c4d.BFV_TOP,0,10,"Visibility",c4d.BORDER_NONE)
            self.AddSeparatorH(0)
            for i in xrange(0,loopToDo):
                self.AddEditNumberArrows(LIGHT_LISTER_LIGHT_VISIBILITY_PERCENT+i+2, c4d.BFH_SCALEFIT|c4d.BFV_TOP ,0 ,16)           
                self.SetPercent(LIGHT_LISTER_LIGHT_VISIBILITY_PERCENT+i+2,self.lm.allLights[i][c4d.LIGHT_VISIBILITY_BRIGHTNESS],0)
                if self.lm.allLights[i][c4d.LIGHT_VLTYPE] is 0:
                    self.Enable(LIGHT_LISTER_LIGHT_VISIBILITY_PERCENT+i+2,False)
                  
            self.GroupEnd()

    #------------------------
    #   VISIBILITY_RADIUS
    #------------------------
    def visibilityRadiusGroup(self,loopToDo):
        if self.GroupBegin(LIGHT_LISTER_LIGHT_VISIBILITY_RADIUS, c4d.BFH_SCALEFIT | c4d.BFV_SCALEFIT, 1, STEP):
            self.AddStaticText(LIGHT_LISTER_LIGHT_VISIBILITY_RADIUS+1,c4d.BFH_SCALEFIT|c4d.BFV_TOP,0,10,"Visibility",c4d.BORDER_NONE)
            self.AddSeparatorH(0)
            for i in xrange(0,loopToDo):
                self.AddEditNumberArrows(LIGHT_LISTER_LIGHT_VISIBILITY_RADIUS+i+2, c4d.BFH_SCALEFIT|c4d.BFV_TOP ,0 ,16)     
                self.SetMeter(LIGHT_LISTER_LIGHT_VISIBILITY_RADIUS+i+2,self.lm.allLights[i][c4d.LIGHT_VISIBILITY_OUTERDISTANCE],0)    
                if self.lm.allLights[i][c4d.LIGHT_VLTYPE] is 0:
                    self.Enable(LIGHT_LISTER_LIGHT_VISIBILITY_RADIUS+i+2,False)

            self.GroupEnd()

    #------------------------
    #      SHADOW_USE
    #------------------------
    def shadowUseGroup(self,loopToDo):
        if self.GroupBegin(LIGHT_LISTER_SHADOW_USE, c4d.BFH_SCALEFIT | c4d.BFV_SCALEFIT, 1, STEP):
            self.AddStaticText(LIGHT_LISTER_SHADOW_USE+1,c4d.BFH_SCALEFIT|c4d.BFV_TOP,0,10,"Shadow",c4d.BORDER_NONE)
            self.AddSeparatorH(0)
            for i in xrange(0,loopToDo):
                self.AddComboBox(LIGHT_LISTER_SHADOW_USE+i+2,c4d.BFH_SCALEFIT|c4d.BFV_TOP, 0, 13, False)
                self.AddChild(LIGHT_LISTER_SHADOW_USE+i+2, 0, "None")         
                self.AddChild(LIGHT_LISTER_SHADOW_USE+i+2, 1, "Shadow Map")         
                self.AddChild(LIGHT_LISTER_SHADOW_USE+i+2, 2, "Raytraced")         
                self.AddChild(LIGHT_LISTER_SHADOW_USE+i+2, 3, "Area")         

                self.SetLong(LIGHT_LISTER_SHADOW_USE+i+2, self.lm.allLights[i][c4d.LIGHT_SHADOWTYPE_VIRTUAL])                  
            self.GroupEnd()

    #------------------------
    #     SHADOW_DENSITY
    #------------------------
    def shadowDensityGroup(self,loopToDo):
        if self.GroupBegin(LIGHT_LISTER_SHADOW_DENSITY, c4d.BFH_SCALEFIT | c4d.BFV_SCALEFIT, 1, STEP):
            self.AddStaticText(LIGHT_LISTER_SHADOW_DENSITY+1,c4d.BFH_SCALEFIT|c4d.BFV_TOP,0,10,"Shadow",c4d.BORDER_NONE)
            self.AddSeparatorH(0)
            for i in xrange(0,loopToDo):
                self.AddEditNumberArrows(LIGHT_LISTER_SHADOW_DENSITY+i+2, c4d.BFH_SCALEFIT|c4d.BFV_TOP ,0 ,16)     
                self.SetPercent(LIGHT_LISTER_SHADOW_DENSITY+i+2,self.lm.allLights[i][c4d.LIGHT_SHADOW_DENSITY])               
            self.GroupEnd()

    #------------------------
    #      SHADOW_COLOR
    #------------------------
    def shadowColorGroup(self,loopToDo):
        if self.GroupBegin(LIGHT_LISTER_SHADOW_COLOR, c4d.BFH_SCALEFIT | c4d.BFV_SCALEFIT, 1, STEP):
            self.AddStaticText(LIGHT_LISTER_SHADOW_COLOR+1,c4d.BFH_SCALEFIT|c4d.BFV_TOP,0,10,"Shadow",c4d.BORDER_NONE)
            self.AddSeparatorH(0)
            for i in xrange(0,loopToDo):
                self.AddColorField(LIGHT_LISTER_SHADOW_COLOR+i+2 ,c4d.BFH_SCALEFIT|c4d.BFV_TOP , 0,15)
                self.SetColorField(LIGHT_LISTER_SHADOW_COLOR+i+2,self.lm.allLights[i][c4d.LIGHT_SHADOW_COLOR],1,1,c4d.DR_COLORFIELD_NO_BRIGHTNESS)               
            self.GroupEnd()

    #------------------------
    #   SHADOW_RESOLUTION
    #------------------------
    def shadowResolutionGroup(self,loopToDo):
        if self.GroupBegin(LIGHT_LISTER_SHADOW_RESOLUTION, c4d.BFH_SCALEFIT | c4d.BFV_SCALEFIT, 1, STEP):
            self.AddStaticText(LIGHT_LISTER_SHADOW_RESOLUTION+1,c4d.BFH_SCALEFIT|c4d.BFV_TOP,0,10,"Resolution",c4d.BORDER_NONE)
            self.AddSeparatorH(0)
            for i in xrange(0,loopToDo):
                self.AddComboBox(LIGHT_LISTER_SHADOW_RESOLUTION+i+2,c4d.BFH_SCALEFIT|c4d.BFV_TOP, 0, 13, False)
                self.AddChild(LIGHT_LISTER_SHADOW_RESOLUTION+i+2, 0, "250x250")     
                self.AddChild(LIGHT_LISTER_SHADOW_RESOLUTION+i+2, 1, "500x500")     
                self.AddChild(LIGHT_LISTER_SHADOW_RESOLUTION+i+2, 2, "750x750")     
                self.AddChild(LIGHT_LISTER_SHADOW_RESOLUTION+i+2, 3, "1000x1000")     
                self.AddChild(LIGHT_LISTER_SHADOW_RESOLUTION+i+2, 4, "1250x1250")     
                self.AddChild(LIGHT_LISTER_SHADOW_RESOLUTION+i+2, 5, "1500x1500")     
                self.AddChild(LIGHT_LISTER_SHADOW_RESOLUTION+i+2, 6, "1750x1750")     
                self.AddChild(LIGHT_LISTER_SHADOW_RESOLUTION+i+2, 7, "2000x2000")     

                self.SetLong(LIGHT_LISTER_SHADOW_RESOLUTION+i+2, self.lm.allLights[i][c4d.LIGHT_SHADOW_MAPSIZE])
                if self.lm.allLights[i][c4d.LIGHT_SHADOWTYPE_VIRTUAL] is not 1:
                    self.Enable(LIGHT_LISTER_SHADOW_RESOLUTION+i+2,False)   
            self.GroupEnd()

    #------------------------
    #      SHADOW_BIAIS
    #------------------------
    def shadowBiaisGroup(self,loopToDo):
        if self.GroupBegin(LIGHT_LISTER_SHADOW_BIAS, c4d.BFH_SCALEFIT | c4d.BFV_SCALEFIT, 1, STEP):
            self.AddStaticText(LIGHT_LISTER_SHADOW_BIAS+1,c4d.BFH_SCALEFIT|c4d.BFV_TOP,0,10,"Biais",c4d.BORDER_NONE)
            self.AddSeparatorH(0)
            for i in xrange(0,loopToDo):
                self.AddEditNumberArrows(LIGHT_LISTER_SHADOW_BIAS+i+2, c4d.BFH_SCALEFIT|c4d.BFV_TOP ,0 ,16)     
                self.SetMeter(LIGHT_LISTER_SHADOW_BIAS+i+2,self.lm.allLights[i][c4d.LIGHT_SHADOW_ABSOLUTEBIAS],0) 
                if self.lm.allLights[i][c4d.LIGHT_SHADOWTYPE_VIRTUAL] is not 1:
                    self.Enable(LIGHT_LISTER_SHADOW_BIAS+i+2,False)           
            self.GroupEnd()

    #------------------------
    #    SHADOW_ACCURACY
    #------------------------
    def shadowAccuracyGroup(self,loopToDo):
        if self.GroupBegin(LIGHT_LISTER_SHADOW_ACCURACY, c4d.BFH_SCALEFIT | c4d.BFV_SCALEFIT, 1, STEP):
            self.AddStaticText(LIGHT_LISTER_SHADOW_ACCURACY+1,c4d.BFH_SCALEFIT|c4d.BFV_TOP,0,10,"Shadow Accuracy",c4d.BORDER_NONE)
            self.AddSeparatorH(0)
            for i in xrange(0,loopToDo):
                self.AddEditNumberArrows(LIGHT_LISTER_SHADOW_ACCURACY+i+2, c4d.BFH_SCALEFIT|c4d.BFV_TOP ,0 ,16 )    
                self.SetPercent(LIGHT_LISTER_SHADOW_ACCURACY+i+2,self.lm.allLights[i][c4d.LIGHT_SHADOW_DENSITY],0,100)
                if self.lm.allLights[i][c4d.LIGHT_SHADOWTYPE_VIRTUAL] is not 3:
                    self.Enable(LIGHT_LISTER_SHADOW_ACCURACY+i+2,False)
            self.GroupEnd()

    #------------------------
    #    SHADOW_MIN_SAMPLE
    #------------------------
    def minSampleGroup(self,loopToDo):
        if self.GroupBegin(LIGHT_LISTER_SHADOW_MIN_SAMPLE, c4d.BFH_SCALEFIT | c4d.BFV_SCALEFIT, 1, STEP):
            self.AddStaticText(LIGHT_LISTER_SHADOW_MIN_SAMPLE+1,c4d.BFH_SCALEFIT|c4d.BFV_TOP,0,10,"Min Sample",c4d.BORDER_NONE)
            self.AddSeparatorH(0)
            for i in xrange(0,loopToDo):
                self.AddEditNumberArrows(LIGHT_LISTER_SHADOW_MIN_SAMPLE+i+2, c4d.BFH_SCALEFIT|c4d.BFV_TOP ,0 ,16)     
                self.SetLong(LIGHT_LISTER_SHADOW_MIN_SAMPLE+i+2,self.lm.allLights[i][c4d.LIGHT_SHADOW_MINSAMPLES])    
                if self.lm.allLights[i][c4d.LIGHT_SHADOWTYPE_VIRTUAL] is not 3:
                    self.Enable(LIGHT_LISTER_SHADOW_MIN_SAMPLE+i+2,False)         
            self.GroupEnd()

    #------------------------
    #    SHADOW_MAX_SAMPLE
    #------------------------
    def maxSampleGroup(self,loopToDo):
        if self.GroupBegin(LIGHT_LISTER_SHADOW_MAX_SAMPLE, c4d.BFH_SCALEFIT | c4d.BFV_SCALEFIT, 1, STEP):
            self.AddStaticText(LIGHT_LISTER_SHADOW_MAX_SAMPLE+1,c4d.BFH_SCALEFIT|c4d.BFV_TOP,0,10,"Max Sample",c4d.BORDER_NONE)
            self.AddSeparatorH(0)
            for i in xrange(0,loopToDo):
                self.AddEditNumberArrows(LIGHT_LISTER_SHADOW_MAX_SAMPLE+i+2, c4d.BFH_SCALEFIT|c4d.BFV_TOP ,0 ,16)     
                self.SetLong(LIGHT_LISTER_SHADOW_MAX_SAMPLE+i+2,self.lm.allLights[i][c4d.LIGHT_SHADOW_MAXSAMPLES])
                if self.lm.allLights[i][c4d.LIGHT_SHADOWTYPE_VIRTUAL] is not 3:
                    self.Enable(LIGHT_LISTER_SHADOW_MAX_SAMPLE+i+2,False)           
            self.GroupEnd()


class UILauncher_Main(c4d.plugins.CommandData):
 dialog = None

 def Execute(self, doc):
    if self.dialog is None:
       self.dialog = mainDialog()
    return self.dialog.Open(dlgtype=c4d.DLG_TYPE_ASYNC, pluginid=PLUGIN_ID, defaultw=200, defaulth=150)
        
 def RestoreLayout(self, sec_ref):
    if self.dialog is None:
       self.dialog = mainDialog()
    return self.dialog.Restore(pluginid=PLUGIN_ID, secret=sec_ref)
 
if __name__ == "__main__":
    dir, file = os.path.split(__file__)
    bmp = c4d.bitmaps.BaseBitmap()
    bmp.InitWith(os.path.join(dir, "easyLightLister.png"))
    c4d.plugins.RegisterCommandPlugin(  id=PLUGIN_ID, 
                                        str="Easy Light Lister",
                                        help="List all lights in the scenes",
                                        info=0,
                                        dat=UILauncher_Main(), 
                                        icon=bmp)