RotaryOps = {}
RotaryOps.transports = {'UH-1H', 'Mi-8MT', 'Mi-24P'}
trigger.action.outText("ROTARY OPS STARTED", 5)
env.info("ROTARY OPS STARTED")


local function tableHasKey(table,key)
    return table[key] ~= nil
end

local function dispMsg(text)
  trigger.action.outText(text, 5)
  return text
end

local function tableHasKey(table,key)
    return table[key] ~= nil
end

local function hasValue (tab, val)
    for index, value in ipairs(tab) do
        if value == val then
            return true
        end
    end
    return false
end

local function getObjectVolume(obj)
  local length = (obj:getDesc().box.max.x + math.abs(obj:getDesc().box.min.x))
  local height = (obj:getDesc().box.max.y + math.abs(obj:getDesc().box.min.y))
  local depth = (obj:getDesc().box.max.z + math.abs(obj:getDesc().box.min.z))
  return length * height * depth
end

function RotaryOps.spawnInfantryOnGrp(grp, src_grp_name, behavior) --allow to spawn on other group units
  trigger.action.outText("attempting to spawn at "..grp:getUnit(1):getTypeName(), 5)
  local vars = {} 
  vars.gpName = src_grp_name
  vars.action = 'clone' 
  vars.point = grp:getUnit(1):getPoint() 
  vars.radius = 5
  vars.disperse = 'disp'
  vars.maxDisp = 5
  local new_grp_table = mist.teleportToPoint(vars) 
  
  if new_grp_table then
    local new_grp = Group.getByName(new_grp_table.name)
    local PATROL = 1
    local AGGRESSIVE = 2
    if behavior == PATROL then
      --trigger.action.outText("new group: "..mist.utils.tableShow(new_grp_table), 5)
      --local id = timer.scheduleFunction(RotaryOps.seekCover, new_grp, timer.getTime() + 1)
      RotaryOps.patrolRadius({grp = new_grp})
    end
    if behavior == AGGRESSIVE then
      RotaryOps.chargeEnemy({grp = new_grp})
    end
  else trigger.action.outText("Infantry failed to spawn. ", 5)  
  end
end

function RotaryOps.chargeEnemy(vars)
 --trigger.action.outText("charge enemies: "..mist.utils.tableShow(vars), 5) 
 local grp = vars.grp
 local search_radius = vars.radius or 5000
 ----
 local first_valid_unit
 if grp:isExist() ~= true then return end
 for index, unit in pairs(grp:getUnits())
 do
   if unit:isExist() == true then
     first_valid_unit = unit
     break
   else --trigger.action.outText("a unit no longer exists", 15) 
   end 
 end
 ----
 
 if first_valid_unit == nil then return end
 local start_point = first_valid_unit:getPoint()
 if not vars.spawn_point then vars.spawn_point = start_point end

 local enemy_coal
 if grp:getCoalition() == 1 then enemy_coal = 2 end
 if grp:getCoalition() == 2 then enemy_coal = 1 end

 --local sphere = trigger.misc.getZone('town')
 local volS = {
   id = world.VolumeType.SPHERE,
   params = {
     point = grp:getUnit(1):getPoint(),  --check if exists, maybe itterate through grp
     radius = search_radius
   }
 }
 local enemy_unit
 local path = {} 
 local ifFound = function(foundItem, val)
  --trigger.action.outText("found item: "..foundItem:getTypeName(), 5)  
  if foundItem:hasAttribute("Infantry") == true and foundItem:getCoalition() == enemy_coal then
    enemy_unit = foundItem
    --trigger.action.outText("found enemy! "..foundItem:getTypeName(), 5) 
    
    path[1] = mist.ground.buildWP(start_point, '', 5) 
    path[2] = mist.ground.buildWP(enemy_unit:getPoint(), '', 5) 
    --path[3] = mist.ground.buildWP(vars.spawn_point, '', 5) 
  else 

    --trigger.action.outText("object found is not enemy inf in "..search_radius, 5)  
  end
  
 return true
 end
 --default path if no units found
 if false then
   trigger.action.outText("group going back to origin", 5)  
   path[1] = mist.ground.buildWP(start_point, '', 5) 
   path[2] = mist.ground.buildWP(vars.spawn_point, '', 5)
   
 end
 world.searchObjects(Object.Category.UNIT, volS, ifFound)
 mist.goRoute(grp, path)
 local id = timer.scheduleFunction(RotaryOps.chargeEnemy, vars, timer.getTime() + math.random(50,70))

end


function RotaryOps.patrolRadius(vars)
 trigger.action.outText("patrol radius: "..mist.utils.tableShow(vars), 5) 
 local grp = vars.grp
 local search_radius = vars.radius or 100
 local first_valid_unit
 if grp:isExist() ~= true then return end
 for index, unit in pairs(grp:getUnits())
 do
   if unit:isExist() == true then
     first_valid_unit = unit
     break
   else --trigger.action.outText("a unit no longer exists", 15) 
   end 
 end
 if first_valid_unit == nil then return end
 local start_point = first_valid_unit:getPoint()
 local object_vol_thresh = 0
 local max_waypoints = 5
 local foundUnits = {}
 --local sphere = trigger.misc.getZone('town')
 local volS = {
   id = world.VolumeType.SPHERE,
   params = {
     point = grp:getUnit(1):getPoint(),  --check if exists, maybe itterate through grp
     radius = search_radius
   }
 }
 
 local ifFound = function(foundItem, val)
  --trigger.action.outText("found item: "..foundItem:getTypeName(), 5)  
  if foundItem:hasAttribute("Infantry") ~= true then  --disregard infantry...we only want objects that might provide cover
    if getObjectVolume(foundItem) > object_vol_thresh then
      foundUnits[#foundUnits + 1] = foundItem
      --trigger.action.outText("valid cover item: "..foundItem:getTypeName(), 5) 
    else trigger.action.outText("object not large enough: "..foundItem:getTypeName(), 5) 
    end
  else --trigger.action.outText("object not the right type", 5)  
  end
 return true
 end
 
 world.searchObjects(1, volS, ifFound)
 world.searchObjects(3, volS, ifFound)
 world.searchObjects(5, volS, ifFound)
 --world.searchObjects(Object.Category.BASE, volS, ifFound)
 local path = {} 
 path[1] = mist.ground.buildWP(start_point, '', 5) 
 local m = math.min(#foundUnits, max_waypoints)
 for i = 1, m, 1
   do
     local rand_index = math.random(1,#foundUnits)
     path[i + 1] = mist.ground.buildWP(foundUnits[rand_index]:getPoint(), '', 5) 
     --trigger.action.outText("waypoint to: "..foundUnits[rand_index]:getTypeName(), 5) 
   end
 if #path <= 3 then
   for i = #path, max_waypoints, 1
   do
     path[#path + 1] = mist.ground.buildWP(mist.getRandPointInCircle(start_point, search_radius), '', 5)
   end
 end
 --trigger.action.outText("new waypoints created: "..(#path - 1), 5) 
 mist.goRoute(grp, path)
 --local timing = mist.getPathLength(path) / 5
 local id = timer.scheduleFunction(RotaryOps.patrolRadius, vars, timer.getTime() + math.random(50,70))

end


function RotaryOps.knowEnemy(vars)
 --trigger.action.outText("charge enemies: "..mist.utils.tableShow(vars), 5) 
 local grp = vars.grp
 local search_radius = vars.radius or 5000
 ----
 local first_valid_unit
 if grp:isExist() ~= true then return end
 for index, unit in pairs(grp:getUnits())
 do
   if unit:isExist() == true then
     first_valid_unit = unit
     break
   else --trigger.action.outText("a unit no longer exists", 15) 
   end 
 end
 ----
 
 if first_valid_unit == nil then return end
 local start_point = first_valid_unit:getPoint()
 if not vars.spawn_point then vars.spawn_point = start_point end

 local enemy_coal
 if grp:getCoalition() == 1 then enemy_coal = 2 end
 if grp:getCoalition() == 2 then enemy_coal = 1 end

 --local sphere = trigger.misc.getZone('town')
 local volS = {
   id = world.VolumeType.SPHERE,
   params = {
     point = grp:getUnit(1):getPoint(),  --check if exists, maybe itterate through grp
     radius = search_radius
   }
 }
 local enemy_unit
 local path = {} 
 local ifFound = function(foundItem, val)
  --trigger.action.outText("found item: "..foundItem:getTypeName(), 5)  
  if foundItem:getCoalition() == enemy_coal then
    enemy_unit = foundItem
    trigger.action.outText("found enemy! "..foundItem:getTypeName(), 5) 
    
    path[1] = mist.ground.buildWP(start_point, '', 5) 
    path[2] = mist.ground.buildWP(enemy_unit:getPoint(), '', 5) 
    --path[3] = mist.ground.buildWP(vars.spawn_point, '', 5)
    grp:getUnit(1):getController():knowTarget(enemy_unit, true, true)
    
     
  else 

    --trigger.action.outText("object found is not enemy inf in "..search_radius, 5)  
  end
  
 return true
 end
 --default path if no units found
 if false then
   trigger.action.outText("group going back to origin", 5)  
   path[1] = mist.ground.buildWP(start_point, '', 5) 
   path[2] = mist.ground.buildWP(vars.spawn_point, '', 5)
   
 end
 world.searchObjects(Object.Category.UNIT, volS, ifFound)
 --mist.goRoute(grp, path)
 local id = timer.scheduleFunction(RotaryOps.knowEnemy, vars, timer.getTime() + 15)

end


------------------------------------------



RotaryOps.zones = {}
RotaryOps.active_zone = ""
RotaryOps.active_zone_index = 1
RotaryOps.conflict = {
  aggressor = 'blue',
  blue_forces_flag = 99,
  red_forces_flag = 98,
  aggressor_zone_is_first = true,
}


function RotaryOps.sortOutInfantry(mixed_units)
  local _infantry = {}
  local _not_infantry = {}
  for index, unit in pairs(mixed_units)
  do
    if unit:hasAttribute("Infantry") then
      _infantry[#_infantry + 1] = unit
    else _not_infantry[#_not_infantry + 1] = unit
    end
  end
  return {infantry = _infantry, not_infantry = _not_infantry} 
end

function RotaryOps.assessUnitsInZone(var)
   --consider adding other unit types
   local red_ground_units = mist.getUnitsInZones(mist.makeUnitTable({'[red][vehicle]'}), {RotaryOps.active_zone})  --consider adding other unit types
   local red_infantry = RotaryOps.sortOutInfantry(red_ground_units).infantry
   local red_vehicles = RotaryOps.sortOutInfantry(red_ground_units).not_infantry
   local blue_ground_units = mist.getUnitsInZones(mist.makeUnitTable({'[blue][vehicle]'}), {RotaryOps.active_zone})  --consider adding other unit types
   local blue_infantry = RotaryOps.sortOutInfantry(blue_ground_units).infantry
   local blue_vehicles = RotaryOps.sortOutInfantry(blue_ground_units).not_infantry
   
   trigger.action.outText("[BATTLE FOR "..RotaryOps.active_zone .. "]   RED: " ..#red_infantry.. " infantry, " .. #red_vehicles .. " vehicles.  BLUE: "..#blue_infantry.. " infantry, " .. #blue_vehicles.." vehicles.", 5, true) 
   local id = timer.scheduleFunction(RotaryOps.assessUnitsInZone, 1, timer.getTime() + 5)
end
local id = timer.scheduleFunction(RotaryOps.assessUnitsInZone, 1, timer.getTime() + 5)


function RotaryOps.drawZones(zones)  --should be drawZones and itterate through all zones, getting the active zone, and incrementing id
  local previous_point
  for index, zone in pairs(zones)
  do
    local point = trigger.misc.getZone(zone.outter_zone_name).point
    local radius = trigger.misc.getZone(zone.outter_zone_name).radius
    local coalition = -1
    local id = index  --this must be UNIQUE!
    local color = {1, 1, 1, 0.5}
    local fill_color = {1, 1, 1, 0.1}
    local text_fill_color = {0, 0, 0, 0}
    local line_type = 5 --1 Solid  2 Dashed  3 Dotted  4 Dot Dash  5 Long Dash  6 Two Dash
    local font_size = 20
    local read_only = false
    local text = zone.outter_zone_name
    if zone.outter_zone_name == RotaryOps.active_zone then
      color = {1, 1, 1, 0.5}
      fill_color = {1, 0, 1, 0.1}
    end
    if previous_point ~= nill then
      trigger.action.lineToAll(coalition, id + 200, point, previous_point, color, line_type)
    end
    previous_point = point
    trigger.action.circleToAll(coalition, id, point, radius, color, fill_color, line_type)
    trigger.action.textToAll(coalition, id + 100, point, color, text_fill_color, font_size, read_only, text)
  end
  

end

--function to automatically add transport craft to ctld, rather than having to define each in the mission editor
function RotaryOps.addPilots(var)
   for uName, uData in pairs(mist.DBs.humansByName) do
     if hasValue(RotaryOps.transports, uData.type) then
       if hasValue(ctld.transportPilotNames, uData.unitName) ~= true then
         ctld.transportPilotNames [#ctld.transportPilotNames + 1] = uData.unitName
       --else trigger.action.outText("player already in pilot table", 5)
       end
     end
   end
 local id = timer.scheduleFunction(RotaryOps.addPilots, 1, timer.getTime() + 15)
end
RotaryOps.addPilots(1)

function RotaryOps.pushZone()
  RotaryOps.active_zone_index = RotaryOps.active_zone_index + 1
  if RotaryOps.active_zone_index > #RotaryOps.zones then 
    RotaryOps.active_zone_index = #RotaryOps.zones 
  end
  RotaryOps.active_zone = RotaryOps.zones[RotaryOps.active_zone_index].outter_zone_name
end

function RotaryOps.fallBack()
  RotaryOps.active_zone_index = RotaryOps.active_zone_index - 1
  if RotaryOps.active_zone_index < 1 then 
    RotaryOps.active_zone_index = 1 
  end
  RotaryOps.active_zone = RotaryOps.zones[RotaryOps.active_zone_index].outter_zone_name
end


function RotaryOps.setupCTLD()
  ctld.enableCrates = false
  ctld.enabledFOBBuilding = false
  ctld.JTAC_lock = "vehicle"
  ctld.location_DMS = true
  ctld.numberOfTroops = 24 --max loading size
  
  ctld.unitLoadLimits = {
    -- Remove the -- below to turn on options
     ["SA342Mistral"] = 4,
     ["SA342L"] = 4,
     ["SA342M"] = 4,
     ["UH-1H"] = 10,
     ["Mi-8MT"] = 24,
     ["Mi-24P"] = 8,
   }
   
   ctld.loadableGroups = {  
   -- {name = "Mortar Squad Red", inf = 2, mortar = 5, side =1 }, --would make a group loadable by RED only
    {name = "Standard Group (10)", inf = 6, mg = 2, at = 2 }, -- will make a loadable group with 6 infantry, 2 MGs and 2 anti-tank for both coalitions
    {name = "Anti Air (5)", inf = 2, aa = 3  },
    {name = "Anti Tank (8)", inf = 2, at = 6  },
    {name = "Mortar Squad (6)", mortar = 6 },
    {name = "Small Standard Group (4)", inf = 2, mg = 1, at = 1 },
    {name = "JTAC Group (5)", inf = 4, jtac = 1 }, -- will make a loadable group with 4 infantry and a JTAC soldier for both coalitions
    {name = "Single JTAC (1)", jtac = 1 },
    {name = "Platoon (24)", inf = 12, mg = 4, at = 3, aa = 1 },
    
}
end
RotaryOps.setupCTLD()


function RotaryOps.logSomething()
  --trigger.action.outText("zones: ".. mist.utils.tableShow(RotaryOps.zones), 5)
  for key, value in pairs(RotaryOps.zones) do 
    trigger.action.outText("zone: ".. RotaryOps.zones[key].outter_zone_name, 5)
  end
end


function RotaryOps.setupRadioMenu()
  local conflict_zones_menu = missionCommands.addSubMenu( "Conflict Zones")

  local push_zone = missionCommands.addCommand( "Push to next zone", conflict_zones_menu , RotaryOps.pushZone)

  local fall_back = missionCommands.addCommand( "Fall back to prev zone"  , conflict_zones_menu , RotaryOps.fallBack)
  
  local log_something = missionCommands.addCommand( "Log something"  , conflict_zones_menu , RotaryOps.logSomething)
end
RotaryOps.setupRadioMenu()


function RotaryOps.addZone(_outter_zone_name, _vars, group_id)  --todo: implement zone group ids 
  group_id = group_id or 1
  table.insert(RotaryOps.zones, {outter_zone_name = _outter_zone_name, vars = _vars})
  RotaryOps.drawZones(RotaryOps.zones)
  --ctld.dropOffZones[#ctld.dropOffZones + 1] = { _outter_zone_name, "green", 0 }
  ctld.pickupZones[#ctld.pickupZones + 1] = { _outter_zone_name, "blue", -1, "yes", 0 }  --should be set as innactive to start, can we dynamically change sides?
  --trigger.action.outText("zones: ".. mist.utils.tableShow(RotaryOps.zones), 5)  
end

function RotaryOps.setupConflict()
  RotaryOps.active_zone = RotaryOps.zones[RotaryOps.active_zone_index].outter_zone_name
  trigger.action.outText("active zone: "..RotaryOps.active_zone, 5)  
end




--[[
vars = {
inner_zone = '',
infantry_spawn = 10,
infantry_respawn = 50,
infantry_spawn_zone = ''
defender_coal = 'red'
}
]]

